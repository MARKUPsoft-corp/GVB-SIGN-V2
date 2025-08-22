import { useAuthStore } from '../../stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Ne pas exécuter côté serveur
  if (process.server) return
  
  const authStore = useAuthStore()
  
  // Initialiser l'authentification depuis le localStorage
  await authStore.initAuth()
  
  // Si l'utilisateur n'est pas connecté, rediriger vers login
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
})
