import {createRouter, createWebHistory} from 'vue-router';
import {useAuthStore} from '@/stores/auth';
import RegisterView from "@/views/RegisterView.vue";
import AddPurchaseView from "@/views/AddPurchaseView.vue";
import StatsView from "@/views/StatsView.vue";
import Settings from "@/views/Settings.vue";
import TrackView from "@/views/TrackView.vue";

// Import views (Lazy loading for better performance)
const LoginView = () => import('@/views/LoginView.vue');
const DashboardView = () => import('@/views/DashboardView.vue'); // To be built

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            // If a logged-in user tries to visit the login page, redirect them
            beforeEnter: (to, from) => {
                const authStore = useAuthStore();
                if (authStore.isAuthenticated) {
                    return {name: 'dashboard'};
                } else {
                    return true;
                }
            }
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView,
            beforeEnter: (to, from) => {
                const authStore = useAuthStore();
                if (authStore.isAuthenticated) {
                    return {name: 'dashboard'};
                } else {
                    return true;
                }
            }
        },
        {
            path: '/forgot-password',
            name: 'forgot-password',
            component: () => import('@/views/ForgotPasswordView.vue'),
        },
        {
            // Dynamic route matching exactly what Django expects: /uidb64/token/
            path: '/reset-password/:uid/:token',
            name: 'reset-password-confirm',
            component: () => import('@/views/ResetPasswordView.vue'),
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: DashboardView,
            meta: {requiresAuth: true} // Custom meta tag to protect this route
        },
        {
            path: '/purchase/new',
            name: 'add-purchase',
            component: AddPurchaseView,
            meta: {requiresAuth: true}
        },
        {
            // LA MODIFICATION EST ICI 👇
            path: '/reflection/:id',
            name: 'reflection',
            component: () => import('@/views/EvaluationWizard.vue'),
            meta: {requiresAuth: true}
        },
        {
            // Catch-all route for 404s (doit être en dernier)
            path: '/:pathMatch(.*)*',
            redirect: {name: 'dashboard'}
        },
        {
            path: '/stats',
            name: 'stats',
            component: StatsView,
            meta: {requiresAuth: true}
        },
        {
            path: '/track',
            name: 'track',
            component: TrackView,
            meta: {requiresAuth: true}
        },
        {
            path: '/settings',
            name: 'settings',
            component: Settings,
            meta: {requiresAuth: true}
        },


        {
            path: '/settings/profile',
            name: 'EditProfileView',
            component: () => import('@/views/settings/EditProfile.vue'),
        },
        {
            path: '/settings/preferences',
            name: 'UserPreferencesView',
            component: () => import('@/views/settings/UserPreferences.vue'),
        },
        {
            path: '/settings/terms',
            name: 'TermsOfServiceView',
            component: () => import('@/views/settings/TermsOfService.vue'),
        },
        {
            path: '/settings/help',
            name: 'HelpSupportView',
            component: () => import('@/views/settings/HelpSupport.vue'),
        },
        {
            path: '/admin/feedbacks',
            name: 'admin-feedbacks',
            component: () => import('@/views/admin/AdminFeedbacksView.vue'),
            meta: {requiresAuth: true, requiresAdmin: true}
        },

    ]
});

// Global Navigation Guard for Authentication
router.beforeEach((to, from) => {
    const authStore = useAuthStore();
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);

    if (requiresAuth && !authStore.isAuthenticated) {
        // Force them to log in
        return {name: 'login'};
    } else if (requiresAdmin && authStore.user && !authStore.user.is_staff) {
        return {name: 'dashboard'};

    } else {
        return true;
    }
});

export default router;