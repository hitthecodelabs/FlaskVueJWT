<!-- src/components/DashboardPage.vue -->

<template>
  <div class="dashboard-container">
    <div v-if="loading" class="loading-indicator">
      <p>Loading...</p>
    </div>
    <div v-else>
      <h1>Welcome to Your Dashboard, {{ fullName }}!</h1>
      <p>Email: {{ email }}</p>
      <p>Company: {{ company }}</p>
      <div v-if="jiraUser">
        <h2>Jira Information</h2>
        <p>Display Name: {{ jiraUser.displayName }}</p>
        <p>Email Address: {{ jiraUser.emailAddress }}</p>
        <p>Account ID: {{ jiraUser.accountId }}</p>
        <p>Time Zone: {{ jiraUser.timeZone }}</p>
        <img :src="jiraUser.avatarUrls['48x48']" alt="User Avatar" />
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { apiRequest } from '../api';

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
  computed: {
    jiraUser() {
      const { jiraUser } = useAuthStore();
      return jiraUser.value;
    }
  },
  methods: {
    async initializeDashboard() {
      const { isAuthenticated, checkAuth, userData, fetchUserData, fetchJiraUserInfo } = useAuthStore();
      const router = useRouter();
      await checkAuth(); // Ensure the auth state is updated

      if (!isAuthenticated.value) {
        router.push('/login');
        return;
      }

      if (userData.value) {
        // Use cached data
        this.fullName = `${userData.value.first_name} ${userData.value.last_name}`;
        this.email = userData.value.email;
        this.company = userData.value.company_name;
      } else {
        // Fetch data from the API
        await fetchUserData();
        if (userData.value) {
          this.fullName = `${userData.value.first_name} ${userData.value.last_name}`;
          this.email = userData.value.email;
          this.company = userData.value.company_name;
        } else {
          console.error("Failed to fetch user data.");
          this.logout();
        }
      }

      // Fetch Jira user info if not already in cache
      await fetchJiraUserInfo();
      this.loading = false; // Data loaded, hide the loading indicator
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
