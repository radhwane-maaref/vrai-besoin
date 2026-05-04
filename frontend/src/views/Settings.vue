<template>
  <!-- Main Wrapper -->
  <!-- We use a subtle off-white/gray background so the white cards pop out -->
  <div class="flex-grow bg-[#F8F6F2] flex flex-col font-sans pb-10">

    <!-- Header -->
    <header class="w-full pt-8 pb-4">
      <h1 class="text-center text-[1.35rem] font-bold text-black tracking-tight">Paramètres</h1>
    </header>

    <!-- Content -->
    <main class="flex-1 w-full max-w-md mx-auto px-6 py-6 flex flex-col gap-8">

      <!-- Section: COMPTE -->
      <section class="flex flex-col gap-2.5">
        <h2 class="text-[13px] font-bold text-gray-600 uppercase tracking-widest pl-2">Compte</h2>

        <div class="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-50/50">
          <router-link :to="{ name: 'EditProfileView' }" class="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 transition-colors group">
            <div class="flex items-center gap-4">
              <svg class="w-6 h-6 text-gray-500 group-hover:text-[#5B8C85] transition-colors" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
              </svg>
              <span class="text-[15px] text-gray-800">Modifier mon profil</span>
            </div>
            <svg class="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: PRÉFÉRENCES -->
      <section class="flex flex-col gap-2.5">
        <h2 class="text-[13px] font-bold text-gray-600 uppercase tracking-widest pl-2">Préférences</h2>

        <div class="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-50/50">
          <!-- Combined single preferences field -->
          <router-link :to="{ name: 'UserPreferencesView' }" class="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 transition-colors group">
            <div class="flex items-center gap-4">
              <svg class="w-6 h-6 text-gray-500 group-hover:text-[#5B8C85] transition-colors" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
              </svg>
              <span class="text-[15px] text-gray-800">Modifier mes préférences</span>
            </div>
            <svg class="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: ASSISTANCE -->
      <section class="flex flex-col gap-2.5">
        <h2 class="text-[13px] font-bold text-gray-600 uppercase tracking-widest pl-2">Assistance</h2>

        <div class="bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-50/50 flex flex-col">
          <router-link :to="{ name: 'TermsOfServiceView' }" class="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100 group">
            <div class="flex items-center gap-4">
              <svg class="w-6 h-6 text-gray-500 group-hover:text-[#5B8C85] transition-colors" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
              </svg>
              <span class="text-[15px] text-gray-800">Conditions d'utilisations</span>
            </div>
            <svg class="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </router-link>

          <router-link :to="{ name: 'HelpSupportView' }" class="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-50 transition-colors group">
            <div class="flex items-center gap-4">
              <svg class="w-6 h-6 text-gray-500 group-hover:text-[#5B8C85] transition-colors" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
              </svg>
              <span class="text-[15px] text-gray-800">Aide et support</span>
            </div>
            <svg class="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Section: LOGOUT -->
      <section class="mt-8 flex justify-center pb-8">
        <button @click="performLogout" class="flex items-center gap-2 text-[#D9534F] font-medium text-[15px] px-6 py-3 rounded-full hover:bg-red-50 transition-colors active:scale-95">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
          </svg>
          Se déconnecter
        </button>
      </section>

    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';

const router = useRouter();
const authStore = useAuthStore();

const performLogout = async () => {
  authStore.logout();
  console.log('User is logging out...');
  await router.push({ name: 'login' });
};
</script>