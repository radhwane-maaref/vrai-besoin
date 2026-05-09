<template>
  <div class="space-y-2">
    <div class="flex justify-between items-end">
      <label class="block text-lg font-medium text-gray-900"
        >Objectifs financiers</label
      >
      <span
        class="text-xs font-semibold px-2 py-0.5 rounded-md"
        :class="
          modelValue.length === 3
            ? 'bg-[#5A877E] text-white'
            : 'bg-gray-200 text-gray-500'
        "
      >
        {{ modelValue.length }} / 3
      </span>
    </div>

    <div
      @click="openSheet"
      class="w-full px-4 py-3.5 border rounded-2xl bg-white shadow-sm flex justify-between items-center cursor-pointer transition-colors"
      :class="
        error
          ? 'border-red-400 bg-red-50'
          : 'border-gray-200 hover:border-[#5A877E]'
      "
    >
      <span class="text-gray-500 truncate">
        {{
          modelValue.length === 0
            ? "Sélectionner (max 3)..."
            : "Modifier les objectifs..."
        }}
      </span>
      <svg
        class="w-5 h-5 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 9l-7 7-7-7"
        />
      </svg>
    </div>

    <div v-if="modelValue.length > 0" class="flex flex-wrap gap-2 pt-1">
      <div
        v-for="goal in modelValue"
        :key="goal"
        class="bg-[#5A877E] text-white px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2 shadow-sm"
      >
        <span>{{ goal }}</span>
        <button
          @click.stop="removeCategory(goal)"
          type="button"
          class="hover:bg-[#436b62] rounded-full p-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-white"
          aria-label="Supprimer l'objectif"
        >
          <svg
            class="w-3.5 h-3.5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2.5"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <p v-if="error" class="text-xs text-red-500 font-medium ml-2">
      {{ error }}
    </p>
    <p v-else-if="modelValue.length === 0" class="text-xs text-gray-500 ml-2">
      Choisissez au moins 1 objectif.
    </p>

    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="isSheetOpen"
          class="fixed inset-0 z-50 flex flex-col justify-end"
        >
          <div
            class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
            @click="closeSheet"
          ></div>

          <div
            class="relative bg-white w-full h-[85vh] md:h-[70vh] md:max-w-md md:mx-auto rounded-t-3xl flex flex-col shadow-2xl"
          >
            <div
              class="pt-4 pb-2 px-6 flex flex-col items-center border-b border-gray-100 shrink-0"
            >
              <div class="w-12 h-1.5 bg-gray-300 rounded-full mb-4"></div>
              <div class="flex justify-between items-center w-full">
                <h2 class="text-xl font-bold text-gray-900">
                  Objectifs ({{ tempSelection.length }}/3)
                </h2>
                <button
                  @click="closeSheet"
                  class="p-2 -mr-2 text-gray-400 hover:text-gray-700 bg-gray-50 rounded-full"
                >
                  <svg
                    class="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <div class="px-6 pt-4 pb-2 shrink-0">
              <div class="relative">
                <div
                  class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                >
                  <svg
                    class="w-5 h-5 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
                <input
                  ref="searchInput"
                  v-model="searchQuery"
                  type="text"
                  placeholder="Rechercher un objectif..."
                  class="w-full pl-10 pr-4 py-3 bg-gray-100 border-transparent rounded-xl focus:bg-white focus:border-[#5A877E] focus:ring-2 focus:ring-[#5A877E]/20 outline-none transition-all text-gray-700"
                />
              </div>
            </div>

            <div class="px-6 pb-4 shrink-0 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <input
                  v-model="customGoalInput"
                  @keyup.enter="handleAddCustomGoal"
                  type="text"
                  placeholder="Ou ajoutez un objectif manuellement..."
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:border-[#5A877E] focus:ring-2 focus:ring-[#5A877E]/20 outline-none transition-all text-gray-700"
                  :disabled="tempSelection.length >= 3"
                />
                <button
                  @click="handleAddCustomGoal"
                  :disabled="
                    !customGoalInput.trim() || tempSelection.length >= 3
                  "
                  class="p-3 bg-[#5A877E] text-white rounded-xl hover:bg-[#436b62] transition-colors disabled:opacity-50 disabled:cursor-not-allowed shrink-0 shadow-sm"
                  aria-label="Ajouter"
                >
                  <svg
                    class="w-6 h-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2.5"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex-1 overflow-y-auto px-4 pb-24 pt-2">
              <ul class="space-y-1">
                <li v-for="item in displayItems" :key="item">
                  <label
                    class="flex items-center p-4 rounded-xl cursor-pointer transition-colors"
                    :class="[
                      tempSelection.includes(item)
                        ? 'bg-teal-50/50'
                        : 'hover:bg-gray-50',
                      tempSelection.length >= 3 &&
                      !tempSelection.includes(item) &&
                      item !== 'Je préfère ne pas répondre'
                        ? 'opacity-50 cursor-not-allowed'
                        : '',
                    ]"
                  >
                    <div
                      class="flex-1 pr-4 text-gray-800 font-medium leading-tight"
                    >
                      <span>{{ item }}</span>
                    </div>

                    <div
                      class="w-6 h-6 rounded flex items-center justify-center shrink-0 transition-colors"
                      :class="
                        tempSelection.includes(item)
                          ? 'bg-[#5A877E] border-transparent'
                          : 'border border-gray-300 bg-white'
                      "
                    >
                      <svg
                        v-if="tempSelection.includes(item)"
                        class="w-4 h-4 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="3"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>

                    <input
                      type="checkbox"
                      class="hidden"
                      :value="item"
                      :checked="tempSelection.includes(item)"
                      @change="toggleCategoryInSheet(item)"
                      :disabled="
                        tempSelection.length >= 3 &&
                        !tempSelection.includes(item) &&
                        item !== 'Je préfère ne pas répondre'
                      "
                    />
                  </label>
                </li>
              </ul>
              <div
                v-if="displayItems.length === 0"
                class="text-center py-10 text-gray-500"
              >
                Aucun objectif trouvé.
              </div>
            </div>

            <div
              class="absolute bottom-0 left-0 w-full p-6 bg-white border-t border-gray-100 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] rounded-t-3xl"
            >
              <button
                @click="confirmSelection"
                :disabled="tempSelection.length === 0"
                class="w-full py-4 rounded-2xl font-bold text-lg transition-all active:scale-[0.98] shadow-sm"
                :class="
                  tempSelection.length > 0
                    ? 'bg-[#5A877E] text-white hover:bg-[#436b62]'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                "
              >
                Valider la sélection ({{ tempSelection.length }})
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from "vue";

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: () => [],
  },
  error: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["update:modelValue", "validate"]);

const baseCategories = [
  "Réduire les dépenses impulsives",
  "Épargner pour un projet",
  "Rembourser des dettes",
  "Investir pour l'avenir",
  "Créer un fonds d'urgence",
  "Acheter un bien immobilier",
  "Je préfère ne pas répondre",
];

const isSheetOpen = ref(false);
const searchQuery = ref("");
const customGoalInput = ref(""); // Nouvel état pour le champ d'ajout manuel
const tempSelection = ref([]);
const customCategories = ref([]);
const searchInput = ref(null);

const allCategories = computed(() => {
  return Array.from(
    new Set([
      ...baseCategories,
      ...props.modelValue,
      ...customCategories.value,
    ]),
  );
});

// La recherche ne fait plus qu'un simple filtrage
const displayItems = computed(() => {
  const q = searchQuery.value.toLowerCase().trim();
  const base = allCategories.value;

  if (!q) {
    return base;
  }

  return base.filter((cat) => cat.toLowerCase().includes(q));
});

const openSheet = () => {
  tempSelection.value = [...props.modelValue];
  searchQuery.value = "";
  customGoalInput.value = "";
  isSheetOpen.value = true;
  document.body.style.overflow = "hidden";

  nextTick(() => {
    if (searchInput.value) searchInput.value.focus();
  });
};

const closeSheet = () => {
  isSheetOpen.value = false;
  document.body.style.overflow = "";
};

const toggleCategoryInSheet = (goal) => {
  let current = [...tempSelection.value];

  if (goal === "Je préfère ne pas répondre") {
    if (current.includes(goal)) {
      tempSelection.value = [];
    } else {
      tempSelection.value = ["Je préfère ne pas répondre"];
    }
    return;
  }

  current = current.filter((c) => c !== "Je préfère ne pas répondre");

  if (current.includes(goal)) {
    current = current.filter((c) => c !== goal);
  } else {
    if (current.length < 3) {
      current.push(goal);
    }
  }

  tempSelection.value = current;
};

// Nouvelle fonction dédiée à l'ajout via l'input spécifique
const handleAddCustomGoal = () => {
  const goalText = customGoalInput.value.trim();

  if (!goalText || tempSelection.value.length >= 3) return;

  let current = [...tempSelection.value];
  current = current.filter((c) => c !== "Je préfère ne pas répondre");

  // Si l'objectif n'existe pas encore dans la sélection, on l'ajoute
  if (!current.includes(goalText)) {
    current.push(goalText);
    customCategories.value.push(goalText);
  }

  tempSelection.value = current;
  customGoalInput.value = ""; // On vide le champ après l'ajout
};

const confirmSelection = () => {
  if (tempSelection.value.length > 0) {
    emit("update:modelValue", tempSelection.value);
    emit("validate");
    closeSheet();
  }
};

const removeCategory = (goal) => {
  const newSelection = props.modelValue.filter((c) => c !== goal);
  emit(
    "update:modelValue",
    newSelection.length === 0 ? ["Je préfère ne pas répondre"] : newSelection,
  );
  emit("validate");
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active .bg-white {
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.fade-leave-active .bg-white {
  transition: transform 0.2s ease-in;
}
.fade-enter-from .bg-white,
.fade-leave-to .bg-white {
  transform: translateY(100%);
}
</style>
