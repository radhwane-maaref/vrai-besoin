<template>
  <div class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] pb-12">
    <!-- Header -->
    <header class="pt-8 pb-6 text-center">
      <h1 class="text-[32px] font-bold text-[#000000]">Suivi</h1>
    </header>

    <div class="max-w-3xl mx-auto px-4 sm:px-6 flex flex-col">

      <!-- Horizontal Tab Selector -->
      <div class="flex justify-center mb-8">
        <div class="bg-[#E5E7EB]/60 rounded-[16px] p-1.5 flex w-full max-w-md relative shadow-inner">
          <button
              @click="activeTab = 'reflexion'"
              class="flex-1 py-3 px-2 text-[14px] sm:text-[15px] transition-all duration-300 z-10 rounded-[12px] whitespace-nowrap"
              :class="activeTab === 'reflexion' ? 'text-[#5B8C85] font-bold shadow-sm bg-[#FFFFFF]' : 'text-[#9CA3AF] font-medium hover:text-[#6B7280]'"
          >
            Période de réflexion
          </button>
          <button
              @click="activeTab = 'historique'"
              class="flex-1 py-3 px-2 text-[14px] sm:text-[15px] transition-all duration-300 z-10 rounded-[12px] whitespace-nowrap"
              :class="activeTab === 'historique' ? 'text-[#5B8C85] font-bold shadow-sm bg-[#FFFFFF]' : 'text-[#9CA3AF] font-medium hover:text-[#6B7280]'"
          >
            Historique
          </button>
        </div>
      </div>

      <!-- Section 1: Intentions d'achat en cours (Affichée seulement si l'onglet est 'reflexion') -->
      <section v-if="activeTab === 'reflexion'" class="mb-10 animate-fade-in">
        <div v-if="visibleActiveItems.length > 0" class="flex flex-col gap-4">
          <!-- Active Items List -->
          <div v-for="item in visibleActiveItems" :key="item.id" class="bg-[#FFFFFF] rounded-[20px] p-5 shadow-sm">

            <!-- Header -->
            <div class="flex justify-between items-center mb-1">
              <h3 class="text-base font-bold text-[#000000]">{{ item.name }}</h3>
              <span class="text-[15px] font-bold text-[#5B8C85]">
                {{ item.price }} {{ currencyStore.currentCurrency.code }}
              </span>
            </div>

            <!-- Progress Bar & Timer Area -->
            <div class="mb-4">
              <span class="text-[13px]" :class="item.timeLeft === 'Expiré' ? 'text-[#F95E5A] font-bold' : 'text-[#DE9D9B]'">
                {{ item.timeLeft === 'Expiré' ? 'Délai expiré (En attente de clôture)' : 'Expire dans ' + item.timeLeft }}
              </span>
              <div class="w-full sm:w-1/2 h-2.5 bg-[#E5E7EB] rounded-full mt-1 overflow-hidden">
                <div class="h-full bg-[#DE9D9B] rounded-full transition-all duration-1000 ease-linear" :style="{ width: item.progress + '%' }"></div>
              </div>
            </div>

            <!-- Action Buttons (Acheté / Abandonné) -->
            <div class="flex gap-3 sm:gap-4">
              <button @click="updateDecision(item.id, 'ABANDON')" class="flex-1 bg-[#5B8C85] text-[#FFFFFF] py-3 sm:py-2.5 rounded-[12px] font-medium transition-opacity hover:opacity-90">
                Abandonné
              </button>
              <button @click="updateDecision(item.id, 'BUY')" class="flex-1 bg-[#F95E5A] text-[#FFFFFF] py-3 sm:py-2.5 rounded-[12px] font-medium transition-opacity hover:opacity-90">
                Acheté
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center bg-white rounded-[20px] p-8 shadow-sm flex flex-col items-center justify-center">
          <div class="w-16 h-16 bg-[#F8F6F2] rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-[#9CA3AF]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-[#999999] text-[15px] font-medium">Aucune analyse en cours de réflexion.</p>
        </div>

        <!-- Voir Plus Toggle -->
        <button v-if="activeItems.length > 3" @click="showAllActive = !showAllActive" class="w-full mt-6 flex items-center justify-center gap-2 text-[#5B8C85] font-bold text-[17px] hover:text-[#4a736d] transition-colors">
          {{ showAllActive ? 'Voir moins' : 'Voir plus' }}
          <svg class="w-5 h-5 transition-transform" :class="{ 'rotate-180': showAllActive }" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </section>

      <!-- Section 2: Historique des analyses (Affichée seulement si l'onglet est 'historique') -->
      <section v-if="activeTab === 'historique'" class="animate-fade-in">

        <!-- Controls & Filters... -->
        <div class="flex gap-3 mb-6 relative">
          <div class="flex-1 flex items-center bg-[#FFFFFF] rounded-[16px] px-4 py-3.5 shadow-sm">
            <svg class="w-6 h-6 text-[#999999] mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input type="text" v-model="searchQuery" placeholder="Rechercher un produit..." class="w-full bg-transparent text-[#000000] placeholder-[#D9D9D9] focus:outline-none">
          </div>

          <button @click="showFilters = !showFilters" class="bg-[#FFFFFF] w-14 rounded-[16px] flex items-center justify-center shadow-sm text-[#999999] hover:text-[#000000] transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
            </svg>
          </button>

          <!-- Filter Dropdown -->
          <div v-if="showFilters" class="absolute top-[60px] right-0 bg-[#FFFFFF] shadow-lg rounded-[16px] p-5 w-72 z-10 border border-[#D9D9D9]/30">
            <h4 class="font-bold text-[#000000] mb-2 text-[14px]">Filtrer par statut</h4>
            <div class="mb-4">
              <CustomSelect
                  v-model="filterStatus"
                  :options="statusOptions"
                  sizeClass="py-2 px-3 h-auto text-[14px] bg-[#F8F6F2] border-none font-medium"
                  roundedClass="rounded-[8px]"
              />
            </div>

            <hr class="border-[#D9D9D9] mb-4">

            <h4 class="font-bold text-[#000000] mb-2 text-[14px]">Trier par</h4>
            <CustomSelect
                v-model="sortBy"
                :options="sortOptions"
                sizeClass="py-2 px-3 h-auto text-[14px] bg-[#F8F6F2] border-none font-medium"
                roundedClass="rounded-[8px]"
            />
          </div>
        </div>

        <!-- History List -->
        <div class="flex flex-col gap-3">
          <div v-for="item in paginatedHistory" :key="item.id" class="bg-[#FFFFFF] rounded-[16px] p-4 flex items-center justify-between shadow-sm">
            <div class="pr-3">
              <h3 class="text-[15px] font-bold text-[#000000] truncate max-w-[180px] sm:max-w-xs">{{ item.name }}</h3>
              <p class="text-[13px] text-[#6B7280] mt-1 flex items-center flex-wrap gap-1">
                <span>{{ item.date }}</span> <span class="text-[10px]">•</span> <span>{{ item.category }}</span>
              </p>
            </div>
            <span class="w-24 sm:w-28 flex-shrink-0 text-center py-1.5 rounded-full text-[#FFFFFF] text-[12px] sm:text-[13px] font-medium"
                  :class="item.status === 'Abandonné' ? 'bg-[#5B8C85]' : 'bg-[#F95E5A]'">
              {{ item.status }}
            </span>
          </div>
        </div>

        <div v-if="paginatedHistory.length === 0" class="text-center text-[#999999] py-8">
          Aucun résultat trouvé pour ces filtres.
        </div>

        <!-- Load More -->
        <button v-if="hasMoreHistory" @click="loadMoreHistory" class="w-full mt-6 flex items-center justify-center gap-2 text-[#5B8C85] font-bold text-[17px] hover:text-[#4a736d] transition-colors">
          Voir plus
        </button>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import api from '@/services/api';
import { useCurrencyStore } from '@/stores/currency';
import CustomSelect from '@/components/shared/CustomSelect.vue';

const currencyStore = useCurrencyStore();

// Gestion des onglets
const activeTab = ref('reflexion'); // 'reflexion' | 'historique'

// Options pour les CustomSelects de filtrage
const statusOptions = [
  { value: 'all', label: 'Tous les statuts' },
  { value: 'Acheté', label: 'Acheté' },
  { value: 'Abandonné', label: 'Abandonné' }
];

const sortOptions = [
  { value: 'date', label: 'Date d\'analyse' },
  { value: 'price_asc', label: 'Prix (Croissant)' },
  { value: 'price_desc', label: 'Prix (Décroissant)' },
  { value: 'category', label: 'Catégorie' }
];

// ==========================================
// SECTION 1: INTENTIONS EN COURS
// ==========================================
const showAllActive = ref(false);
const activeItems = ref([]);
let countdownInterval = null;

const visibleActiveItems = computed(() => {
  return showAllActive.value ? activeItems.value : activeItems.value.slice(0, 3);
});

// Calcule la différence de temps en temps réel
const calculateProgress = () => {
  const now = new Date().getTime();

  activeItems.value.forEach(item => {
    if (!item.expiresAt) return;

    const expires = new Date(item.expiresAt).getTime();
    const updated = new Date(item.updatedAt).getTime();

    const totalDuration = expires - updated;
    const remainingTime = expires - now;

    if (remainingTime <= 0) {
      item.timeLeft = "Expiré";
      item.progress = 0;
    } else {
      // Conversion en HH:MM:SS
      const h = Math.floor(remainingTime / (1000 * 60 * 60));
      const m = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
      const s = Math.floor((remainingTime % (1000 * 60)) / 1000);

      item.timeLeft = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;

      // Barre de progression (% restant)
      item.progress = Math.max(0, Math.min(100, (remainingTime / totalDuration) * 100));
    }
  });
};

// Charge les intentions avec statut = 'Attendre' (qui correspond à CALM)
const fetchActiveIntentions = async () => {
  try {
    const response = await api.get('/purchase-intentions/history/', {
      params: { status: 'Attendre', page_size: 50 }
    });

    activeItems.value = response.data.results.map(item => ({
      id: item.id,
      name: item.product_name,
      price: parseFloat(item.product_price),
      expiresAt: item.cooldown_expires_at,
      updatedAt: item.updated_at,
      timeLeft: 'Calcul...',
      progress: 100
    }));

    calculateProgress(); // Force le premier calcul immédiatement
  } catch (error) {
    console.error("Erreur chargement analyses en cours:", error);
  }
};

// Clôturer une analyse (Acheté / Abandonné)
const updateDecision = async (id, decisionCode) => {
  try {
    await api.patch(`/purchase-intentions/${id}/final-decision/`, {
      user_final_decision: decisionCode
    });
    // On rafraîchit la page : l'item passe des 'actifs' vers l'historique
    fetchActiveIntentions();
    fetchHistory(true);
  } catch (err) {
    console.error("Erreur lors de la mise à jour :", err);
  }
};

// ==========================================
// SECTION 2: HISTORIQUE
// ==========================================
const searchQuery = ref('');
const showFilters = ref(false);
const filterStatus = ref('all');
const filterCategory = ref('all');
const filterPrice = ref('all');
const sortBy = ref('date');

const historyItems = ref([]);
const currentPage = ref(1);
const hasMoreHistory = ref(false);

const mapStatusToLabel = (dbStatus) => {
  const map = {
    'BUY': 'Acheté',
    'ABANDON': 'Abandonné'
  };
  return map[dbStatus] || 'Inconnu';
};

const formatDate = (isoString) => {
  return new Date(isoString).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
};

const fetchHistory = async (reset = false) => {
  if (reset) {
    currentPage.value = 1;
    historyItems.value = [];
  }
  try {
    const response = await api.get('/purchase-intentions/history/', {
      params: {
        page: currentPage.value,
        search: searchQuery.value,
        status: filterStatus.value,
        category: filterCategory.value,
        price: filterPrice.value,
        sort_by: sortBy.value
      }
    });
    const formattedResults = response.data.results.map(item => ({
      id: item.id,
      name: item.product_name,
      date: formatDate(item.created_at),
      category: item.product_category,
      price: parseFloat(item.product_price),
      status: mapStatusToLabel(item.user_final_decision)
    }));

    if (reset) historyItems.value = formattedResults;
    else historyItems.value.push(...formattedResults);

    hasMoreHistory.value = response.data.next !== null;
  } catch (error) {
    console.error("Erreur Historique:", error);
  }
};

const paginatedHistory = computed(() => historyItems.value);

const loadMoreHistory = () => {
  if (hasMoreHistory.value) {
    currentPage.value++;
    fetchHistory(false);
  }
};

watch([searchQuery, filterStatus, filterCategory, filterPrice, sortBy], () => {
  fetchHistory(true);
});

// ==========================================
// CYCLE DE VIE
// ==========================================
onMounted(() => {
  fetchActiveIntentions();
  fetchHistory(true);

  // Met à jour l'horloge toutes les 1000ms (1 seconde)
  countdownInterval = setInterval(calculateProgress, 1000);
});

onUnmounted(() => {
  // Détruit le chronomètre quand on quitte la page pour éviter les fuites de mémoire
  if (countdownInterval) clearInterval(countdownInterval);
});
</script>

<style scoped>
/* Animation douce lors du basculement d'onglets */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>