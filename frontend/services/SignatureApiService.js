/**
 * Service pour l'API des signatures de documents (Firebase)
 */
import { getApp } from 'firebase/app'
import { getFirestore, collection, addDoc, getDocs, getDoc, doc, query, where, serverTimestamp } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'
import CloudinaryService from './CloudinaryService'

export class SignatureApiService {
  constructor() {
    this.db = null
    this.auth = null
  }

  /**
   * Initialisation sécurisée de Firebase
   */
  getFirebase() {
    if (this.db && this.auth) return { db: this.db, auth: this.auth }
    
    try {
      const app = getApp()
      this.db = getFirestore(app)
      this.auth = getAuth(app)
      return { db: this.db, auth: this.auth }
    } catch (error) {
      console.warn("⚠️ [SignatureApiService] Firebase n'est pas encore initialisé, tentative d'initialisation via appNuxt...")
      throw new Error("Firebase n'est pas initialisé.")
    }
  }

  /**
   * Convertir un fichier en base64
   */
  async fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        const base64 = reader.result.split(',')[1]
        resolve(base64)
      }
      reader.onerror = error => reject(error)
    })
  }

  /**
   * Convertir des données Uint8Array en base64
   */
  uint8ArrayToBase64(uint8Array) {
    let binary = ''
    const bytes = new Uint8Array(uint8Array)
    const len = bytes.byteLength
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
  }

  /**
   * Enregistrer une signature de document dans Firestore
   */
  async saveDocumentSignature(signatureData) {
    try {
      const { db, auth } = this.getFirebase()
      const user = auth.currentUser

      if (!user) {
        throw new Error("Utilisateur non authentifié")
      }

      const signaturesRef = collection(db, 'signatures')
      
      const payload = {
        ...signatureData,
        userId: user.uid,
        createdAt: serverTimestamp()
      }

      const docRef = await addDoc(signaturesRef, payload)
      
      return {
        success: true,
        id: docRef.id,
        message: "Signature enregistrée avec succès"
      }
    } catch (error) {
      console.error('Erreur SignatureApiService.saveDocumentSignature:', error)
      throw error
    }
  }

  /**
   * Enregistrer plusieurs signatures en une fois
   */
  async saveMultipleSignatures(signaturesData) {
    try {
      const { db, auth } = this.getFirebase()
      const user = auth.currentUser

      if (!user) throw new Error("Utilisateur non authentifié")

      const signaturesRef = collection(db, 'signatures')
      const results = []

      // Dans un vrai environnement on utiliserait un writeBatch
      for (const sigData of signaturesData) {
        const docRef = await addDoc(signaturesRef, {
          ...sigData,
          userId: user.uid,
          createdAt: serverTimestamp()
        })
        results.push(docRef.id)
      }

      return {
        success: true,
        ids: results,
        message: `${results.length} signatures enregistrées`
      }
    } catch (error) {
      console.error('Erreur SignatureApiService.saveMultipleSignatures:', error)
      throw error
    }
  }

  /**
   * Récupérer la liste des signatures de l'utilisateur
   */
  async getUserSignatures() {
    try {
      const { db, auth } = this.getFirebase()
      const user = auth.currentUser

      if (!user) throw new Error("Utilisateur non authentifié")

      const signaturesRef = collection(db, 'signatures')
      const q = query(signaturesRef, where('userId', '==', user.uid))
      const snapshot = await getDocs(q)
      
      const signatures = []
      snapshot.forEach(doc => {
        signatures.push({
          id: doc.id,
          ...doc.data()
        })
      })

      return signatures
    } catch (error) {
      console.error('Erreur SignatureApiService.getUserSignatures:', error)
      throw error
    }
  }

  /**
   * Créer une préparation de document
   */
  async createDocumentPreparation(submissionData) {
    try {
      const { db, auth } = this.getFirebase()
      const user = auth.currentUser

      if (!user) {
        throw new Error('Utilisateur non connecté')
      }

      const prepRef = collection(db, 'document_preparations')
      
      const payload = {
        ...submissionData,
        userId: user.uid,
        status: 'prepared',
        current_step: 0,
        createdAt: serverTimestamp()
      }

      const docRef = await addDoc(prepRef, payload)
      
      return {
        success: true,
        document_preparation: {
          id: docRef.id,
          ...payload
        }
      }
    } catch (error) {
      console.error('Erreur SignatureApiService.createDocumentPreparation:', error)
      throw error
    }
  }
  
  /**
   * Récupérer les préparations de documents pour une organisation
   */
  async getDocumentPreparations(organizationId) {
    try {
      const { db } = this.getFirebase()
      const prepRef = collection(db, 'document_preparations')
      const q = query(prepRef, where('organization.id', '==', organizationId))
      
      const querySnapshot = await getDocs(q)
      const preparations = []
      
      querySnapshot.forEach((doc) => {
        const data = doc.data()
        // Filtrer côté client pour éviter les erreurs d'index composite Firestore
        if (['prepared', 'in_progress', 'pending_signature'].includes(data.status)) {
          preparations.push({
            id: doc.id,
            ...data
          })
        }
      })
      
      return { success: true, preparations }
    } catch (error) {
      console.error('Erreur SignatureApiService.getDocumentPreparations:', error)
      throw error
    }
  }

  /**
   * Récupérer les documents signés pour une organisation
   */
  async getSignedDocuments(organizationId) {
    try {
      const { db } = this.getFirebase()
      const prepRef = collection(db, 'document_preparations')
      const q = query(prepRef, where('organization.id', '==', organizationId))
      
      const querySnapshot = await getDocs(q)
      const documents = []
      
      querySnapshot.forEach((doc) => {
        const data = doc.data()
        // Filtrer côté client pour éviter les erreurs d'index composite Firestore
        if (data.status === 'completed') {
          documents.push({
            id: doc.id,
            ...data
          })
        }
      })
      
      return { success: true, documents }
    } catch (error) {
      console.error('Erreur SignatureApiService.getSignedDocuments:', error)
      throw error
    }
  }

  /**
   * Récupérer les détails d'une signature
   */
  async getSignatureDetails(signatureId) {
    try {
      const { db } = this.getFirebase()
      const docRef = doc(db, 'signatures', signatureId)
      const docSnap = await getDoc(docRef)
      
      if (!docSnap.exists()) {
        throw new Error('Signature introuvable')
      }

      return {
        id: docSnap.id,
        ...docSnap.data()
      }
    } catch (error) {
      console.error('Erreur SignatureApiService.getSignatureDetails:', error)
      throw error
    }
  }

  /**
   * Préparer les données de signature pour Firestore
   */
  async prepareSignatureData(signatureResult, originalFileData, certificateInfo) {
    try {
      const { auth } = this.getFirebase()
      const user = auth.currentUser

      if (!user) {
        throw new Error('Utilisateur non connecté')
      }

      const originalDocumentBase64 = this.uint8ArrayToBase64(originalFileData)
      const signedDocumentBase64 = this.uint8ArrayToBase64(signatureResult.signedDocument)

      // Upload vers Cloudinary
      const originalDocumentUrl = await CloudinaryService.uploadPdf(
        `data:application/pdf;base64,${originalDocumentBase64}`, 
        `original_${signatureResult.fileName || 'document.pdf'}`
      )
      
      const signedDocumentUrl = await CloudinaryService.uploadPdf(
        `data:application/pdf;base64,${signedDocumentBase64}`, 
        `signed_${signatureResult.fileName || 'document.pdf'}`
      )

      return {
        document_id: signatureResult.documentId,
        signer_full_name: user.displayName || 'Utilisateur',
        signer_email: user.email,
        original_filename: signatureResult.fileName || 'document.pdf',
        document_hash: signatureResult.originalHash,
        public_key: signatureResult.publicKeyPem,
        signature: signatureResult.signature,
        signature_timestamp: signatureResult.timestamp,
        file_size_original: originalFileData.byteLength,
        file_size_signed: signatureResult.signedDocument.byteLength,
        execution_time: parseFloat(signatureResult.executionTime) || 0,
        original_document_url: originalDocumentUrl,
        signed_document_url: signedDocumentUrl
      }
    } catch (error) {
      console.error('Erreur lors de la préparation des données:', error)
      throw error
    }
  }

  /**
   * Tester l'authentification (vérifie si l'utilisateur est connecté via Firebase Auth)
   */
  async testAuthentication() {
    try {
      const { auth } = this.getFirebase()
      return auth.currentUser !== null
    } catch (error) {
      console.error('Erreur test auth:', error)
      return false
    }
  }
}
