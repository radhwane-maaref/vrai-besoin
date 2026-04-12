<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col items-center px-6 py-12 font-sans selection:bg-[#5A877E] selection:text-white">

    <div class="w-16 h-16 bg-[#EFF3F3] rounded-2xl flex items-center justify-center mb-6 shadow-sm">
      <svg class="w-8 h-8 text-[#5A877E]" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17 5.98c-3.14-1.74-7.46-.86-10.2 1.88C4.05 10.6 3.16 14.91 4.9 18.05c.16.29.56.36.83.13 4.1-3.5 7.15-5.5 10.15-5.5 1.48 0 2.8.44 3.96 1.15.25.15.56.02.66-.25.59-1.57.82-3.32.6-5.1-.24-1.95-1.12-3.8-2.6-5.26-.2-.2-.5-.26-.75-.12l-.75-.12z"/>
      </svg>
    </div>

    <h1 class="text-4xl font-serif font-bold text-[#2A3039] mb-3 tracking-tight">Vrai Besoin</h1>
    <p class="text-center text-[#6B7280] text-sm mb-8 max-w-[280px] leading-relaxed">
      Reprenez le contrôle de vos achats impulsifs et retrouvez votre sérénité financière.
    </p>

    <div class="flex w-full max-w-sm bg-[#F3F4F6] p-1.5 rounded-2xl mb-8">
      <button class="flex-1 bg-white shadow-sm rounded-xl py-2.5 text-sm font-semibold text-[#1F2937] transition-all">
        Connexion
      </button>
      <button @click="router.push('/register')" class="flex-1 rounded-xl py-2.5 text-sm font-medium text-[#6B7280] hover:text-[#374151] transition-all">
        Inscription
      </button>
    </div>

    <form @submit.prevent="handleLogin" class="w-full max-w-sm space-y-5">
      <div class="space-y-1.5">
        <label for="email" class="block text-sm font-medium text-[#374151]">Email</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </div>
          <input
              type="email" id="email" v-model="formData.email" placeholder="exemple@email.com" autocomplete="username"
              class="block w-full pl-11 pr-4 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
              required
          />
        </div>
      </div>

      <div class="space-y-1.5">
        <label for="password" class="block text-sm font-medium text-[#374151]">Mot de passe</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
          <input
              :type="showPassword ? 'text' : 'password'" id="password" v-model="formData.password" placeholder="••••••••" autocomplete="current-password"
              class="block w-full pl-11 pr-12 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
              required
          />
          <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none">
            <svg v-if="!showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="flex justify-end">
        <router-link to="/forgot-password" class="text-xs font-medium text-[#5A877E] hover:text-[#456B63] transition-colors">
          Mot de passe oublié ?
        </router-link>
      </div>

      <button type="submit" :disabled="authStore.loading" class="w-full bg-[#5A877E] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed">
        <span v-if="authStore.loading">Connexion en cours...</span>
        <span v-else>Se connecter</span>
      </button>

      <p v-if="authStore.error" class="text-xs text-red-500 text-center mt-2">{{ authStore.error }}</p>

    </form>

    <div class="w-full max-w-sm flex items-center my-8">
      <div class="flex-grow border-t border-gray-200"></div>
      <span class="flex-shrink-0 mx-4 text-gray-400 text-xs font-medium tracking-wider">OU CONTINUER AVEC</span>
      <div class="flex-grow border-t border-gray-200"></div>
    </div>

    <SocialLoginButton text="Se connecter avec Google" @success="handleGoogleCallback" />

    <p class="mt-8 text-sm text-[#6B7280]">
      Pas encore de compte ?
      <router-link to="/register" class="font-medium text-[#5A877E] hover:text-[#456B63] transition-colors">Créer un compte</router-link>
    </p>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';
import SocialLoginButton from '@/components/SocialLoginButton.vue';

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);

const formData = reactive({
  email: '',
  password: ''
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  try {
    await authStore.login({
      email: formData.email,
      password: formData.password
    });
    router.push('/dashboard');
  } catch (err) {
    // Error is handled and displayed via authStore.error in the template
  }
};

const handleGoogleCallback = async (response) => {
  try {
    await authStore.googleLogin(response.credential);
    router.push('/dashboard');
  } catch (err) {
    console.error("Google SSO Error:", err);
  }
};
</script>