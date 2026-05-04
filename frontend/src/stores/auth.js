import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", () => {
  // --- State ---
  const user = ref(null);
  const isAuthenticated = ref(!!localStorage.getItem("access_token"));
  const loading = ref(false);
  const error = ref(null);

  // --- Getters ---
  const getUser = computed(() => user.value);
  const getAuthStatus = computed(() => isAuthenticated.value);

  const handleAuthSuccess = async (response) => {
    const { access, refresh } = response.data.tokens;
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    isAuthenticated.value = true;
    await fetchUserProfile();
  };
  // --- Actions ---
  const login = async (credentials) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.post("/auth/login/", credentials);
      await handleAuthSuccess(response);
    } catch (err) {
      error.value = err.response?.data?.error || "Authentication failed.";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const register = async (userData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.post("/auth/register/", userData);
      await handleAuthSuccess(response);
    } catch (err) {
      // ... error handling remains unchanged ...
    } finally {
      loading.value = false;
    }
  };

  const googleLogin = async (token) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.post("/auth/google/", { access_token: token });

      const { access, refresh } = response.data.tokens;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      isAuthenticated.value = true;
      await fetchUserProfile();
    } catch (err) {
      const backendError =
        err.response?.data?.non_field_errors?.[0] || err.response?.data?.error;
      error.value = backendError || "Échec de l'authentification Google.";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchUserProfile = async () => {
    try {
      const response = await api.get("/users/me/");
      user.value = response.data;
    } catch (err) {
      console.error("Failed to fetch user profile:", err);
    }
  };

  const logout = () => {
    user.value = null;
    isAuthenticated.value = false;
    error.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  return {
    user,
    isAuthenticated,
    loading,
    error,
    getUser,
    getAuthStatus,
    login,
    googleLogin,
    register,
    fetchUserProfile,
    logout,
  };
});
