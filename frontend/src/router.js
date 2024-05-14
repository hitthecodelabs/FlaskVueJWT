// src/router.js

import { useAuthStore } from '@/store/auth';
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import SignupForm from './components/SignupForm.vue';
import LoginForm from './components/LoginForm.vue';
import DashboardPage from './components/DashboardPage.vue';
import AboutUs from './components/AboutUs.vue';
import ContactUs from './components/ContactUs.vue';
import PricingPlans from './components/PricingPlans.vue';
import PrivacyPolicy from './components/PrivacyPolicy.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/signup', component: SignupForm, meta: { guestOnly: true } },
  { path: '/login', component: LoginForm, meta: { guestOnly: true } },
  { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/pricing', component: PricingPlans, meta: { requiresAuth: true } },
  { path: '/about', component: AboutUs },
  { path: '/contact', component: ContactUs },
  { path: '/privacy', component: PrivacyPolicy },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const { isAuthenticated, checkAuth } = useAuthStore();
  checkAuth(); // Ensure the auth state is updated

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login');
  } else if (to.meta.guestOnly && isAuthenticated.value) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
