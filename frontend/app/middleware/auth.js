import { useAuthStore } from '../../stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Ne pas exécuter côté serveur
  if (process.server) return
  
  const authStore = useAuthStore()
  
  // Vérifier d'abord si on a des données en localStorage
  if (process.client) {
    const savedUser = localStorage.getItem('user')
    const savedToken = localStorage.getItem('token')
    
    if (savedUser && savedToken) {
      // Restaurer l'état sans faire d'appel API immédiat
      authStore.user = JSON.parse(savedUser)
      authStore.token = savedToken
      authStore.isAuthenticated = true
      
      // Vérifier la session en arrière-plan (non bloquant)
      authStore.verifySessionInBackground()
    } else {
      // Pas de données locales, rediriger vers login
      return navigateTo('/login')
    }
  }
  
  // Si l'utilisateur n'est pas connecté, rediriger vers login
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
})
