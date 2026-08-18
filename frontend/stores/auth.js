import { defineStore } from 'pinia'
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } from 'firebase/auth'
import { initializeApp, getApps, getApp } from 'firebase/app'

const ensureFirebaseInitialized = () => {
  if (!getApps().length) {
    const config = useRuntimeConfig()
    initializeApp({
      apiKey: config.public.firebaseApiKey,
      authDomain: config.public.firebaseAuthDomain,
      projectId: config.public.firebaseProjectId,
      storageBucket: config.public.firebaseStorageBucket,
      messagingSenderId: config.public.firebaseMessagingSenderId,
      appId: config.public.firebaseAppId,
      measurementId: config.public.firebaseMeasurementId
    })
  }
}
import { getFirestore, doc, setDoc, getDoc, serverTimestamp } from 'firebase/firestore'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    authInitialized: false
  }),

  getters: {
    getUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    // Initialise l'écouteur d'état d'authentification Firebase
    initAuth() {
      return new Promise((resolve) => {
        if (process.server) return resolve(false);
        
        // Ne pas initialiser plusieurs fois
        if (this.authInitialized) {
          return resolve(this.isAuthenticated);
        }
        
        try {
          ensureFirebaseInitialized()
          const auth = getAuth()
          onAuthStateChanged(auth, async (firebaseUser) => {
            if (firebaseUser) {
              const db = getFirestore()
              const userRef = doc(db, 'users', firebaseUser.uid)
              
              try {
                const userSnap = await getDoc(userRef)
                let role = 'member'
                if (userSnap.exists()) {
                  role = userSnap.data().role || 'member'
                }
                
                // L'utilisateur est connecté
                this.user = {
                  uid: firebaseUser.uid,
                  email: firebaseUser.email,
                  displayName: firebaseUser.displayName,
                  photoURL: firebaseUser.photoURL,
                  role: role
                }
                this.isAuthenticated = true
              } catch (e) {
                console.error("Erreur lors de la récupération du rôle:", e)
                // Fallback de sécurité
                this.user = {
                  uid: firebaseUser.uid,
                  email: firebaseUser.email,
                  displayName: firebaseUser.displayName,
                  photoURL: firebaseUser.photoURL,
                  role: 'member'
                }
                this.isAuthenticated = true
              }
            } else {
              // L'utilisateur est déconnecté
              this.user = null
              this.isAuthenticated = false
            }
            this.authInitialized = true
            resolve(this.isAuthenticated)
          }, (error) => {
            console.error("Erreur onAuthStateChanged:", error)
            this.authInitialized = true
            resolve(false)
          })
        } catch (error) {
          console.error("Erreur critique initAuth:", error)
          this.authInitialized = true
          resolve(false)
        }
      })
    },

    // Connexion avec Google (gère aussi l'inscription implicitement)
    async loginWithGoogle() {
      try {
        ensureFirebaseInitialized()
        const auth = getAuth()
        const provider = new GoogleAuthProvider()
        // Force la sélection du compte Google si l'utilisateur en a plusieurs
        provider.setCustomParameters({ prompt: 'select_account' })
        
        const result = await signInWithPopup(auth, provider)
        const user = result.user

        // Enregistrer l'utilisateur dans Firestore s'il est nouveau
        const db = getFirestore()
        const userRef = doc(db, 'users', user.uid)
        const userSnap = await getDoc(userRef)

        if (!userSnap.exists()) {
          // Nouvel utilisateur : on crée son profil dans Firestore
          await setDoc(userRef, {
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL,
            createdAt: serverTimestamp(),
            role: 'member' // Rôle par défaut
          })
        }

        this.user = {
          uid: user.uid,
          email: user.email,
          displayName: user.displayName,
          photoURL: user.photoURL,
          role: userSnap.exists() ? (userSnap.data().role || 'member') : 'member'
        }
        this.isAuthenticated = true
        
        return { success: true, user: this.user }
      } catch (error) {
        console.error('Erreur lors de la connexion avec Google:', error)
        return { success: false, message: error.message }
      }
    },

    // Déconnexion
    async logout() {
      try {
        ensureFirebaseInitialized()
        const auth = getAuth()
        await signOut(auth)
        this.clearAuth()
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
      }
    },

    // Nettoyer l'état local
    clearAuth() {
      this.user = null
      this.isAuthenticated = false
      
      if (process.client) {
        // Nettoyer les données locales
        localStorage.removeItem('user_has_organization')
        localStorage.removeItem('user_organization')
        localStorage.removeItem('certificateInfo')
        sessionStorage.clear()
      }
    },
    
    // Rafraîchir la session (rôle et token)
    async refreshSession() {
      if (process.server) return false;
      
      try {
        ensureFirebaseInitialized()
        const auth = getAuth()
        const firebaseUser = auth.currentUser
        
        if (firebaseUser) {
          // Forcer le rafraîchissement du token
          await firebaseUser.getIdToken(true)
          
          // Rafraîchir le rôle
          const db = getFirestore()
          const userRef = doc(db, 'users', firebaseUser.uid)
          const userSnap = await getDoc(userRef)
          
          if (userSnap.exists() && this.user) {
            this.user.role = userSnap.data().role || 'member'
          }
          return true
        }
        return false
      } catch (error) {
        console.error("Erreur refreshSession:", error)
        return false
      }
    }
  }
})
