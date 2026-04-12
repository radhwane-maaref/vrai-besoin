<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col items-center px-6 py-12 font-sans selection:bg-[#5A877E] selection:text-white">

    <div class="w-16 h-16 bg-[#EFF3F3] rounded-2xl flex items-center justify-center mb-6 shadow-sm">
      <svg class="w-8 h-8 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    </div>

    <h1 class="text-3xl font-serif font-bold text-[#2A3039] mb-3 tracking-tight">Nouveau mot de passe</h1>
    <p class="text-center text-[#6B7280] text-sm mb-8 max-w-[280px] leading-relaxed">
      Veuillez saisir votre nouveau mot de passe ci-dessous.
    </p>

    <div v-if="successMessage" class="w-full max-w-sm bg-green-50 border border-green-200 text-green-700 rounded-2xl p-4 text-sm text-center mb-6">
      {{ successMessage }} <br/>
      <span class="text-xs opacity-80 mt-2 block">Redirection vers la connexion...</span>
    </div>

    <form v-else @submit.prevent="handleResetConfirm" class="w-full max-w-sm space-y-4">

      <div class="space-y-1">
        <label for="password" class="block text-xs font-medium text-[#374151] ml-1">Nouveau mot de passe</label>
        <input
            type="password" id="password" v-model="formData.password" placeholder="••••••••" autocomplete="new-password"
            class="block w-full px-4 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
            required
        />
      </div>

      <div class="space-y-1">
        <label for="password_confirm" class="block text-xs font-medium text-[#374151] ml-1">Confirmer le mot de passe</label>
        <input
            type="password" id="password_confirm" v-model="formData.password_confirm" placeholder="••••••••" autocomplete="new-password"
            class="block w-full px-4 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
            required
        />
      </div>

      <button type="submit" :disabled="isLoading || passwordMismatch" class="w-full mt-4 bg-[#5A877E] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed">
        <span v-if="isLoading">Mise à jour...</span>
        <span v-else>Enregistrer</span>
      </button>

      <p v-if="errorMessage" class="text-xs text-red-500 text-center mt-2">{{ errorMessage }}</p>

    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const formData = reactive({
  password: '',
  password_confirm: ''
});

const passwordMismatch = computed(() => {
  return formData.password && formData.password_confirm && formData.password !== formData.password_confirm;
});

const handleResetConfirm = async () => {
  if (passwordMismatch.value) return;

  isLoading.value = true;
  errorMessage.value = '';

  // Extract variables dynamically from Vue Router
  const uid = route.params.uid;
  const token = route.params.token;

  try {
    const response = await api.post(`/auth/password-reset-confirm/${uid}/${token}/`, formData);
    successMessage.value = response.data.message;

    // Automatically redirect to login after a brief pause so they can read the success message
    setTimeout(() => {
      router.push('/login');
    }, 2500);

  } catch (err) {
    if (err.response?.data?.error) {
      errorMessage.value = err.response.data.error; // e.g., "Le lien a expiré."
    } else if (err.response?.data?.password) {
      errorMessage.value = err.response.data.password[0]; // Django password validation errors
    } else {
      errorMessage.value = 'Une erreur est survenue.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>