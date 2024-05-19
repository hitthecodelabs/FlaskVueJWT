// src/store/auth.js

import axios from 'axios';
import { apiRequest } from '../api';
import { reactive, toRefs } from 'vue';

const state = reactive({
  isAuthenticated: false,
  userData: null,
  jiraUser: null // Add Jira user state
});

const setAuth = (isAuth) => {
  state.isAuthenticated = isAuth;
};

const checkAuth = () => {
  const token = document.cookie.split(';').find(item => item.trim().startsWith('access_token='));
  setAuth(!!token);
};

const fetchUserData = async () => {
  const token = document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1];
  try {
    const response = await fetchUserDataFromApi(token);
    state.userData = response;
  } catch (error) {
    console.error("Error fetching user data:", error);
    state.userData = null;
  }
};

const fetchUserDataFromApi = async (token) => {
  const baseUrl = process.env.VUE_APP_API_URL || 'http://localhost:5000';
  try {
    const response = await axios.get(`${baseUrl}/api/userdata`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    return null;
  }
};

const fetchJiraUserInfo = async () => {
  if (!state.jiraUser) {
    try {
      const response = await apiRequest('/api/jira_user_info', 'get');
      if (response.success) {
        state.jiraUser = response.data;
      } else {
        console.error("Failed to fetch Jira user info:", response.error);
      }
    } catch (error) {
      console.error("Error fetching Jira user info:", error);
    }
  }
};

// Call checkAuth immediately to update state on initial load
checkAuth();

export const useAuthStore = () => {
  return {
    ...toRefs(state),
    setAuth,
    checkAuth,
    fetchUserData,
    fetchJiraUserInfo // Export the new function
  };
};
