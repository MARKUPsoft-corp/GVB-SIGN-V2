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
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      
      let csrfToken = null
      if (csrfResponse.ok) {
        const csrfData = await csrfResponse.json()
        csrfToken = csrfData.csrfToken
      }

      const headers = {
        'Content-Type': 'application/json',
      }
      
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken
      }

      console.log('📤 Envoi des données de mise à jour:', organizationData)
      console.log('📤 Headers:', headers)
      console.log('📤 URL:', `${API_BASE_URL}/organizations/${organizationId}/update/`)

      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/update/`, {
        method: 'PUT',
        headers,
        credentials: 'include',
        body: JSON.stringify(organizationData)
      })

      console.log('📥 Réponse du serveur:', response.status, response.statusText)

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
  static async deleteOrganization(organizationId, password) {
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
      }

      const headers = {
        'Content-Type': 'application/json',
      }
      
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken
      }

      // Inclure le mot de passe dans le body
      const requestData = {
        password: password
      }

      console.log('📤 Suppression organisation - ID:', organizationId)
      console.log('📤 Mot de passe fourni:', password ? 'Oui' : 'Non')

      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/delete/`, {
        method: 'DELETE',
        headers,
        credentials: 'include',
        body: JSON.stringify(requestData)
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
   * Récupérer une organisation spécifique
   */
  static async getOrganization(organizationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Récupérer les codes d'invitation d'une organisation
   */
  static async getInvitationCodes(organizationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/invitations/list/?organization_id=${organizationId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la récupération des codes d\'invitation:', error)
      throw error
    }
  }

  /**
   * Désactiver un code d'invitation
   */
  static async deactivateInvitationCode(codeId) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      const csrfData = await csrfResponse.json()
      const csrfToken = csrfData.csrfToken

      console.log('🔍 Désactivation code d\'invitation:', codeId)
      console.log('🔍 Token CSRF:', csrfToken)

      const response = await fetch(`${API_BASE_URL}/organizations/invitations/${codeId}/deactivate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la désactivation du code d\'invitation:', error)
      throw error
    }
  }

  /**
   * Réactiver un code d'invitation
   */
  static async reactivateInvitationCode(codeId) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      const csrfData = await csrfResponse.json()
      const csrfToken = csrfData.csrfToken

      console.log('🔍 Réactivation code d\'invitation:', codeId)
      console.log('🔍 Token CSRF:', csrfToken)

      const response = await fetch(`${API_BASE_URL}/organizations/invitations/${codeId}/reactivate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la réactivation du code d\'invitation:', error)
      throw error
    }
  }

  /**
   * Supprimer un code d'invitation
   */
  static async deleteInvitationCode(codeId) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      const csrfData = await csrfResponse.json()
      const csrfToken = csrfData.csrfToken

      console.log('🔍 Suppression code d\'invitation:', codeId)
      console.log('🔍 Token CSRF:', csrfToken)

      const response = await fetch(`${API_BASE_URL}/organizations/invitations/${codeId}/delete/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la suppression du code d\'invitation:', error)
      throw error
    }
  }

  /**
   * Récupérer les certificats d'une organisation
   */
  static async getOrganizationCertificates(organizationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/certificates/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la récupération des certificats:', error)
      throw error
    }
  }

  /**
   * Créer un certificat pour une organisation
   */
  static async createOrganizationCertificate(organizationId, certificateData) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      const csrfData = await csrfResponse.json()
      const csrfToken = csrfData.csrfToken

      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/certificates/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(certificateData)
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la création du certificat:', error)
      throw error
    }
  }

  /**
   * Supprimer un certificat d'organisation
   */
  static async deleteOrganizationCertificate(organizationId, certificateId) {
    try {
      // Récupérer le token CSRF
      const csrfResponse = await fetch(`${API_BASE_URL}/auth/csrf/`, {
        method: 'GET',
        credentials: 'include'
      })
      const csrfData = await csrfResponse.json()
      const csrfToken = csrfData.csrfToken

      const response = await fetch(`${API_BASE_URL}/organizations/${organizationId}/certificates/${certificateId}/delete/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include'
      })
  
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
  
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Erreur lors de la suppression du certificat:', error)
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
