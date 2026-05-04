import {defineStore} from 'pinia';
import {ref, watch} from 'vue';
import {useAuthStore} from './auth';
import api from '@/services/api';

export const useCurrencyStore = defineStore('currency', () => {
    const authStore = useAuthStore();

    // Initialisation locale
    const savedCurrency = localStorage.getItem('user_favorite_currency');
    const defaultCurrency = {code: 'TND', name: 'Dinar tunisien', flag: '🇹🇳'};
    const currentCurrency = ref(savedCurrency ? JSON.parse(savedCurrency) : defaultCurrency);

    // Écoute les données du backend au chargement de l'app
    watch(() => authStore.user, (newUser) => {
        if (newUser && newUser.preferred_currency) {
            // Si la BDD contient une devise différente, on met à jour l'affichage
            if (currentCurrency.value.code !== newUser.preferred_currency) {
                currentCurrency.value.code = newUser.preferred_currency;
            }
        }
    }, {immediate: true});

    // Action pour sauvegarder
    const setCurrency = async (currencyObj) => {
        // 1. Mise à jour instantanée de l'UI (Optimistic UI)
        currentCurrency.value = currencyObj;
        localStorage.setItem('user_favorite_currency', JSON.stringify(currencyObj)); // Sert de cache

        // 2. Envoi silencieux vers la base de données
        if (authStore.isAuthenticated) {
            try {
                await api.patch('/users/me/', {preferred_currency: currencyObj.code});
                // Met à jour le store utilisateur pour que tout reste synchro
                if (authStore.user) {
                    authStore.user.preferred_currency = currencyObj.code;
                }
            } catch (error) {
                console.error("Erreur lors de la sauvegarde de la devise en BDD:", error);
            }
        }
    };

    return {
        currentCurrency,
        setCurrency
    };
});