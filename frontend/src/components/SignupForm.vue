<!-- src/components/SignupForm.vue -->

<template>
  <div class="signup-form-container">
    <h2>Join Us</h2>
    <form @submit.prevent="handleSubmit" class="signup-form">
      <div class="input-group">
        <input type="email" id="email" v-model="email" required placeholder="Email" aria-label="Email"/>
      </div>
      <div class="input-group">
        <input type="password" id="password" v-model="password" required placeholder="Password" aria-label="Password"/>
      </div>
      <div class="name-group">
        <div class="input-group half-width">
          <input type="text" id="first-name" v-model="first_name" placeholder="First Name" aria-label="First Name"/>
        </div>
        <div class="input-group half-width">
          <input type="text" id="last-name" v-model="last_name" placeholder="Last Name" aria-label="Last Name"/>
        </div>
      </div>
      <div class="input-group">
        <input type="text" id="company-name" v-model="company_name" placeholder="Company Name" aria-label="Company Name"/>
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <div class="button-container">
        <button type="submit" class="submit-btn">Sign Up</button>
      </div>
    </form>
  </div>
</template>

<script>
import { registerUser, validateUserInput, redirectToDashboard, resetFormData } from '../api';

export default {
  data() {
    return {
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      company_name: '',
      errorMessage: ''
    };
  },
  methods: {
    async handleSubmit() {
      const { isValid, message } = validateUserInput(this.email, this.password);
      if (!isValid) {
        this.$toast.open({
          message: message,
          type: 'error',
          duration: 5000
        });
        return;
      }

      const { success, error } = await registerUser({
        email: this.email,
        password: this.password,
        first_name: this.first_name,
        last_name: this.last_name,
        company_name: this.company_name
      });

      if (success) {
        this.$toast.open({
          message: 'Registration Successful!',
          type: 'success',
          duration: 5000
        });
        redirectToDashboard();
        resetFormData(this.$data);
      } else {
        this.$toast.open({
          message: error,
          type: 'error',
          duration: 5000
        });
      }
    }
  }
};
</script>

<style scoped>
</style>
