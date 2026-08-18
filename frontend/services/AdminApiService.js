import { getFirestore, collection, doc, updateDoc, onSnapshot } from 'firebase/firestore'
import { getApp, getApps } from 'firebase/app'

class AdminApiService {
  /**
   * Helper: Récupère l'instance Firestore
   */
  static getDb() {
    if (process.server) throw new Error("Ne peut pas être appelé côté serveur")
    
    if (!getApps().length) {
      throw new Error("Firebase n'est pas initialisé.")
    }
    
    const app = getApp()
    return getFirestore(app)
  }

  /**
   * SUPER ADMIN : Écouter tous les utilisateurs en temps réel
   * @param {Function} callback Fonction appelée avec les nouvelles données
   * @returns {Function} Fonction pour se désabonner (unsubscribe)
   */
  static listenAllUsers(callback) {
    try {
      const db = this.getDb()
      const usersRef = collection(db, 'users')
      
      const unsubscribe = onSnapshot(usersRef, (snapshot) => {
        const users = []
        snapshot.forEach((doc) => {
          users.push({ id: doc.id, ...doc.data() })
        })
        callback(users)
      }, (error) => {
        console.error('Erreur listenAllUsers:', error)
      })
      
      return unsubscribe
    } catch (error) {
      console.error('Erreur lors de l\'initialisation de l\'écouteur d\'utilisateurs:', error)
      throw error
    }
  }

  /**
   * SUPER ADMIN : Changer le rôle d'un utilisateur
   */
  static async updateUserRole(userId, newRole) {
    try {
      const db = this.getDb()
      const userRef = doc(db, 'users', userId)
      
      await updateDoc(userRef, {
        role: newRole,
        updatedAt: new Date().toISOString()
      })
      
      return { success: true }
    } catch (error) {
      console.error('Erreur lors de la mise à jour du rôle utilisateur:', error)
      throw error
    }
  }

  /**
   * SUPER ADMIN : Écouter toutes les signatures (historique global)
   * @param {Function} callback Fonction appelée avec les nouvelles données
   * @returns {Function} Fonction pour se désabonner (unsubscribe)
   */
  static listenAllSignatures(callback) {
    try {
      const db = this.getDb()
      const signaturesRef = collection(db, 'signatures')
      
      const unsubscribe = onSnapshot(signaturesRef, (snapshot) => {
        const signatures = []
        snapshot.forEach((doc) => {
          signatures.push({ id: doc.id, ...doc.data() })
        })
        callback(signatures)
      }, (error) => {
        console.error('Erreur listenAllSignatures:', error)
      })
      
      return unsubscribe
    } catch (error) {
      console.error('Erreur lors de l\'initialisation de l\'écouteur de signatures:', error)
      throw error
    }
  }
}

export default AdminApiService
