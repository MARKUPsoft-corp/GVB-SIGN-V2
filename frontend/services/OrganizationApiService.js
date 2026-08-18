import { getFirestore, collection, doc, setDoc, getDoc, getDocs, updateDoc, deleteDoc, query, where, serverTimestamp, addDoc, collectionGroup, onSnapshot, orderBy } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'
import { initializeApp, getApps, getApp } from 'firebase/app'

class OrganizationApiService {
  /**
   * Helper: Récupère l'instance Firestore et Auth (vérifie qu'on est côté client)
   */
  static getFirebase() {
    if (process.server) throw new Error("Ne peut pas être appelé côté serveur")
    
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
    
    return {
      db: getFirestore(),
      auth: getAuth()
    }
  }

  /**
   * Helper: Récupère l'utilisateur actuellement connecté
   */
  static getCurrentUser(auth) {
    const user = auth.currentUser
    if (!user) throw new Error("Utilisateur non connecté")
    return user
  }

  /**
   * Créer une nouvelle organisation
   */
  static async createOrganization(organizationData) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)

      // Créer une nouvelle référence de document pour l'organisation
      const orgRef = doc(collection(db, 'organizations'))
      const orgId = orgRef.id

      const orgDoc = {
        id: orgId,
        name: organizationData.name,
        description: organizationData.description || '',
        email: organizationData.email || '',
        phone: organizationData.phone || '',
        address: organizationData.address || '',
        website: organizationData.website || '',
        organization_type: organizationData.organization_type || '',
        industry: organizationData.sector || organizationData.industry || '',
        size: organizationData.size || '',
        ownerId: user.uid,
        approval_status: 'pending', // Nouveau statut pour validation par le super-admin
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }

      await setDoc(orgRef, orgDoc)

      // Mettre à jour l'utilisateur pour l'assigner à cette organisation en tant que propriétaire/admin
      const userRef = doc(db, 'users', user.uid)
      await setDoc(userRef, {
        organizationId: orgId,
        role: 'admin', // Le créateur est l'administrateur
        updated_at: new Date().toISOString()
      }, { merge: true })

      console.log('✅ Organisation créée dans Firestore:', orgDoc)
      return orgDoc
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
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)

      // Récupérer le document utilisateur pour avoir son organizationId
      const userDocRef = doc(db, 'users', user.uid)
      const userDocSnap = await getDoc(userDocRef)

      if (!userDocSnap.exists() || !userDocSnap.data().organizationId) {
        throw new Error("L'utilisateur n'appartient à aucune organisation")
      }

      const orgId = userDocSnap.data().organizationId

      // Récupérer l'organisation
      const orgRef = doc(db, 'organizations', orgId)
      const orgSnap = await getDoc(orgRef)

      if (!orgSnap.exists()) {
        throw new Error("Organisation introuvable")
      }

      return { id: orgSnap.id, ...orgSnap.data() }
    } catch (error) {
      if (error.message !== "L'utilisateur n'appartient à aucune organisation") {
        console.error('Erreur lors de la récupération de l\'organisation:', error)
      }
      throw error
    }
  }

  /**
   * Écouter l'organisation de l'utilisateur connecté en temps réel
   */
  static listenUserOrganization(callback, errorCallback) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)

      const userDocRef = doc(db, 'users', user.uid)
      let orgUnsubscribe = null

      const userUnsubscribe = onSnapshot(userDocRef, (userDocSnap) => {
        if (!userDocSnap.exists() || !userDocSnap.data().organizationId) {
          if (orgUnsubscribe) {
            orgUnsubscribe()
            orgUnsubscribe = null
          }
          callback(null)
          return
        }

        const orgId = userDocSnap.data().organizationId
        const userRole = userDocSnap.data().role || 'member'
        const orgRef = doc(db, 'organizations', orgId)

        if (orgUnsubscribe) orgUnsubscribe()

        orgUnsubscribe = onSnapshot(orgRef, (orgSnap) => {
          if (orgSnap.exists()) {
            callback({ id: orgSnap.id, ...orgSnap.data(), role: userRole })
          } else {
            callback(null)
          }
        }, (error) => {
          if (errorCallback) errorCallback(error)
        })
      }, (error) => {
        if (errorCallback) errorCallback(error)
      })

      // Retourner une fonction pour tout nettoyer
      return () => {
        if (userUnsubscribe) userUnsubscribe()
        if (orgUnsubscribe) orgUnsubscribe()
      }
    } catch (error) {
      if (errorCallback) errorCallback(error)
      return () => {}
    }
  }

  /**
   * Mettre à jour une organisation
   */
  static async updateOrganization(organizationId, organizationData) {
    try {
      const { db } = this.getFirebase()
      const orgRef = doc(db, 'organizations', organizationId)
      
      const updateData = {
        ...organizationData,
        updated_at: new Date().toISOString()
      }
      
      await updateDoc(orgRef, updateData)

      // Récupérer la nouvelle version pour la retourner
      const orgSnap = await getDoc(orgRef)
      return orgSnap.data()
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
      const { db, auth } = this.getFirebase()
      const orgRef = doc(db, 'organizations', organizationId)
      
      await deleteDoc(orgRef)
      
      // Mettre à jour l'utilisateur pour supprimer sa référence à l'organisation
      const user = this.getCurrentUser(auth)
      const userRef = doc(db, 'users', user.uid)
      
      await updateDoc(userRef, {
        organizationId: null,
        role: 'member'
      })
      
      return { success: true, message: "Organisation supprimée avec succès" }
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
      const { db } = this.getFirebase()
      const orgRef = doc(db, 'organizations', organizationId)
      const orgSnap = await getDoc(orgRef)
      
      if (!orgSnap.exists()) {
        throw new Error("Organisation introuvable")
      }
      return orgSnap.data()
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
      const { db } = this.getFirebase()
      const invitationsRef = collection(db, 'organizations', organizationId, 'invitations')
      const snapshot = await getDocs(invitationsRef)
      
      const codes = []
      snapshot.forEach(doc => {
        codes.push({ id: doc.id, ...doc.data() })
      })
      
      return codes
    } catch (error) {
      console.error('Erreur lors de la récupération des codes d\'invitation:', error)
      throw error
    }
  }

  /**
   * Écouter les codes d'invitation d'une organisation en temps réel
   */
  static listenInvitationCodes(organizationId, callback, errorCallback) {
    try {
      const { db } = this.getFirebase()
      const invitationsRef = collection(db, 'organizations', organizationId, 'invitations')
      
      return onSnapshot(invitationsRef, (snapshot) => {
        const codes = []
        snapshot.forEach(doc => {
          codes.push({ id: doc.id, ...doc.data() })
        })
        callback(codes)
      }, errorCallback)
    } catch (error) {
      console.error('Erreur lors de l\'écoute des codes d\'invitation:', error)
      if (errorCallback) errorCallback(error)
      throw error
    }
  }

  /**
   * Désactiver un code d'invitation
   */
  static async deactivateInvitationCode(codeId) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      const userDocSnap = await getDoc(doc(db, 'users', user.uid))
      const orgId = userDocSnap.data().organizationId

      const codeRef = doc(db, 'organizations', orgId, 'invitations', codeId)
      await updateDoc(codeRef, { is_active: false })
      
      const snap = await getDoc(codeRef)
      return { id: snap.id, ...snap.data() }
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
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      const userDocSnap = await getDoc(doc(db, 'users', user.uid))
      const orgId = userDocSnap.data().organizationId

      const codeRef = doc(db, 'organizations', orgId, 'invitations', codeId)
      await updateDoc(codeRef, { is_active: true })
      
      const snap = await getDoc(codeRef)
      return { id: snap.id, ...snap.data() }
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
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      const userDocSnap = await getDoc(doc(db, 'users', user.uid))
      const orgId = userDocSnap.data().organizationId

      const codeRef = doc(db, 'organizations', orgId, 'invitations', codeId)
      await deleteDoc(codeRef)
      
      return { success: true }
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
      const { db } = this.getFirebase()
      const certsRef = collection(db, 'organizations', organizationId, 'certificates')
      const snapshot = await getDocs(certsRef)
      
      const certificates = []
      snapshot.forEach(doc => {
        certificates.push({ id: doc.id, ...doc.data() })
      })
      
      return certificates
    } catch (error) {
      console.error('Erreur lors de la récupération des certificats:', error)
      throw error
    }
  }

  /**
   * Écouter les certificats d'une organisation en temps réel
   */
  static listenOrganizationCertificates(organizationId, callback, errorCallback) {
    try {
      const { db } = this.getFirebase()
      const certsRef = collection(db, 'organizations', organizationId, 'certificates')
      
      return onSnapshot(certsRef, (snapshot) => {
        const certs = []
        snapshot.forEach(doc => {
          certs.push({ id: doc.id, ...doc.data() })
        })
        callback(certs)
      }, errorCallback)
    } catch (error) {
      console.error('Erreur lors de l\'écoute des certificats:', error)
      if (errorCallback) errorCallback(error)
      throw error
    }
  }

  /**
   * Créer un certificat pour une organisation
   */
  static async createOrganizationCertificate(organizationId, certificateData) {
    try {
      const { db } = this.getFirebase()
      const certsRef = collection(db, 'organizations', organizationId, 'certificates')
      
      const dataToSave = {
        ...certificateData,
        created_at: new Date().toISOString()
      }
      
      const docRef = await addDoc(certsRef, dataToSave)
      return { id: docRef.id, ...dataToSave }
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
      const { db } = this.getFirebase()
      const certRef = doc(db, 'organizations', organizationId, 'certificates', certificateId)
      await deleteDoc(certRef)
      return { success: true }
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
      const { db } = this.getFirebase()
      
      // On requête la collection globale 'users' où organizationId correspond
      const usersRef = collection(db, 'users')
      const q = query(usersRef, where('organizationId', '==', organizationId))
      const snapshot = await getDocs(q)
      
      const members = []
      snapshot.forEach(doc => {
        const data = doc.data()
        members.push({
          id: doc.id,
          name: data.displayName || 'Utilisateur',
          email: data.email,
          role: data.role || 'member'
        })
      })
      
      return members
    } catch (error) {
      console.error('Erreur lors de la récupération des membres:', error)
      throw error
    }
  }

  /**
   * Écouter les membres d'une organisation en temps réel
   */
  static listenOrganizationMembers(organizationId, callback, errorCallback) {
    try {
      const { db } = this.getFirebase()
      const usersRef = collection(db, 'users')
      const q = query(usersRef, where('organizationId', '==', organizationId))
      
      return onSnapshot(q, (snapshot) => {
        const members = []
        snapshot.forEach(doc => {
          members.push({ id: doc.id, ...doc.data() })
        })
        callback(members)
      }, errorCallback)
    } catch (error) {
      console.error('Erreur lors de l\'écoute des membres:', error)
      if (errorCallback) errorCallback(error)
      throw error
    }
  }

  /**
   * Rejoindre une organisation avec un code d'invitation
   */
  static async joinOrganization(inviteCode) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      
      // Note: Il n'y a pas de "collection group query" par défaut qui soit rapide sans index.
      // Pour retrouver l'orga à partir du code, on pourrait l'avoir de manière globale ou scanner
      // Par simplicité, si on a un objet "invitations" global ça serait plus simple,
      // sinon on doit faire une Collection Group Query sur "invitations"
      const invitationsQuery = query(collectionGroup(db, 'invitations'), where('code', '==', inviteCode), where('is_active', '==', true))
      // TODO: Pour éviter des erreurs complexes, vous devez créer l'index Collection Group pour 'invitations'
      // dans la console Firebase. 
      
      const snapshot = await getDocs(invitationsQuery)
      if (snapshot.empty) {
        throw new Error("Code d'invitation invalide ou expiré")
      }
      
      const inviteDoc = snapshot.docs[0]
      const inviteData = inviteDoc.data()
      const organizationId = inviteDoc.ref.parent.parent.id // remonter vers orgRef
      const roleToAssign = inviteData.role || 'member'
      
      // Mettre à jour l'utilisateur courant
      const userRef = doc(db, 'users', user.uid)
      await setDoc(userRef, {
        organizationId: organizationId,
        role: roleToAssign,
        updated_at: new Date().toISOString()
      }, { merge: true })
      
      return { success: true, organizationId }
    } catch (error) {
      console.error('Erreur lors de l\'adhésion à l\'organisation:', error)
      throw error
    }
  }

  /**
   * Récupérer toutes les organisations approuvées
   */
  static async getAllOrganizations() {
    try {
      const { db } = this.getFirebase()
      const orgsRef = collection(db, 'organizations')
      const snapshot = await getDocs(orgsRef)
      
      const organizations = []
      snapshot.forEach(doc => {
        const data = doc.data()
        // Dans un flux réel, on filtre par approval_status == 'approved'
        if (data.approval_status !== 'rejected') {
          organizations.push({ id: doc.id, ...data })
        }
      })
      
      return organizations
    } catch (error) {
      console.error('Erreur lors de la récupération de toutes les organisations:', error)
      throw error
    }
  }

  /**
   * Vérifier l'adhésion d'un utilisateur à une organisation
   */
  static async checkMembership(organizationId) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      
      // Vérifier si l'utilisateur est déjà membre
      const userDocSnap = await getDoc(doc(db, 'users', user.uid))
      const userData = userDocSnap.data()
      if (userData && userData.organizationId === organizationId) {
        return { success: true, is_member: true, has_pending_request: false }
      }
      
      // Vérifier s'il y a une demande en attente
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      const q = query(requestsRef, where('userId', '==', user.uid), where('status', '==', 'pending'))
      const snapshot = await getDocs(q)
      
      if (!snapshot.empty) {
        return { success: true, is_member: false, has_pending_request: true }
      }
      
      return { success: true, is_member: false, has_pending_request: false }
    } catch (error) {
      console.error('Erreur lors de la vérification de l\'adhésion:', error)
      throw error
    }
  }

  /**
   * Demander l'adhésion à une organisation
   */
  static async requestMembership(organizationId, role, message) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      await addDoc(requestsRef, {
        userId: user.uid,
        userName: user.displayName || 'Utilisateur',
        userEmail: user.email,
        requestedRole: role,
        message: message,
        status: 'pending',
        createdAt: serverTimestamp()
      })
      
      return { success: true, message: "Demande d'adhésion envoyée avec succès" }
    } catch (error) {
      console.error('Erreur lors de la demande d\'adhésion:', error)
      throw error
    }
  }

  /**
   * Quitter une organisation
   */
  static async leaveOrganization(organizationId) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      
      const userRef = doc(db, 'users', user.uid)
      await updateDoc(userRef, {
        organizationId: null,
        role: null
      })
      
      return { success: true, message: "Vous avez quitté l'organisation avec succès" }
    } catch (error) {
      console.error('Erreur lors du départ de l\'organisation:', error)
      throw error
    }
  }

  /**
   * Récupérer les demandes d'adhésion en attente
   */
  static async getPendingMembershipRequests(organizationId) {
    try {
      const { db } = this.getFirebase()
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      const q = query(requestsRef, where('status', '==', 'pending'))
      
      const snapshot = await getDocs(q)
      const requests = []
      snapshot.forEach(doc => {
        requests.push({ id: doc.id, ...doc.data() })
      })
      
      return { success: true, requests }
    } catch (error) {
      console.error('Erreur getPendingMembershipRequests:', error)
      throw error
    }
  }

  /**
   * Écouter les demandes d'adhésion en attente en temps réel
   */
  static listenPendingMembershipRequests(organizationId, callback, errorCallback) {
    try {
      const { db } = this.getFirebase()
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      const q = query(requestsRef, where('status', '==', 'pending'))
      
      return onSnapshot(q, (snapshot) => {
        const requests = []
        snapshot.forEach(doc => {
          requests.push({ id: doc.id, ...doc.data() })
        })
        callback({ success: true, requests })
      }, errorCallback)
    } catch (error) {
      console.error('Erreur listenPendingMembershipRequests:', error)
      if (errorCallback) errorCallback(error)
      throw error
    }
  }

  /**
   * Récupérer les demandes d'adhésion rejetées
   */
  static async getRejectedMembershipRequests(organizationId) {
    try {
      const { db } = this.getFirebase()
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      const q = query(requestsRef, where('status', '==', 'rejected'))
      
      const snapshot = await getDocs(q)
      const requests = []
      snapshot.forEach(doc => {
        requests.push({ id: doc.id, ...doc.data() })
      })
      
      return { success: true, requests }
    } catch (error) {
      console.error('Erreur getRejectedMembershipRequests:', error)
      throw error
    }
  }

  /**
   * Écouter les demandes d'adhésion rejetées en temps réel
   */
  static listenRejectedMembershipRequests(organizationId, callback, errorCallback) {
    try {
      const { db } = this.getFirebase()
      const requestsRef = collection(db, 'organizations', organizationId, 'membership_requests')
      const q = query(requestsRef, where('status', '==', 'rejected'))
      
      return onSnapshot(q, (snapshot) => {
        const requests = []
        snapshot.forEach(doc => {
          requests.push({ id: doc.id, ...doc.data() })
        })
        callback({ success: true, requests })
      }, errorCallback)
    } catch (error) {
      console.error('Erreur listenRejectedMembershipRequests:', error)
      if (errorCallback) errorCallback(error)
      throw error
    }
  }

  /**
   * Approuver une demande d'adhésion
   */
  static async approveMembershipRequest(organizationId, requestId, userId, role) {
    try {
      const { db } = this.getFirebase()
      
      // Mettre à jour la demande
      const requestRef = doc(db, 'organizations', organizationId, 'membership_requests', requestId)
      await updateDoc(requestRef, {
        status: 'approved',
        updatedAt: serverTimestamp()
      })
      
      // Mettre à jour l'utilisateur
      const userRef = doc(db, 'users', userId)
      await updateDoc(userRef, {
        organizationId: organizationId,
        role: role || 'member'
      })
      
      return { success: true, message: 'Demande approuvée avec succès' }
    } catch (error) {
      console.error('Erreur approveMembershipRequest:', error)
      throw error
    }
  }

  /**
   * Rejeter une demande d'adhésion
   */
  static async rejectMembershipRequest(organizationId, requestId) {
    try {
      const { db } = this.getFirebase()
      const requestRef = doc(db, 'organizations', organizationId, 'membership_requests', requestId)
      
      await updateDoc(requestRef, {
        status: 'rejected',
        updatedAt: serverTimestamp()
      })
      
      return { success: true, message: 'Demande rejetée' }
    } catch (error) {
      console.error('Erreur rejectMembershipRequest:', error)
      throw error
    }
  }

  /**
   * Créer une invitation
   */
  static async createInvitation(organizationId, role, expiresAt) {
    try {
      const { db, auth } = this.getFirebase()
      const user = this.getCurrentUser(auth)
      
      // Générer un code unique (ex: INV-XXXX)
      const code = 'INV-' + Math.random().toString(36).substring(2, 8).toUpperCase()
      
      const invitationsRef = collection(db, 'organizations', organizationId, 'invitations')
      await addDoc(invitationsRef, {
        code: code,
        role: role,
        expiresAt: expiresAt,
        createdBy: user.uid,
        status: 'active',
        is_active: true,
        createdAt: serverTimestamp()
      })
      
      return { 
        success: true, 
        invitation: {
          code: code,
          role: role,
          expires_at: expiresAt
        } 
      }
    } catch (error) {
      console.error('Erreur createInvitation:', error)
      throw error
    }
  }

  /**
   * SUPER ADMIN : Écouter toutes les organisations en temps réel
   * @param {Function} callback Fonction appelée avec les nouvelles données
   * @returns {Function} Fonction pour se désabonner (unsubscribe)
   */
  static listenAllOrganizations(callback) {
    try {
      const { db } = this.getFirebase()
      const orgsRef = collection(db, 'organizations')
      
      // On peut ajouter orderBy si nécessaire, mais on fera le tri côté client pour plus de flexibilité
      const unsubscribe = onSnapshot(orgsRef, (snapshot) => {
        const organizations = []
        snapshot.forEach((doc) => {
          organizations.push({ id: doc.id, ...doc.data() })
        })
        callback(organizations)
      }, (error) => {
        console.error('Erreur listenAllOrganizations:', error)
      })
      
      return unsubscribe
    } catch (error) {
      console.error('Erreur lors de l\'initialisation de l\'écouteur d\'organisations:', error)
      throw error
    }
  }

  /**
   * SUPER ADMIN : Valider une organisation
   */
  static async validateOrganization(organizationId) {
    try {
      const { db } = this.getFirebase()
      const orgRef = doc(db, 'organizations', organizationId)
      
      await updateDoc(orgRef, {
        approval_status: 'approved',
        updated_at: new Date().toISOString()
      })
      
      return { success: true }
    } catch (error) {
      console.error('Erreur lors de la validation de l\'organisation:', error)
      throw error
    }
  }

  /**
   * SUPER ADMIN : Rejeter une organisation
   */
  static async rejectOrganization(organizationId) {
    try {
      const { db } = this.getFirebase()
      const orgRef = doc(db, 'organizations', organizationId)
      
      await updateDoc(orgRef, {
        approval_status: 'rejected',
        updated_at: new Date().toISOString()
      })
      
      return { success: true }
    } catch (error) {
      console.error('Erreur lors du rejet de l\'organisation:', error)
      throw error
    }
  }

}

export default OrganizationApiService
