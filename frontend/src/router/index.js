import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import RegisterView from "@/views/RegisterView.vue";
import AddPurchaseView from "@/views/AddPurchaseView.vue";
import StatsView from "@/views/StatsView.vue";
import Settings from "@/views/Settings.vue";
import TrackView from "@/views/TrackView.vue";

const LoginView = () => import("@/views/LoginView.vue");
const DashboardView = () => import("@/views/DashboardView.vue");
const OnboardingStepper = () => import("@/views/OnboardingStepper.vue");
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
      beforeEnter: (to, from) => {
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
          return authStore.user?.is_staff
            ? { name: "admin-dashboard" }
            : { name: "dashboard" };
        }
        return true;
      },
    },
    {
      path: "/onboarding",
      name: "onboarding",
      component: OnboardingStepper,
      meta: { requiresAuth: true, hideBottomNav: true },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      beforeEnter: (to, from) => {
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
          return authStore.user?.is_staff
            ? { name: "admin-dashboard" }
            : { name: "dashboard" };
        }
        return true;
      },
    },
    {
      path: "/forgot-password",
      name: "forgot-password",
      component: () => import("@/views/ForgotPasswordView.vue"),
    },
    {
      path: "/reset-password/:uid/:token",
      name: "reset-password-confirm",
      component: () => import("@/views/ResetPasswordView.vue"),
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: "/purchase/new",
      name: "add-purchase",
      component: AddPurchaseView,
      meta: { requiresAuth: true },
    },
    {
      path: "/reflection/:id",
      name: "reflection",
      component: () => import("@/views/EvaluationWizard.vue"),
      meta: { requiresAuth: true, hideBottomNav: true },
    },
    {
      path: "/stats",
      name: "stats",
      component: StatsView,
      meta: { requiresAuth: true },
    },
    {
      path: "/track",
      name: "track",
      component: TrackView,
      meta: { requiresAuth: true },
    },
    {
      path: "/settings",
      name: "settings",
      component: Settings,
      meta: { requiresAuth: true },
    },
    {
      path: "/settings/profile",
      name: "EditProfileView",
      component: () => import("@/views/settings/EditProfile.vue"),
    },
    {
      path: "/settings/preferences",
      name: "UserPreferencesView",
      component: () => import("@/views/settings/UserPreferences.vue"),
    },
    {
      path: "/settings/terms",
      name: "TermsOfServiceView",
      component: () => import("@/views/settings/TermsOfService.vue"),
    },
    {
      path: "/settings/help",
      name: "HelpSupportView",
      component: () => import("@/views/settings/HelpSupport.vue"),
    },

    // Admin Routes
    {
      path: "/admin",
      name: "admin-dashboard",
      component: () => import("@/views/admin/AdminDashboard.vue"),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: "/admin/errors",
      name: "admin-errors",
      component: () => import("@/views/admin/AdminSystemHealth.vue"),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: "/admin/users",
      name: "admin-users",
      component: () => import("@/views/admin/ManagingUser.vue"), // Créer ce fichier plus tard
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: "/admin/settings",
      name: "admin-settings",
      component: () => import("@/views/admin/AdminSettings.vue"), // Créer ce fichier plus tard
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
});

// Global Navigation Guard for Authentication
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);

  if (authStore.isAuthenticated && !authStore.user) {
    try {
      await authStore.fetchUserProfile();
    } catch (e) {
      authStore.logout();
      return { name: "login" };
    }
  }

  // Redirect to log in if the route requires authentication but the user is not logged in
  if (requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" };
  }
  if (authStore.isAuthenticated && authStore.user) {
    // Exclude admin accounts from onboarding loop to prevent lockouts
    if (!authStore.user.is_staff) {
      // If not onboarded and trying to access anything other than onboarding
      if (!authStore.user.is_onboarded && to.name !== "onboarding") {
        return { name: "onboarding" };
      }

      // If already onboarded and trying to access the onboarding page manually
      if (authStore.user.is_onboarded && to.name === "onboarding") {
        return { name: "dashboard" };
      }
    }
  }
  // Restrict Admin users from accessing client pages
  if (authStore.isAuthenticated && authStore.user?.is_staff) {
    // Define the specific non-admin routes the admin is allowed to access
    const allowedAdminRoutes = [
      "settings",
      "EditProfileView",
      "UserPreferencesView",
      "TermsOfServiceView",
      "HelpSupportView",
      "login",
      "register",
      "forgot-password",
      "reset-password-confirm",
      "admin-errors",
      "admin/users",
      "admin-settings",
    ];

    // If the route is not an admin route AND not in the allowed list, force redirect to admin-dashboard
    if (!requiresAdmin && !allowedAdminRoutes.includes(to.name)) {
      return { name: "admin-dashboard" };
    }
  }

  // FIX: Safely bounce standard users out of the admin panel
  if (requiresAdmin && !authStore.user?.is_staff) {
    return { name: "dashboard" };
  }

  return true;
});

export default router;
