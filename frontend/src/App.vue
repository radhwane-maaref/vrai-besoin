<script setup>
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

// Hydrate user profile on application startup if a token exists
onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      await authStore.fetchUserProfile();
    } catch (error) {
      console.warn("Could not fetch user profile on startup.");
    }
  }
});
</script>

<template>
  <RouterView />
</template>

<style>
/* Global resets handled by Tailwind in main.css */
body {
  overscroll-behavior-y: none;
  background-color: #FAFAFA;
}
</style>