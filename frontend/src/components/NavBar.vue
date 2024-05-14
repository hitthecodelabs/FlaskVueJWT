<!-- src/components/NavBar.vue -->

<template>
  <nav class="navbar">
    <ul class="nav-links">
      <li><router-link to="/" class="nav-link">Home</router-link></li>
      <li v-if="isAuthenticated"><router-link to="/dashboard" class="nav-link">Dashboard</router-link></li>
      <li v-if="isAuthenticated"><router-link to="/pricing" class="nav-link">Pricing</router-link></li>
      <li v-if="!isAuthenticated"><router-link to="/login" class="nav-link">Log In</router-link></li>
      <li v-if="!isAuthenticated"><router-link to="/signup" class="nav-link">Sign Up</router-link></li>
      <li v-if="isAuthenticated"><router-link to="#" @click="logout" class="nav-link">Logout</router-link></li>
    </ul>
  </nav>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const { isAuthenticated, setAuth } = useAuthStore();

    const logout = async (event) => {
      event.preventDefault();
      document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      setAuth(false);
      router.push('/login');
    };

    return {
      isAuthenticated,
      logout
    };
  }
};
</script>

<style scoped>
.nav-link {
  display: block;
  padding: 10px 15px;
  text-decoration: none;
  color: inherit;
  font-weight: bold;
  border: none;
  background: none;
  cursor: pointer;
}

.nav-link:hover {
  background-color: #0056b3;
  color: #ffffff;
}
</style>

