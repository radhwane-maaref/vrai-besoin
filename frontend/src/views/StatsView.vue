<template>
  <div class="min-h-screen bg-[#F8F6F2] px-5 py-8 pb-28 font-sans selection:bg-[#5A877E]/20">

    <header class="mb-8">
      <h1 class="text-3xl font-serif font-bold text-gray-900 tracking-tight">Statistiques</h1>
      <p class="text-sm text-gray-500 mt-1">Analysez l'impact de votre coach IA sur vos finances.</p>
    </header>

    <section class="bg-white p-4 rounded-3xl shadow-sm border border-gray-100 mb-8 space-y-4">
      <div class="flex items-center gap-2 mb-2">
        <svg class="w-4 h-4 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
        </svg>
        <span class="text-sm font-bold text-gray-700">Filtres d'analyse</span>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <!-- Remplacement par CustomSelect pour la période -->
        <CustomSelect
            v-model="filters.period"
            @change="fetchStats"
            :options="periodOptions"
            sizeClass="py-3 h-auto text-sm font-semibold bg-gray-50 border-none"
            roundedClass="rounded-xl"
        />

        <!-- Remplacement par CustomSelect pour la catégorie -->
        <CustomSelect
            v-model="filters.category"
            @change="fetchStats"
            :options="categoryOptions"
            placeholder="Toutes catégories"
            sizeClass="py-3 h-auto text-sm font-semibold bg-gray-50 border-none"
            roundedClass="rounded-xl"
        />
      </div>
    </section>

    <section class="grid grid-cols-2 gap-4 mb-8">
      <StatCard title="Économisé" :value="stats.total_saved" :unit="currencyStore.currentCurrency.code"
                class="col-span-2">
        <template #icon>
          <svg class="w-5 h-5 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </template>
      </StatCard>

      <StatCard title="Maîtrise" :value="stats.mastery_rate" unit="%">
        <template #icon>
          <svg class="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </template>
      </StatCard>

      <StatCard title="Évités" :value="stats.abandoned_count">
        <template #icon>
          <svg class="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </template>
      </StatCard>
    </section>

    <section class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
      <h3 class="text-sm font-bold text-gray-800 mb-6 uppercase tracking-wider">Répartition des décisions</h3>

      <div v-if="isLoading" class="flex justify-center py-10">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-[#5A877E]"></div>
      </div>

      <div v-else class="space-y-6">
        <div v-for="item in chartData" :key="item.label" class="space-y-2">
          <div class="flex justify-between items-end">
            <span class="text-xs font-bold text-gray-500">{{ item.label }}</span>
            <span class="text-sm font-black text-gray-900">{{ item.value }}</span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
            <div
                class="h-full rounded-full transition-all duration-1000 ease-out"
                :style="{ width: calculateWidth(item.value), backgroundColor: item.color }"
            ></div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import api from '@/services/api';
import StatCard from '@/components/stats/StatCard.vue';
import { useCurrencyStore } from '@/stores/currency';
import CustomSelect from '@/components/shared/CustomSelect.vue';

const currencyStore = useCurrencyStore();
const isLoading = ref(true);

const categories = ['Smartphones', 'Ordinateurs', 'Vêtements', 'Maison', 'Autre'];

// Création d'objets formatés pour le CustomSelect
const periodOptions = [
  { value: 'today', label: 'Aujourd\'hui' },
  { value: 'month', label: 'Ce mois' },
  { value: 'year', label: 'Cette année' },
  { value: 'all', label: 'Global' }
];

// Ajout d'une option "vide" pour pouvoir réinitialiser le filtre catégorie
const categoryOptions = [
  { value: '', label: 'Toutes catégories' },
  ...categories.map(cat => ({ value: cat, label: cat }))
];

const filters = reactive({
  period: 'month',
  category: ''
});

const stats = ref({
  total_saved: 0,
  abandoned_count: 0,
  mastery_rate: 0
});

const chartData = ref([]);

// --- Logic ---
const fetchStats = async () => {
  isLoading.value = true;
  try {
    const response = await api.get('/dashboard/stats/', {
      params: filters
    });

    stats.value = response.data.summary;
    chartData.value = response.data.chart_data;
  } catch (error) {
    console.error("Erreur Stats:", error);
  } finally {
    isLoading.value = false;
  }
};

const calculateWidth = (value) => {
  const max = Math.max(...chartData.value.map(d => d.value), 1);
  return `${(value / max) * 100}%`;
};

onMounted(fetchStats);
</script>

<style scoped>
/* Transition douce pour les barres du graphique */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 1000ms;
}
</style>
