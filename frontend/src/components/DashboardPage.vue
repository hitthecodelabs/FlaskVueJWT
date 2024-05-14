<!-- src/components/Dashboard.vue -->

<template>
  <div class="dashboard-container">
    <div v-if="loading" class="loading-indicator">
      <p>Loading...</p>
    </div>
    <div v-else>
      <h1>Welcome to Your Dashboard, {{ fullName }}!</h1>
      <p>Email: {{ email }}</p>
      <p>Company: {{ company }}</p>
      <!-- <button @click="logout">Logout</button> -->
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { apiRequest } from '../api';
import { useRouter } from 'vue-router';

export default {
  name: 'DashboardPage',
  data() {
    return {
      fullName: '',
      email: '',
      company: '',
      loading: true
    };
  },
  async mounted() {
    await this.initializeDashboard();
  },
  methods: {
    async initializeDashboard() {
      const { isAuthenticated, checkAuth, userData, fetchUserData } = useAuthStore();
      const router = useRouter();
      checkAuth(); // Ensure the auth state is updated

      if (!isAuthenticated.value) {
        router.push('/login');
        return;
      }

      if (userData.value) {
        // Use cached data
        this.fullName = `${userData.value.first_name} ${userData.value.last_name}`;
        this.email = userData.value.email;
        this.company = userData.value.company_name;
        this.loading = false; // Data loaded, hide the loading indicator
      } else {
        // Fetch data from the API
        await fetchUserData();
        if (userData.value) {
          this.fullName = `${userData.value.first_name} ${userData.value.last_name}`;
          this.email = userData.value.email;
          this.company = userData.value.company_name;
          this.loading = false; // Data loaded, hide the loading indicator
        } else {
          console.error("Failed to fetch user data.");
          this.logout();
        }
      }
    },
    logout() {
      apiRequest('/api/logout', 'post').then(() => {
        this.$router.push('/login');
      }).catch((error) => {
        console.error("Logout failed:", error);
      });
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  text-align: center;
}

.loading-indicator {
  padding: 20px;
  text-align: center;
  font-size: 20px;
}

button {
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
