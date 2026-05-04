<template>
  <div
    class="min-h-screen bg-[#F6F5F2] flex flex-col items-center px-6 py-12 font-sans selection:bg-[#5A877E] selection:text-white"
  >
    <div
      class="w-16 h-16 bg-[#EFF3F3] rounded-2xl flex items-center justify-center mb-6 shadow-sm"
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M3.05859 6.04688C-1.01953 10.125 -1.01953 16.7344 3.05859 20.8828C5.23828 15.75 9.17578 11.4609 14.0977 8.92969C9.94922 12.4453 6.99609 17.3672 6.01172 22.9219C9.87891 24.75 14.6602 24.1172 17.8945 20.8828C22.3945 16.3828 23.6602 4.14844 23.9414 0.773438C23.9414 0.351562 23.5898 0 23.168 0C19.793 0.28125 7.55859 1.54688 3.05859 6.04688Z"
          fill="#5B8C85"
        />
      </svg>
    </div>

    <h1
      class="text-4xl font-serif font-bold text-[#2A3039] mb-3 tracking-tight"
    >
      Vrai Besoin
    </h1>
    <p
      class="text-center text-[#6B7280] text-sm mb-8 max-w-[280px] leading-relaxed"
    >
      Reprenez le contrôle de vos achats impulsifs et retrouvez votre sérénité
      financière.
    </p>

    <div class="flex w-full max-w-sm bg-[#F3F4F6] p-1.5 rounded-2xl mb-8">
      <button
        class="flex-1 bg-white shadow-sm rounded-xl py-2.5 text-sm font-semibold text-[#1F2937] transition-all"
      >
        Connexion
      </button>
      <button
        @click="router.push('/register')"
        class="flex-1 rounded-xl py-2.5 text-sm font-medium text-[#6B7280] hover:text-[#374151] transition-all"
      >
        Inscription
      </button>
    </div>

    <form @submit.prevent="handleLogin" class="w-full max-w-sm space-y-5">
      <div class="space-y-1.5">
        <label for="email" class="block text-sm font-medium text-[#374151]"
          >Email</label
        >
        <div class="relative">
          <div
            class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
          >
            <svg
              class="h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            placeholder="exemple@email.com"
            autocomplete="username"
            class="block w-full pl-11 pr-4 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400"
            required
          />
        </div>
      </div>

      <div class="space-y-1.5">
        <label for="password" class="block text-sm font-medium text-[#374151]"
          >Mot de passe</label
        >
        <div class="relative">
          <div
            class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"
          >
            <svg
              class="h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
            </svg>
          </div>
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="formData.password"
            placeholder="••••••••"
            autocomplete="current-password"
            class="block w-full pl-11 pr-12 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
            required
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none"
          >
            <svg
              v-if="!showPassword"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
              />
            </svg>
            <svg
              v-else
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
          </button>
        </div>
      </div>

      <div class="flex justify-end">
        <router-link
          to="/forgot-password"
          class="text-xs font-medium text-[#5A877E] hover:text-[#456B63] transition-colors"
        >
          Mot de passe oublié ?
        </router-link>
      </div>

      <button
        type="submit"
        :disabled="authStore.loading"
        class="w-full bg-[#5A877E] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <span v-if="authStore.loading">Connexion en cours...</span>
        <span v-else>Se connecter</span>
      </button>

      <p v-if="authStore.error" class="text-xs text-red-500 text-center mt-2">
        {{ authStore.error }}
      </p>
    </form>

    <div class="w-full max-w-sm flex items-center my-8">
      <div class="flex-grow border-t border-gray-200"></div>
      <span
        class="flex-shrink-0 mx-4 text-gray-400 text-xs font-medium tracking-wider"
        >OU CONTINUER AVEC</span
      >
      <div class="flex-grow border-t border-gray-200"></div>
    </div>

    <!-- Zone du Bouton Google 100% Personnalisé -->
    <div class="w-full max-w-sm flex flex-col items-center">
      <button
        type="button"
        @click="loginWithGoogle"
        class="w-full flex items-center justify-center gap-3 bg-white border border-gray-200 rounded-2xl py-3.5 font-medium text-sm text-[#374151] hover:bg-gray-50 hover:border-gray-300 transition-all active:scale-[0.98] shadow-sm"
      >
        <svg
          class="w-5 h-5"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            fill="#4285F4"
          />
          <path
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.16v2.84C3.99 20.53 7.7 23 12 23z"
            fill="#34A853"
          />
          <path
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.16C1.43 8.55 1 10.22 1 12s.43 3.45 1.16 4.93l3.68-2.84z"
            fill="#FBBC05"
          />
          <path
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.16 7.07l3.68 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            fill="#EA4335"
          />
        </svg>
        Google
      </button>

      <!-- Affichage de l'erreur en Français -->
      <p
        v-if="googleError"
        class="text-xs text-red-500 text-center mt-3 font-medium"
      >
        {{ googleError }}
      </p>
    </div>

    <p class="mt-8 text-sm text-[#6B7280]">
      Pas encore de compte ?
      <router-link
        to="/register"
        class="font-medium text-[#5A877E] hover:text-[#456B63] transition-colors"
        >Créer un compte
      </router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
import { useTokenClient } from "vue3-google-signin";

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);
const googleError = ref("");

const formData = reactive({
  email: "",
  password: "",
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  try {
    await authStore.login({
      email: formData.email,
      password: formData.password,
    });
    router.push("/dashboard");
  } catch (err) {
    // L'erreur est gérée et affichée via authStore.error dans le template
  }
};

// Implémentation via useTokenClient pour autoriser le bouton 100% personnalisé
const { login: loginWithGoogle } = useTokenClient({
  onSuccess: async (response) => {
    googleError.value = "";
    try {
      await authStore.googleLogin(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      console.error("Erreur SSO Google :", err);

      const backendError =
        err.response?.data?.error || err.response?.data?.non_field_errors?.[0];

      if (backendError) {
        googleError.value = backendError;
      } else if (err.response?.status === 400 || err.response?.status === 401) {
        googleError.value =
          "Connexion impossible. Si vous avez créé votre compte avec un mot de passe, veuillez l'utiliser.";
      } else {
        googleError.value =
          "Échec de l'authentification avec Google. Veuillez réessayer.";
      }
    }
  },
  onError: () => {
    googleError.value = "La connexion Google a été annulée ou a échoué.";
  },
});
</script>
