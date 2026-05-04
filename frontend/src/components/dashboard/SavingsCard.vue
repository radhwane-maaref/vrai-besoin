<template>
  <div class="bg-white rounded-3xl p-5 shadow-sm border border-gray-50">
    <div class="flex justify-between items-start mb-1">
      <h3 class="text-xl font-bold text-gray-900">Savings Goal</h3>
      <div class="flex items-center gap-1.5 bg-gray-100 px-3 py-1 rounded-full">
        <span class="text-[#5A877E] text-xs">💎</span>
        <span class="text-xs font-bold text-gray-600">Premium</span>
      </div>
    </div>

    <p class="text-sm text-gray-600 mb-4">Objectif: {{ goalName }}</p>

    <div class="w-full bg-gray-200 rounded-full h-2.5 mb-2 overflow-hidden">
      <div
          class="bg-[#5A877E] h-2.5 rounded-full transition-all duration-700 ease-out"
          :style="{ width: progressWidth }"
      ></div>
    </div>

    <div class="flex justify-between items-center text-sm">
      <div class="font-bold">
        <span class="text-[#5A877E]">{{ currentAmount }} TND</span>
        <span class="text-gray-400 font-normal ml-1">saved</span>
      </div>
      <div class="text-gray-800 font-medium">{{ targetAmount }} TND</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  goalName: { type: String, required: true },
  currentAmount: { type: Number, required: true },
  targetAmount: { type: Number, required: true }
});

// Propriété calculée pour la largeur de la barre (max 100%)
const progressWidth = computed(() => {
  if (props.targetAmount <= 0) return '0%';
  const rawPercentage = (props.currentAmount / props.targetAmount) * 100;
  // Math.min s'assure que la barre ne dépasse pas 100% même si on économise plus
  const safePercentage = Math.min(rawPercentage, 100);
  return `${safePercentage}%`;
});
</script>