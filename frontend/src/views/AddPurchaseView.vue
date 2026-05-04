<template>
  <div class="min-h-screen bg-[#F8F6F2] flex flex-col font-sans selection:bg-[#5A877E] selection:text-white">

    <div v-if="step === 1" class="flex flex-col flex-grow relative pb-20">
      <div class="px-6 py-6 flex items-center gap-3">
        <div class="w-10 h-10 flex items-center justify-center">
          <svg width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg"
               xmlns:xlink="http://www.w3.org/1999/xlink">
            <path d="M52 0H0V52H52V0Z" fill="url(#pattern0_98_127)"/>
            <defs>
              <pattern id="pattern0_98_127" patternContentUnits="objectBoundingBox" width="1" height="1">
                <use xlink:href="#image0_98_127" transform="scale(0.00337838)"/>
              </pattern>
              <image id="image0_98_127" width="296" height="296" preserveAspectRatio="none"
                     xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASgAAAEoCAYAAADr..."/>
            </defs>
          </svg>
        </div>
        <span class="font-bold text-gray-900 text-lg tracking-tight">Vrai Besoin</span>
      </div>

      <div class="flex-grow flex flex-col items-center justify-center px-6 mt-[-40px]">
        <div class="w-32 h-32 bg-[#E1EBE8] rounded-full flex items-center justify-center mb-6">
          <svg class="w-16 h-16 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-[#1F2937] mb-2 text-center">Analysez votre envie</h1>
        <p class="text-[#6B7280] text-center mb-10 text-sm px-4 leading-relaxed">
          Collez un lien ou une image pour évaluer si cet achat est nécessaire.
        </p>

        <div class="relative w-full max-w-sm rounded-3xl border-2 border-dashed border-gray-400 bg-white p-8 flex flex-col items-center justify-center transition-all hover:bg-gray-50 group">
          <input
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              :disabled="coachStore.loading"
          />
          <div class="w-12 h-12 bg-[#F3F4F6] rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-6 h-6 text-[#5A877E]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
          <span class="text-sm font-semibold text-gray-800 mb-1">Télécharger une capture d'écran</span>
          <span class="text-xs text-gray-400">PNG, JPG jusqu'à 5MB</span>
        </div>
      </div>

      <div class="px-6 flex justify-center mb-8">
        <button @click="goToManualEntry"
                class="flex items-center gap-2 text-[#6B7280] hover:text-[#374151] transition-colors font-medium text-sm">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
          </svg>
          Saisir manuellement
        </button>
      </div>
    </div>

    <div v-else class="flex flex-col px-6 py-6">

      <div class="flex items-center relative mb-8">
        <button @click="resetToStep1" class="absolute left-0 text-gray-400 hover:text-gray-800 transition-colors">
          <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <h1 class="w-full text-center text-2xl font-semibold text-[#1F2937]">Analyse du Besoin</h1>
      </div>

      <div class="bg-[#F8FAF9] rounded-2xl p-4 flex gap-3 mb-8 border border-[#EBEBEB]">
        <div class="mt-0.5">
          <svg class="w-5 h-5 text-[#5A877E]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clip-rule="evenodd"/>
          </svg>
        </div>
        <div>
          <h3 class="text-[15px] font-semibold text-[#1F2937] mb-1">Qualifiez votre envie</h3>
          <p class="text-sm text-[#4B5563] leading-snug">Ces informations permettent à l'IA d'évaluer la véritable
            utilité de cet achat.</p>
        </div>
      </div>

      <div v-if="isExtracting" class="flex flex-col items-center justify-center mb-6">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#5A877E]"></div>
        <span class="text-sm text-[#5A877E] mt-2 font-medium">L'IA analyse votre image...</span>
      </div>

      <form @submit.prevent="() => handleSubmitIntention(false)" class="space-y-6 flex-grow flex flex-col">

        <div class="space-y-4">
          <label class="block text-sm text-gray-500 font-bold uppercase tracking-wider ml-1">L'Objet</label>

          <div class="space-y-1">
            <div class="relative">
              <input type="text"
                     v-model="formData.product_name"
                     @blur="touched.product_name = true"
                     placeholder="Nom du produit"
                     class="w-full px-5 py-4 border rounded-3xl text-[#1F2937] font-semibold outline-none transition-all shadow-sm bg-white"
                     :class="isNameInvalid ? 'border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50' : 'border-gray-200 focus:ring-2 focus:ring-[#5A877E]'"
                     required/>
            </div>
            <p v-if="isNameInvalid" class="text-xs text-red-500 font-medium ml-2 animate-pulse">
              Le nom doit contenir au moins 3 caractères (lettres, chiffres et espaces uniquement).
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <div class="relative">
                <input type="number"
                       v-model="formData.product_price"
                       @blur="touched.product_price = true"
                       step="0.01"
                       placeholder="Prix"
                       class="w-full px-5 py-4 border rounded-3xl text-[#1F2937] font-semibold outline-none transition-all shadow-sm bg-white"
                       :class="isPriceInvalid ? 'border-red-400 focus:ring-2 focus:ring-red-400 bg-red-50' : 'border-gray-200 focus:ring-2 focus:ring-[#5A877E]'"
                       required/>
                <div class="absolute right-5 top-1/2 transform -translate-y-1/2 text-gray-400 font-medium text-xs">
                  {{ currencyStore.currentCurrency.code }}
                </div>
              </div>
              <p v-if="isPriceInvalid" class="text-xs text-red-500 font-medium ml-2">
                Le prix doit être positif
              </p>
            </div>

            <div class="relative">
              <select v-model="formData.product_category"
                      class="w-full h-[58px] pl-5 pr-10 py-4 border border-gray-200 rounded-3xl text-[#1F2937] font-semibold focus:ring-2 focus:ring-[#5A877E] outline-none transition-all shadow-sm bg-white appearance-none"
                      required>
                <option value="" disabled>Catégorie</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
          </div>
        </div>

        <hr class="border-gray-100 my-2"/>

        <div class="space-y-4">
          <label class="block text-sm text-gray-500 font-bold uppercase tracking-wider ml-1">L'Utilité</label>

          <div class="space-y-2">
            <span class="block text-sm text-gray-800 font-medium ml-1">À quelle fréquence allez-vous l'utiliser ?</span>
            <div class="relative">
              <select v-model="formData.usage_frequency"
                      class="w-full px-5 py-4 border border-gray-200 rounded-3xl text-[#1F2937] font-semibold focus:ring-2 focus:ring-[#5A877E] outline-none transition-all shadow-sm bg-white appearance-none"
                      required>
                <option value="" disabled>Sélectionnez une fréquence</option>
                <option v-for="freq in frequencies" :key="freq" :value="freq">{{ freq }}</option>
              </select>
              <div class="absolute right-5 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <span class="block text-sm text-gray-800 font-medium ml-1">Possédez-vous déjà un article similaire ?</span>
            <div class="flex gap-3">
              <label
                  class="flex-1 flex items-center justify-center p-4 border rounded-2xl cursor-pointer transition-all"
                  :class="formData.has_similar_item === true ? 'bg-[#FEE2E2] border-red-300 text-red-600 shadow-sm' : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'">
                <input type="radio" v-model="formData.has_similar_item" :value="true" class="hidden"/>
                <span class="font-bold text-sm">Oui, j'en ai un</span>
              </label>

              <label
                  class="flex-1 flex items-center justify-center p-4 border rounded-2xl cursor-pointer transition-all"
                  :class="formData.has_similar_item === false ? 'bg-[#E1EBE8] border-[#5A877E] text-[#5A877E] shadow-sm' : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'">
                <input type="radio" v-model="formData.has_similar_item" :value="false" class="hidden"/>
                <span class="font-bold text-sm">Non, aucun</span>
              </label>
            </div>
          </div>
        </div>

        <hr class="border-gray-100 my-2"/>

        <div class="space-y-4">
          <label class="block text-sm text-gray-500 font-bold uppercase tracking-wider ml-1">Psychologie</label>

          <div class="space-y-2 bg-white p-6 border border-gray-200 rounded-3xl shadow-sm">
            <div class="flex justify-between items-end mb-4">
              <span class="block text-sm text-gray-800 font-medium">Quel est le niveau d'urgence ?</span>
              <span class="text-xl font-black text-[#5A877E]">{{ formData.urgency_level }}/5</span>
            </div>
            <input type="range" v-model="formData.urgency_level" min="1" max="5" step="1"
                   class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#5A877E]"/>
            <div class="flex justify-between text-xs text-gray-400 mt-3 font-semibold px-1">
              <span>Peut attendre</span>
              <span>Besoin Immédiat</span>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-4 pb-4">
          <button
              type="submit"
              :disabled="coachStore.loading || !isFormValid"
              class="w-full bg-[#5A877E] text-white rounded-[2rem] py-4 font-bold text-lg hover:bg-[#4a7269] transition-all active:scale-[0.98] shadow-lg shadow-[#5A877E]/20 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2 mb-4"
          >
            <span v-if="coachStore.loading && !isExtracting" class="flex items-center gap-3">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Vérification...
            </span>
            <span v-else class="flex items-center gap-2">
              Passer à l'interrogatoire
              <div class="bg-white/20 rounded-full p-1 ml-1">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </span>
          </button>
        </div>
      </form>
    </div>

    <!-- Modale d'Erreur IA (bien insérée DANS la balise racine) -->
    <div v-if="showErrorModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4 transition-opacity">
      <div class="bg-white p-6 rounded-[2rem] w-full max-w-sm text-center shadow-2xl border border-gray-100">
        <!-- Icône... -->
        <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <h3 class="font-bold text-xl text-gray-900 mb-2">Saisie Incohérente</h3>
        <p class="text-gray-500 text-sm mb-8 leading-relaxed">{{ errorMessage }}</p>

        <!-- Boutons d'actions -->
        <div class="flex flex-col gap-3">
          <button @click="showErrorModal = false" class="w-full py-3.5 rounded-xl bg-[#5A877E] font-bold text-white hover:bg-[#4a7269] transition-colors shadow-sm">
            Corriger ma saisie
          </button>
          <button @click="forceSubmit" class="w-full py-3.5 rounded-xl bg-red-50 font-bold text-red-600 hover:bg-red-100 transition-colors">
            Continuer quand même
          </button>
        </div>
      </div>
    </div>

  </div> <!-- Fermeture Correcte de la balise racine -->
</template>

<script setup>
import {ref, reactive, watch, computed} from 'vue';
import {useRouter} from 'vue-router';
import {useCoachStore} from '@/stores/coach.js';
import {useCurrencyStore} from '@/stores/currency';

const isExtracting = ref(false);
const currencyStore = useCurrencyStore();
const router = useRouter();
const coachStore = useCoachStore();
const showErrorModal = ref(false);
const errorMessage = ref('');
const step = ref(1);
const imagePreview = ref(null);
const selectedFile = ref(null);

const categories = [
  'Smartphones', 'Ordinateurs & Informatique', 'Jeux vidéo & Consoles',
  'Vêtements & Mode', 'Maison & Décoration', 'Électroménager',
  'Beauté & Santé', 'Sport & Loisirs', 'Alimentation & Sorties', 'Autre'
];

const frequencies = ['Quotidien', 'Hebdomadaire', 'Mensuel', 'Rarement'];

const formData = reactive({
  product_name: '',
  product_price: '',
  product_category: '',
  usage_frequency: '',
  has_similar_item: null, // Boolean (true/false)
  urgency_level: 3 // Slider default
});

const isValidProductName = (name) => {
  const regex = /^[a-zA-ZÀ-ÿ0-9\s]{3,}$/;
  return regex.test(name.trim());
};

const touched = reactive({
  product_name: false,
  product_price: false
});

const isNameInvalid = computed(() => {
  return touched.product_name && formData.product_name.trim().length === 0;
});

const isPriceInvalid = computed(() => {
  if (!touched.product_price) return false;
  const price = parseFloat(formData.product_price);
  return isNaN(price) || price <= 0;
});

const isFormValid = computed(() => {
  return formData.product_name.trim() !== '' &&
      formData.product_price !== '' &&
      formData.product_price > 0 &&
      formData.product_category !== '' &&
      formData.usage_frequency !== '' &&
      formData.has_similar_item !== null;
});

watch(() => coachStore.extractedData, (newData) => {
  if (newData) {
    formData.product_name = newData.product_name || '';
    formData.product_price = newData.product_price || '';
    if (categories.includes(newData.product_category)) {
      formData.product_category = newData.product_category;
    } else if (newData.product_category) {
      formData.product_category = 'Autre';
    }
  }
}, {deep: true});

const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  selectedFile.value = file;
  imagePreview.value = URL.createObjectURL(file);
  step.value = 2;
  isExtracting.value = true;
  try {
    await coachStore.extractFromImage(file);
  } catch (err) {
    console.error("Erreur d'extraction :", err);
  } finally {
    isExtracting.value = false;
  }
};

const goToManualEntry = () => {
  step.value = 2;
};

const resetToStep1 = () => {
  step.value = 1;
  imagePreview.value = null;
  selectedFile.value = null;
  formData.product_name = '';
  formData.product_price = '';
  formData.product_category = '';
  formData.usage_frequency = '';
  formData.has_similar_item = null;
  formData.urgency_level = 3;
};

// Extrait pour corriger le problème de portée (scoping)
const handleSubmitIntention = async (bypassed = false) => {
  try {
    const payload = {
      product_name: formData.product_name,
      product_price: parseFloat(formData.product_price),
      product_category: formData.product_category,
      usage_frequency: formData.usage_frequency,
      has_similar_item: formData.has_similar_item,
      urgency_level: parseInt(formData.urgency_level),
      is_incoherent_bypassed: bypassed
    };

    await coachStore.createPurchaseIntention(payload);
    router.push({name: 'reflection', params: {id: coachStore.currentIntentionId}});
  } catch (err) {
    console.error("Erreur lors de l'enregistrement :", err);
    errorMessage.value = coachStore.error || "Ces informations semblent incohérentes. Veuillez vérifier votre saisie.";
    showErrorModal.value = true;
  }
};

// Placée DANS l'espace setup racine
const forceSubmit = () => {
  showErrorModal.value = false;
  handleSubmitIntention(true);
};
</script>

<style scoped>
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #5A877E;
  cursor: pointer;
  margin-top: -6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  background: #E5E7EB;
  border-radius: 4px;
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