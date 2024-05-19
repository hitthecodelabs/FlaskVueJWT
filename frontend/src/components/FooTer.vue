<!-- src/components/FooTer.vue -->

<template>
    <footer class="footer">
      <div class="footer-content">
        <p>© {{ currentYear }} Quikzer. All rights reserved.</p>
        <p>221 West Lake Lansing Road Suite 200 East Lansing, MI 48823</p> <ul class="footer-links">
          <li><router-link to="/about">About Us</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
          <li><router-link to="/privacy">Privacy Policy</router-link></li>
        </ul>
      </div>
    </footer>
</template>
  
<script>
export default {
data() {
    return {
    currentYear: new Date().getFullYear()
    };
}
};
</script>

<style scoped>
/* Styles already imported in main.js, no need to duplicate here */
</style>
  
  
