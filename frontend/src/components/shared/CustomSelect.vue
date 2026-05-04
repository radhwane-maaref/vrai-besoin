<template>
  <div class="relative w-full" ref="dropdownRef">
    <!-- Dropdown Trigger -->
    <button
        type="button"
        @click="toggleDropdown"
        class="w-full flex items-center justify-between px-5 bg-white border outline-none transition-all shadow-sm text-left"
        :class="[
        sizeClass,
        roundedClass,
        isOpen ? 'border-[#5A877E] ring-2 ring-[#5A877E]/20' : 'border-gray-200 hover:border-gray-300 focus:ring-2 focus:ring-[#5A877E]/20',
        error ? 'border-red-400 bg-red-50' : ''
      ]"
        :disabled="disabled"
    >
      <span :class="selectedLabel ? 'text-[#1F2937] font-semibold' : 'text-gray-400 font-medium'">
        {{ selectedLabel || placeholder }}
      </span>

      <!-- Chevron Icon -->
      <svg
          class="w-5 h-5 text-gray-400 transition-transform duration-300"
          :class="{ 'rotate-180': isOpen }"
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
    >
      <ul
          v-show="isOpen"
          class="absolute z-50 w-full mt-2 bg-white border border-gray-100 shadow-lg max-h-60 overflow-y-auto py-2"
          :class="roundedClass"
      >
        <li
            v-for="(option, index) in normalizedOptions"
            :key="index"
            @click="selectOption(option)"
            class="px-5 py-3 cursor-pointer transition-colors text-sm font-medium"
            :class="isSelected(option) ? 'bg-[#E1EBE8] text-[#5A877E]' : 'text-gray-700 hover:bg-gray-50'"
        >
          {{ option.label }}
        </li>
        <li v-if="normalizedOptions.length === 0" class="px-5 py-3 text-sm text-gray-400">
          Aucune option
        </li>
      </ul>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number, Object],
    default: ''
  },
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Sélectionnez une option'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: Boolean,
    default: false
  },
  // Allows customizing the height/padding based on where it's used
  sizeClass: {
    type: String,
    default: 'py-4 h-[58px]'
  },
  // Allows customizing border radius (e.g., rounded-xl for stats, rounded-3xl for forms)
  roundedClass: {
    type: String,
    default: 'rounded-3xl'
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const isOpen = ref(false);
const dropdownRef = ref(null);

// Normalizes array of strings ['A', 'B'] OR objects [{value: 'a', label: 'A'}]
const normalizedOptions = computed(() => {
  return props.options.map(opt => {
    if (typeof opt === 'object' && opt !== null) {
      return { value: opt.value, label: opt.label };
    }
    return { value: opt, label: opt };
  });
});

const selectedLabel = computed(() => {
  const selected = normalizedOptions.value.find(opt => opt.value === props.modelValue);
  return selected ? selected.label : '';
});

const isSelected = (option) => option.value === props.modelValue;

const toggleDropdown = () => {
  if (!props.disabled) isOpen.value = !isOpen.value;
};

const selectOption = (option) => {
  emit('update:modelValue', option.value);
  emit('change', option.value);
  isOpen.value = false;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onUnmounted(() => document.removeEventListener('click', handleClickOutside));
</script>