<template>
  <div class="register-page">
    <AuthSignupForm />
  </div>
</template>

<script setup>
import AuthSignupForm from '../../components/auth/SignupForm.vue'

definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

useHead({
  title: 'Inscription - GVB Sign',
  meta: [{ name: 'description', content: 'Créez votre compte GVB Sign pour accéder à vos documents sécurisés.' }]
})
</script>

<style scoped>
.register-page {
  width: 100%;
}
</style>
