<template>
  <div class="layout-wrapper">
    <!-- Navigation -->
    <SharedNavbar />
    
    <!-- Contenu principal -->
    <main class="main-content">
      <slot />
    </main>
    
    <!-- Footer -->
    <SharedFooter />
  </div>
</template>

<script setup>
// Import explicite des composants
import SharedNavbar from '../../components/shared/Navbar.vue'
import SharedFooter from '../../components/shared/Footer.vue'

// Meta tags par défaut
useHead({
  htmlAttrs: {
    lang: 'fr'
  },
  meta: [
    { name: 'format-detection', content: 'telephone=no' }
  ],
  link: [
    { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
    { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Raleway:wght@100;200;300;400;500;600;700;800;900&display=swap' },
    { rel: 'icon', type: 'image/png', href: '/gvb-favicon-1755744029.png' },
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
})
</script>

<style>
/* Variables CSS intégrées */
:root {
  --primary-blue: #0066cc;
  --primary-blue-dark: #004d99;
  --primary-blue-light: #3385d6;
  --secondary-blue: #f0f8ff;
  --accent-blue: #007bff;
  --white: #ffffff;
  --light-gray: #f8f9fa;
  --dark-gray: #6c757d;
  --text-dark: #2c3e50;
  --gradient-primary: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
  --gradient-hero: linear-gradient(135deg, var(--primary-blue-dark) 0%, var(--primary-blue) 50%, var(--accent-blue) 100%);
  --shadow-light: rgba(0, 102, 204, 0.1);
  --shadow-medium: rgba(0, 102, 204, 0.2);
}

/* Styles de base */
body {
  font-family: 'Raleway', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-dark);
  background-color: var(--white);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.fade-in-up {
  animation: fadeInUp 0.8s ease-out;
}

.float-animation {
  animation: float 6s ease-in-out infinite;
}

/* Styles globaux pour le layout */
.layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 60px; /* Espace minimal pour la navbar fixe */
}

/* Scroll smooth pour toute la page */
html {
  scroll-behavior: smooth;
}

/* Styles pour la scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: var(--primary-blue);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--primary-blue-dark);
}

/* Amélioration de la performance des animations */
* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Classes utilitaires globales */
.text-primary-blue {
  color: var(--primary-blue) !important;
}

.bg-primary-blue {
  background-color: var(--primary-blue) !important;
}

.btn-primary-custom {
  background: var(--gradient-primary);
  border: none;
  color: white;
  font-weight: 600;
  padding: 12px 30px;
  border-radius: 50px;
  font-family: 'Raleway', sans-serif;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--shadow-medium);
  background: var(--primary-blue-dark);
  color: white;
}

.section-padding {
  padding: 5rem 0;
}

.section-padding-sm {
  padding: 3rem 0;
}

@media (max-width: 768px) {
  .main-content {
    padding-top: 50px;
  }
  
  .section-padding {
    padding: 3rem 0;
  }
  
  .section-padding-sm {
    padding: 2rem 0;
  }
}
</style>
