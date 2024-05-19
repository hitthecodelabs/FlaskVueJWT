<!-- src/components/ContactUs.vue -->

<template>
  <div class="contact-us">
    <h2>Contact Us</h2>
    <p>Have any questions or need help getting started? Reach out to us!</p>
    <ul class="contact-info">
      <li>
        <svg class="icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M2.5 3a1.5 1.5 0 00-1.5 1.5v10a1.5 1.5 0 003 3L16.5 6.5a1.5 1.5 0 00-2.121-2.121L2.5 3z" clip-rule="evenodd"></path>
          <path d="M15 8a1.5 1.5 0 01-1.5-1.5V2.5a1.5 1.5 0 00-3 3L4.5 13.5a1.5 1.5 0 012.121 2.121L15 8z"></path>
        </svg>
        Email: <a href="mailto:info@quikzer.com">info@quikzer.com</a>
      </li>
      </ul>
    <p>
      For other inquiries, please fill out the form below and we'll get back to you
      shortly.
    </p>
    <form class="contact-form">
      <button type="submit">Send Message</button>
    </form>
  </div>
</template>
  
  <script>
  export default {
    // No data or methods required for this simple page
  };
  </script>
  
  <style scoped>
  /* Styles for the Contact Us section */
  </style>
  
