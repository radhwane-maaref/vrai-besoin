import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { useAuthStore } from "./auth";
import api from "@/services/api";

export const useCurrencyStore = defineStore("currency", () => {
  const authStore = useAuthStore();
  const availableCurrencies = [
    { code: "TND", name: "Dinar tunisien", countryCode: "tn" },
    { code: "EUR", name: "Euro", countryCode: "eu" },
    { code: "USD", name: "Dollar américain", countryCode: "us" },
    { code: "GBP", name: "Livre sterling", countryCode: "gb" },
    { code: "CAD", name: "Dollar canadien", countryCode: "ca" },
    { code: "JPY", name: "Yen japonais", countryCode: "jp" },
    { code: "AUD", name: "Dollar australien", countryCode: "au" },
    { code: "CHF", name: "Franc suisse", countryCode: "ch" },
    { code: "CNY", name: "Yuan chinois", countryCode: "cn" },
    { code: "AED", name: "Dirham des EAU", countryCode: "ae" },
    { code: "SAR", name: "Riyal saoudien", countryCode: "sa" },
    { code: "MAD", name: "Dirham marocain", countryCode: "ma" },
    { code: "DZD", name: "Dinar algérien", countryCode: "dz" },
    { code: "ZAR", name: "Rand sud-africain", countryCode: "za" },
    { code: "BRL", name: "Réal brésilien", countryCode: "br" },
    { code: "INR", name: "Roupie indienne", countryCode: "in" },
    { code: "EGP", name: "Livre égyptienne", countryCode: "eg" },
    { code: "QAR", name: "Riyal qatari", countryCode: "qa" },
    { code: "KWD", name: "Dinar koweïtien", countryCode: "kw" },
    { code: "BHD", name: "Dinar bahreïni", countryCode: "bh" },
    { code: "OMR", name: "Rial omanais", countryCode: "om" },
    { code: "JOD", name: "Dinar jordanien", countryCode: "jo" },
    { code: "LBP", name: "Livre libanaise", countryCode: "lb" },
    { code: "KRW", name: "Won sud-coréen", countryCode: "kr" },
    { code: "SGD", name: "Dollar de Singapour", countryCode: "sg" },
    { code: "HKD", name: "Dollar de Hong Kong", countryCode: "hk" },
    { code: "NZD", name: "Dollar néo-zélandais", countryCode: "nz" },
    { code: "MYR", name: "Ringgit malaisien", countryCode: "my" },
    { code: "IDR", name: "Roupie indonésienne", countryCode: "id" },
    { code: "THB", name: "Baht thaïlandais", countryCode: "th" },
    { code: "MXN", name: "Peso mexicain", countryCode: "mx" },
    { code: "ARS", name: "Peso argentin", countryCode: "ar" },
    { code: "COP", name: "Peso colombien", countryCode: "co" },
    { code: "CLP", name: "Peso chilien", countryCode: "cl" },
    { code: "SEK", name: "Couronne suédoise", countryCode: "se" },
    { code: "NOK", name: "Couronne norvégienne", countryCode: "no" },
    { code: "DKK", name: "Couronne danoise", countryCode: "dk" },
    { code: "PLN", name: "Złoty polonais", countryCode: "pl" },
    { code: "CZK", name: "Couronne tchèque", countryCode: "cz" },
    { code: "HUF", name: "Forint hongrois", countryCode: "hu" },
    { code: "TRY", name: "Livre turque", countryCode: "tr" },
    { code: "RUB", name: "Rouble russe", countryCode: "ru" },
  ];
  // Initialisation locale
  const savedCurrency = localStorage.getItem("user_favorite_currency");
  const defaultCurrency = availableCurrencies[0];
  const currentCurrency = ref(
    savedCurrency ? JSON.parse(savedCurrency) : defaultCurrency,
  );

  // Écoute les données du backend au chargement de l'app
  watch(
    () => authStore.user,
    (newUser) => {
      if (newUser && newUser.preferred_currency) {
        // Si la BDD contient une devise différente
        if (currentCurrency.value.code !== newUser.preferred_currency) {
          // FIX : On cherche l'objet complet pour mettre à jour le code ET le countryCode (drapeau)
          const fullCurrencyObject = availableCurrencies.find(
            (c) => c.code === newUser.preferred_currency,
          );

          if (fullCurrencyObject) {
            currentCurrency.value = { ...fullCurrencyObject };
            localStorage.setItem(
              "user_favorite_currency",
              JSON.stringify(fullCurrencyObject),
            );
          } else {
            // Fallback de sécurité si la devise n'est pas dans la liste
            currentCurrency.value.code = newUser.preferred_currency;
          }
        }
      }
    },
    { immediate: true },
  );

  // Action pour sauvegarder
  const setCurrency = async (currencyObj) => {
    // 1. Mise à jour instantanée de l'UI (Optimistic UI)
    currentCurrency.value = currencyObj;
    localStorage.setItem("user_favorite_currency", JSON.stringify(currencyObj)); // Sert de cache

    // 2. Envoi silencieux vers la base de données
    if (authStore.isAuthenticated) {
      try {
        await api.patch("/users/me/", { preferred_currency: currencyObj.code });
        // Met à jour le store utilisateur pour que tout reste synchro
        if (authStore.user) {
          authStore.user.preferred_currency = currencyObj.code;
        }
      } catch (error) {
        console.error(
          "Erreur lors de la sauvegarde de la devise en BDD:",
          error,
        );
      }
    }
  };

  return {
    currentCurrency,
    setCurrency,
    availableCurrencies,
  };
});
