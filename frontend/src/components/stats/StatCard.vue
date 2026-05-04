<template>
  <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-50 flex flex-col justify-between h-32 transition-transform active:scale-95">
    <div class="flex items-center justify-between">
      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{{ title }}</span>
      <div class="p-2 bg-[#F0F5F4] rounded-lg">
        <slot name="icon"></slot>
      </div>
    </div>
    <div>
      <span class="text-2xl font-bold text-gray-900">{{ value }}</span>
      <span v-if="unit" class="text-xs font-semibold text-gray-400 ml-1">{{ unit }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  unit: String
});
</script>