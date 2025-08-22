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
            this.user = JSON.parse(savedUser)
            this.token = savedToken
            this.isAuthenticated = true
            return true
          } catch (error) {
            console.error('Erreur lors de la récupération des données:', error)
            this.clearAuth()
            return false
          }
        }
      }
      return false
    },

    // Connexion
    async login(credentials) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify(credentials)
        })

        const result = await response.json()

        if (response.ok && result.success) {
          const userData = {
            id: result.user.id,
            email: result.user.email,
            full_name: result.user.full_name || `${result.user.first_name} ${result.user.last_name}`,
            first_name: result.user.first_name,
            last_name: result.user.last_name
          }
          
          this.setUser(userData, result.token || 'authenticated')
          return { success: true, user: userData }
        } else {
          return { success: false, errors: result.errors, message: result.message }
        }
      } catch (error) {
        console.error('Erreur de connexion:', error)
        return { success: false, message: 'Erreur de connexion au serveur' }
      }
    },

    // Inscription
    async register(userData) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify(userData)
        })

        const result = await response.json()

        if (response.ok && result.success) {
          const user = {
            id: result.user.id,
            email: result.user.email,
            full_name: result.user.full_name || `${userData.first_name} ${userData.last_name}`,
            first_name: result.user.first_name || userData.first_name,
            last_name: result.user.last_name || userData.last_name
          }
          
          this.setUser(user, result.token || 'authenticated')
          return { success: true, user }
        } else {
          return { success: false, errors: result.errors, message: result.message }
        }
      } catch (error) {
        console.error('Erreur d\'inscription:', error)
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

    // Déconnexion
    async logout() {
      try {
        // Appel API de déconnexion
        await fetch('http://127.0.0.1:8000/api/auth/logout/', {
          method: 'POST',
          credentials: 'include'
        })
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
      } finally {
        // Nettoyer l'état même si l'API échoue
        this.clearAuth()
      }
    },

    // Nettoyer l'authentification
    clearAuth() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // Nettoyer le localStorage
      if (process.client) {
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      }
    }
  }
})
