import { useAuthStore } from '../stores/auth'

export const useSessionRefresh = () => {
  const authStore = useAuthStore()
  let refreshInterval = null

  // Démarrer le rafraîchissement automatique de session
  const startSessionRefresh = () => {
    if (process.client && authStore.isAuthenticated) {
      // Rafraîchir la session toutes les 5 minutes
      refreshInterval = setInterval(async () => {
        await authStore.refreshSession()
      }, 5 * 60 * 1000) // 5 minutes
      
      console.log('🔄 Rafraîchissement automatique de session activé')
    }
  }

  // Arrêter le rafraîchissement automatique
  const stopSessionRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
      console.log('⏹️ Rafraîchissement automatique de session arrêté')
    }
  }

  // Rafraîchir manuellement la session
  const refreshSession = async () => {
    return await authStore.refreshSession()
  }

  // Nettoyer à la déconnexion
  const cleanup = () => {
    stopSessionRefresh()
  }

  return {
    startSessionRefresh,
    stopSessionRefresh,
    refreshSession,
    cleanup
  }
}
