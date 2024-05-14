// src/main.js

import { createApp, reactive } from 'vue';
import VueToast from 'vue-toast-notification';
import App from './App.vue';
import router from './router';
import './assets/styles.css';  // global styles
import 'vue-toast-notification/dist/theme-default.css';  // CSS for the toast

const app = createApp(App);

// Define a global reactive state
const globalState = reactive({
  isLoggedIn: false,

});

app.provide('globalState', globalState);

app.use(VueToast, {
  position: 'top-right',
});

app.use(router);
app.mount('#app');
