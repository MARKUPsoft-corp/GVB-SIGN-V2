<template>
  <div class="homepage">
    <!-- Hero Section -->
    <HomepageHeroSection />
    
    <!-- Features Section -->
    <HomepageFeaturesSection />
    
          <!-- Pricing Section -->
      <HomepagePricingSection />
      
      <!-- Contact Section -->
      <HomepageContactSection />
    </div>
  </template>

<script setup>
// Import explicite des composants
import HomepageHeroSection from '../../components/homepage/HeroSection.vue'
import HomepageFeaturesSection from '../../components/homepage/FeaturesSection.vue'
import HomepagePricingSection from '../../components/homepage/PricingSection.vue'
import HomepageContactSection from '../../components/homepage/ContactSection.vue'

// Meta tags pour la page d'accueil
import { useI18n } from '../../composables/useI18n'

const { locale } = useI18n()

useHead(() => ({
  title: locale.value === 'fr' 
    ? 'GVB Sign - Solution de Signature Électronique Innovante' 
    : 'GVB Sign - Innovative Electronic Signature Solution',
  meta: [
    {
      name: 'description',
      content: locale.value === 'fr'
        ? 'Révolutionnez vos signatures avec GVB Sign. Technologie QR Code, sécurité maximale, signature instantanée.'
        : 'Revolutionize your signatures with GVB Sign. QR Code technology, maximum security, instant signature.'
    }
  ]
}))
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
