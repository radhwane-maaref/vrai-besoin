<template>
  <header class="flex items-center gap-4 sm:gap-5 mb-8 sm:mb-10">
    <button
        @click="router.push({ name: 'settings' })"
        class="text-[#9CA3AF] hover:text-[#6B7280] transition-colors focus:outline-none flex items-center justify-center"
        aria-label="Retour aux paramètres"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 sm:w-8 sm:h-8" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="20" y1="12" x2="4" y2="12"></line>
        <polyline points="10 19 3 12 10 5"></polyline>
      </svg>
    </button>
    <h1 class="text-2xl sm:text-3xl font-bold text-[#000000]">
      {{ title }}
    </h1>
  </header>
</template>

<script setup>
import {useRouter} from 'vue-router';

defineProps({
  title: {
    type: String,
    required: true
  }
});
const router = useRouter();
</script>