<!-- src/components/HomePage.vue -->

<template>
  <div class="home">
    <h1>Welcome!</h1>
    <!-- <h1>Welcome to Our Application!</h1> -->
    <!-- Conditionally render buttons based on authentication status -->
    <!-- <button v-if="!isAuthenticated" @click="goToSignup">Sign Up</button> -->
    <!-- <button v-if="!isAuthenticated" @click="goToLogin">Log In</button> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Check local storage for authentication token to determine if user is authenticated
      isAuthenticated: localStorage.getItem('access_token') ? true : false
    };
  },
  methods: {
    goToSignup() {
      this.$router.push('/signup');
    },
    goToLogin() {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
</style>
