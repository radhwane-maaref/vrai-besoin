<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col items-center px-6 py-10 font-sans selection:bg-[#5A877E] selection:text-white">

    <div class="w-12 h-12 bg-[#EFF3F3] rounded-xl flex items-center justify-center mb-4 shadow-sm">
      <svg class="w-6 h-6 text-[#5A877E]" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17 5.98c-3.14-1.74-7.46-.86-10.2 1.88C4.05 10.6 3.16 14.91 4.9 18.05c.16.29.56.36.83.13 4.1-3.5 7.15-5.5 10.15-5.5 1.48 0 2.8.44 3.96 1.15.25.15.56.02.66-.25.59-1.57.82-3.32.6-5.1-.24-1.95-1.12-3.8-2.6-5.26-.2-.2-.5-.26-.75-.12l-.75-.12z" />
      </svg>
    </div>

    <h1 class="text-3xl font-serif font-bold text-[#2A3039] mb-2 tracking-tight">Rejoignez-nous</h1>
    <p class="text-center text-[#6B7280] text-sm mb-6 max-w-[280px] leading-relaxed">
      Configurez votre profil financier pour que l'IA puisse vous conseiller efficacement.
    </p>

    <div class="flex w-full max-w-sm bg-[#F3F4F6] p-1.5 rounded-2xl mb-6">
      <button @click="router.push('/login')" class="flex-1 rounded-xl py-2.5 text-sm font-medium text-[#6B7280] hover:text-[#374151] transition-all">
        Connexion
      </button>
      <button class="flex-1 bg-white shadow-sm rounded-xl py-2.5 text-sm font-semibold text-[#1F2937] transition-all">
        Inscription
      </button>
    </div>

    <form @submit.prevent="handleRegister" class="w-full max-w-sm space-y-4">

      <div class="space-y-1">
        <label for="email" class="block text-xs font-medium text-[#374151] ml-1">Email</label>
        <input
            type="email" id="email" v-model="formData.email" placeholder="exemple@email.com" autocomplete="username"
            class="block w-full px-4 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
            required
        />
      </div>

      <div class="space-y-1">
        <label for="password" class="block text-xs font-medium text-[#374151] ml-1">Mot de passe</label>
        <div class="relative">
          <input
              :type="showPassword ? 'text' : 'password'" id="password" v-model="formData.password" placeholder="••••••••" autocomplete="new-password"
              class="block w-full pl-4 pr-12 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
              required
          />
          <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600">
            <svg v-if="!showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>
      </div>

      <div class="space-y-1">
        <label for="confirm_password" class="block text-xs font-medium text-[#374151] ml-1">Confirmer le mot de passe</label>
        <input
            :type="showPassword ? 'text' : 'password'" id="confirm_password" v-model="formData.confirm_password" placeholder="••••••••" autocomplete="new-password"
            class="block w-full pl-4 pr-12 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
            required
        />
        <p v-if="passwordMismatch" class="text-xs text-red-500 mt-1 ml-1">Les mots de passe ne correspondent pas</p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="space-y-1">
          <label for="profession" class="block text-xs font-medium text-[#374151] ml-1">Profession</label>
          <input
              type="text" id="profession" v-model="formData.profession" placeholder="Ex: Étudiant..."
              class="block w-full px-4 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
          />
        </div>
        <div class="space-y-1">
          <label for="budget" class="block text-xs font-medium text-[#374151] ml-1">Budget Mensuel (€)</label>
          <input
              type="number" id="budget" v-model="formData.monthly_budget" placeholder="Ex: 1500" min="0" step="0.01"
              class="block w-full px-4 py-3 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
          />
        </div>
      </div>

      <button type="submit" :disabled="authStore.loading || passwordMismatch" class="w-full mt-2 bg-[#5A877E] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed">
        <span v-if="authStore.loading">Création en cours...</span>
        <span v-else>S'inscrire</span>
      </button>

      <p v-if="authStore.error" class="text-xs text-red-500 text-center mt-2">{{ authStore.error }}</p>

    </form>

    <div class="w-full max-w-sm flex items-center my-6">
      <div class="flex-grow border-t border-gray-200"></div>
      <span class="flex-shrink-0 mx-4 text-gray-400 text-xs font-medium tracking-wider">OU</span>
      <div class="flex-grow border-t border-gray-200"></div>
    </div>

    <SocialLoginButton text="S'inscrire avec Google" @success="handleGoogleCallback" />
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';
import SocialLoginButton from '@/components/SocialLoginButton.vue';

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);

const formData = reactive({
  email: '',
  password: '',
  confirm_password: '',
  profession: '',
  monthly_budget: null
});

const passwordMismatch = computed(() => {
  return formData.password && formData.confirm_password && formData.password !== formData.confirm_password;
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleRegister = async () => {
  if (passwordMismatch.value) return;

  try {
    const { confirm_password, ...payload } = formData;

    // Casting de sécurité : Conversion propre en Float pour correspondre au DecimalField de Django
    if (payload.monthly_budget) {
      payload.monthly_budget = parseFloat(payload.monthly_budget);
    }

    await authStore.register(payload);
    router.push('/dashboard');
  } catch (err) {
    // Les erreurs sont capturées et affichées via le template
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