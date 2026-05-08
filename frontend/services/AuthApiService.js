/**
 * Service API pour l'authentification avec système de tokens
 */
class AuthApiService {
  constructor() {
    this.baseURL = 'http://92.112.184.194:8000/api/auth'
  }

  /**
   * Récupérer le token depuis le localStorage
   */
  getToken() {
    if (process.client) {
      return localStorage.getItem('token')
    }
    return null
  }

  /**
   * Créer les headers avec le token d'authentification
   */
  getAuthHeaders() {
    const token = this.getToken()
    const headers = {
      'Content-Type': 'application/json',
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    return headers
  }

  /**
   * Connexion utilisateur
   */
  async login(credentials) {
    try {
      const response = await fetch(`${this.baseURL}/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...credentials,
          device_info: {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            timestamp: new Date().toISOString()
          }
        })
      })

      const result = await response.json()
      
      if (result.success) {
        // Sauvegarder le token
        if (process.client) {
          localStorage.setItem('token', result.token)
          localStorage.setItem('tokenExpiresAt', result.expires_at)
        }
      }
      
      return result
    } catch (error) {
      console.error('Erreur lors de la connexion:', error)
      return { success: false, message: 'Erreur de connexion au serveur' }
    }
  }

  /**
   * Déconnexion utilisateur
   */
  async logout() {
    try {
      const response = await fetch(`${this.baseURL}/logout/`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })

      const result = await response.json()
      
      // Nettoyer le token local
      if (process.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('tokenExpiresAt')
      }
      
      return result
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
      return { success: false, message: 'Erreur de déconnexion' }
    }
  }

  /**
   * Récupérer le profil utilisateur
   */
  async getProfile() {
    try {
      const response = await fetch(`${this.baseURL}/profile/`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })

      if (response.ok) {
        return await response.json()
      } else {
        return { success: false, message: 'Token invalide ou expiré' }
      }
    } catch (error) {
      console.error('Erreur lors de la récupération du profil:', error)
      return { success: false, message: 'Erreur de connexion au serveur' }
    }
  }

  /**
   * Valider un token
   */
  async validateToken(token) {
    try {
      const response = await fetch(`${this.baseURL}/validate-token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token })
      })

      return await response.json()
    } catch (error) {
      console.error('Erreur lors de la validation du token:', error)
      return { success: false, valid: false, message: 'Erreur de validation' }
    }
  }

  /**
   * Rafraîchir un token
   */
  async refreshToken() {
    try {
      const response = await fetch(`${this.baseURL}/refresh-token/`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })

      const result = await response.json()
      
      if (result.success) {
        // Sauvegarder le nouveau token
        if (process.client) {
          localStorage.setItem('token', result.token)
          localStorage.setItem('tokenExpiresAt', result.expires_at)
        }
      }
      
      return result
    } catch (error) {
      console.error('Erreur lors du rafraîchissement du token:', error)
      return { success: false, message: 'Erreur de rafraîchissement' }
    }
  }

  /**
   * Récupérer les tokens de l'utilisateur
   */
  async getUserTokens() {
    try {
      const response = await fetch(`${this.baseURL}/user-tokens/`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })

      return await response.json()
    } catch (error) {
      console.error('Erreur lors de la récupération des tokens:', error)
      return { success: false, message: 'Erreur de récupération' }
    }
  }

  /**
   * Vérifier si le token est expiré
   */
  isTokenExpired() {
    if (process.client) {
      const expiresAt = localStorage.getItem('tokenExpiresAt')
      if (expiresAt) {
        const expirationDate = new Date(expiresAt)
        const now = new Date()
        return now >= expirationDate
      }
    }
    return true
  }

  /**
   * Vérifier si l'utilisateur est authentifié
   */
  async isAuthenticated() {
    const token = this.getToken()
    
    if (!token || this.isTokenExpired()) {
      return false
    }

    try {
      const result = await this.validateToken(token)
      return result.success && result.valid
    } catch (error) {
      console.error('Erreur lors de la vérification d\'authentification:', error)
      return false
    }
  }
}

// Export de l'instance unique
export default new AuthApiService()
