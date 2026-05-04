<template>
  <div class="mb-4">
    <h2 class="text-3xl font-bold text-black mb-4">Salut {{ userName }} !</h2>

    <div class="bg-gradient-to-r from-[#d9f2e6] to-[#e6f7ef] rounded-2xl p-4 shadow-sm relative overflow-hidden">
      <div class="flex justify-between items-start">
        <h3 class="font-bold text-gray-900 mb-1">Coach IA</h3>
        <svg class="w-6 h-6 text-[#5A877E] opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
        </svg>
      </div>
      <p class="text-sm text-gray-700 leading-snug">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  userName: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  }
});
</script>