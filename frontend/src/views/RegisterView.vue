<template>
  <div
    class="min-h-screen bg-[#F6F5F2] flex flex-col items-center px-6 py-10 font-sans selection:bg-[#5A877E] selection:text-white relative"
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

    <div class="flex w-full max-w-sm bg-[#F3F4F6] p-1.5 rounded-2xl mb-6">
      <button
        @click="router.push('/login')"
        class="flex-1 rounded-xl py-2.5 text-sm font-medium text-[#6B7280] hover:text-[#374151] transition-all"
      >
        Connexion
      </button>
      <button
        class="flex-1 bg-white shadow-sm rounded-xl py-2.5 text-sm font-semibold text-[#1F2937] transition-all"
      >
        Inscription
      </button>
    </div>

    <form @submit.prevent="handleRegister" class="w-full max-w-sm space-y-4">
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

      <div class="space-y-1.5">
        <label
          for="confirm_password"
          class="block text-sm font-medium text-[#374151]"
          >Confirmer le mot de passe</label
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
            id="confirm_password"
            v-model="formData.confirm_password"
            placeholder="••••••••"
            autocomplete="new-password"
            class="block w-full pl-11 pr-12 py-3.5 border border-gray-200 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E] focus:border-transparent outline-none transition-all placeholder-gray-400 tracking-widest"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        :disabled="isRequestingOtp || isFormInvalid"
        class="w-full mt-2 bg-[#5B8C85] text-white rounded-2xl py-3.5 font-semibold text-sm hover:bg-[#4A726A] transition-colors active:scale-[0.98] shadow-md shadow-[#5A877E]/20 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <span v-if="isRequestingOtp">Envoi du code...</span>
        <span v-else>S'inscrire</span>
      </button>

      <p
        v-if="authStore.error && !showOtpModal"
        class="text-xs text-red-500 text-center mt-2"
      >
        {{ authStore.error }}
      </p>
    </form>

    <div class="w-full max-w-sm flex items-center my-6">
      <div class="flex-grow border-t border-gray-200"></div>
      <span
        class="flex-shrink-0 mx-4 text-gray-400 text-xs font-medium tracking-wider"
        >Ou continuer avec</span
      >
      <div class="flex-grow border-t border-gray-200"></div>
    </div>

    <div class="w-full max-w-sm flex flex-col items-center">
      <button
        type="button"
        @click="registerWithGoogle"
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
      <p
        v-if="googleError"
        class="text-xs text-red-500 text-center mt-3 font-medium"
      >
        {{ googleError }}
      </p>
    </div>

    <div
      v-if="showOtpModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4"
    >
      <div class="bg-white rounded-3xl p-8 max-w-sm w-full relative shadow-2xl">
        <button
          @click="showOtpModal = false"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
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

        <h2 class="text-2xl font-bold text-[#2A3039] mb-2 text-center">
          Vérifiez votre e-mail
        </h2>
        <p class="text-center text-[#6B7280] text-sm mb-6">
          Nous avons envoyé un code à 6 chiffres à <br />
          <span class="font-medium text-[#374151]">{{ formData.email }}</span>
        </p>

        <div class="flex justify-between gap-2 mb-6">
          <input
            v-for="(digit, index) in otpCode"
            :key="index"
            ref="otpInputs"
            type="text"
            inputmode="numeric"
            maxlength="1"
            v-model="otpCode[index]"
            @input="handleOtpInput(index, $event)"
            @keydown="handleOtpKeydown(index, $event)"
            @paste="handleOtpPaste"
            :disabled="isVerifying"
            :class="[
              'w-10 h-12 sm:w-12 sm:h-14 text-center text-xl sm:text-2xl font-bold rounded-xl outline-none transition-all disabled:opacity-50 border',
              otpError
                ? 'bg-red-50 border-red-500 text-red-600 focus:ring-2 focus:ring-red-500/20'
                : 'bg-[#F3F4F6] text-[#2A3039] border-transparent focus:bg-white focus:border-[#5A877E] focus:ring-2 focus:ring-[#5A877E]/20',
            ]"
          />
        </div>

        <p
          v-if="otpError"
          class="text-red-500 text-sm text-center mb-4 font-medium"
        >
          {{ otpError }}
        </p>

        <div class="text-center mt-2">
          <p class="text-sm text-[#6B7280] mb-2">
            Vous n'avez pas reçu le code ?
          </p>
          <button
            @click="resendOtp"
            :disabled="resendCountdown > 0 || isRequestingOtp"
            class="text-[#5B8C85] font-semibold text-sm hover:text-[#4A726A] disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Renvoyer le code
            <span v-if="resendCountdown > 0">({{ resendCountdown }}s)</span>
            <span v-else-if="isRequestingOtp">...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
import { useTokenClient } from "vue3-google-signin";
import api from "@/services/api.js";

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);
const googleError = ref("");

// État OTP
const showOtpModal = ref(false);
const otpCode = ref(["", "", "", "", "", ""]);
const otpInputs = ref([]);
const otpError = ref("");
const resendCountdown = ref(0);
const isRequestingOtp = ref(false);
const isVerifying = ref(false);
let timerInterval = null;

const formData = reactive({
  email: "",
  password: "",
  confirm_password: "",
});

const isFormInvalid = computed(() => {
  return (
    !formData.email ||
    !formData.password ||
    !formData.confirm_password ||
    formData.password !== formData.confirm_password
  );
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// 1. Demande de l'OTP
const handleRegister = async () => {
  if (isFormInvalid.value) return;
  try {
    isRequestingOtp.value = true;
    authStore.error = "";

    await api.post("/auth/request-otp/", { email: formData.email });

    showOtpModal.value = true;
    otpCode.value = ["", "", "", "", "", ""];
    otpError.value = "";
    startResendTimer();

    setTimeout(() => {
      if (otpInputs.value[0]) otpInputs.value[0].focus();
    }, 100);
  } catch (err) {
    authStore.error =
      err.response?.data?.error ||
      "Erreur lors de la demande du code de vérification.";
  } finally {
    isRequestingOtp.value = false;
  }
};

// Fonction de vérification centralisée (Remplace le watcher capricieux)
const checkOtpAndSubmit = async () => {
  const code = otpCode.value.join("");
  if (code.length === 6 && !otpCode.value.includes("")) {
    await verifyOtpAndRegister(code);
  }
};

// 2. Vérification et Inscription
const verifyOtpAndRegister = async (code) => {
  if (isVerifying.value) return; // Sécurité anti-double exécution
  try {
    isVerifying.value = true;
    otpError.value = "";

    // Appel à l'API d'inscription finale
    await authStore.register({ ...formData, otp: code });

    // --- SUCCÈS ---
    showOtpModal.value = false;

    // Redirection sécurisée
    router.push("/onboarding").catch(() => {
      router.push("/dashboard");
    });
  } catch (err) {
    // --- ERREUR ---
    console.error("Erreur de validation:", err);

    // Capture robuste du message d'erreur renvoyé par Django (gestion des dictionnaires d'erreurs)
    const data = err.response?.data;
    let backendError = data?.error;

    if (!backendError && data) {
      // S'il s'agit d'un dictionnaire d'erreurs DRF, on récupère le premier message
      const firstKey = Object.keys(data)[0];
      if (firstKey) {
        backendError = Array.isArray(data[firstKey])
          ? data[firstKey][0]
          : data[firstKey];
      }
    }

    if (backendError) {
      otpError.value = backendError;
    } else {
      otpError.value =
        "Le code est incorrect ou une erreur serveur est survenue.";
    }

    // Vide la DERNIÈRE case pour forcer l'utilisateur à la retaper et re-déclencher la validation
    setTimeout(() => {
      if (otpInputs.value[5]) {
        otpCode.value[5] = "";
        otpInputs.value[5].focus();
      }
    }, 50);
  } finally {
    isVerifying.value = false;
  }
};

// --- Interactions avec les Inputs ---
const handleOtpInput = (index, event) => {
  const value = event.target.value;

  // On n'efface l'erreur que SI on a tapé un vrai chiffre
  if (value && /^\d*$/.test(value) && otpError.value) {
    otpError.value = "";
  }

  // Interdire les lettres
  if (!/^\d*$/.test(value)) {
    otpCode.value[index] = "";
    return;
  }

  // Passage auto au champ suivant
  if (value && index < 5) {
    otpInputs.value[index + 1].focus();
  }

  // Vérification de la complétude
  checkOtpAndSubmit();
};

const handleOtpKeydown = (index, event) => {
  if (event.key === "Backspace" && !otpCode.value[index] && index > 0) {
    otpInputs.value[index - 1].focus();
    otpError.value = ""; // Efface l'erreur si on recule
  }
};

const handleOtpPaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData
    .getData("text")
    .replace(/\D/g, "")
    .slice(0, 6);
  if (pastedData) {
    otpError.value = ""; // Efface l'erreur au collage
    for (let i = 0; i < pastedData.length; i++) {
      otpCode.value[i] = pastedData[i];
    }
    const nextIndex = pastedData.length < 6 ? pastedData.length : 5;
    otpInputs.value[nextIndex].focus();

    checkOtpAndSubmit();
  }
};

// --- Timer et Renvoyer ---
const startResendTimer = () => {
  resendCountdown.value = 60;
  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    resendCountdown.value--;
    if (resendCountdown.value <= 0) clearInterval(timerInterval);
  }, 1000);
};

const resendOtp = async () => {
  if (resendCountdown.value > 0) return;
  try {
    isRequestingOtp.value = true;
    otpError.value = "";
    await api.post("/auth/request-otp/", { email: formData.email });
    startResendTimer();
    otpCode.value = ["", "", "", "", "", ""];
    setTimeout(() => {
      if (otpInputs.value[0]) otpInputs.value[0].focus();
    }, 100);
  } catch (err) {
    otpError.value =
      err.response?.data?.error || "Impossible de renvoyer le code.";
  } finally {
    isRequestingOtp.value = false;
  }
};

// --- Authentification Google ---
const { login: registerWithGoogle } = useTokenClient({
  onSuccess: async (response) => {
    googleError.value = "";
    try {
      await authStore.googleLogin(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      const backendError =
        err.response?.data?.error || err.response?.data?.non_field_errors?.[0];
      if (backendError) {
        googleError.value = backendError;
      } else if (err.response?.status === 400 || err.response?.status === 401) {
        googleError.value =
          "Un compte utilise déjà cet email. Veuillez vous connecter avec votre mot de passe.";
      } else {
        googleError.value =
          "Échec de l'inscription avec Google. Veuillez réessayer.";
      }
    }
  },
  onError: () => {
    googleError.value = "L'inscription Google a été annulée ou a échoué.";
  },
});
</script>
