<template>
  <nav class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 z-50 pb-[env(safe-area-inset-bottom)] shadow-[0_-2px_10px_rgba(0,0,0,0.02)]">
    <div class="flex justify-around items-center h-16 max-w-md mx-auto px-2">

      <router-link :to="{ name: 'dashboard' }" custom v-slot="{ isActive, navigate }">
        <button @click="navigate" class="flex flex-col items-center justify-center w-16 transition-colors" :class="isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'">
          <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" :stroke="isActive ? 'currentColor' : 'currentColor'" :stroke-width="isActive ? '2.5' : '2'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Accueil</span>
        </button>
      </router-link>

      <router-link :to="{ name: 'stats' }" custom v-slot="{ isActive, navigate }">
        <button @click="navigate" class="flex flex-col items-center justify-center w-16 transition-colors" :class="isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'">
          <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" :stroke="isActive ? 'currentColor' : 'currentColor'" :stroke-width="isActive ? '2.5' : '2'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Stats</span>
        </button>
      </router-link>

      <router-link :to="{ name: 'add-purchase' }" custom v-slot="{ isActive, navigate }">
        <button @click="navigate" class="flex flex-col items-center justify-center -mt-5 relative group">
          <div class="bg-white p-1.5 rounded-full shadow-sm">
            <div class="w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-md" :class="isActive ? 'bg-[#4a7269]' : 'bg-[#5A877E] group-hover:bg-[#4a7269]'">
              <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
            </div>
          </div>
          <span class="text-[10px] font-bold text-[#5A877E] mt-0.5">Analyser</span>
        </button>
      </router-link>

      <router-link :to="{ name: 'track' }" custom v-slot="{ isActive, navigate }">
        <button @click="navigate" class="flex flex-col items-center justify-center w-16 transition-colors" :class="isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'">
          <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" :stroke="isActive ? 'currentColor' : 'currentColor'" :stroke-width="isActive ? '2.5' : '2'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Suivi</span>
        </button>
      </router-link>

      <router-link :to="{ name: 'settings' }" custom v-slot="{ isActive, navigate }">
        <button @click="navigate" class="flex flex-col items-center justify-center w-16 transition-colors" :class="isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'">
          <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" :stroke="isActive ? 'currentColor' : 'currentColor'" :stroke-width="isActive ? '2.5' : '2'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Profil</span>
        </button>
      </router-link>

    </div>
  </nav>
</template>

<script setup>
// Pas de logique complexe requise ici, Vue Router (v-slot="{ isActive }") gère tout nativement !
</script>