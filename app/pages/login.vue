<template>
  <div class="login-page">
    <!-- Contenu de la page de connexion -->
    <AuthLoginForm />
  </div>
</template>

<script setup>
// Import explicite du composant
import AuthLoginForm from '../../components/auth/LoginForm.vue'

// Définir le layout et le middleware
definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

// Meta tags pour la page de connexion
useHead({
  title: 'Connexion - GVB Sign',
  meta: [
    {
      name: 'description',
      content: 'Connectez-vous à votre compte GVB Sign pour accéder à vos documents sécurisés.'
    }
  ]
})
</script>

<style scoped>
.login-page {
  width: 100%;
}

/* Animation pour l'entrée de la page */
.login-page {
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
</style>
