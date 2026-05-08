<template>
  <div class="relative w-full" ref="containerRef">
    <input
      type="text"
      :id="id"
      v-model="internalValue"
      @input="onInput"
      @focus="onFocus"
      :placeholder="placeholder"
      autocomplete="off"
      :class="[
        'block w-full outline-none transition-all placeholder-gray-400 focus:ring-2 focus:ring-[#5A877E] focus:border-transparent',
        customClasses,
      ]"
    />

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
        v-show="isOpen && filteredOptions.length > 0"
        class="absolute z-50 w-full mt-2 bg-white border border-gray-100 shadow-lg max-h-60 overflow-y-auto py-2 rounded-2xl"
      >
        <li
          v-for="(option, index) in filteredOptions"
          :key="index"
          @click="selectOption(option)"
          class="px-5 py-3 cursor-pointer transition-colors text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-[#5A877E]"
        >
          <!-- v-html used securely here to inject bold tags for matching text -->
          <span v-html="highlightMatch(option)"></span>
        </li>
      </ul>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  modelValue: { type: String, default: "" },
  placeholder: { type: String, default: "Ex: Étudiant..." },
  id: { type: String, default: "profession" },
  customClasses: {
    type: String,
    default: "px-4 py-3 border border-gray-200 rounded-2xl text-sm",
  },
});

const emit = defineEmits(["update:modelValue"]);

const internalValue = ref(props.modelValue);
const isOpen = ref(false);
const containerRef = ref(null);

// Curated list of professions
const professions = [
  "Agriculteur",
  "Architecte",
  "Artisan",
  "Avocat",
  "Cadre",
  "Chef d'entreprise",
  "Commerçant",
  "Comptable",
  "Consultant",
  "Designer UI/UX",
  "Développeur Front-end",
  "Développeur Back-end",
  "Développeur Full-Stack",
  "Employé de bureau",
  "Enseignant",
  "Entrepreneur",
  "Étudiant",
  "Étudiant en informatique",
  "Ingénieur Logiciel",
  "Ingénieur Système",
  "Journaliste",
  "Lycéen",
  "Manageur",
  "Médecin",
  "Ouvrier",
  "Pharmacien",
  "Retraité",
  "Sans emploi",
  "Technicien IT",
  "Vendeur",
  "Autre",
];

// Filter logic
const filteredOptions = computed(() => {
  const query = internalValue.value
    ? internalValue.value.toLowerCase().trim()
    : "";
  if (!query) {
    // Show a few default suggestions when empty and focused
    return professions.slice(0, 5);
  }
  return professions.filter((p) => p.toLowerCase().includes(query));
});

// Event Handlers
const onInput = () => {
  isOpen.value = true;
  emit("update:modelValue", internalValue.value);
};

const onFocus = () => {
  isOpen.value = true;
};

const selectOption = (option) => {
  internalValue.value = option;
  emit("update:modelValue", option);
  isOpen.value = false;
};

// Text Highlighting for better UX
const highlightMatch = (text) => {
  if (!internalValue.value) return text;
  // Escape regex characters just in case
  const safeQuery = internalValue.value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${safeQuery})`, "gi");
  return text.replace(
    regex,
    '<span class="font-bold text-[#5A877E]">$1</span>',
  );
};

// Click-outside directive logic
const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

watch(
  () => props.modelValue,
  (newVal) => {
    internalValue.value = newVal;
  },
);

onMounted(() => document.addEventListener("click", handleClickOutside));
onUnmounted(() => document.removeEventListener("click", handleClickOutside));
</script>
