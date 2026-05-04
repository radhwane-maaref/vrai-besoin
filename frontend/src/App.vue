<script setup>
import {onMounted} from 'vue';
import {RouterView} from 'vue-router';
import {useAuthStore} from '@/stores/auth';
import BottomNavBar from '@/components/BottomNavBar.vue';

const authStore = useAuthStore();

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

  <div
      class="min-h-screen flex flex-col font-sans"
      :class="authStore.isAuthenticated ? 'pb-[calc(4rem+env(safe-area-inset-bottom))]' : ''"
  >
    <router-view class="flex-grow"/>
    <BottomNavBar v-if="authStore.isAuthenticated"/>
  </div>
</template>

<style>
body {
  overscroll-behavior-y: none;
  background-color: #FAFAFA;
}
</style>