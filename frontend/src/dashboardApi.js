// dashboardApi.js

import axios from 'axios';

// This file can include API calls, utility functions, and any other interactions specific to the dashboard

// Example function to fetch user-specific data (placeholder for actual implementation)
export async function fetchUserData(access_token) {
  // Ensure you're using the full URL with the environment variable
  const baseUrl = process.env.VUE_APP_API_URL || 'http://localhost:5000'; // Default URL in case the env variable is not set
  try {
    const response = await axios.get(`${baseUrl}/api/userdata`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    return null; // or handle error as needed
  }
}

