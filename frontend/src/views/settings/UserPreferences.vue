<template>
  <div
    class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] flex justify-center"
  >
    <div class="w-full max-w-3xl px-4 sm:px-6 md:px-8 py-6 sm:py-8 lg:py-10">
      <SettingsPageHeader title="Mes préférences" />

      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
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

        <p
          class="mt-3 sm:mt-4 text-[#6B7280] text-[14px] sm:text-[16px] leading-relaxed"
        >
          Temps d'attente imposé avant de valider un achat impulsif.
        </p>

        <div class="mt-6 sm:mt-8 mb-2">
          <input
            type="range"
            min="0"
            max="3"
            step="1"
            v-model="periodIndex"
            class="custom-slider w-full"
          />

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

      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Configuration
      </h2>

      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
        <div class="mb-6 sm:mb-8 relative z-50">
          <h3 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
            Devise
          </h3>

          <div class="relative w-full">
            <button
              @click="isDropdownOpen = !isDropdownOpen"
              class="w-full flex items-center justify-between border border-[#D9D9D9] bg-[#FFFFFF] rounded-[12px] sm:rounded-[15px] px-3 sm:px-4 py-2.5 sm:py-3 focus:outline-none focus:ring-2 focus:ring-[#5B8C85]/30 transition-all"
            >
              <div class="flex items-center gap-2 sm:gap-3">
                <img
                  :src="`https://flagcdn.com/w40/${selectedCurrency.countryCode}.png`"
                  :alt="selectedCurrency.code"
                  class="w-6 sm:w-7 object-cover rounded-[2px] shadow-sm"
                />
                <span
                  class="text-[15px] sm:text-base text-[#9CA3AF] font-medium"
                >
                  {{ selectedCurrency.code }}
                </span>
              </div>
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
                  <img
                    :src="`https://flagcdn.com/w40/${currency.countryCode}.png`"
                    :alt="currency.code"
                    class="w-6 sm:w-7 object-cover rounded-[2px] shadow-sm"
                  />
                  <span
                    class="text-[14px] sm:text-[15px] text-[#6B7280] font-medium"
                  >
                    {{ currency.code }} - {{ currency.name }}
                  </span>
                </li>
              </ul>
            </transition>
          </div>
        </div>

        <div>
          <h3 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
            Niveau de rigueur d'évaluation
          </h3>

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

      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Notifications
      </h2>

      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm"
      >
        <div class="flex items-center justify-between gap-3 sm:gap-4">
          <div class="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <div
              class="w-10 sm:w-12 flex-shrink-0 flex justify-center items-center text-[#5B8C85]"
            >
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

      <h2
        class="text-xl sm:text-2xl font-bold text-[#000000] mb-3 sm:mb-4 mt-6 sm:mt-8 px-1 sm:px-2"
      >
        Remise à zéro
      </h2>

      <section
        class="bg-[#FFFFFF] rounded-[20px] sm:rounded-[24px] p-5 sm:p-6 mb-6 sm:mb-8 shadow-sm hover:bg-[#F8F6F2] transition-colors cursor-pointer group"
        @click="resetHistory"
      >
        <div class="flex items-center justify-between gap-3 sm:gap-4">
          <div class="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <div
              class="w-10 sm:w-12 flex-shrink-0 flex justify-center items-center text-[#D16D6A]"
            >
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

    <div
      v-if="showClearHistoryModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4 transition-opacity"
    >
      <div
        class="bg-white p-6 sm:p-8 rounded-[2rem] w-full max-w-sm text-center shadow-2xl border border-gray-100"
      >
        <div
          class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg
            class="w-8 h-8 text-red-500"
            viewBox="0 0 24 24"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z"
            />
          </svg>
        </div>
        <h3 class="font-bold text-xl text-gray-900 mb-2">
          Effacer l'historique ?
        </h3>
        <p class="text-gray-500 text-sm mb-6 leading-relaxed">
          Cette action masquera toutes vos analyses et statistiques passées.
          Vous repartirez à zéro. Êtes-vous sûr de vouloir continuer ?
        </p>
        <div class="flex gap-3">
          <button
            @click="showClearHistoryModal = false"
            class="flex-1 py-3.5 rounded-xl bg-gray-100 font-bold text-gray-700 hover:bg-gray-200 transition-colors"
          >
            Annuler
          </button>
          <button
            @click="confirmClearHistory"
            :disabled="isClearingHistory"
            class="flex-1 py-3.5 rounded-xl bg-[#FEE2E2] font-bold text-[#EF4444] hover:bg-red-200 transition-colors disabled:opacity-50"
          >
            {{ isClearingHistory ? "Effacement..." : "Oui, effacer" }}
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showNotificationModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4 transition-opacity"
    >
      <div
        class="bg-white p-6 sm:p-8 rounded-[2rem] w-full max-w-sm text-center shadow-2xl border border-gray-100"
      >
        <div
          class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
          :class="
            notificationType === 'success'
              ? 'bg-green-50 text-green-500'
              : 'bg-red-50 text-red-500'
          "
        >
          <svg
            v-if="notificationType === 'success'"
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="3"
              d="M5 13l4 4L19 7"
            ></path>
          </svg>
          <svg
            v-else
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="3"
              d="M6 18L18 6M6 6l12 12"
            ></path>
          </svg>
        </div>

        <h3 class="font-bold text-xl text-gray-900 mb-2">
          {{ notificationType === "success" ? "Succès !" : "Oups..." }}
        </h3>
        <p class="text-gray-500 text-sm mb-6 leading-relaxed">
          {{ notificationMessage }}
        </p>

        <button
          @click="showNotificationModal = false"
          class="w-full py-3.5 rounded-xl font-bold text-white transition-colors"
          :class="
            notificationType === 'success'
              ? 'bg-[#5B8C85] hover:bg-[#4a736d]'
              : 'bg-[#EF4444] hover:bg-red-600'
          "
        >
          Fermer
        </button>
      </div>
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

const showClearHistoryModal = ref(false);
const isClearingHistory = ref(false);

const showNotificationModal = ref(false);
const notificationType = ref("success");
const notificationMessage = ref("");

const labels = ["12h", "24h", "48h", "72h"];
const periodValues = [12, 24, 48, 72];
const periodIndex = ref(1);

watch(
  () => authStore.user?.cooldown_preference,
  (newVal) => {
    if (newVal) {
      const idx = periodValues.indexOf(newVal);
      if (idx !== -1 && periodIndex.value !== idx) {
        periodIndex.value = idx;
      }
    }
  },
  { immediate: true },
);

watch(periodIndex, async (newIndex) => {
  const selectedHours = periodValues[newIndex];
  if (authStore.user?.cooldown_preference === selectedHours) return;

  try {
    await api.patch("/users/me/", { cooldown_preference: selectedHours });
    if (authStore.user) {
      authStore.user.cooldown_preference = selectedHours;
    }
  } catch (err) {
    console.error("Erreur de sauvegarde de la préférence", err);
  }
});

const isDropdownOpen = ref(false);
const currencyStore = useCurrencyStore();

// FIX : On importe la liste directement depuis le store pour éviter la duplication
const currencies = currencyStore.availableCurrencies;
const selectedCurrency = computed(() => currencyStore.currentCurrency);

const selectCurrency = (currency) => {
  currencyStore.setCurrency(currency);
  isDropdownOpen.value = false;
};

const rigueurLevels = ["Indulgent", "Équilibré", "Impitoyable"];
const selectedRigueur = ref("Équilibré");

const notificationsEnabled = ref(true);
watch(
  () => authStore.user?.wants_cooldown_reminders,
  (newVal) => {
    if (newVal !== undefined && notificationsEnabled.value !== newVal) {
      notificationsEnabled.value = newVal;
    }
  },
  { immediate: true },
);
watch(notificationsEnabled, async (newVal) => {
  if (authStore.user?.wants_cooldown_reminders === newVal) return;

  try {
    await api.patch("/users/me/", { wants_cooldown_reminders: newVal });
    if (authStore.user) {
      authStore.user.wants_cooldown_reminders = newVal;
    }
  } catch (err) {
    console.error(
      "Erreur lors de la sauvegarde de la préférence de notification",
      err,
    );
    notificationsEnabled.value = !newVal;
  }
});

const resetHistory = () => {
  showClearHistoryModal.value = true;
};

const confirmClearHistory = async () => {
  isClearingHistory.value = true;
  try {
    await api.post("/users/me/clear-history/");
    showClearHistoryModal.value = false;
    notificationType.value = "success";
    notificationMessage.value =
      "Votre historique a été effacé avec succès. Vous repartez à zéro !";
    showNotificationModal.value = true;
    await authStore.fetchUserProfile();
  } catch (err) {
    console.error("Erreur lors de l'effacement de l'historique :", err);
    showClearHistoryModal.value = false;
    notificationType.value = "error";
    notificationMessage.value =
      "Une erreur est survenue lors de l'effacement. Veuillez réessayer.";
    showNotificationModal.value = true;
  } finally {
    isClearingHistory.value = false;
  }
};

watch(
  () => authStore.user?.evaluation_rigor,
  (newVal) => {
    if (newVal && rigueurLevels.includes(newVal)) {
      if (selectedRigueur.value !== newVal) {
        selectedRigueur.value = newVal;
      }
    }
  },
  { immediate: true },
);

watch(selectedRigueur, async (newVal) => {
  if (authStore.user?.evaluation_rigor === newVal) return;
  try {
    await api.patch("/users/me/", { evaluation_rigor: newVal });
    if (authStore.user) {
      authStore.user.evaluation_rigor = newVal;
    }
  } catch (err) {
    console.error("Erreur de sauvegarde du niveau de rigueur", err);
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap");

.custom-slider {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
}

.custom-slider:focus {
  outline: none;
}

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

.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  height: 26px;
  width: 26px;
  border-radius: 50%;
  background: #5b8c85;
  cursor: pointer;
  margin-top: -7px;
  border: 4px solid #ffffff;
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
