<template>
  <!-- Main Wrapper -->
  <div
    class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] pb-12 px-4"
  >
    <!-- Header -->
    <header class="w-full pt-4 sm:pt-12 pb-3 sm:pb-6">
      <h1
        class="text-center text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight"
      >
        Paramètres
      </h1>
    </header>

    <!-- Content -->
    <main
      class="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 md:px-8 py-6 sm:py-8 flex flex-col gap-8 sm:gap-10"
    >
      <!-- Section: COMPTE -->
      <section class="flex flex-col gap-2.5 sm:gap-4">
        <h2
          class="text-[13px] sm:text-sm font-bold text-gray-500 uppercase tracking-widest pl-2"
        >
          Compte
        </h2>

        <div
          class="bg-white rounded-2xl sm:rounded-3xl shadow-sm overflow-hidden border border-gray-100"
        >
          <router-link
            :to="{ name: 'EditProfileView' }"
            class="w-full flex items-center justify-between px-5 py-4 sm:px-6 sm:py-5 hover:bg-gray-50 transition-colors group"
          >
            <div class="flex items-center gap-4 sm:gap-5">
              <svg
                class="w-6 h-6 sm:w-7 sm:h-7 text-gray-500 group-hover:text-[#5B8C85] transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
                />
              </svg>
              <span
                class="text-[15px] sm:text-lg font-medium text-gray-800 group-hover:text-gray-900"
                >Modifier mon profil</span
              >
            </div>
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
              />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: PRÉFÉRENCES -->
      <section class="flex flex-col gap-2.5 sm:gap-4">
        <h2
          class="text-[13px] sm:text-sm font-bold text-gray-500 uppercase tracking-widest pl-2"
        >
          Préférences
        </h2>

        <div
          class="bg-white rounded-2xl sm:rounded-3xl shadow-sm overflow-hidden border border-gray-100"
        >
          <router-link
            :to="{ name: 'UserPreferencesView' }"
            class="w-full flex items-center justify-between px-5 py-4 sm:px-6 sm:py-5 hover:bg-gray-50 transition-colors group"
          >
            <div class="flex items-center gap-4 sm:gap-5">
              <svg
                class="w-6 h-6 sm:w-7 sm:h-7 text-gray-500 group-hover:text-[#5B8C85] transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75"
                />
              </svg>
              <span
                class="text-[15px] sm:text-lg font-medium text-gray-800 group-hover:text-gray-900"
                >Modifier mes préférences</span
              >
            </div>
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
              />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: ASSISTANCE -->
      <section class="flex flex-col gap-2.5 sm:gap-4">
        <h2
          class="text-[13px] sm:text-sm font-bold text-gray-500 uppercase tracking-widest pl-2"
        >
          Assistance
        </h2>

        <div
          class="bg-white rounded-2xl sm:rounded-3xl shadow-sm overflow-hidden border border-gray-100 flex flex-col"
        >
          <router-link
            :to="{ name: 'TermsOfServiceView' }"
            class="w-full flex items-center justify-between px-5 py-4 sm:px-6 sm:py-5 hover:bg-gray-50 transition-colors border-b border-gray-100 group"
          >
            <div class="flex items-center gap-4 sm:gap-5">
              <svg
                class="w-6 h-6 sm:w-7 sm:h-7 text-gray-500 group-hover:text-[#5B8C85] transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
                />
              </svg>
              <span
                class="text-[15px] sm:text-lg font-medium text-gray-800 group-hover:text-gray-900"
                >Conditions d'utilisations</span
              >
            </div>
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
              />
            </svg>
          </router-link>

          <router-link
            :to="{ name: 'HelpSupportView' }"
            class="w-full flex items-center justify-between px-5 py-4 sm:px-6 sm:py-5 hover:bg-gray-50 transition-colors group"
          >
            <div class="flex items-center gap-4 sm:gap-5">
              <svg
                class="w-6 h-6 sm:w-7 sm:h-7 text-gray-500 group-hover:text-[#5B8C85] transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
                />
              </svg>
              <span
                class="text-[15px] sm:text-lg font-medium text-gray-800 group-hover:text-gray-900"
                >Aide et support</span
              >
            </div>
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 text-gray-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
              />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: ACTIONS (Logout & Delete) -->
      <section
        class="mt-4 sm:mt-8 flex flex-col sm:flex-row justify-center items-center gap-4 sm:gap-6 pb-8"
      >
        <button
          @click="performLogout"
          class="w-full sm:w-auto flex items-center justify-center gap-2 text-[#D9534F] font-medium text-[15px] sm:text-base px-8 py-3.5 sm:py-3 bg-white sm:bg-transparent rounded-2xl sm:rounded-full shadow-sm sm:shadow-none border border-red-50 sm:border-transparent hover:bg-red-50 hover:border-red-100 transition-colors active:scale-95"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75"
            />
          </svg>
          Se déconnecter
        </button>

        <button
          @click="showDeleteConfirmModal = true"
          class="w-full sm:w-auto flex items-center justify-center gap-2 text-gray-500 font-medium text-[15px] sm:text-base px-8 py-3.5 sm:py-3 bg-white sm:bg-transparent rounded-2xl sm:rounded-full shadow-sm sm:shadow-none border border-gray-100 sm:border-transparent hover:bg-red-50 hover:text-red-500 hover:border-red-100 transition-colors active:scale-95"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
          Supprimer mon compte
        </button>
      </section>
    </main>

    <!-- Modale d'Avertissement (Confirmation) -->
    <div
      v-if="showDeleteConfirmModal"
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
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <h3 class="font-bold text-xl text-gray-900 mb-2">
          Supprimer le compte ?
        </h3>
        <p class="text-gray-500 text-sm sm:text-base mb-6 leading-relaxed">
          Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est
          irréversible et toutes vos analyses seront perdues.
        </p>
        <div class="flex gap-3">
          <button
            @click="showDeleteConfirmModal = false"
            class="flex-1 py-3.5 rounded-xl bg-gray-100 font-bold text-gray-700 hover:bg-gray-200 transition-colors"
          >
            Annuler
          </button>
          <button
            @click="executeAccountDeletion"
            :disabled="isDeleting"
            class="flex-1 py-3.5 rounded-xl bg-[#FEE2E2] font-bold text-[#EF4444] hover:bg-red-200 transition-colors disabled:opacity-50"
          >
            {{ isDeleting ? "Suppression..." : "Oui, supprimer" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modale de Succès -->
    <div
      v-if="showDeleteSuccessModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4 transition-opacity"
    >
      <div
        class="bg-white p-6 sm:p-8 rounded-[2rem] w-full max-w-sm text-center shadow-2xl border border-gray-100"
      >
        <div
          class="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg
            class="w-8 h-8 text-green-500"
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
        <h3 class="font-bold text-xl text-gray-900 mb-2">Compte supprimé</h3>
        <p class="text-gray-500 text-sm sm:text-base mb-6 leading-relaxed">
          Votre compte et vos données ont été effacés avec succès. Nous espérons
          vous revoir bientôt !
        </p>
        <button
          @click="finalizeDeletionAndLogout"
          class="w-full py-3.5 rounded-xl bg-[#5B8C85] font-bold text-white hover:bg-[#4a736d] transition-colors shadow-sm"
        >
          Retour à l'accueil
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
import api from "@/services/api";

const router = useRouter();
const authStore = useAuthStore();
const showDeleteConfirmModal = ref(false);
const showDeleteSuccessModal = ref(false);
const isDeleting = ref(false);

const performLogout = async () => {
  authStore.logout();
  console.log("User is logging out...");
  await router.push({ name: "login" });
};

const executeAccountDeletion = async () => {
  isDeleting.value = true;
  try {
    await api.delete("/users/me/");
    showDeleteConfirmModal.value = false;
    showDeleteSuccessModal.value = true;
  } catch (error) {
    console.error("Erreur lors de la suppression du compte :", error);
    alert("Une erreur est survenue. Veuillez réessayer.");
  } finally {
    isDeleting.value = false;
  }
};

const finalizeDeletionAndLogout = async () => {
  showDeleteSuccessModal.value = false;
  authStore.logout();
  await router.push({ name: "login" });
};
</script>
