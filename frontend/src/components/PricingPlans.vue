<!-- src/components/PricingPlan.vue -->

<template>
  <div class="pricing-plans">
    <h2>Pricing Plans</h2>
    <p>Choose the plan that best suits your needs:</p>
    <div class="plan-container">
      <div class="plan most-popular" v-for="plan in pricingPlans" :key="plan.title">
        <h3>{{ plan.title }}</h3>
        <div class="plan__price">
          <span v-if="!plan.pricePerAgent">{{ plan.price }}</span>
          <span v-else>
            ${{ plan.pricePerAgent }}
            <span>/agent/month</span>
          </span>
        </div>
        <ul>
          <li v-for="feature in plan.features" :key="feature">{{ feature }}</li>
        </ul>
        <button>{{ plan.buttonText }}</button>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  data() {
    return {
      pricingPlans: [
        {
          title: "Free Plan",
          price: "Free",
          features: [
            "Ideal for small teams and startups",
            "Up to 300 tickets per month",
            "Limited to one agent",
            "Access to essential features to get you started",
          ],
          buttonText: "Sign Up",
        },
        {
          title: "Pay-Per-Agent Plan",
          pricePerAgent: 75,
          features: [
            "Unlimited tickets",
            "Perfect for businesses with a consistent level of ticket volume",
            "Access to all features for seamless IT support management",
          ],
          buttonText: "Get Started",
        },
        {
          title: "Enterprise Plan",
          price: "Contact Us",
          features: [
            "Customizable features and integrations",
          "Dedicated account manager",
          "Priority support",
          "Advanced security features",
          ],
          buttonText: "Contact Sales",
        },
      ],
    };
  },
};
</script>
  
<style scoped>
</style>