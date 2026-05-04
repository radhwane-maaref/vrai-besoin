<template>
  <div class="min-h-screen bg-[#F8F6F2] px-4 py-6 pb-24 font-sans">
    <h1 class="text-xl font-medium text-gray-800 mb-6">Tableau de bord Vrai Besoin</h1>

    <div v-if="isLoading" class="flex justify-center items-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#5B8C85]"></div>
    </div>

    <div v-else-if="dashboardData" class="space-y-6">
      <AiCoachMessage
          :user-name="dashboardData.user_name"
          :message="dashboardData.ai_coach_message"
      />
      <!-- On rapelle l'utilisateur de finaliser sa décision -->
      <ReminderBanner
          v-if="dashboardData.pending_intentions"
          :intentions="dashboardData.pending_intentions"
      />

      <!-- NOUVEAU : Carte des économies du mois -->
      <div class="bg-gradient-to-r from-[#5B8C85] to-[#4a736d] rounded-[24px] p-6 shadow-sm text-white">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm font-medium opacity-90 mb-1">Économies ce mois-ci</p>
            <div class="flex items-baseline gap-1.5">
              <!-- Formatage à 2 décimales pour un affichage financier propre -->
              <h2 class="text-4xl font-bold">
                {{ Number(dashboardData.stats.monthly_savings).toFixed(2) }}
              </h2>
              <!-- Utilisation du store Pinia pour la devise -->
              <span class="text-lg font-medium opacity-90">
          {{ currencyStore.currentCurrency.code }}
        </span>
            </div>
          </div>

          <!-- Icône tirelire / économie -->
          <div class="bg-white/20 p-3 rounded-2xl backdrop-blur-sm">
            <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>


      <MasteryRatioChart
          :percentage="dashboardData.mastery_ratio"
      />

      <SavingsCard
          v-if="dashboardData.savings_goal"
          :goal-name="dashboardData.savings_goal.goal_name"
          :current-amount="dashboardData.savings_goal.saved_amount"
          :target-amount="dashboardData.savings_goal.target_amount"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import api from '@/services/api';
import {useCurrencyStore} from '@/stores/currency';

import AiCoachMessage from '@/components/dashboard/AiCoachMessage.vue';
import MasteryRatioChart from '@/components/dashboard/MasteryRatioChart.vue';
import SavingsCard from '@/components/dashboard/SavingsCard.vue';
import ReminderBanner from '@/components/dashboard/ReminderBanner.vue'; // NOUVEAU

const isLoading = ref(true);
const dashboardData = ref(null);
const currencyStore = useCurrencyStore();

onMounted(async () => {
  try {
    const response = await api.get('/dashboard/summary/');
    dashboardData.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement du dashboard :", error);
  } finally {
    isLoading.value = false;
  }
});
</script>