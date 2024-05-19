// src/api.js

import axios from 'axios';
import router from './router';

axios.defaults.withCredentials = true;

// Function to validate user input
export function validateUserInput(email, password) {
  if (!email || !password) {
    return { isValid: false, message: 'Email and password are required.' };
  }
  if (!email.includes('@')) {
    return { isValid: false, message: 'Please enter a valid email.' };
  }
  if (password.length < 8) {
    return { isValid: false, message: 'Password must be at least 8 characters.' };
  }
  return { isValid: true, message: '' };
}

// Function to handle API requests for registration
export async function registerUser(userData) {
  try {
    const response = await axios({
      method: 'post',
      url: `${process.env.VUE_APP_API_URL}/api/register`,  // Use environment variable
      data: userData,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token); // Store access_token if present
    }
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response ? error.response.data : 'Server error',
    };
  }
}

// Function to handle API requests
export async function apiRequest(url, method, data = null) {
  const fullUrl = `${process.env.VUE_APP_API_URL}${url}`;
  console.log("Request URL:", fullUrl); // Log the URL
  try {
    const response = await axios({
      method: method,
      url: fullUrl,
      data: method.toLowerCase() === 'get' ? null : data, // Only include data for non-GET requests
      headers: {
        'Content-Type': 'application/json',
      }
    });
    console.log("Response Data:", response.data); // Log the response data
    return { success: true, data: response.data, error: null };
  } catch (error) {
    console.error("Axios Error:", error); // Log the axios error to the console
    console.log("Error Response:", error.response); // Log the error response
    return {
      success: false,
      data: null,
      error: handleError(error),
    };
  }
}

// Function to handle and parse errors
function handleError(error) {
  if (error.response) {
    return error.response.data.error || error.response.data.message || `Server responded with status: ${error.response.status}`;
  } else if (error.request) {
    return 'No response from the server, check network.';
  } else {
    return error.message;
  }
}

// Redirect function
export function redirectToDashboard() {
  router.push('/dashboard');
}

// Reset form data function for reuse in components
export function resetFormData(dataObject) {
  for (const key in dataObject) {
    dataObject[key] = '';
  }
}

// Function to save API key
export async function saveApiKey(apiKey, jiraDomain, jiraEmail) {
  return await apiRequest('/api/save_api_key', 'post', { api_key: apiKey, jira_domain: jiraDomain, jira_email: jiraEmail });
}

// Function to get API key
export async function getApiKey() {
  return await apiRequest('/api/get_api_key', 'get');
}
