import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import RegisterView from "@/views/RegisterView.vue";

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
                    return { name: 'dashboard' };
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
                    return { name: 'dashboard' };
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
            meta: { requiresAuth: true } // Custom meta tag to protect this route
        },
        {
            // Catch-all route for 404s
            path: '/:pathMatch(.*)*',
            redirect: { name: 'dashboard' }
        }
    ]
});

// Global Navigation Guard for Authentication
router.beforeEach((to, from) => {
    const authStore = useAuthStore();
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    if (requiresAuth && !authStore.isAuthenticated) {
        // Force them to log in
        return { name: 'login' };
    } else {
        // All good, let them pass
        return true;
    }
});

export default router;