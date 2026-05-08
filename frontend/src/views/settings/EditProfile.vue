<template>
  <div class="flex-grow bg-[#F6F5F2] flex flex-col px-6 py-6 dm-sans">
    <header class="flex items-center justify-between mb-8 relative">
      <button
        @click="router.back()"
        class="text-gray-500 hover:text-gray-800 transition-colors z-10"
      >
        <svg
          class="w-7 h-7"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
      </button>
      <h1 class="absolute w-full text-center text-xl font-bold text-gray-900">
        Mon profil
      </h1>
    </header>
    <div
      v-if="showSuccessMessage"
      class="fixed top-6 left-1/2 transform -translate-x-1/2 bg-[#538278] text-white px-6 py-3 rounded-2xl shadow-lg z-50 flex items-center gap-2 transition-all duration-300"
    >
      <svg
        class="w-5 h-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M5 13l4 4L19 7"
        />
      </svg>
      <span class="font-medium">Modifications enregistrées avec succès</span>
    </div>
    <form
      @submit.prevent="handleSubmit"
      class="space-y-4 flex-grow flex flex-col"
    >
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900"
          >Nom complet</label
        >
        <input
          type="text"
          v-model="formData.full_name"
          @input="validateField('full_name')"
          placeholder="Julien Alvarez"
          class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm"
          :class="
            errors.full_name
              ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700'
              : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'
          "
        />
        <p
          v-if="errors.full_name"
          class="text-xs text-red-500 font-medium ml-2"
        >
          {{ errors.full_name }}
        </p>
      </div>

      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900">Email</label>
        <input
          type="email"
          v-model="formData.email"
          readonly
          class="w-full px-4 py-3.5 border border-gray-200 rounded-2xl outline-none shadow-sm bg-gray-100 text-gray-500 cursor-not-allowed"
        />
      </div>
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900"
          >Ancien mot de passe</label
        >
        <input
          type="password"
          v-model="formData.old_password"
          placeholder="Votre mot de passe actuel"
          class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm tracking-widest"
          :class="
            errors.old_password
              ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700'
              : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'
          "
        />
        <p
          v-if="errors.old_password"
          class="text-xs text-red-500 font-medium ml-2 mt-1"
        >
          {{ errors.old_password }}
        </p>
      </div>
      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900"
          >Nouveau mot de passe</label
        >
        <input
          type="password"
          v-model="formData.new_password"
          @input="handlePasswordInput"
          placeholder="Min. 8 caractères"
          class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm tracking-widest"
          :class="
            errors.new_password
              ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700'
              : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'
          "
        />

        <div
          v-if="formData.new_password"
          class="mt-2 px-1 space-y-1.5 transition-all"
        >
          <div class="flex justify-between items-center text-xs font-semibold">
            <span class="text-gray-500">Force :</span>
            <span :class="passwordStrength.textColor">{{
              passwordStrength.label
            }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
            <div
              class="h-1.5 transition-all duration-300 ease-out"
              :class="passwordStrength.color"
              :style="{ width: passwordStrength.percent + '%' }"
            ></div>
          </div>
        </div>

        <p
          v-if="errors.new_password"
          class="text-xs text-red-500 font-medium ml-2 mt-1"
        >
          {{ errors.new_password }}
        </p>
      </div>

      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900"
          >Confirmer nouveau mot de passe</label
        >
        <input
          type="password"
          v-model="formData.confirm_password"
          @input="validateField('confirm_password')"
          placeholder="Répétez le mot de passe"
          class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm tracking-widest"
          :class="
            errors.confirm_password
              ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700'
              : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'
          "
        />
        <p
          v-if="errors.confirm_password"
          class="text-xs text-red-500 font-medium ml-2"
        >
          {{ errors.confirm_password }}
        </p>
      </div>

      <div class="space-y-1 pt-2">
        <label class="block text-lg font-medium text-gray-900"
          >Date de naissance</label
        >
        <input
          type="date"
          v-model="formData.birth_date"
          class="w-full px-4 py-3.5 border border-gray-200 rounded-2xl outline-none transition-all shadow-sm bg-white focus:ring-2 focus:ring-[#5A877E] text-gray-600"
        />
        <p
          v-if="errors.birth_date"
          class="text-xs text-red-500 font-medium ml-2"
        >
          {{ errors.birth_date }}
        </p>
      </div>

      <SocioProSelect
        v-model="formData.socio_professional_categories"
        :error="errors.socio_professional_categories"
        @validate="validateField('socio_professional_categories')"
      />

      <div class="space-y-1">
        <label class="block text-lg font-medium text-gray-900"
          >Objectif financier</label
        >

        <CustomSelect
          v-model="formData.financial_goal"
          :options="goalOptions"
          @change="validateField('financial_goal')"
          sizeClass="py-3.5 h-auto text-gray-600 bg-white border-gray-200"
          roundedClass="rounded-2xl"
        />
      </div>

      <div v-if="formData.financial_goal === 'Autre'" class="space-y-1 mt-2">
        <label class="block text-sm font-medium text-gray-700 ml-1"
          >Précisez votre objectif</label
        >
        <input
          type="text"
          v-model="formData.custom_financial_goal"
          @input="validateField('custom_financial_goal')"
          placeholder="Ex: Économiser pour un voyage au Japon..."
          class="w-full px-4 py-3.5 rounded-2xl outline-none transition-all shadow-sm"
          :class="
            errors.custom_financial_goal
              ? 'border-2 border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50 text-red-700'
              : 'border border-gray-200 focus:ring-2 focus:ring-[#5A877E] bg-white'
          "
        />
        <p
          v-if="errors.custom_financial_goal"
          class="text-xs text-red-500 font-medium ml-2"
        >
          {{ errors.custom_financial_goal }}
        </p>
      </div>

      <div class="space-y-1 pb-6">
        <label class="block text-lg font-medium text-gray-900"
          >Budget mensuel</label
        >
        <CustomSelect
          v-model="formData.monthly_budget"
          :options="budgetOptions"
          @change="validateField('monthly_budget')"
          sizeClass="py-3.5 h-auto text-gray-600 bg-white border-gray-200"
          roundedClass="rounded-2xl"
          placeholder="Sélectionnez une tranche"
        />
        <p
          v-if="errors.monthly_budget"
          class="text-xs text-red-500 font-medium ml-2"
        >
          {{ errors.monthly_budget }}
        </p>
      </div>

      <div class="mt-auto pt-6 flex justify-center">
        <button
          type="submit"
          :disabled="isSaving"
          class="w-[280px] bg-[#538278] text-white rounded-full py-3.5 font-medium text-[1.15rem] hover:bg-[#436b62] transition-all active:scale-[0.98] shadow-sm flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <span v-if="isSaving">Enregistrement...</span>
          <template v-else>
            <svg
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
            Enregistrer
          </template>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import { useCurrencyStore } from "@/stores/currency";
import CustomSelect from "@/components/shared/CustomSelect.vue";
import SocioProSelect from "@/components/shared/SocioProSelect.vue";

const router = useRouter();
const authStore = useAuthStore();
const isSaving = ref(false);
const currencyStore = useCurrencyStore();

const goalOptions = [
  "Réduire les dépenses impulsives",
  "Épargner pour un projet",
  "Rembourser des dettes",
  "Investir pour l'avenir",
  "Créer un fonds d'urgence",
  "Acheter un bien immobilier",
  "Autre",
];

const baseBudgetRanges = [
  "Je préfère ne pas répondre",
  "Moins de 500",
  "500 - 1 000",
  "1 000 - 2 000",
  "2 000 - 3 500",
  "3 500 - 5 000",
  "5 000 - 8 000",
  "8 000 - 15 000",
  "15 000+",
];
const showSuccessMessage = ref(false);

const budgetOptions = computed(() => {
  const currencyCode = currencyStore.currentCurrency.code;
  return baseBudgetRanges.map((range) => {
    if (range === "Je préfère ne pas répondre") {
      return { value: range, label: range };
    }
    return { value: range, label: `${range} ${currencyCode}` };
  });
});

const formData = reactive({
  full_name: "",
  email: "",
  old_password: "",
  new_password: "",
  confirm_password: "",
  birth_date: "",
  financial_goal: "Réduire les dépenses impulsives",
  custom_financial_goal: "",
  monthly_budget: null,
  socio_professional_categories: ["Préfère ne pas répondre"],
});

const errors = reactive({
  full_name: null,
  old_password: null,
  new_password: null,
  confirm_password: null,
  birth_date: null,
  monthly_budget: null,
  custom_financial_goal: null,
  socio_professional_categories: null,
});

onMounted(() => {
  if (authStore.user) {
    formData.full_name = authStore.user.full_name || "";
    formData.email = authStore.user.email || "";
    formData.birth_date = authStore.user.birth_date || "";
    formData.monthly_budget = authStore.user.monthly_budget || null;

    if (authStore.user.socio_professional_categories?.length > 0) {
      formData.socio_professional_categories = [
        ...authStore.user.socio_professional_categories,
      ];
    }

    const savedGoal =
      authStore.user.financial_goal || "Réduire les dépenses impulsives";
    if (goalOptions.includes(savedGoal)) {
      formData.financial_goal = savedGoal;
    } else {
      formData.financial_goal = "Autre";
      formData.custom_financial_goal = savedGoal;
    }
  }
});

const passwordStrength = computed(() => {
  const pwd = formData.new_password;
  if (!pwd)
    return {
      percent: 0,
      color: "bg-transparent",
      textColor: "text-gray-400",
      label: "",
    };

  let score = 0;
  if (pwd.length >= 8) score += 25;
  if (/[A-Z]/.test(pwd)) score += 25;
  if (/[0-9]/.test(pwd)) score += 25;
  if (/[^A-Za-z0-9]/.test(pwd)) score += 25;

  if (score <= 25)
    return {
      percent: 25,
      color: "bg-red-400",
      textColor: "text-red-500",
      label: "Faible",
    };
  if (score === 50)
    return {
      percent: 50,
      color: "bg-orange-400",
      textColor: "text-orange-500",
      label: "Moyen",
    };
  if (score === 75)
    return {
      percent: 75,
      color: "bg-blue-400",
      textColor: "text-blue-500",
      label: "Bon",
    };
  return {
    percent: 100,
    color: "bg-[#5A877E]",
    textColor: "text-[#5A877E]",
    label: "Fort",
  };
});

const handlePasswordInput = () => {
  validateField("new_password");
  if (formData.confirm_password) {
    validateField("confirm_password");
  }
};

const validateField = (field) => {
  if (field === "full_name") {
    const nameLength = formData.full_name.trim().length;
    if (nameLength < 3 || nameLength > 50) {
      errors.full_name = "Le nom doit comporter entre 3 et 50 caractères.";
    } else if (/\d/.test(formData.full_name)) {
      errors.full_name = "Le nom complet ne peut pas contenir de chiffres.";
    } else {
      errors.full_name = null;
    }
  }
  if (field === "birth_date" && formData.birth_date) {
    const today = new Date();
    const birthDate = new Date(formData.birth_date);
    if (birthDate > today) {
      errors.birth_date =
        "La date de naissance ne peut pas être dans le futur.";
    } else {
      errors.birth_date = null;
    }
  }
  if (field === "custom_financial_goal" || field === "financial_goal") {
    if (formData.financial_goal === "Autre") {
      const val = formData.custom_financial_goal.trim();
      const wordCount = val.split(/\s+/).length;
      const hasLetters = /[a-zA-Z]/.test(val);

      if (val.length < 5) {
        errors.custom_financial_goal =
          "L'objectif doit contenir au moins 5 caractères.";
      } else if (!hasLetters) {
        errors.custom_financial_goal =
          "L'objectif ne peut pas contenir uniquement des chiffres.";
      } else if (wordCount < 2) {
        errors.custom_financial_goal =
          "Veuillez détailler votre objectif (au moins deux mots).";
      } else {
        errors.custom_financial_goal = null;
      }
    } else {
      errors.custom_financial_goal = null;
    }
  }

  if (field === "socio_professional_categories") {
    if (formData.socio_professional_categories.length === 0) {
      errors.socio_professional_categories =
        "Veuillez sélectionner au moins une catégorie.";
    } else {
      errors.socio_professional_categories = null;
    }
  }

  if (field === "new_password") {
    if (formData.new_password && formData.new_password.length < 8) {
      errors.new_password =
        "Le mot de passe doit contenir au moins 8 caractères.";
    } else {
      errors.new_password = null;
    }
  }

  if (field === "confirm_password") {
    if (
      formData.confirm_password &&
      formData.confirm_password !== formData.new_password
    ) {
      errors.confirm_password = "Les mots de passe doivent être identiques.";
    } else {
      errors.confirm_password = null;
    }
  }
};

const handleSubmit = async () => {
  validateField("full_name");
  validateField("birth_date");
  validateField("monthly_budget");
  validateField("custom_financial_goal");
  validateField("socio_professional_categories");

  if (formData.new_password || formData.confirm_password) {
    // Validation rapide de l'ancien mot de passe
    if (!formData.old_password) {
      errors.old_password = "Votre ancien mot de passe est requis.";
    } else {
      errors.old_password = null;
    }
    validateField("new_password");
    validateField("confirm_password");
  } else {
    errors.old_password = null;
  }

  if (Object.values(errors).some((e) => e !== null)) return;

  isSaving.value = true;

  try {
    const nameParts = formData.full_name.trim().split(" ");
    const payload = {
      first_name: nameParts[0] || "",
      last_name: nameParts.slice(1).join(" ") || "",
      birth_date: formData.birth_date || null,
      financial_goal:
        formData.financial_goal === "Autre"
          ? formData.custom_financial_goal.trim()
          : formData.financial_goal,
      monthly_budget: formData.monthly_budget || null,
      socio_professional_categories: [
        ...formData.socio_professional_categories,
      ],
    };

    // Ajout de l'ancien mot de passe dans le payload
    if (formData.new_password) {
      payload.old_password = formData.old_password; // <-- Ajout
      payload.new_password = formData.new_password;
    }

    await api.patch("/users/me/", payload);
    await authStore.fetchUserProfile();

    showSuccessMessage.value = true;
    formData.old_password = ""; // <-- Réinitialisation
    formData.new_password = "";
    formData.confirm_password = "";

    setTimeout(() => {
      showSuccessMessage.value = false;
    }, 3000);
  } catch (error) {
    console.error("Erreur de mise à jour: ", error);
    // Optionnel: Gérer l'erreur 400 spécifiquement pour l'afficher à l'utilisateur
    if (error.response?.status === 400 && error.response?.data?.old_password) {
      errors.old_password = "L'ancien mot de passe est incorrect.";
    }
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap");
.dm-sans {
  font-family: "DM Sans", sans-serif;
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

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
