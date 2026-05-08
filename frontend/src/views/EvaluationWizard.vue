<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col font-sans">
    <div class="relative z-10 border-b border-gray-100 bg-white/50">
      <header class="px-6 py-5 flex justify-center items-center relative">
        <h1 class="text-xl font-bold text-gray-900 text-center">
          <span v-if="currentStep === 'QUESTIONS'">Interrogatoire</span>
          <span v-else-if="currentStep === 'LOADING'">Vrai Besoin</span>
          <span v-else>Décision finale</span>
        </h1>
        <button
          @click="showCancelModal = true"
          class="absolute right-4 p-2 text-gray-400 rounded-full hover:text-gray-700 hover:bg-gray-200 active:bg-gray-300 transition-all"
          aria-label="Fermer"
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
      </header>

      <div
        v-if="currentStep === 'QUESTIONS'"
        class="px-6 pb-4 w-full max-w-lg mx-auto"
      >
        <div class="flex justify-between items-center mb-2">
          <span
            class="text-xs font-bold text-[#5A877E] uppercase tracking-wider"
          >
            Question {{ activeQuestionIndex + 1 }} sur 3
          </span>
        </div>
        <div class="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-full bg-[#5A877E] transition-all duration-500 ease-out rounded-full"
            :style="{ width: `${((activeQuestionIndex + 1) / 3) * 100}%` }"
          ></div>
        </div>
      </div>
    </div>

    <main
      v-if="currentStep === 'GENERATING_QUESTIONS'"
      class="flex-grow flex flex-col items-center justify-center px-6"
    >
      <div class="relative w-24 h-24 mb-8">
        <div
          class="absolute inset-0 border-4 border-[#E1EBE8] rounded-full"
        ></div>
        <div
          class="absolute inset-0 border-4 border-[#5A877E] rounded-full border-t-transparent animate-spin"
        ></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <svg
            class="w-8 h-8 text-[#5A877E] animate-pulse"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>
      </div>
      <h2 class="text-2xl font-serif font-bold text-gray-900 mb-2">
        Préparation du coach...
      </h2>
      <p class="text-gray-500 text-center text-sm px-4 leading-relaxed">
        L'IA analyse votre profil et conçoit un interrogatoire sur-mesure.
      </p>
    </main>

    <main
      v-else-if="currentStep === 'QUESTIONS'"
      class="flex-grow flex flex-col items-center pt-8 px-4 pb-6"
    >
      <div v-if="currentQuestion" class="w-full max-w-lg flex flex-col h-full">
        <div class="space-y-6 flex-grow">
          <div
            class="bg-white px-8 py-10 rounded-[2rem] shadow-md border border-gray-100 text-center flex flex-col justify-center min-h-[140px]"
          >
            <h2
              class="text-xl sm:text-2xl font-serif font-medium text-[#1F2937] leading-relaxed max-w-md mx-auto"
            >
              {{ currentQuestion.question_text }}
            </h2>
          </div>

          <div class="space-y-4">
            <button
              v-for="(option, idx) in currentQuestion.ai_options"
              :key="idx"
              @click="selectOption(option)"
              class="w-full p-5 rounded-2xl text-base font-medium transition-all duration-200 ease-out text-left border shadow-[0_2px_8px_rgba(0,0,0,0.04)]"
              :class="
                selectedAnswer === option
                  ? 'border-[#5A877E] bg-[#E1EBE8] text-[#5A877E] shadow-md ring-2 ring-[#5A877E]/20'
                  : 'border-gray-100 bg-white text-gray-700 hover:border-[#5A877E]/40 hover:bg-[#F8FAFA] hover:shadow-md'
              "
            >
              {{ option }}
            </button>

            <div v-if="showCustomInput" class="w-full">
              <input
                v-model="customAnswerText"
                type="text"
                placeholder="Précisez votre pensée..."
                class="w-full p-5 border rounded-2xl shadow-[0_2px_8px_rgba(0,0,0,0.04)] focus:outline-none transition-all duration-200"
                :class="
                  customAnswerText.trim()
                    ? 'border-[#5A877E] ring-4 ring-[#E1EBE8]/50 bg-white'
                    : 'border-gray-200 focus:border-[#5A877E] focus:ring-4 focus:ring-[#E1EBE8]/50'
                "
                @keyup.enter="goNext"
                autofocus
              />
            </div>
            <button
              v-else
              @click="enableCustomInput"
              class="w-full p-5 rounded-2xl text-base font-medium bg-white border border-gray-100 text-gray-500 shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:border-gray-300 hover:bg-gray-50 hover:shadow-md transition-all duration-200 ease-out text-left"
            >
              Autre (saisir une réponse)
            </button>
          </div>
        </div>

        <div class="flex gap-3 pt-6 mt-6 border-t border-gray-100">
          <button
            @click="goPrevious"
            :disabled="activeQuestionIndex === 0"
            class="flex-1 px-6 py-2 rounded-2xl font-medium transition-all bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 disabled:opacity-40 disabled:hover:bg-white disabled:cursor-not-allowed"
          >
            Précédent
          </button>
          <button
            @click="goNext"
            :disabled="!currentAnswerValid"
            class="flex-1 py-2 px-6 rounded-2xl font-medium transition-all bg-[#5A877E] text-white shadow-sm hover:bg-[#4a7269] hover:shadow-md active:scale-[0.98] disabled:opacity-50 disabled:active:scale-100 disabled:hover:bg-[#5A877E] disabled:cursor-not-allowed"
          >
            {{ activeQuestionIndex === 2 ? "Obtenir mon verdict" : "Suivant" }}
          </button>
        </div>
      </div>
    </main>

    <main
      v-else-if="currentStep === 'LOADING'"
      class="flex-grow flex flex-col items-center justify-center px-6"
    >
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Analyse en cours...</h2>
      <div
        class="w-full max-w-sm bg-white rounded-full h-8 overflow-hidden shadow-sm border border-gray-100 p-1"
      >
        <div
          class="bg-gradient-to-r from-[#5A877E] to-[#80E8C4] h-full rounded-full transition-all duration-300 ease-out"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
      <p class="mt-4 text-xl font-bold text-gray-800">
        {{ progressPercentage }}%
      </p>
    </main>

    <main
      v-else-if="currentStep === 'RESULT'"
      class="flex-grow flex flex-col px-4 pb-8"
    >
      <div
        class="flex items-center gap-4 bg-white p-4 rounded-2xl shadow-sm mb-6"
      >
        <div
          class="w-16 h-16 bg-gray-50 rounded-xl overflow-hidden flex-shrink-0 flex items-center justify-center border border-gray-100"
        >
          <img
            v-if="intentionData.product_image"
            :src="intentionData.product_image"
            class="w-full h-full object-cover"
            alt="Produit"
          />
          <svg
            v-else
            class="w-8 h-8 text-gray-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
        </div>
        <div>
          <h3 class="font-bold text-lg text-gray-900">
            {{ intentionData.product_name }}
          </h3>
          <p class="text-gray-400 font-semibold">
            {{ intentionData.product_price }}
            {{ currencyStore.currentCurrency.code }}
          </p>
        </div>
      </div>

      <div
        class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 mb-8 flex flex-col"
      >
        <h4 class="font-bold text-lg mb-4 text-gray-800 text-center">
          Verdict final
        </h4>

        <div
          v-if="intentionData.ai_verdict"
          class="w-fit mx-auto mb-5 flex items-center gap-3 px-6 py-3 rounded-2xl border"
          :class="{
            'bg-[#FEE2E2]/50 border-[#FEE2E2] text-[#EF4444]':
              intentionData.ai_verdict === 'BUY',
            'bg-[#FEF3C7]/50 border-[#FEF3C7] text-[#D97706]':
              intentionData.ai_verdict === 'CALM',
            'bg-[#E1EBE8]/50 border-[#E1EBE8] text-[#5A877E]':
              intentionData.ai_verdict === 'ABANDON',
          }"
        >
          <svg
            v-if="intentionData.ai_verdict === 'BUY'"
            class="w-6 h-6 flex-shrink-0"
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
          <svg
            v-else-if="intentionData.ai_verdict === 'CALM'"
            class="w-6 h-6 flex-shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <svg
            v-else-if="intentionData.ai_verdict === 'ABANDON'"
            class="w-6 h-6 flex-shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>

          <span class="font-bold text-base tracking-wide flex-grow">
            {{ formatVerdict(intentionData.ai_verdict) }}
          </span>
        </div>

        <p
          class="text-gray-600 leading-relaxed whitespace-pre-wrap text-center"
        >
          {{ intentionData.ai_reasoning }}
        </p>
      </div>

      <div class="space-y-4 mt-auto pt-3">
        <p class="text-center text-sm text-gray-400 mb-4">
          Quelle est ta décision finale ?
        </p>

        <button
          @click="triggerAction('BUY')"
          class="relative w-full flex flex-col items-center py-4 rounded-2xl transition-all duration-200"
          :class="[
            intentionData.ai_verdict === 'BUY'
              ? 'bg-[#FEE2E2] ring-4 ring-red-100 border-2 border-red-400 shadow-md scale-[1.02]'
              : 'bg-[#FEE2E2] hover:bg-red-200 border-2 border-transparent',
          ]"
        >
          <span
            v-if="intentionData.ai_verdict === 'BUY'"
            class="absolute -top-3 left-1/2 -translate-x-1/2 bg-white text-[#EF4444] border-2 border-[#FEE2E2] text-[10px] font-extrabold uppercase tracking-widest py-1 px-4 rounded-full shadow-sm whitespace-nowrap"
          >
            Recommandé
          </span>
          <span class="font-bold text-[#EF4444] text-lg">Acheter</span>
          <span class="text-xs text-red-400">J'en ai vraiment besoin</span>
        </button>

        <button
          @click="triggerAction('CALM')"
          class="relative w-full flex flex-col items-center py-4 rounded-2xl transition-all duration-200"
          :class="[
            intentionData.ai_verdict === 'CALM'
              ? 'bg-[#FEF3C7] ring-4 ring-yellow-100 border-2 border-yellow-400 shadow-md scale-[1.02]'
              : 'bg-[#FEF3C7] hover:bg-yellow-200 border-2 border-transparent',
          ]"
        >
          <span
            v-if="intentionData.ai_verdict === 'CALM'"
            class="absolute -top-3 left-1/2 -translate-x-1/2 bg-white text-[#D97706] border-2 border-[#FEF3C7] text-[10px] font-extrabold uppercase tracking-widest py-1 px-4 rounded-full shadow-sm whitespace-nowrap"
          >
            Recommandé
          </span>
          <span class="font-bold text-[#D97706] text-lg">Attendre</span>
          <span class="text-xs text-yellow-500"
            >Réfléchir {{ cooldownHours }}h de plus</span
          >
        </button>

        <button
          @click="triggerAction('ABANDON')"
          class="relative w-full flex flex-col items-center justify-center py-4 rounded-2xl transition-all duration-200"
          :class="[
            intentionData.ai_verdict === 'ABANDON'
              ? 'bg-[#E1EBE8] ring-4 ring-[#E1EBE8]/60 border-2 border-[#5A877E] shadow-md scale-[1.02]'
              : 'bg-[#E1EBE8] hover:bg-[#cbe3dc] border-2 border-transparent',
          ]"
        >
          <span
            v-if="intentionData.ai_verdict === 'ABANDON'"
            class="absolute -top-3 left-1/2 -translate-x-1/2 bg-white text-[#5A877E] border-2 border-[#E1EBE8] text-[10px] font-extrabold uppercase tracking-widest py-1 px-4 rounded-full shadow-sm whitespace-nowrap"
          >
            Recommandé
          </span>
          <span class="font-bold text-[#5A877E] text-lg">Abandonner</span>
          <span class="text-xs text-[#5A877E]/70">Je sauve mon budget</span>
        </button>
      </div>
    </main>

    <div
      v-if="showCancelModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4 transition-opacity"
    >
      <div
        class="bg-white p-6 rounded-[2rem] w-full max-w-sm text-center shadow-2xl border border-gray-100"
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
          Annuler l'analyse ?
        </h3>
        <p class="text-gray-500 text-sm mb-8 leading-relaxed">
          Si tu quittes maintenant, toutes les données de cette réflexion seront
          perdues.
        </p>
        <div class="flex gap-3">
          <button
            @click="showCancelModal = false"
            class="flex-1 py-3.5 rounded-xl bg-gray-100 font-bold text-gray-700 hover:bg-gray-200 transition-colors"
          >
            Continuer
          </button>
          <button
            @click="executeCancel"
            class="flex-1 py-3.5 rounded-xl bg-[#FEE2E2] font-bold text-[#EF4444] hover:bg-red-200 transition-colors"
          >
            Oui, quitter
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4"
    >
      <div
        class="bg-white p-6 rounded-3xl w-full max-w-sm text-center shadow-xl border border-gray-100"
      >
        <div
          class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
          :class="modalContent.iconBg"
        >
          <svg
            class="w-8 h-8"
            :class="modalContent.iconColor"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              :d="modalContent.iconPath"
            />
          </svg>
        </div>
        <h3 class="font-bold text-xl mb-2 text-gray-900">
          {{ modalContent.title }}
        </h3>
        <p class="text-gray-500 text-sm mb-6">{{ modalContent.description }}</p>
        <div class="flex gap-3">
          <button
            @click="showModal = false"
            class="flex-1 py-3 rounded-xl bg-gray-100 font-semibold text-gray-600 hover:bg-gray-200"
          >
            Annuler
          </button>
          <button
            @click="submitFinalDecision"
            class="flex-1 py-3 rounded-xl font-semibold text-white shadow-sm bg-[#5A877E]"
            :class="modalContent.btnColor"
          >
            Confirmer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { useCurrencyStore } from "@/stores/currency";
import { useAuthStore } from "@/stores/auth.js";

const authStore = useAuthStore();
const currencyStore = useCurrencyStore();
const route = useRoute();
const router = useRouter();
const intentionId = route.params.id;

const cooldownHours = computed(() => {
  return authStore.user?.cooldown_preference || 24;
});

const showModal = ref(false);
const pendingAction = ref(null);

const modalContent = computed(() => {
  if (pendingAction.value === "BUY") {
    return {
      title: "Valider l'achat ?",
      description:
        "Es-tu sûr que cet achat est réellement indispensable aujourd'hui ?",
      iconBg: "bg-red-50",
      iconColor: "text-red-500",
      btnColor: "bg-red-500 hover:bg-red-600",
      iconPath:
        "M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z",
    };
  } else if (pendingAction.value === "CALM") {
    return {
      title: "Mettre en pause ?",
      description: `L'analyse sera suspendue pendant ${cooldownHours.value} heures pour te laisser le temps de la réflexion.`,
      iconBg: "bg-yellow-50",
      iconColor: "text-yellow-500",
      btnColor: "bg-yellow-500 hover:bg-yellow-600",
      iconPath: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    };
  } else {
    return {
      title: "Abandonner cet achat ?",
      description:
        "Excellent choix ! Ton budget te remerciera de cette décision rationnelle.",
      iconBg: "bg-[#E1EBE8]",
      iconColor: "text-[#5A877E]",
      btnColor: "bg-[#5A877E hover:bg-[#4a7269]",
      iconPath: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    };
  }
});

const currentStep = ref("INITIALIZING");
const questions = ref([]);
const activeQuestionIndex = ref(0);
const userAnswers = ref([]);
const intentionData = ref({});
const progressPercentage = ref(0);
const showCancelModal = ref(false);

const showCustomInput = ref(false);
const customAnswerText = ref("");
const selectedAnswer = ref("");

const formatVerdict = (verdict) => {
  const labels = {
    BUY: "Acheter",
    CALM: "Attendre",
    ABANDON: "Abandonner",
  };
  return labels[verdict] || verdict;
};

onMounted(async () => {
  try {
    const intentionRes = await api.get(`/purchase-intentions/${intentionId}/`);
    intentionData.value = intentionRes.data;

    if (intentionData.value.ai_verdict) {
      currentStep.value = "RESULT";
    } else {
      currentStep.value = "GENERATING_QUESTIONS";
      const response = await api.post(
        `/purchase-intentions/${intentionId}/generate-questions/`,
      );
      questions.value = response.data;
      currentStep.value = "QUESTIONS";
    }
  } catch (error) {
    console.error("Erreur lors de l'initialisation du wizard", error);
  }
});

const currentQuestion = computed(
  () => questions.value[activeQuestionIndex.value],
);

const currentAnswerValid = computed(() => {
  if (showCustomInput.value) return customAnswerText.value.trim().length > 0;
  return selectedAnswer.value.length > 0;
});

const selectOption = (option) => {
  selectedAnswer.value = option;
  showCustomInput.value = false;
  customAnswerText.value = "";
};

const enableCustomInput = () => {
  showCustomInput.value = true;
  selectedAnswer.value = "";
};

const restoreAnswerState = () => {
  const saved = userAnswers.value[activeQuestionIndex.value];
  if (saved) {
    const isAiOption = questions.value[
      activeQuestionIndex.value
    ]?.ai_options.includes(saved.answer);
    if (isAiOption) {
      selectedAnswer.value = saved.answer;
      showCustomInput.value = false;
      customAnswerText.value = "";
    } else {
      showCustomInput.value = true;
      customAnswerText.value = saved.answer;
      selectedAnswer.value = "";
    }
  } else {
    selectedAnswer.value = "";
    showCustomInput.value = false;
    customAnswerText.value = "";
  }
};

const goNext = async () => {
  if (!currentAnswerValid.value) return;

  const finalAnswer = showCustomInput.value
    ? customAnswerText.value.trim()
    : selectedAnswer.value;

  // Enregistrer ou écraser la réponse
  userAnswers.value[activeQuestionIndex.value] = {
    id: currentQuestion.value.id,
    answer: finalAnswer,
  };

  if (activeQuestionIndex.value < 2) {
    activeQuestionIndex.value++;
    restoreAnswerState();
  } else {
    currentStep.value = "LOADING";
    startProgressAnimation();
    await fetchVerdict();
  }
};

const goPrevious = () => {
  if (activeQuestionIndex.value > 0) {
    activeQuestionIndex.value--;
    restoreAnswerState();
  }
};

let progressInterval;
const startProgressAnimation = () => {
  progressPercentage.value = 0;
  progressInterval = setInterval(() => {
    if (progressPercentage.value < 90) {
      progressPercentage.value += Math.floor(Math.random() * 5) + 2;
    }
  }, 200);
};

const fetchVerdict = async () => {
  try {
    const response = await api.post(
      `/purchase-intentions/${intentionId}/verdict/`,
      {
        answers: userAnswers.value,
      },
    );

    clearInterval(progressInterval);
    progressPercentage.value = 100;
    intentionData.value = response.data;

    setTimeout(() => {
      currentStep.value = "RESULT";
    }, 500);
  } catch (error) {
    clearInterval(progressInterval);
    alert("Une erreur est survenue lors de l'analyse.");
    currentStep.value = "QUESTIONS";
  }
};

const triggerAction = (decisionCode) => {
  pendingAction.value = decisionCode;
  showModal.value = true;
};

const submitFinalDecision = async () => {
  try {
    await api.patch(`/purchase-intentions/${intentionId}/final-decision/`, {
      user_final_decision: pendingAction.value,
    });
    showModal.value = false;
    router.push({ name: "dashboard" });
  } catch (error) {
    console.error("Erreur sauvegarde décision", error);
  }
};

const executeCancel = () => {
  showCancelModal.value = false;
  router.push({ name: "dashboard" });
};
</script>
