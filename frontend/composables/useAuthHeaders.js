import { useAuthStore } from '../stores/auth'

/**
 * Composable pour récupérer les headers d'authentification avec tokens CSRF et Auth
 * À utiliser dans toutes les requêtes API nécessitant une authentification
 */
export const useAuthHeaders = () => {
  const authStore = useAuthStore()

  /**
   * Récupère les headers d'authentification complets
   * @returns {Promise<Object>} Headers avec CSRF et Authorization
   */
  const getAuthHeaders = async () => {
    const authToken = authStore.token || localStorage.getItem('token')
    
    // Récupérer un nouveau token CSRF depuis l'API
    let csrfToken = null
    try {
      console.log('🔄 Récupération du token CSRF...')
      const csrfResponse = await fetch('http://127.0.0.1:8000/api/auth/csrf/', {
        method: 'GET',
        credentials: 'include'
      })
      
      if (csrfResponse.ok) {
        const csrfData = await csrfResponse.json()
        csrfToken = csrfData.csrfToken
        console.log('🔑 Token CSRF récupéré:', csrfToken ? 'OK' : 'VIDE')
        
        // Stocker le token pour les prochaines requêtes
        if (csrfToken) {
          localStorage.setItem('csrfToken', csrfToken)
        }
      } else {
        console.warn('⚠️ Impossible de récupérer le token CSRF:', csrfResponse.status)
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération du token CSRF:', error)
    }
    
    // Fallback vers les sources locales si la récupération API échoue
    if (!csrfToken) {
      csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                  document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
                  localStorage.getItem('csrfToken')
      
      if (csrfToken) {
        console.log('🔄 Token CSRF récupéré depuis le cache/DOM')
      } else {
        console.warn('⚠️ Aucun token CSRF disponible')
      }
    }
    
    // Préparer les headers avec tous les tokens nécessaires
    const headers = {
      'Content-Type': 'application/json'
    }
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }
    
    if (authToken) {
      headers['Authorization'] = `Token ${authToken}`
    }
    
    console.log('📋 Headers préparés:', {
      'Content-Type': headers['Content-Type'],
      'X-CSRFToken': headers['X-CSRFToken'] ? 'OK' : 'MANQUANT',
      'Authorization': headers['Authorization'] ? 'OK' : 'MANQUANT'
    })
    
    return headers
  }

  /**
   * Fait une requête API avec authentification automatique
   * @param {string} url - URL de l'API
   * @param {Object} options - Options de fetch (method, body, etc.)
   * @returns {Promise<Response>} Réponse de fetch
   */
  const authenticatedFetch = async (url, options = {}) => {
    const headers = await getAuthHeaders()
    
    // Merger les headers personnalisés avec les headers d'auth
    const finalHeaders = {
      ...headers,
      ...options.headers
    }
    
    return fetch(url, {
      ...options,
      headers: finalHeaders,
      credentials: 'include' // Toujours inclure les cookies
    })
  }

  return {
    getAuthHeaders,
    authenticatedFetch
  }
}
