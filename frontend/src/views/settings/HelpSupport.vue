<template>
  <!-- Full page wrapper centering the content on large screens -->
  <div class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] flex justify-center">

    <!-- Responsive inner container -->
    <div class="w-full max-w-3xl px-4 sm:px-6 md:px-8 py-6 sm:py-8 lg:py-10 flex flex-col">

      <!-- Header Section -->
      <SettingsPageHeader title="Aide et support"/>

      <!-- Main Content -->
      <main class="flex-grow flex flex-col">

        <!-- Intro Text -->
        <div class="mb-8 sm:mb-10 px-1 sm:px-2">
          <h2 class="text-[20px] sm:text-[22px] font-bold text-[#000000] mb-3 leading-snug">
            Comment pouvons-nous vous aider ?
          </h2>
          <p class="text-[#9CA3AF] text-[15px] sm:text-[16px] leading-relaxed max-w-lg">
            Remplissez le formulaire ci-dessous et notre équipe vous répondra dans les plus brefs délais.
          </p>
        </div>

        <!-- Contact Form -->
        <form @submit.prevent="submitForm" class="flex flex-col gap-6 sm:gap-8 px-1 sm:px-2">

          <!-- Objet Field -->
          <div class="flex flex-col gap-3">
            <label for="objet" class="text-[17px] sm:text-[18px] font-bold text-[#000000]">
              Objet
            </label>
            <input
                id="objet"
                type="text"
                v-model="form.subject"
                placeholder="Exp : Problème de connexion"
                class="w-full bg-[#FFFFFF] border border-[#D9D9D9] rounded-[15px] px-5 py-4 text-[15px] sm:text-[16px] text-[#000000] placeholder-[#9CA3AF] focus:outline-none focus:ring-2 focus:ring-[#5B8C85]/30 focus:border-[#5B8C85] transition-all"
                required
            />
          </div>

          <!-- Message Field -->
          <div class="flex flex-col gap-3">
            <label for="message" class="text-[17px] sm:text-[18px] font-bold text-[#000000]">
              Message
            </label>
            <textarea
                id="message"
                v-model="form.message"
                rows="6"
                placeholder="Décrivez votre problème en détail ..."
                class="w-full bg-[#FFFFFF] border border-[#D9D9D9] rounded-[15px] px-5 py-4 text-[15px] sm:text-[16px] text-[#000000] placeholder-[#9CA3AF] focus:outline-none focus:ring-2 focus:ring-[#5B8C85]/30 focus:border-[#5B8C85] transition-all resize-none"
                required
            ></textarea>
          </div>

          <!-- Submit Button -->
          <div class="mt-8 sm:mt-12 flex justify-center">
            <button
                type="submit"
                :disabled="isSubmitting"
                class="bg-[#5B8C85] hover:bg-[#4a736d] text-[#FFFFFF] text-[20px] sm:text-[22px] font-medium px-12 sm:px-16 py-4 rounded-[24px] sm:rounded-[30px] w-full sm:w-auto min-w-[280px] transition-colors shadow-sm focus:outline-none focus:ring-4 focus:ring-[#5B8C85]/20 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              <!-- Optional: Add a loading state text like {{ isSubmitting ? 'Envoi...' : 'Envoyer' }} -->
              Envoyer
            </button>
          </div>

        </form>

      </main>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'

import api from '@/services/api'

import SettingsPageHeader from '@/components/shared/SettingsPageHeader.vue'

// Form state
const form = ref({
  subject: '',
  message: ''
})

const isSubmitting = ref(false)


const submitForm = async () => {
  if (!form.value.subject || !form.value.message) return;

  isSubmitting.value = true;

  try {
    // Map "message" to "comment". Passing "subject" for the backend email dispatcher.
    const payload = {
      rating: 5,
      comment: form.value.message,
      subject: form.value.subject
    }

    // Call the backend endpoint
    await api.post('/app-feedback/', payload)

    // Display success popup
    alert('Votre message a   envoy  avec succ s !')

    // Clear form
    form.value.subject = ''
    form.value.message = ''
  } catch (error) {
    console.error('Erreur lors de la soumission du formulaire:', error)
    alert('Une erreur est survenue lors de l\'envoi de votre message.')
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
/*
  Ensures DM Sans is loaded for this component.
  If you already import this globally in your main.css or index.html, you can safely remove this block.
*/
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
</style>