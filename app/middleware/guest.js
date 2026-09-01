import { useAuthStore } from '../../stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  if (process.server) return
  
  const authStore = useAuthStore()
  
  try {
    if (!authStore.authInitialized) {
      await authStore.initAuth()
    }
  } catch (err) {
    console.error("Guest middleware error:", err)
  }
  
  if (authStore.isAuthenticated) {
    return navigateTo('/dashboard')
  }
})
