import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import router from "@/router";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor: Attach the access token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response Interceptor: Handle 401 and Token Refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Failsafe: If the refresh endpoint itself returns a 401, abort immediately to prevent loops
    if (
      error.response?.status === 401 &&
      originalRequest.url.includes("/auth/token/refresh/")
    ) {
      return Promise.reject(error);
    }
    if (
      error.response?.status === 401 &&
      (originalRequest.url.includes("/auth/login/") ||
        originalRequest.url.includes("/auth/google/"))
    ) {
      return Promise.reject(error); // On renvoie l'erreur à la vue pour qu'elle l'affiche
    }
    // If 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const authStore = useAuthStore();
      const refreshToken = localStorage.getItem("refresh_token");

      // If there's no refresh token in storage, don't bother hitting the API
      if (!refreshToken) {
        authStore.logout();
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        router.push({ name: "login" });
        return Promise.reject(error);
      }

      try {
        // Attempt to refresh the token via Django DRF SimpleJWT
        const response = await axios.post(
          `${api.defaults.baseURL}/auth/token/refresh/`,
          {
            refresh: refreshToken,
          },
        );

        const newAccessToken = response.data.access;

        // Update local storage with the new token
        localStorage.setItem("access_token", newAccessToken);

        // Update the header and retry the original request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails (e.g., refresh token is expired or invalid)
        authStore.logout();

        // Forcefully clear local storage to ensure a clean slate
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        // Redirect user to the login page
        router.push({ name: "login" });

        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);

export default api;
