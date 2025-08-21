<template>
  <div class="homepage">
    <!-- Hero Section -->
    <HomepageHeroSection />
    
    <!-- Features Section -->
    <HomepageFeaturesSection />
  </div>
</template>

<script setup>
// Import explicite des composants
import HomepageHeroSection from '../../components/homepage/HeroSection.vue'
import HomepageFeaturesSection from '../../components/homepage/FeaturesSection.vue'

// Meta tags pour la page d'accueil
useHead({
  title: 'GVB Sign - Solution de Signature Électronique Innovante',
  meta: [
    {
      name: 'description',
      content: 'Révolutionnez vos signatures avec GVB Sign. Technologie QR Code, sécurité maximale, signature instantanée.'
    }
  ]
})
</script>

<style scoped>
.homepage {
  overflow-x: hidden;
}

/* Animation pour l'entrée de la page */
.homepage {
  opacity: 0;
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Optimisation pour les transitions entre sections */
.homepage > * {
  will-change: transform;
}
</style>
