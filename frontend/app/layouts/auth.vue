<template>
  <div class="auth-layout">
    <!-- Contenu principal sans navbar et footer -->
    <main class="auth-main">
      <slot />
    </main>
  </div>
</template>

<script setup>
// Meta tags par défaut pour les pages d'auth
useHead({
  htmlAttrs: {
    lang: 'fr'
  },
  meta: [
    { name: 'format-detection', content: 'telephone=no' }
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
  margin: 0;
  padding: 0;
}

/* Layout d'authentification */
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 2rem 1rem;
}

.auth-main {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
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

/* Responsive */
@media (max-width: 768px) {
  .auth-layout {
    padding: 1rem;
  }
}
</style>
