const API_BASE_URL = 'http://127.0.0.1:8000/api'

class OrganizationApiService {
  /**
   * Créer une nouvelle organisation
   */
  static async createOrganization(organizationData) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      
      let csrfToken = null
      if (csrfResponse.ok) {
        const csrfData = await csrfResponse.json()
        csrfToken = csrfData.csrfToken
        console.log('🔑 Token CSRF récupéré pour organisation:', csrfToken)
      } else {
        console.warn('⚠️ Impossible de récupérer le token CSRF pour organisation')
      }

      const headers = {
        'Content-Type': 'application/json',
      }
      
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken
      }

      console.log('📤 Envoi des données d\'organisation:', organizationData)
      console.log('📤 Headers:', headers)

      const response = await fetch(`${API_BASE_URL}/organizations/create/`, {
        method: 'POST',
        headers,
        credentials: 'include',
        body: JSON.stringify(organizationData)
      })

      console.log('📥 Réponse du serveur:', response.status, response.statusText)

      const data = await response.json()
      console.log('📥 Données reçues:', data)
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de la création de l\'organisation')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de la création de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Récupérer l'organisation de l'utilisateur connecté
   */
  static async getUserOrganization() {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/my-organization/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de la récupération de l\'organisation')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Mettre à jour une organisation
   */
  static async updateOrganization(organizationId, organizationData) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(organizationData)
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de la mise à jour de l\'organisation')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de la mise à jour de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Supprimer une organisation
   */
  static async deleteOrganization(organizationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/delete/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de la suppression de l\'organisation')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Récupérer les membres d'une organisation
   */
  static async getOrganizationMembers(organizationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/members/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de la récupération des membres')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de la récupération des membres:', error)
      throw error
    }
  }

  /**
   * Rejoindre une organisation avec un code d'invitation
   */
  static async joinOrganization(inviteCode) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/join/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ invite_code: inviteCode })
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de l\'adhésion à l\'organisation')
      }

      return data
    } catch (error) {
      console.error('Erreur lors de l\'adhésion à l\'organisation:', error)
      throw error
    }
  }
}

export default OrganizationApiService
