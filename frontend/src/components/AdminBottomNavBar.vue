<template>
  <nav
    class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 z-50 pb-[env(safe-area-inset-bottom)] shadow-[0_-2px_10px_rgba(0,0,0,0.02)]"
  >
    <div class="flex justify-around items-center h-16 max-w-md mx-auto px-2">
      <!-- 1. Dashboard Admin -->
      <router-link
        :to="{ name: 'admin-dashboard' }"
        custom
        v-slot="{ isActive, navigate }"
      >
        <button
          @click="navigate"
          class="flex flex-col items-center justify-center w-16 transition-colors"
          :class="
            isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'
          "
        >
          <svg
            class="w-6 h-6 mb-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            :stroke-width="isActive ? '2.5' : '2'"
          >
            <!-- Icône Chart/Dashboard -->
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Tableau</span>
        </button>
      </router-link>

      <!-- 2. System Health / Error Log -->
      <router-link
        :to="{ name: 'admin-errors' }"
        custom
        v-slot="{ isActive, navigate }"
      >
        <button
          @click="navigate"
          class="flex flex-col items-center justify-center w-16 transition-colors"
          :class="
            isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'
          "
        >
          <svg
            class="w-6 h-6 mb-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            :stroke-width="isActive ? '2.5' : '2'"
          >
            <!-- Icône Shield/Warning -->
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide">Erreurs</span>
        </button>
      </router-link>

      <!-- 3. Gestion Utilisateurs -->
      <router-link
        :to="{ name: 'admin-users' }"
        custom
        v-slot="{ isActive, navigate }"
      >
        <button
          @click="navigate"
          class="flex flex-col items-center justify-center w-16 transition-colors"
          :class="
            isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'
          "
        >
          <svg
            class="w-6 h-6 mb-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            :stroke-width="isActive ? '2.5' : '2'"
          >
            <!-- Icône User Group -->
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide"
            >Utilisateurs</span
          >
        </button>
      </router-link>

      <!-- 4. Paramètres Admin -->
      <router-link
        :to="{ name: 'admin-settings' }"
        custom
        v-slot="{ isActive, navigate }"
      >
        <button
          @click="navigate"
          class="flex flex-col items-center justify-center w-16 transition-colors"
          :class="
            isActive ? 'text-[#5A877E]' : 'text-gray-400 hover:text-gray-600'
          "
        >
          <svg
            class="w-6 h-6 mb-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            :stroke-width="isActive ? '2.5' : '2'"
          >
            <!-- Icône Cog/Paramètres -->
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span class="text-[10px] font-semibold tracking-wide"
            >Paramètres</span
          >
        </button>
      </router-link>
    </div>
  </nav>
</template>
