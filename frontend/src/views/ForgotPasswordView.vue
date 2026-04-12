<template>
  <div
      class="min-h-screen bg-[#FAFAFA] flex flex-col items-center px-6 py-12 font-sans selection:bg-[#5A877E] selection:text-white">

    <div class="w-16 h-16 bg-[#EFF3F3] rounded-2xl flex items-center justify-center mb-6 shadow-sm">
      <svg class="w-8 h-8 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
      </svg>
    </div>

    <h1 class="text-3xl font-serif font-bold text-[#2A3039] mb-3 tracking-tight">Mot de passe oublié</h1>
    <p class="text-center text-[#6B7280] text-sm mb-8 max-w-[280px] leading-relaxed">
      Entrez votre adresse e-mail. Si un compte y est associé, nous vous enverrons un lien de réinitialisation.
    </p>

    <div v-if="successMessage"
         class="w-full max-w-sm bg-green-50 border border-green-200 text-green-700 rounded-2xl p-4 text-sm text-center mb-6">
      {{ successMessage }}
    </div>

    <form v-else @submit.prevent="handleRequestReset" class="w-full max-w-sm space-y-5">
      <div class="space-y-1.5">
        <label for="email" class="block text-sm font-medium text-[#374151]">Email</label>
        <div class="relative">
          <input
              type="email" id="email" v-model="email" placeholder="exemple@email.com" autocomplete="username"
              class="block w-full px-4 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
              required
          />
        </div>
      </div>

      <button type="submit" :disabled="isLoading"
              class="w-full bg-[#5A877E] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed">
        <span v-if="isLoading">Envoi en cours...</span>
        <span v-else>Envoyer le lien</span>
      </button>

      <p v-if="errorMessage" class="text-xs text-red-500 text-center mt-2">{{ errorMessage }}</p>
    </form>

    <div class="mt-8 text-center">
      <router-link to="/login"
                   class="text-sm font-medium text-[#6B7280] hover:text-[#374151] transition-colors flex items-center justify-center gap-2">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Retour à la connexion
      </router-link>
    </div>

  </div>
</template>

<script setup>
import {ref} from 'vue';
import api from '@/services/api';

const email = ref('');
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const handleRequestReset = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await api.post('/auth/password-reset/', {email: email.value});
    successMessage.value = response.data.message;
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data;

      // Cas 1 : Django a crashé et renvoie une string (ex: "Server Error (500)")
      if (typeof data === 'string') {
        errorMessage.value = "Erreur serveur critique. Regardez le terminal Django.";
      }
      // Cas 2 : Notre API renvoie proprement {"error": "..."}
      else if (data.error) {
        errorMessage.value = data.error;
      }
      // Cas 3 : Erreur de formulaire DRF {"email": ["L'adresse..."]}
      else {
        const firstKey = Object.keys(data)[0];
        const errorContent = data[firstKey];
        errorMessage.value = Array.isArray(errorContent) ? errorContent[0] : errorContent;
      }
    } else {
      errorMessage.value = 'Erreur réseau impossible à joindre le serveur.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>