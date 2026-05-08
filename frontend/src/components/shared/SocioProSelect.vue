<template>
  <div class="space-y-2">
    <div class="flex justify-between items-end">
      <label class="block text-lg font-medium text-gray-900"
        >Catégorie socio-pro</label
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
      <span class="text-gray-500 truncate"> Sélectionner (max 3)... </span>
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
        v-for="cat in modelValue"
        :key="cat"
        class="bg-[#5A877E] text-white px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2 shadow-sm"
      >
        <span>{{ cat }}</span>
        <button
          @click.stop="removeCategory(cat)"
          type="button"
          class="hover:bg-[#436b62] rounded-full p-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-white"
          aria-label="Supprimer la catégorie"
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
      Choisissez au moins 1 catégorie.
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
                  Catégories ({{ tempSelection.length }}/3)
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

            <div class="px-6 py-4 shrink-0">
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
                  placeholder="Rechercher une catégorie..."
                  class="w-full pl-10 pr-4 py-3 bg-gray-100 border-transparent rounded-xl focus:bg-white focus:border-[#5A877E] focus:ring-2 focus:ring-[#5A877E]/20 outline-none transition-all text-gray-700"
                />
              </div>
            </div>

            <div class="flex-1 overflow-y-auto px-4 pb-24">
              <div
                v-if="filteredCategories.length === 0"
                class="text-center py-10 text-gray-500"
              >
                Aucune catégorie trouvée.
              </div>
              <ul v-else class="space-y-1">
                <li v-for="cat in filteredCategories" :key="cat">
                  <label
                    class="flex items-center p-4 rounded-xl cursor-pointer transition-colors"
                    :class="[
                      tempSelection.includes(cat)
                        ? 'bg-teal-50'
                        : 'hover:bg-gray-50',
                      tempSelection.length >= 3 &&
                      !tempSelection.includes(cat) &&
                      cat !== 'Préfère ne pas répondre'
                        ? 'opacity-50 cursor-not-allowed'
                        : '',
                    ]"
                  >
                    <div
                      class="flex-1 pr-4 text-gray-800 font-medium leading-tight"
                    >
                      {{ cat }}
                    </div>

                    <div
                      class="w-6 h-6 rounded border flex items-center justify-center shrink-0 transition-colors"
                      :class="
                        tempSelection.includes(cat)
                          ? 'bg-[#5A877E] border-[#5A877E]'
                          : 'border-gray-300 bg-white'
                      "
                    >
                      <svg
                        v-if="tempSelection.includes(cat)"
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
                      :value="cat"
                      :checked="tempSelection.includes(cat)"
                      @change="toggleCategoryInSheet(cat)"
                      :disabled="
                        tempSelection.length >= 3 &&
                        !tempSelection.includes(cat) &&
                        cat !== 'Préfère ne pas répondre'
                      "
                    />
                  </label>
                </li>
              </ul>
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

const availableCategories = [
  "Étudiant",
  "Employé",
  "Fonctionnaire",
  "Indépendant / Freelance",
  "Entrepreneur / Chef d'entreprise",
  "Commerçant / Artisan",
  "Profession libérale",
  "Ouvrier / Technicien",
  "Sans emploi",
  "Retraité",
  "Au foyer",
  "Autre",
  "Préfère ne pas répondre",
];

const isSheetOpen = ref(false);
const searchQuery = ref("");
const tempSelection = ref([]);
const searchInput = ref(null);

const filteredCategories = computed(() => {
  if (!searchQuery.value) return availableCategories;
  const q = searchQuery.value.toLowerCase().trim();
  return availableCategories.filter((cat) => cat.toLowerCase().includes(q));
});

const openSheet = () => {
  // On copie la sélection actuelle dans le state temporaire du modal
  tempSelection.value = [...props.modelValue];
  searchQuery.value = "";
  isSheetOpen.value = true;
  // Bloquer le scroll du body
  document.body.style.overflow = "hidden";

  // Focus auto sur la barre de recherche
  nextTick(() => {
    if (searchInput.value) searchInput.value.focus();
  });
};

const closeSheet = () => {
  isSheetOpen.value = false;
  document.body.style.overflow = "";
};

const toggleCategoryInSheet = (cat) => {
  let current = [...tempSelection.value];

  // Règle 1: Exclusivité "Préfère ne pas répondre"
  if (cat === "Préfère ne pas répondre") {
    if (current.includes(cat)) {
      tempSelection.value = []; // Désélection
    } else {
      tempSelection.value = ["Préfère ne pas répondre"]; // Sélection exclusive
    }
    return;
  }

  // Règle 2: Retirer "Préfère ne pas répondre" si une autre option est cliquée
  current = current.filter((c) => c !== "Préfère ne pas répondre");

  // Règle 3: Toggle standard avec limite de 3
  if (current.includes(cat)) {
    // Retirer
    current = current.filter((c) => c !== cat);
  } else {
    // Ajouter (si la limite de 3 n'est pas atteinte)
    if (current.length < 3) {
      current.push(cat);
    }
  }

  tempSelection.value = current;
};

const confirmSelection = () => {
  if (tempSelection.value.length > 0) {
    // On émet la nouvelle valeur vers le v-model du parent
    emit("update:modelValue", tempSelection.value);
    emit("validate"); // Pour déclencher la validation côté parent (retirer le message d'erreur)
    closeSheet();
  }
};

const removeCategory = (cat) => {
  const newSelection = props.modelValue.filter((c) => c !== cat);
  // Si on a tout supprimé, on remet le défaut "Préfère ne pas répondre" ou on laisse vide.
  // Selon vos règles, on peut laisser vide pour forcer l'utilisateur à re-choisir.
  emit(
    "update:modelValue",
    newSelection.length === 0 ? ["Préfère ne pas répondre"] : newSelection,
  );
  emit("validate");
};
</script>

<style scoped>
/* Animations pour le Bottom Sheet */
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
