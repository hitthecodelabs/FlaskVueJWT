<!-- src/components/SabeApiKey.vue -->

<template>
  <div class="signup-form-container api-key-management">
    <div v-if="loading" class="loading-indicator">
      <p>Loading...</p>
    </div>
    <div v-else>
      <h2>Jira API Key Management</h2>
      <form @submit.prevent="saveApiKey">
        <div class="input-group">
          <label for="jiraDomain">Jira Domain:</label>
          <input type="text" v-model="jiraDomain" required />
        </div>
        <div class="input-group">
          <label for="jiraEmail">Jira Email:</label>
          <input type="email" v-model="jiraEmail" required />
        </div>
        <div class="input-group">
          <label for="apiKey">API Key:</label>
          <input type="text" v-model="apiKey" required />
        </div>
        <div class="button-container">
          <button type="submit" class="submit-btn">Save</button>
        </div>
      </form>
      <div v-if="message" :class="{'success-message': success, 'error-message': !success}">
        {{ message }}
      </div>
      <div v-if="displayApiKey" class="current-api-key">
        <h3>Current API Key</h3>
        <p>{{ maskedApiKey }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { saveApiKey, getApiKey } from '@/api';

export default {
  data() {
    return {
      jiraDomain: '',
      jiraEmail: '',
      apiKey: '',
      displayApiKey: '',
      showApiKey: false,
      message: '',
      success: false,
      loading: true,
      cachedApiKey: localStorage.getItem('cachedApiKey') || null, // Initialize cache from localStorage
      cachedJiraDomain: localStorage.getItem('cachedJiraDomain') || null,
      cachedJiraEmail: localStorage.getItem('cachedJiraEmail') || null
    };
  },
  computed: {
    maskedApiKey() {
      if (this.showApiKey) {
        return this.displayApiKey;
      } else {
        return `${this.displayApiKey.slice(0, 4)}****${this.displayApiKey.slice(-4)}`;
      }
    }
  },
  methods: {
    async saveApiKey() {
      const response = await saveApiKey(this.apiKey, this.jiraDomain, this.jiraEmail);
      if (response.success) {
        this.message = response.data.message;
        this.success = true;
        this.cachedApiKey = this.apiKey;
        this.cachedJiraDomain = this.jiraDomain;
        this.cachedJiraEmail = this.jiraEmail;
        localStorage.setItem('cachedApiKey', this.apiKey); // Update cache in localStorage
        localStorage.setItem('cachedJiraDomain', this.jiraDomain);
        localStorage.setItem('cachedJiraEmail', this.jiraEmail);
        await this.fetchApiKey(); // Refresh the displayed API key
      } else {
        this.message = response.error;
        this.success = false;
      }
    },
    async fetchApiKey() {
      if (this.cachedApiKey) {
        // Use cached API key
        this.displayApiKey = this.cachedApiKey;
        this.jiraDomain = this.cachedJiraDomain;
        this.jiraEmail = this.cachedJiraEmail;
        this.loading = false; // Data loaded, hide loading indicator
      } else {
        const response = await getApiKey();
        if (response.success) {
          this.displayApiKey = response.data.api_key;
          this.jiraDomain = response.data.jira_domain;
          this.jiraEmail = response.data.jira_email;
          this.cachedApiKey = response.data.api_key;
          this.cachedJiraDomain = response.data.jira_domain;
          this.cachedJiraEmail = response.data.jira_email;
          localStorage.setItem('cachedApiKey', response.data.api_key); // Cache API key
          localStorage.setItem('cachedJiraDomain', response.data.jira_domain);
          localStorage.setItem('cachedJiraEmail', response.data.jira_email);
        } else {
          this.displayApiKey = '';
          this.jiraDomain = '';
          this.jiraEmail = '';
        }
        this.loading = false; // Data loaded, hide loading indicator
      }
    },
    toggleShowApiKey() {
      this.showApiKey = !this.showApiKey;
    }
  },
  async mounted() {
    await this.fetchApiKey();
  }
};
</script>

<style scoped>
.api-key-management {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f7f7f7;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #444;
  font-size: 14px;
}

.input-group input[type="text"],
.input-group input[type="email"] {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.input-group input:focus {
  border-color: #0056b3;
}

.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.submit-btn {
  width: auto;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 5px;
  color: #fff;
  background-color: #007bff;
  font-size: 1rem;
  letter-spacing: 0.05rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.submit-btn:hover {
  background-color: #003975;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.success-message {
  color: green;
  margin-top: 10px;
  text-align: center;
}

.error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
}

.current-api-key {
  margin-top: 20px;
  text-align: center;
}

.loading-indicator {
  padding: 20px;
  text-align: center;
  font-size: 20px;
}
</style>
  
