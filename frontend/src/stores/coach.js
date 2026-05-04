import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export const useCoachStore = defineStore('coach', () => {
    // --- State ---
    const currentIntentionId = ref(null);
    const extractedData = ref({
        product_name: '',
        product_price: '',
        product_category: ''
    });
    const loading = ref(false);
    const error = ref(null);

    // --- Actions ---

    // 1. Appel à l'IA pour extraire les infos de l'image
    const extractFromImage = async (imageFile) => {
        loading.value = true;
        error.value = null;
        try {
            const formData = new FormData();
            formData.append('image', imageFile);

            const response = await api.post('/purchase-intentions/extract/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            extractedData.value = {
                product_name: response.data.data.product_name || '',
                product_price: response.data.data.product_price || '',
                product_category: response.data.data.product_category || ''
            };

            return response.data.message;
        } catch (err) {
            error.value = err.response?.data?.error || "L'extraction a échoué. Veuillez saisir manuellement.";
            throw err;
        } finally {
            loading.value = false;
        }
    };

    // 2. Création finale de l'intention d'achat en base de données
    const createPurchaseIntention = async (payload) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await api.post('/purchase-intentions/', payload);
            currentIntentionId.value = response.data.id;
            return response.data;
        } catch (err) {
            if (err.response?.data && !err.response.data.error) {
                const firstErrorKey = Object.keys(err.response.data)[0];
                error.value = err.response.data[firstErrorKey][0];
            } else {
                error.value = err.response?.data?.error || "Erreur lors de l'enregistrement.";
            }
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const resetFlow = () => {
        currentIntentionId.value = null;
        extractedData.value = { product_name: '', product_price: '', product_category: '' };
        error.value = null;
    };

    return {
        currentIntentionId,
        extractedData,
        loading,
        error,
        extractFromImage,
        createPurchaseIntention,
        resetFlow
    };
});