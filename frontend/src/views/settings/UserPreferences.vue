<template>
  <!-- Full page wrapper centering the content on large screens -->
  <div
    class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] flex justify-center"
  >
    <!-- Responsive inner container -->
    <div class="w-full max-w-3xl px-4 sm:px-6 md:px-8 py-6 sm:py-8 lg:py-10">
      <SettingsPageHeader title="Mes préférences" />

      <!-- Période de réflexion Section -->
      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
        <!-- Title & Icon -->
        <div class="flex items-center gap-3">
          <img
            src="../../assets/Sport%20Stopwatch.png"
            alt="Timer Icon"
            class="w-6 h-6 sm:w-8 sm:h-8 object-contain"
          />
          <h2 class="text-xl sm:text-2xl font-bold text-[#000000]">
            Période de réflexion
          </h2>
        </div>

        <!-- Description -->
        <p
          class="mt-3 sm:mt-4 text-[#6B7280] text-[14px] sm:text-[16px] leading-relaxed"
        >
          Temps d'attente imposé avant de valider un achat impulsif.
        </p>

        <!-- Interactive Slider Area -->
        <div class="mt-6 sm:mt-8 mb-2">
          <input
            type="range"
            min="0"
            max="3"
            step="1"
            v-model="periodIndex"
            class="custom-slider w-full"
          />

          <!-- Dynamic Labels -->
          <div class="flex justify-between mt-4 px-1">
            <span
              v-for="(label, index) in labels"
              :key="index"
              @click="periodIndex = index"
              class="text-[13px] sm:text-[15px] cursor-pointer transition-colors duration-200"
              :class="
                periodIndex == index
                  ? 'text-[#5B8C85] font-bold'
                  : 'text-[#9CA3AF] font-normal'
              "
            >
              {{ label }}
            </span>
          </div>
        </div>
      </section>

      <!-- Configuration Section Heading -->
      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Configuration
      </h2>

      <!-- Configuration Card -->
      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
        <!-- Devise (Currency) -->
        <div class="mb-6 sm:mb-8 relative z-50">
          <h3 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
            Devise
          </h3>

          <!-- Custom Dropdown Container -->
          <div class="relative w-full">
            <!-- Dropdown Trigger -->
            <button
              @click="isDropdownOpen = !isDropdownOpen"
              class="w-full flex items-center justify-between border border-[#D9D9D9] bg-[#FFFFFF] rounded-[12px] sm:rounded-[15px] px-3 sm:px-4 py-2.5 sm:py-3 focus:outline-none focus:ring-2 focus:ring-[#5B8C85]/30 transition-all"
            >
              <div class="flex items-center gap-2 sm:gap-3">
                <span class="text-xl sm:text-2xl leading-none">{{
                  selectedCurrency.flag
                }}</span>
                <span
                  class="text-[15px] sm:text-base text-[#9CA3AF] font-medium"
                  >{{ selectedCurrency.code }}</span
                >
              </div>
              <!-- Chevron Icon -->
              <svg
                class="w-4 h-4 sm:w-5 sm:h-5 text-[#9CA3AF] transition-transform duration-300"
                :class="{ 'rotate-180': isDropdownOpen }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2.5"
                  d="M19 9l-7 7-7-7"
                />
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
                v-if="isDropdownOpen"
                class="absolute z-50 w-full mt-2 bg-[#FFFFFF] border border-[#D9D9D9] rounded-[12px] sm:rounded-[15px] shadow-lg max-h-60 overflow-y-auto py-2"
              >
                <li
                  v-for="currency in currencies"
                  :key="currency.code"
                  @click="selectCurrency(currency)"
                  class="flex items-center gap-2 sm:gap-3 px-3 sm:px-4 py-2.5 cursor-pointer hover:bg-[#F8F6F2] transition-colors"
                  :class="{
                    'bg-[#F8F6F2]': selectedCurrency.code === currency.code,
                  }"
                >
                  <span class="text-xl sm:text-2xl leading-none">{{
                    currency.flag
                  }}</span>
                  <span
                    class="text-[14px] sm:text-[15px] text-[#6B7280] font-medium"
                    >{{ currency.code }} - {{ currency.name }}</span
                  >
                </li>
              </ul>
            </transition>
          </div>
        </div>

        <!-- Niveau de rigueur d'évaluation -->
        <div>
          <h3 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
            Niveau de rigueur d'évaluation
          </h3>

          <!-- Toggle Container -->
          <div
            class="bg-[#E5E7EB] rounded-[12px] sm:rounded-[15px] p-1 sm:p-1.5 flex w-full relative"
          >
            <button
              v-for="(level, index) in rigueurLevels"
              :key="level"
              @click="selectedRigueur = level"
              class="flex-1 py-2 sm:py-2.5 px-1 sm:px-0 text-center text-[13px] sm:text-[15px] transition-all duration-300 z-10 rounded-[10px] sm:rounded-[12px] whitespace-nowrap"
              :class="
                selectedRigueur === level
                  ? 'text-[#5B8C85] font-bold shadow-sm bg-[#FFFFFF]'
                  : 'text-[#9CA3AF] font-medium hover:text-[#6B7280]'
              "
            >
              {{ level }}
            </button>
          </div>
        </div>
      </section>

      <!-- Notifications Section Heading -->
      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Notifications
      </h2>

      <!-- Notifications Card -->
      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
        <div class="flex items-center justify-between gap-3 sm:gap-4">
          <!-- Icon and Text Group -->
          <div class="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <!-- Fixed width icon container for perfect alignment -->
            <div
              class="w-10 sm:w-12 flex-shrink-0 flex justify-center items-center text-[#5B8C85]"
            >
              <!-- Bell Icon -->
              <svg
                class="w-7 h-7 sm:w-8 sm:h-8"
                viewBox="0 0 24 24"
                fill="currentColor"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 22C13.1 22 14 21.1 14 20H10C10 21.1 10.9 22 12 22ZM18 16V11C18 7.93 16.36 5.36 13.5 4.68V4C13.5 3.17 12.83 2.5 12 2.5C11.17 2.5 10.5 3.17 10.5 4V4.68C7.63 5.36 6 7.92 6 11V16L4 18V19H20V18L18 16Z"
                />
                <path
                  d="M4 19H20"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <h3
                class="text-[15px] sm:text-[17px] font-bold text-[#000000] leading-tight sm:leading-normal"
              >
                Alerte de fin de période
              </h3>
              <p
                class="text-[13px] sm:text-[15px] text-[#9CA3AF] mt-1 sm:mt-0.5 leading-snug"
              >
                Recevoir un mail avant la fin de<br
                  class="hidden sm:inline"
                />période de réflexion
              </p>
            </div>
          </div>

          <!-- Custom Toggle Switch -->
          <button
            @click="notificationsEnabled = !notificationsEnabled"
            class="relative inline-flex h-[28px] w-[50px] sm:h-[32px] sm:w-[56px] shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-[#5B8C85] focus-visible:ring-opacity-75"
            :class="notificationsEnabled ? 'bg-[#5B8C85]' : 'bg-[#E5E7EB]'"
            role="switch"
            :aria-checked="notificationsEnabled.toString()"
          >
            <span class="sr-only">Activer les notifications</span>
            <span
              aria-hidden="true"
              class="pointer-events-none inline-block h-[20px] w-[20px] sm:h-[24px] sm:w-[24px] transform rounded-full bg-[#FFFFFF] shadow-md ring-0 transition duration-200 ease-in-out"
              :class="
                notificationsEnabled
                  ? 'translate-x-[22px] sm:translate-x-[24px]'
                  : 'translate-x-[4px]'
              "
            />
          </button>
        </div>
      </section>

      <!-- Remise à zéro Section Heading -->
      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Remise à zéro
      </h2>

      <!-- Remise à zéro Card -->
      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm hover:bg-[#F8F6F2] transition-colors cursor-pointer group"
        @click="resetHistory"
      >
        <div class="flex items-center justify-between gap-3 sm:gap-4">
          <!-- Icon and Text Group -->
          <div class="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <!-- Fixed width icon container for perfect alignment -->
            <div
              class="w-10 sm:w-12 flex-shrink-0 flex justify-center items-center text-[#D16D6A]"
            >
              <!-- History/Reset Icon -->
              <svg
                class="w-7 h-7 sm:w-8 sm:h-8"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                <path d="M3 3v5h5" />
                <path d="M12 7v5l4 2" />
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <h3
                class="text-[15px] sm:text-[17px] font-bold text-[#D16D6A] leading-tight sm:leading-normal"
              >
                Effacer l'historique
              </h3>
              <p
                class="text-[13px] sm:text-[15px] text-[#9CA3AF] mt-1 sm:mt-0.5 leading-snug"
              >
                Réinitialiser toutes les évaluations<br
                  class="hidden sm:inline"
                />passées
              </p>
            </div>
          </div>

          <!-- Trash Icon -->
          <button
            class="w-10 h-10 sm:w-12 sm:h-12 flex-shrink-0 flex justify-center items-center text-[#D16D6A] opacity-80 group-hover:opacity-100 transition-opacity"
            aria-label="Effacer"
          >
            <svg
              class="w-5 h-5 sm:w-6 sm:h-6"
              viewBox="0 0 24 24"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z"
              />
            </svg>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useCurrencyStore } from "@/stores/currency";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import SettingsPageHeader from "@/components/shared/SettingsPageHeader.vue";

const authStore = useAuthStore();

const labels = ["12h", "24h", "48h", "72h"];
const periodValues = [12, 24, 48, 72];
const periodIndex = ref(1); // Par défaut 24h

// 1. SYNCHRONISATION STORE -> UI (Gère le rafraîchissement F5)
watch(
  () => authStore.user?.cooldown_preference,
  (newVal) => {
    if (newVal) {
      const idx = periodValues.indexOf(newVal);
      // On met à jour le slider uniquement s'il n'est pas déjà sur la bonne valeur
      if (idx !== -1 && periodIndex.value !== idx) {
        periodIndex.value = idx;
      }
    }
  },
  { immediate: true }, // immediate: true force l'exécution dès le chargement du composant
);

// 2. SYNCHRONISATION UI -> BACKEND (Gère l'action de l'utilisateur sur le slider)
watch(periodIndex, async (newIndex) => {
  const selectedHours = periodValues[newIndex];

  // SÉCURITÉ : Si la valeur du slider est déjà celle du store (ex: au chargement de la page),
  // on ne fait pas d'appel API inutile.
  if (authStore.user?.cooldown_preference === selectedHours) return;

  try {
    await api.patch("/users/me/", { cooldown_preference: selectedHours });
    // On met à jour le store localement après la confirmation du serveur
    if (authStore.user) {
      authStore.user.cooldown_preference = selectedHours;
    }
  } catch (err) {
    console.error("Erreur de sauvegarde de la préférence", err);
  }
});

const isDropdownOpen = ref(false);

const currencyStore = useCurrencyStore();
const currencies = [
  { code: "TND", name: "Dinar tunisien", flag: "🇹🇳" },
  { code: "EUR", name: "Euro", flag: "🇪🇺" },
  { code: "USD", name: "Dollar américain", flag: "🇺🇸" },
  { code: "GBP", name: "Livre sterling", flag: "🇬🇧" },
  { code: "CAD", name: "Dollar canadien", flag: "🇨🇦" },
  { code: "JPY", name: "Yen japonais", flag: "🇯🇵" },
  { code: "AUD", name: "Dollar australien", flag: "🇦🇺" },
  { code: "CHF", name: "Franc suisse", flag: "🇨🇭" },
  { code: "CNY", name: "Yuan chinois", flag: "🇨🇳" },
  { code: "AED", name: "Dirham des EAU", flag: "🇦🇪" },
  { code: "SAR", name: "Riyal saoudien", flag: "🇸🇦" },
  { code: "MAD", name: "Dirham marocain", flag: "🇲🇦" },
  { code: "DZD", name: "Dinar algérien", flag: "🇩🇿" },
  { code: "ZAR", name: "Rand sud-africain", flag: "🇿🇦" },
  { code: "BRL", name: "Réal brésilien", flag: "🇧🇷" },
  { code: "INR", name: "Roupie indienne", flag: "🇮🇳" },
];
const selectedCurrency = computed(() => currencyStore.currentCurrency);

const selectCurrency = (currency) => {
  currencyStore.setCurrency(currency);
  isDropdownOpen.value = false;
};

const rigueurLevels = ["Indulgent", "Équilibré", "Impitoyable"];
const selectedRigueur = ref("Équilibré");

const notificationsEnabled = ref(true);

const resetHistory = () => {
  console.log("Historique réinitialisé");
};

watch(
  () => authStore.user?.evaluation_rigor,
  (newVal) => {
    // Vérifier que newVal existe et fait bien partie des choix autorisés
    if (newVal && rigueurLevels.includes(newVal)) {
      if (selectedRigueur.value !== newVal) {
        selectedRigueur.value = newVal;
      }
    }
  },
  { immediate: true },
);

watch(selectedRigueur, async (newVal) => {
  // SÉCURITÉ : Ne pas envoyer de requête inutile si c'est déjà la bonne valeur
  if (authStore.user?.evaluation_rigor === newVal) return;

  try {
    await api.patch("/users/me/", { evaluation_rigor: newVal });
    // Mise à jour du store en local
    if (authStore.user) {
      authStore.user.evaluation_rigor = newVal;
    }
  } catch (err) {
    console.error("Erreur de sauvegarde du niveau de rigueur", err);
  }
});
</script>

<style scoped>
/*
  Ensures DM Sans is loaded for this component.
  If you already import this globally in your main.css or index.html, you can safely remove this block.
*/
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap");

/* Reset default browser styles for the range input */
.custom-slider {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
}

.custom-slider:focus {
  outline: none;
}

/* Style the track */
.custom-slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 12px;
  cursor: pointer;
  background: #e5e7eb;
  border-radius: 9999px;
}

.custom-slider::-moz-range-track {
  width: 100%;
  height: 12px;
  cursor: pointer;
  background: #e5e7eb;
  border-radius: 9999px;
}

/* Style the interactive thumb */
.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  height: 26px;
  width: 26px;
  border-radius: 50%;
  background: #5b8c85;
  cursor: pointer;
  margin-top: -7px; /* Centers the thumb vertically on the 12px track */
  border: 4px solid #ffffff;
  /* Replicates the soft blueish/purple glow seen in the design */
  box-shadow: 0 0 12px 2px rgba(199, 210, 254, 0.6);
}

.custom-slider::-moz-range-thumb {
  height: 26px;
  width: 26px;
  border-radius: 50%;
  background: #5b8c85;
  cursor: pointer;
  border: 4px solid #ffffff;
  box-shadow: 0 0 12px 2px rgba(199, 210, 254, 0.6);
}
</style>
