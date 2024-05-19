// src/main.js

import { createApp } from 'vue';
import VueToast from 'vue-toast-notification';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/styles.css';  // global styles
import 'vue-toast-notification/dist/theme-default.css';  // CSS for the toast

const app = createApp(App);

// Define a global reactive state
const pinia = createPinia();
app.use(pinia);

app.use(VueToast, {
  position: 'top-right',
});

app.use(router);
app.mount('#app');
