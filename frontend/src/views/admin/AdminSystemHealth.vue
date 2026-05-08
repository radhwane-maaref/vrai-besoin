<template>
  <div class="h-screen bg-[#F8F6F2] font-sans flex flex-col overflow-hidden">
    <header class="w-full max-w-5xl mx-auto px-4 pt-8 pb-4 shrink-0">
      <h1 class="text-2xl font-serif font-bold text-gray-900">
        Suivi des anomalies
      </h1>
    </header>

    <div class="flex-1 overflow-y-auto pb-28">
      <div class="w-full max-w-5xl mx-auto px-4">
        <div
          class="bg-white p-3 rounded-3xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-3 mb-6 relative z-10"
        >
          <input
            v-model="filters.search"
            @keyup.enter="loadData"
            type="text"
            placeholder="Rechercher une erreur..."
            class="flex-1 px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl text-sm focus:ring-2 focus:ring-[#5A877E]/20 focus:border-[#5A877E] outline-none transition-all"
          />
          <div class="w-full md:w-48">
            <CustomSelect
              v-model="filters.status"
              :options="statusOptions"
              placeholder="Tous les statuts"
              sizeClass="py-3 h-[46px]"
              roundedClass="rounded-2xl"
              @change="loadData"
            />
          </div>
        </div>

        <div v-if="adminStore.loading" class="flex justify-center py-12">
          <div
            class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#5A877E]"
          ></div>
        </div>

        <div
          v-else-if="groupedErrors.length === 0"
          class="text-center py-16 bg-white rounded-3xl border border-dashed border-gray-200"
        >
          <p class="text-gray-400 font-medium text-sm">
            Aucune anomalie trouvée.
          </p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="group in groupedErrors"
            :key="group.latest.id"
            @click="openDetails(group.latest)"
            class="bg-white p-5 rounded-3xl border border-gray-100 hover:border-[#5A877E]/40 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
          >
            <div class="flex justify-between items-start mb-3">
              <div class="flex items-center gap-2 flex-wrap">
                <span
                  :class="statusColors[group.latest.status]"
                  class="text-[10px] font-bold px-2.5 py-1 rounded-lg uppercase tracking-wider"
                >
                  {{ translateStatus(group.latest.status) }}
                </span>
                <span
                  v-if="group.latest.priority === 'CRITICAL'"
                  class="text-[10px] font-bold px-2.5 py-1 bg-red-100 text-red-600 rounded-lg uppercase"
                >
                  Critique
                </span>
              </div>
              <span class="text-[10px] text-gray-400 font-medium">{{
                timeAgo(group.latest.created_at)
              }}</span>
            </div>
            <h3
              class="text-sm font-medium text-gray-800 line-clamp-2 group-hover:text-[#5A877E] transition-colors leading-relaxed"
            >
              {{ group.latest.error_message }}
            </h3>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedLog" class="fixed inset-0 z-[70] flex justify-end">
      <div
        class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity"
        @click="closeDetails"
      ></div>

      <div
        class="relative w-full max-w-md bg-white h-full shadow-2xl flex flex-col animate-slide-in"
      >
        <div
          class="p-6 border-b border-gray-100 flex justify-between items-center shrink-0"
        >
          <div>
            <h2 class="text-xl font-serif font-bold text-gray-900">
              Détails anomalie
            </h2>
            <p
              class="text-[10px] text-gray-400 mt-1 uppercase tracking-widest font-bold"
            >
              Signalé le
              {{ new Date(selectedLog.created_at).toLocaleDateString("fr-FR") }}
            </p>
          </div>
          <button
            @click="closeDetails"
            class="w-10 h-10 rounded-full bg-gray-50 hover:bg-gray-100 flex items-center justify-center text-gray-500 transition-colors"
          >
            ✕
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label
                class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-1"
                >Statut</label
              >
              <CustomSelect
                v-model="editForm.status"
                :options="statusOptions"
                sizeClass="h-12"
                roundedClass="rounded-xl"
              />
            </div>
            <div class="space-y-2">
              <label
                class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-1"
                >Sévérité</label
              >
              <CustomSelect
                v-model="editForm.priority"
                :options="priorityOptions"
                sizeClass="h-12"
                roundedClass="rounded-xl"
              />
            </div>
          </div>

          <section class="space-y-2">
            <label
              class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-1"
              >Description système</label
            >
            <div class="bg-red-50/50 border border-red-100/50 p-4 rounded-2xl">
              <p
                class="text-xs font-mono text-red-700 leading-relaxed break-words"
              >
                {{ selectedLog.error_message }}
              </p>
            </div>
          </section>

          <section class="space-y-2">
            <label
              class="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-1"
              >Notes</label
            >
            <textarea
              v-model="editForm.note"
              class="w-full text-sm border border-gray-100 rounded-2xl focus:ring-2 focus:ring-[#5A877E]/10 focus:border-[#5A877E] p-4 bg-[#F8F6F2]/50 outline-none transition-all resize-none min-h-[140px]"
              placeholder="Expliquez ici la cause ou la résolution..."
            ></textarea>
          </section>

          <details
            v-if="selectedLog.stack_trace"
            class="group border border-gray-100 rounded-2xl overflow-hidden"
          >
            <summary
              class="list-none cursor-pointer p-4 text-[10px] font-bold text-gray-500 uppercase flex justify-between items-center hover:bg-gray-50 transition-colors"
            >
              Rapport technique complet
              <span
                class="group-open:rotate-180 transition-transform text-gray-300"
                >▼</span
              >
            </summary>
            <div class="p-4 bg-gray-900 overflow-x-auto">
              <pre class="text-[10px] font-mono text-green-400 leading-tight">{{
                selectedLog.stack_trace
              }}</pre>
            </div>
          </details>
        </div>

        <div class="p-6 border-t border-gray-100 bg-white shrink-0">
          <button
            @click="handleSave"
            class="w-full bg-[#5A877E] text-white py-4 rounded-2xl font-bold text-sm hover:bg-[#4b7269] transition-all shadow-lg shadow-[#5A877E]/20 flex justify-center items-center gap-2"
          >
            Sauvegarder les modifications
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showNoteModal"
      class="fixed inset-0 z-[100] flex items-center justify-center px-4"
    >
      <div
        class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm"
        @click="showNoteModal = false"
      ></div>
      <div
        class="bg-white rounded-[2rem] p-8 w-full max-w-sm relative z-10 shadow-2xl animate-pop"
      >
        <div
          class="w-14 h-14 rounded-full bg-orange-100 flex items-center justify-center mb-6"
        >
          <svg
            class="w-7 h-7 text-orange-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2.5"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-3">Note manquante</h3>
        <p class="text-sm text-gray-500 mb-8 leading-relaxed">
          Vous enregistrez une modification sans ajouter de note de résolution.
          Est-ce volontaire ?
        </p>
        <div class="flex gap-3">
          <button
            @click="showNoteModal = false"
            class="flex-1 py-3.5 bg-gray-100 text-gray-600 rounded-xl font-bold text-xs transition-colors"
          >
            Retour
          </button>
          <button
            @click="confirmSave"
            class="flex-1 py-3.5 bg-[#5A877E] text-white rounded-xl font-bold text-xs transition-colors"
          >
            Confirmer
          </button>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div
        v-if="toastMsg"
        class="fixed bottom-24 left-1/2 -translate-x-1/2 z-[110] bg-[#1F2937] text-white px-6 py-3 rounded-full text-xs font-bold shadow-2xl flex items-center gap-3"
      >
        <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
        {{ toastMsg }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useAdminStore } from "@/stores/admin";
import CustomSelect from "@/components/shared/CustomSelect.vue";

const adminStore = useAdminStore();
const selectedLog = ref(null);
const toastMsg = ref("");
const showNoteModal = ref(false);

// Formulaire d'édition temporaire
const editForm = reactive({
  status: "",
  priority: "",
  note: "",
});

// Dictionnaires de traduction
const statusLabels = {
  NEW: "Nouveau",
  TRIAGED: "En analyse",
  IN_PROGRESS: "En cours",
  FIXED: "Corrigé",
  VERIFIED: "Vérifié",
  CLOSED: "Fermé",
};

const priorityLabels = {
  LOW: "Basse",
  MEDIUM: "Moyenne",
  HIGH: "Haute",
  CRITICAL: "Critique",
};

// Options formatées pour CustomSelect
const statusOptions = [
  { value: "", label: "Tous les statuts" },
  ...Object.entries(statusLabels).map(([v, l]) => ({ value: v, label: l })),
];

const priorityOptions = [
  { value: "", label: "Toutes priorités" },
  ...Object.entries(priorityLabels).map(([v, l]) => ({ value: v, label: l })),
];

const filters = reactive({ status: "", priority: "", search: "" });

const statusColors = {
  NEW: "bg-purple-50 text-purple-600",
  TRIAGED: "bg-blue-50 text-blue-600",
  IN_PROGRESS: "bg-orange-50 text-orange-600",
  FIXED: "bg-green-50 text-green-600",
  VERIFIED: "bg-teal-50 text-teal-600",
  CLOSED: "bg-gray-100 text-gray-500",
};

// Regroupement des erreurs similaires (UI Fingerprint)
const groupedErrors = computed(() => {
  const groups = {};
  adminStore.errors.forEach((log) => {
    const key = `${log.http_method}_${log.endpoint_url}_${log.error_message}`;
    if (!groups[key]) groups[key] = { count: 0, latest: log };
    groups[key].count++;
    if (new Date(log.created_at) > new Date(groups[key].latest.created_at))
      groups[key].latest = log;
  });
  return Object.values(groups).sort(
    (a, b) => new Date(b.latest.created_at) - new Date(a.latest.created_at),
  );
});

const loadData = () => adminStore.fetchErrors(filters);

const translateStatus = (val) => statusLabels[val] || val;

const openDetails = (log) => {
  selectedLog.value = log;
  editForm.status = log.status;
  editForm.priority = log.priority;
  editForm.note = log.resolution_note || "";
};

const closeDetails = () => {
  selectedLog.value = null;
  showNoteModal.value = false;
};

const showToast = (msg) => {
  toastMsg.value = msg;
  setTimeout(() => (toastMsg.value = ""), 3000);
};

// Logique de validation et sauvegarde
const handleSave = () => {
  if (!selectedLog.value) return;

  // Si le statut est final (Fixé/Fermé) et qu'il n'y a pas de note (min 5 chars)
  const isFinalStatus = ["FIXED", "CLOSED", "VERIFIED"].includes(
    editForm.status,
  );
  if (isFinalStatus && editForm.note.trim().length < 5) {
    showNoteModal.value = true;
  } else {
    confirmSave();
  }
};

const confirmSave = async () => {
  showNoteModal.value = false;
  try {
    const payload = {
      status: editForm.status,
      priority: editForm.priority,
      resolution_note: editForm.note.trim(),
    };

    await adminStore.updateErrorLog(selectedLog.value.id, payload);

    showToast("Anomalie mise à jour");
    loadData();
    closeDetails();
  } catch (e) {
    showToast("Erreur de mise à jour");
  }
};

const timeAgo = (dateStr) => {
  const diff = Math.floor((new Date() - new Date(dateStr)) / 1000);
  if (diff < 3600) return `Il y a ${Math.floor(diff / 60)}m`;
  if (diff < 86400) return `Il y a ${Math.floor(diff / 3600)}h`;
  return `Il y a ${Math.floor(diff / 86400)}j`;
};

onMounted(() => loadData());
</script>

<style scoped>
.animate-slide-in {
  animation: slideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.animate-pop {
  animation: pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes pop {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.4s ease,
    transform 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
</style>
