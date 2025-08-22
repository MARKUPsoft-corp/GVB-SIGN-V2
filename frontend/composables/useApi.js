// Composable pour les appels API
export const useApi = () => {
  const API_BASE_URL = 'http://127.0.0.1:8000/api'

  // Configuration par défaut pour fetch
  const defaultFetchOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Pour les cookies de session
  }

  // Fonction utilitaire pour les appels API
  const apiCall = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`
    
    const fetchOptions = {
      ...defaultFetchOptions,
      ...options,
      headers: {
        ...defaultFetchOptions.headers,
        ...options.headers,
      }
    }

    try {
      const response = await fetch(url, fetchOptions)
      const data = await response.json()
      
      return {
        success: response.ok,
        status: response.status,
        data,
      }
    } catch (error) {
      console.error('Erreur API:', error)
      return {
        success: false,
        status: 0,
        data: { message: 'Erreur de connexion au serveur' },
      }
    }
  }

  // API d'authentification
  const auth = {
    // Inscription
    register: async (userData) => {
      return await apiCall('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(userData),
      })
    },

    // Connexion
    login: async (credentials) => {
      return await apiCall('/auth/login/', {
        method: 'POST',
        body: JSON.stringify(credentials),
      })
    },

    // Déconnexion
    logout: async () => {
      return await apiCall('/auth/logout/', {
        method: 'POST',
      })
    },

    // Profil utilisateur
    profile: async () => {
      return await apiCall('/auth/profile/')
    },

    // Vérifier si email existe
    checkEmail: async (email) => {
      return await apiCall(`/auth/check-email/?email=${encodeURIComponent(email)}`)
    }
  }

  return {
    apiCall,
    auth,
  }
}
