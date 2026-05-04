<template>
  <div class="min-h-screen bg-[#F8F6F2] px-6 py-8 font-sans pb-24">
    <header class="mb-8">
      <h1 class="text-3xl font-serif font-bold text-gray-900 tracking-tight">Support Tickets (Admin)</h1>
      <p class="text-sm text-gray-500 mt-1">Gérez les retours et problèmes des utilisateurs.</p>
    </header>

    <div v-if="isLoading" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#5A877E]"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-if="feedbacks.length === 0" class="text-center text-gray-500 py-10">
        Aucun message de support pour le moment.
      </div>

      <!-- Ticket Cards -->
      <div
          v-for="ticket in feedbacks"
          :key="ticket.id"
          class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100"
      >
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-bold text-gray-900 text-lg">{{ ticket.subject || 'Sans objet' }}</h3>
            <p class="text-xs text-[#5A877E] font-medium">{{ ticket.user_email }}</p>
          </div>
          <span class="text-xs text-gray-400 font-medium">
            {{ new Date(ticket.created_at).toLocaleDateString('fr-FR') }}
          </span>
        </div>

        <div class="mt-3 bg-gray-50 p-3 rounded-xl border border-gray-100">
          <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ ticket.comment }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const feedbacks = ref([]);
const isLoading = ref(true);

onMounted(async () => {
  try {
    const response = await api.get('/admin-api/feedbacks/');
    feedbacks.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des tickets :", error);
    alert("Impossible de charger les tickets. Vérifiez que vous avez les droits d'administration.");
  } finally {
    isLoading.value = false;
  }
});
</script>