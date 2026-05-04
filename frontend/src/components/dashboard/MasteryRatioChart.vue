<template>
  <div class="bg-white rounded-[24px] p-6 shadow-sm border border-gray-100 flex flex-col gap-5">

    <!-- En-tête du composant -->
    <div class="flex justify-between items-start">
      <div>
        <h3 class="text-[17px] font-bold text-gray-900 leading-tight">Taux d’achats évités</h3>
        <p class="text-[13px] text-gray-500 mt-1">Sur le total de vos intentions ce mois-ci</p>
      </div>
      <div class="bg-[#E1EBE8] px-3 py-1.5 rounded-xl shadow-inner">
        <span class="text-xl font-black text-[#5B8C85]">{{ percentage }}%</span>
      </div>
    </div>

    <!-- Barre de progression -->
    <div class="relative w-full pt-2">
      <!-- Arrière-plan (Piste) -->
      <div class="w-full h-4 bg-gray-100 rounded-full overflow-hidden shadow-inner">
        <!-- Remplissage dynamique avec dégradé -->
        <div
            class="h-full bg-gradient-to-r from-[#80E8C4] to-[#5B8C85] rounded-full transition-all duration-1000 ease-out"
            :style="{ width: `${percentage}%` }"
        ></div>
      </div>
    </div>

    <!-- Légende -->
    <div class="flex justify-between items-center text-xs font-semibold text-gray-400 mt-1">
      <span class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-[#5B8C85] shadow-sm"></span>
        Achats abandonnés
      </span>
      <span class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-gray-200 shadow-sm"></span>
        Achats effectués
      </span>
    </div>

  </div>
</template>

<script setup>
defineProps({
  percentage: {
    type: Number,
    required: true,
    default: 0
  }
});
</script>