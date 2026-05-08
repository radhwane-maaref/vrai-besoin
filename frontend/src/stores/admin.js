import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/services/api";

export const useAdminStore = defineStore("admin", () => {
  const stats = ref(null);
  const errors = ref([]);
  const users = ref([]);
  const loading = ref(false);

  const fetchStats = async (period = "all") => {
    loading.value = true;
    try {
      const response = await api.get("/admin-api/stats/", {
        params: { period },
      });
      stats.value = response.data;
    } catch (error) {
      console.error("Erreur lors du chargement des statistiques admin", error);
    } finally {
      loading.value = false;
    }
  };

  // Mise à jour : accepte les filtres et gère les erreurs silencieusement
  const fetchErrors = async (filters = {}) => {
    loading.value = true;
    try {
      const params = new URLSearchParams(filters).toString();
      const response = await api.get(`/admin-api/errors/?${params}`);
      errors.value = response.data;
    } catch (error) {
      console.error("Erreur lors du chargement des logs :", error);
      errors.value = []; // Empêche l'interface de crasher si l'API échoue
    } finally {
      loading.value = false;
    }
  };

  const updateErrorLog = async (id, payload) => {
    const response = await api.patch(`/admin-api/errors/${id}/`, payload);
    // Optimistic UI update locally
    const index = errors.value.findIndex((e) => e.id === id);
    if (index !== -1) errors.value[index] = response.data;
    return response.data;
  };

  const fetchUsers = async () => {
    loading.value = true;
    try {
      const response = await api.get("/admin-api/users/");
      users.value = response.data;
    } finally {
      loading.value = false;
    }
  };

  const interveneUser = async (id, action) => {
    await api.patch(`/admin-api/users/${id}/`, { action });
    await fetchUsers();
  };

  return {
    stats,
    errors,
    users,
    loading,
    fetchStats,
    fetchErrors,
    updateErrorLog,
    fetchUsers,
    interveneUser,
  };
});
