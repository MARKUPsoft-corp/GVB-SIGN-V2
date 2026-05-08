import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    token: null
  }),

  getters: {
    getUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    // Initialiser l'authentification depuis le localStorage
    async initAuth() {
      if (process.client) {
        const savedUser = localStorage.getItem('user')
        const savedToken = localStorage.getItem('token')
        
        if (savedUser && savedToken) {
          try {
            // Vérifier si la session Django est toujours valide
            const response = await fetch('http://92.112.184.194:8000/api/auth/profile/', {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
              credentials: 'include'
            })

            if (response.ok) {
              // Session Django valide, restaurer l'état local
              this.user = JSON.parse(savedUser)
              this.token = savedToken
              this.isAuthenticated = true
              return true
            } else {
              // Session Django invalide, nettoyer le localStorage
              console.log('Session Django expirée, nettoyage du localStorage')
              this.clearAuth()
              return false
            }
          } catch (error) {
            console.error('Erreur lors de la vérification de la session:', error)
            this.clearAuth()
            return false
          }
        }
      }
      return false
    },

    // Vérifier la session en arrière-plan (non bloquant)
    async verifySessionInBackground() {
      if (process.client && this.isAuthenticated) {
        try {
          const response = await fetch('http://:8000/api/auth/profile/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include'
          })

          if (!response.ok) {
            console.log('Session Django expirée en arrière-plan, nettoyage du localStorage')
            this.clearAuth()
            // Rediriger vers login seulement si on n'est pas déjà sur une page d'auth
            if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
              await navigateTo('/login')
            }
          }
        } catch (error) {
          console.error('Erreur lors de la vérification de session en arrière-plan:', error)
          // Ne pas nettoyer automatiquement en cas d'erreur réseau
        }
      }
    },

    // Connexion
    async login(credentials) {
      try {
        console.log('🔄 Tentative de connexion avec:', credentials)
        
        // Récupérer le token CSRF
        const csrfResponse = await fetch('http://92.112.184.194:8000/api/auth/csrf/', {
          method: 'GET',
          credentials: 'include'
        })
        
        let csrfToken = null
        if (csrfResponse.ok) {
          const csrfData = await csrfResponse.json()
          csrfToken = csrfData.csrfToken
          console.log('🔑 Token CSRF récupéré:', csrfToken)
        } else {
          console.warn('⚠️ Impossible de récupérer le token CSRF')
        }
        
        const headers = {
          'Content-Type': 'application/json',
        }
        
        if (csrfToken) {
          headers['X-CSRFToken'] = csrfToken
        }
        
        const response = await fetch('http://92.112.184.194:8000/api/auth/login/', {
          method: 'POST',
          headers,
          credentials: 'include',
          body: JSON.stringify(credentials)
        })

        console.log('📡 Réponse HTTP:', response.status, response.statusText)
        console.log('📋 Headers de réponse:', Object.fromEntries(response.headers.entries()))

        // Vérifier si la réponse est OK avant de parser JSON
        if (!response.ok) {
          console.error('❌ Réponse HTTP non-OK:', response.status)
          const errorText = await response.text()
          console.error('❌ Contenu de l\'erreur:', errorText)
          return { 
            success: false, 
            message: `Erreur HTTP ${response.status}: ${response.statusText}`,
            status: response.status
          }
        }

        const result = await response.json()
        console.log('📦 Résultat JSON:', result)

        if (result.success) {
          const userData = {
            id: result.user.id,
            email: result.user.email,
            full_name: result.user.full_name || `${result.user.first_name} ${result.user.last_name}`,
            first_name: result.user.first_name,
            last_name: result.user.last_name
          }
          
          this.setUser(userData, result.token || 'authenticated')
          console.log('✅ Connexion réussie!')
          return { success: true, user: userData }
        } else {
          console.log('❌ Échec de connexion dans la réponse:', result)
          return { success: false, errors: result.errors, message: result.message }
        }
      } catch (error) {
        console.error('💥 Erreur de connexion:', error)
        return { success: false, message: 'Erreur de connexion au serveur' }
      }
    },

    // Inscription
    async register(userData) {
      try {
        console.log('🔄 Tentative d\'inscription avec:', userData)
        
        // Récupérer le token CSRF
        const csrfResponse = await fetch('http://92.112.184.194:8000/api/auth/csrf/', {
          method: 'GET',
          credentials: 'include'
        })
        
        let csrfToken = null
        if (csrfResponse.ok) {
          const csrfData = await csrfResponse.json()
          csrfToken = csrfData.csrfToken
          console.log('🔑 Token CSRF récupéré:', csrfToken)
        } else {
          console.warn('⚠️ Impossible de récupérer le token CSRF')
        }
        
        const headers = {
          'Content-Type': 'application/json',
        }
        
        if (csrfToken) {
          headers['X-CSRFToken'] = csrfToken
        }
        
        const response = await fetch('http://92.112.184.194/api/auth/register/', {
          method: 'POST',
          headers,
          credentials: 'include',
          body: JSON.stringify(userData)
        })

        console.log('📡 Réponse HTTP:', response.status, response.statusText)
        console.log('📋 Headers de réponse:', Object.fromEntries(response.headers.entries()))

        // Vérifier si la réponse est OK avant de parser JSON
        if (!response.ok) {
          console.error('❌ Réponse HTTP non-OK:', response.status)
          const errorText = await response.text()
          console.error('❌ Contenu de l\'erreur:', errorText)
          return { 
            success: false, 
            message: `Erreur HTTP ${response.status}: ${response.statusText}`,
            status: response.status
          }
        }

        const result = await response.json()
        console.log('📦 Résultat JSON:', result)

        if (result.success) {
          const user = {
            id: result.user.id,
            email: result.user.email,
            full_name: result.user.full_name || `${userData.first_name} ${userData.last_name}`,
            first_name: result.user.first_name || userData.first_name,
            last_name: result.user.last_name || userData.last_name
          }
          
          this.setUserDirect(user, result.token || 'authenticated')
          console.log('✅ Inscription réussie!')
          return { success: true, user }
        } else {
          console.log('❌ Échec d\'inscription dans la réponse:', result)
          return { success: false, errors: result.errors, message: result.message }
        }
      } catch (error) {
        console.error('💥 Erreur d\'inscription:', error)
        return { success: false, message: 'Erreur de connexion au serveur' }
      }
    },

    // Définir l'utilisateur
    setUser(userData, token = 'authenticated') {
      this.user = userData
      this.token = token
      this.isAuthenticated = true
      
      // Sauvegarder dans localStorage
      if (process.client) {
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('token', token)
      }
    },

    // Définir l'utilisateur sans vérification de session (pour l'inscription)
    setUserDirect(userData, token = 'authenticated') {
      this.user = userData
      this.token = token
      this.isAuthenticated = true
      
      // Sauvegarder dans localStorage
      if (process.client) {
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('token', token)
      }
    },

    // Déconnexion
    async logout() {
      try {
        // Appel API de déconnexion
        await fetch('http://92.112.184.194:8000/api/auth/logout/', {
          method: 'POST',
          credentials: 'include'
        })
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
      } finally {
        // Nettoyer complètement l'état même si l'API échoue
        this.clearAllData()
      }
    },

    // Rafraîchir la session (pour éviter les expirations)
    async refreshSession() {
      if (process.client && this.isAuthenticated) {
        try {
          const response = await fetch('http://92.112.184.194:8000/api/auth/profile/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include'
          })

          if (response.ok) {
            console.log('✅ Session rafraîchie avec succès')
            return true
          } else {
            console.log('❌ Session expirée, nettoyage nécessaire')
            this.clearAuth()
            return false
          }
        } catch (error) {
          console.error('Erreur lors du rafraîchissement de session:', error)
          return false
        }
      }
      return false
    },

    // Nettoyer l'authentification (version optimisée)
    clearAuth() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // Nettoyer seulement les données d'authentification essentielles
      if (process.client) {
        // Nettoyer les données d'authentification
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        
        // Nettoyer les données de session
        localStorage.removeItem('sessionId')
        localStorage.removeItem('csrfToken')
        
        console.log('🧹 Session d\'authentification effacée')
      }
    },

    // Nettoyer complètement (pour déconnexion volontaire)
    clearAllData() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // Nettoyer complètement le localStorage et sessionStorage
      if (process.client) {
        // Nettoyer les données d'authentification
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        
        // Nettoyer les données d'organisation
        localStorage.removeItem('user_has_organization')
        localStorage.removeItem('user_organization')
        
        // Nettoyer les données de certificat
        localStorage.removeItem('certificate')
        localStorage.removeItem('certificateInfo')
        localStorage.removeItem('privateKey')
        localStorage.removeItem('publicKey')
        
        // Nettoyer les données de signature
        localStorage.removeItem('signatureResults')
        localStorage.removeItem('uploadedFiles')
        localStorage.removeItem('signatureData')
        
        // Nettoyer les données de session
        localStorage.removeItem('sessionId')
        localStorage.removeItem('csrfToken')
        
        // Nettoyer le sessionStorage également
        sessionStorage.clear()
        
        // Nettoyer tous les cookies (si possible côté client)
        document.cookie.split(";").forEach(function(c) { 
          document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        })
        
        console.log('🧹 Session complètement effacée du navigateur')
      }
    }
  }
})
