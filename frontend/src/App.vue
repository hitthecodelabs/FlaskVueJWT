<!-- src/App.vue -->

<template>
  <div id="app">
    <NavBar /> <!-- This will render the Navbar component -->
    <router-view /> <!-- This will render the matched component -->
    <FooTer />  <!-- Include the footer component here -->
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'; // Import the Navbar component
import FooTer from './components/FooTer.vue'; // Import the FooTer component

export default {
  name: 'App',
  components: {
    NavBar, // Register Navbar as a component used in App.vue
    FooTer
  }
};
</script>

<style scoped>
/* Styles already imported in main.js, no need to duplicate here */
</style>
