import './assets/main.css'; // Your Tailwind CSS directives should live here

import {createApp} from 'vue';
import {createPinia} from 'pinia';
import GoogleSignInPlugin from 'vue3-google-signin';
import App from './App.vue';
import router from './router';
// We will define this next

const app = createApp(App);
const pinia = createPinia();

// ⚠️ Architecture Note:
// Always register Pinia BEFORE the router.
// This ensures that if you use Vue Router navigation guards
// (e.g., checking if a user is authenticated before hitting the dashboard),
// the Pinia auth store is already initialized and available.

app.use(GoogleSignInPlugin, {
    clientId: import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID,
});
app.use(pinia);
app.use(router);

app.mount('#app');