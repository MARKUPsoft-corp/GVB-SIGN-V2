<template>
  <div class="login-page">
    <!-- Contenu de la page de connexion -->
    <AuthLoginForm />
  </div>
</template>

<script setup>
// Import explicite du composant
import AuthLoginForm from '../../components/auth/LoginForm.vue'
import { useI18n } from '../../composables/useI18n'

const { locale } = useI18n()

// Définir le layout et le middleware
definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

// Meta tags pour la page de connexion
useHead(() => ({
  title: locale.value === 'fr' ? 'Connexion - GVB Sign' : 'Login - GVB Sign',
  meta: [
    {
      name: 'description',
      content: locale.value === 'fr' 
        ? 'Connectez-vous à votre compte GVB Sign pour accéder à vos documents sécurisés.' 
        : 'Sign in to your GVB Sign account to access your secured documents.'
    }
  ]
}))
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
