<!-- src/components/LoginForm.vue -->

<template>
  <div class="signup-form-container">
    <h2>Login</h2>
    <form @submit.prevent="handleSubmit" class="signup-form">
      <div class="input-group">
        <input type="email" id="email" v-model="email" required placeholder="Email" aria-label="Email" autocomplete="off"/>
      </div>
      <div class="input-group">
        <input type="password" id="password" v-model="password" required placeholder="Password" aria-label="Password" autocomplete="off"/>
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <div class="button-container">
        <button type="submit" class="submit-btn">Login</button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiRequest } from '../api';
import { useAuthStore } from '@/store/auth';
import { useToast } from 'vue-toast-notification';

export default {
  setup() {
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();
    const { setAuth } = useAuthStore();

    const handleSubmit = async () => {
      const response = await apiRequest('/api/login', 'post', {
        email: email.value,
        password: password.value
      });

      if (response.success) {
        useToast().open({
          message: 'Login Successful!',
          type: 'success',
          duration: 1000
        });
        setAuth(true);
        router.push('/dashboard');
      } else {
        errorMessage.value = response.error || 'Login failed. Please check your email and password.';
        useToast().open({
          message: errorMessage.value,
          type: 'error',
          duration: 5000
        });
      }
    };

    return { email, password, errorMessage, handleSubmit };
  }
};
</script>

<style scoped>
/* Style content is minimal as styles are included globally */
</style>
