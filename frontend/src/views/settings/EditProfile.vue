<template>
  <div class="flex-grow bg-[#F6F5F2] flex flex-col px-6 py-6 dm-sans">
    <!-- Header -->
    <header class="flex items-center justify-between mb-8 relative">
      <button @click="router.back()" class="text-gray-500 hover:text-gray-800 transition-colors z-10">
        <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
      </button>
      <h1 class="absolute w-full text-center text-xl font-bold text-gray-900">Mon profil</h1>
    </header>

    <!-- Avatar Section -->
    <div class="flex justify-center mb-8">
      <div class="relative">
        <div class="w-28 h-28 rounded-full overflow-hidden border-2 border-gray-100 shadow-sm bg-gray-200">
          <img src="https://i.pravatar.cc/150?img=11" alt="Avatar" class="w-full h-full object-cover grayscale"/>
        </div>
        <button type="button"
                class="absolute bottom-0 right-0 bg-[#5A877E] p-2.5 rounded-full border-4 border-[#F6F5F2] shadow-sm hover:bg-[#4a7269] transition-colors">
          <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="space-y-4 flex-grow flex flex-col">

      <!-- Nom complet -->
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900">Nom complet</label>
        <input
            type="text"
            v-model="formData.full_name"
            @input="validateField('full_name')"
            placeholder="Julien Alvarez"
            class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm"
            :class="errors.full_name ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700' : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'"
        />
        <p v-if="errors.full_name" class="text-xs text-red-500 font-medium ml-2">{{ errors.full_name }}</p>
      </div>

      <!-- Email (Read Only) -->
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900">Email</label>
        <input
            type="email"
            v-model="formData.email"
            readonly
            class="w-full px-4 py-3.5 border border-gray-200 rounded-2xl outline-none shadow-sm bg-gray-100 text-gray-500 cursor-not-allowed"
        />
      </div>

      <!-- New Password -->
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900  ">Nouveau mot de passe</label>
        <input
            type="password"
            v-model="formData.new_password"
            @input="handlePasswordInput"
            placeholder="Min. 8 caractères"
            class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm tracking-widest"
            :class="errors.new_password ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700' : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'"
        />

        <!-- Dynamic Password Strength Indicator -->
        <div v-if="formData.new_password" class="mt-2 px-1 space-y-1.5 transition-all">
          <div class="flex justify-between items-center text-xs font-semibold">
            <span class="text-gray-500">Force :</span>
            <span :class="passwordStrength.textColor">{{ passwordStrength.label }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
            <div
                class="h-1.5 transition-all duration-300 ease-out"
                :class="passwordStrength.color"
                :style="{ width: passwordStrength.percent + '%' }">
            </div>
          </div>
        </div>

        <p v-if="errors.new_password" class="text-xs text-red-500 font-medium ml-2 mt-1">{{ errors.new_password }}</p>
      </div>

      <!-- Confirm New Password -->
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900">Confirmer nouveau mot de passe</label>
        <input
            type="password"
            v-model="formData.confirm_password"
            @input="validateField('confirm_password')"
            placeholder="Répétez le mot de passe"
            class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm tracking-widest"
            :class="errors.confirm_password ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700' : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'"
        />
        <p v-if="errors.confirm_password" class="text-xs text-red-500 font-medium ml-2">{{
            errors.confirm_password
          }}</p>
      </div>

      <!-- Date de naissance -->
      <div class="space-y-1 pt-2">
        <label class="block text-lg font-medium text-gray-900">Date de naissance</label>
        <input
            type="date"
            v-model="formData.birth_date"
            class="w-full px-4 py-3.5 border border-gray-200 rounded-2xl outline-none transition-all shadow-sm bg-white focus:ring-2 focus:ring-[#5A877E] text-gray-600"
        />
      </div>

      <!-- Objectif financier -->
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900">Objectif financier</label>
        <div class="relative">
          <select
              v-model="formData.financial_goal"
              class="w-full px-4 py-3.5 border border-gray-200 rounded-2xl outline-none transition-all shadow-sm bg-white focus:ring-2 focus:ring-[#5A877E] appearance-none text-gray-600"
          >
            <option value="Réduire les dépenses impulsives">Réduire les dépenses impulsives</option>
            <option value="Épargner pour un projet">Épargner pour un projet</option>
            <option value="Rembourser des dettes">Rembourser des dettes</option>
            <option value="Investir pour l'avenir">Investir pour l'avenir</option>
            <option value="Créer un fonds d'urgence">Créer un fonds d'urgence</option>
            <option value="Acheter un bien immobilier">Acheter un bien immobilier</option>
          </select>
          <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- Budget mensuel -->
      <div class="space-y-1 pb-6">
        <label class="block text-lg font-medium text-gray-900">Budget mensuel</label>
        <div class="relative">
          <input
              type="number"
              v-model="formData.monthly_budget"
              placeholder="3500"
              class="w-full px-4 pr-16 py-3.5 border border-gray-200 rounded-2xl outline-none transition-all shadow-sm bg-white focus:ring-2 focus:ring-[#5A877E] text-gray-600"
          />
          <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none">
            <span class="text-gray-500 font-medium">{{ currencyStore.currentCurrency.code }}</span>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="mt-auto pt-6 flex justify-center">
        <button
            type="submit"
            :disabled="isSaving"
            class="w-[280px] bg-[#538278] text-white rounded-full py-3.5 font-medium text-[1.15rem] hover:bg-[#436b62] transition-all active:scale-[0.98] shadow-sm flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <span v-if="isSaving">Enregistrement...</span>
          <template v-else>
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
            Enregistrer
          </template>
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import {reactive, ref, onMounted, computed} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '@/stores/auth';
import api from '@/services/api';
import {useCurrencyStore} from '@/stores/currency';

const router = useRouter();
const authStore = useAuthStore();
const isSaving = ref(false);

const currencyStore = useCurrencyStore();

const formData = reactive({
  full_name: '',
  email: '',
  current_password: '',
  new_password: '',
  confirm_password: '',
  birth_date: '',
  financial_goal: 'Réduire les dépenses impulsives',
  monthly_budget: null
});

const errors = reactive({
  full_name: null,
  new_password: null,
  confirm_password: null,
});

onMounted(() => {
  if (authStore.user) {
    formData.full_name = authStore.user.full_name || '';
    formData.email = authStore.user.email || '';
    formData.birth_date = authStore.user.birth_date || '';
    formData.financial_goal = authStore.user.financial_goal || 'Réduire les dépenses impulsives';
    formData.monthly_budget = authStore.user.monthly_budget || null;
  }
});

// Dynamic Password Strength Calculator
const passwordStrength = computed(() => {
  const pwd = formData.new_password;
  if (!pwd) return {percent: 0, color: 'bg-transparent', textColor: 'text-gray-400', label: ''};

  let score = 0;
  if (pwd.length >= 8) score += 25; // Good length
  if (/[A-Z]/.test(pwd)) score += 25; // Has uppercase
  if (/[0-9]/.test(pwd)) score += 25; // Has number
  if (/[^A-Za-z0-9]/.test(pwd)) score += 25; // Has special character

  if (score <= 25) return {percent: 25, color: 'bg-red-400', textColor: 'text-red-500', label: 'Faible'};
  if (score === 50) return {percent: 50, color: 'bg-orange-400', textColor: 'text-orange-500', label: 'Moyen'};
  if (score === 75) return {percent: 75, color: 'bg-blue-400', textColor: 'text-blue-500', label: 'Bon'};
  return {percent: 100, color: 'bg-[#5A877E]', textColor: 'text-[#5A877E]', label: 'Fort'};
});

// Ensures confirmation validation updates dynamically if the user modifies the first password field
const handlePasswordInput = () => {
  validateField('new_password');
  if (formData.confirm_password) {
    validateField('confirm_password');
  }
};

const validateField = (field) => {
  if (field === 'full_name') {
    const nameLength = formData.full_name.trim().length;
    if (nameLength < 3 || nameLength > 50) {
      errors.full_name = "Le nom doit comporter entre 3 et 50 caractères.";
    } else if (/\d/.test(formData.full_name)) {
      errors.full_name = "Le nom complet ne peut pas contenir de chiffres.";
    } else {
      errors.full_name = null;
    }
  }

  if (field === 'new_password') {
    if (formData.new_password && formData.new_password.length < 8) {
      errors.new_password = "Le mot de passe doit contenir au moins 8 caractères.";
    } else {
      errors.new_password = null;
    }
  }

  if (field === 'confirm_password') {
    if (formData.confirm_password && formData.confirm_password !== formData.new_password) {
      errors.confirm_password = "Les mots de passe doivent être identiques.";
    } else {
      errors.confirm_password = null;
    }
  }
};

const handleSubmit = async () => {
  validateField('full_name');

  // Only trigger password validation if the user is attempting to change it
  if (formData.new_password || formData.confirm_password) {
    validateField('new_password');
    validateField('confirm_password');
  }

  // Block submission if there are any active errors
  if (errors.full_name || errors.new_password || errors.confirm_password) return;

  isSaving.value = true;

  try {
    const payload = {
      full_name: formData.full_name,
      birth_date: formData.birth_date,
      financial_goal: formData.financial_goal,
      monthly_budget: formData.monthly_budget ? parseFloat(formData.monthly_budget) : null,
    };

    if (formData.new_password) {
      payload.current_password = formData.current_password;
      payload.new_password = formData.new_password;
      // We don't send confirm_password to the backend API
    }

    await api.patch('/users/me/', payload);
    await authStore.fetchUserProfile();
    router.push({name: 'settings'});

  } catch (error) {
    console.error("Erreur de mise à jour: ", error);
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;500;700&display=swap');

.dm-sans {
  font-family: 'DM Sans', sans-serif;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: 0.2s;
}

input[type="date"]::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>