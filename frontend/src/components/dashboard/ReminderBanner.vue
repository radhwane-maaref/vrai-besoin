<template>
  <div v-if="visibleIntentions.length > 0" class="bg-[#FEF9C3] rounded-3xl p-5 shadow-sm border border-[#FEF08A] mb-6">
    <div class="flex items-center gap-3 mb-4">
      <div class="bg-[#FEF08A] p-2 rounded-xl">
        <svg class="w-5 h-5 text-[#B45309]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
      </div>
      <div>
        <h2 class="text-[15px] font-bold text-[#92400E]">Analyses en attente</h2>
        <p class="text-xs text-[#B45309]">Confirmez vos intentions pour clôturer l'analyse.</p>
      </div>
    </div>

    <div class="space-y-3">
      <div v-for="item in displayedIntentions" :key="item.id" class="bg-white/80 rounded-2xl p-4 flex flex-col gap-3 border border-[#FEF08A]/50">
        <div class="flex justify-between items-start">
          <span class="font-bold text-gray-800 text-sm">{{ item.product_name }}</span>
          <span class="font-bold text-[#5B8C85] text-sm">{{ item.product_price }} {{ currencyStore.currentCurrency.code }}</span>
        </div>

        <div class="flex gap-2 w-full mt-1">
          <button @click="ignoreItem(item.id)" class="flex-1 py-2 bg-white border border-gray-200 text-gray-500 text-xs font-bold rounded-xl hover:bg-gray-50 transition-colors">
            Ignorer pour 24h
          </button>
          <button @click="confirmItem(item.id)" class="flex-1 py-2 bg-[#5B8C85] text-white text-xs font-bold rounded-xl hover:bg-[#4a736d] transition-colors shadow-sm">
            Confirmer
          </button>
        </div>
      </div>
    </div>

    <!-- Contrôle Voir Plus / Voir Moins -->
    <button v-if="visibleIntentions.length > 5" @click="expanded = !expanded" class="w-full mt-4 flex justify-center items-center gap-1 text-[#92400E] text-xs font-bold hover:underline">
      {{ expanded ? 'Voir moins' : `Voir toutes les analyses (${visibleIntentions.length})` }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCurrencyStore } from '@/stores/currency';

const props = defineProps({
  intentions: {
    type: Array,
    required: true,
    default: () => []
  }
});

const router = useRouter();
const currencyStore = useCurrencyStore();
const expanded = ref(false);
const hiddenItems = ref({});

onMounted(() => {
  // Récupérer l'état de l'ignorance depuis le localStorage
  const stored = localStorage.getItem('vrai_besoin_hidden_reminders');
  if (stored) {
    hiddenItems.value = JSON.parse(stored);
  }
});

const visibleIntentions = computed(() => {
  const now = Date.now();
  const ONE_DAY = 24 * 60 * 60 * 1000;

  return props.intentions.filter(item => {
    const hiddenAt = hiddenItems.value[item.id];
    // Si l'objet a été masqué il y a moins de 24h, on l'exclut
    if (hiddenAt && (now - hiddenAt) < ONE_DAY) {
      return false;
    }
    return true;
  });
});

const displayedIntentions = computed(() => {
  return expanded.value ? visibleIntentions.value : visibleIntentions.value.slice(0, 5);
});

const ignoreItem = (id) => {
  hiddenItems.value[id] = Date.now();
  localStorage.setItem('vrai_besoin_hidden_reminders', JSON.stringify(hiddenItems.value));
};

const confirmItem = (id) => {
  // Redirige vers la vue d'évaluation pour finaliser la décision
  router.push({ name: 'reflection', params: { id } });
};
</script>