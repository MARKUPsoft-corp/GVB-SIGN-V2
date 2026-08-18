/**
 * Service de gestion de la signature des documents
 * Orchestre la récupération des données et la signature (Firebase)
 */
import { SignatureService } from './SignatureService'
import { CertificateService } from './CertificateService'
import forge from 'node-forge'
import { getApp } from 'firebase/app'
import { getFirestore, doc, getDoc, collection, query, where, getDocs, updateDoc, arrayUnion, serverTimestamp } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'

export class DocumentSigningService {
  constructor() {
    this.signatureService = new SignatureService()
    this.certificateService = new CertificateService()
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
      console.warn("⚠️ [DocumentSigningService] Firebase n'est pas encore initialisé.")
      throw new Error("Firebase n'est pas initialisé.")
    }
  }

  /**
   * Initialise le service
   */
  initialize() {
    console.log('🔧 Initialisation du DocumentSigningService')
    this.signatureService.initialize()
  }

  /**
   * ÉTAPE 1 : Récupérer toutes les données nécessaires depuis la BDD (Firestore)
   */
  async fetchSigningData(preparationId, organizationId) {
    try {
      console.log('📥 === RÉCUPÉRATION DES DONNÉES DE SIGNATURE ===')
      
      const documentPreparation = await this.fetchDocumentPreparation(preparationId)
      console.log('✅ Document préparation récupéré')

      const pdfData = await this.downloadCurrentPDF(documentPreparation)
      console.log('✅ PDF téléchargé, taille:', pdfData.byteLength, 'octets')

      const elementsConfig = this.extractElementsConfiguration(documentPreparation)
      console.log('✅ Configuration des éléments extraite')

      const certificate = await this.fetchOrganizationCertificate(organizationId)
      console.log('✅ Certificat chargé')

      const workflowInfo = this.extractWorkflowInfo(documentPreparation)
      console.log('✅ Informations workflow extraites')

      return {
        documentPreparation,
        pdfData,
        elementsConfig,
        certificate,
        workflowInfo
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des données de signature:', error)
      throw new Error(`Erreur de récupération des données: ${error.message}`)
    }
  }

  /**
   * Récupère les détails complets du document préparé depuis Firestore
   */
  async fetchDocumentPreparation(preparationId) {
    const { db } = this.getFirebase()
    const docRef = doc(db, 'document_preparations', preparationId)
    const docSnap = await getDoc(docRef)

    if (!docSnap.exists()) {
      throw new Error("Préparation de document introuvable dans Firestore")
    }

    return { id: docSnap.id, ...docSnap.data() }
  }

  /**
   * Télécharge le PDF actuel du document (Stockage Firebase ou URL externe)
   */
  async downloadCurrentPDF(documentPreparation) {
    let pdfUrl = documentPreparation.current_document || documentPreparation.original_document

    if (!pdfUrl) {
      throw new Error('Aucun document PDF disponible')
    }
    
    // Si l'URL est un base64 direct (data URL)
    if (pdfUrl.startsWith('data:application/pdf;base64,')) {
      const base64Data = pdfUrl.split(',')[1]
      const binaryString = window.atob(base64Data)
      const len = binaryString.length
      const bytes = new Uint8Array(len)
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i)
      }
      return bytes
    }

    const response = await fetch(pdfUrl, { method: 'GET' })

    if (!response.ok) {
      throw new Error(`Erreur lors du téléchargement du PDF: ${response.statusText}`)
    }

    const arrayBuffer = await response.arrayBuffer()
    return new Uint8Array(arrayBuffer)
  }

  /**
   * Extrait la configuration des éléments
   */
  extractElementsConfiguration(documentPreparation) {
    const config = documentPreparation.elements_configuration || {}

    const qrConfig = {
      x: documentPreparation.qr_code_x || config.qr_code?.x || 85,
      y: documentPreparation.qr_code_y || config.qr_code?.y || 10,
      size: documentPreparation.qr_code_size || config.qr_code?.size || 'medium',
      mode: documentPreparation.page_mode || config.page_mode || 'all',
      pages: documentPreparation.applied_pages || config.applied_pages || [],
      positions: config.qr_code?.positions || {}
    }

    const signatureConfig = {
      x: documentPreparation.signature_x || config.signature?.x || 50,
      y: documentPreparation.signature_y || config.signature?.y || 80,
      width: documentPreparation.signature_width || config.signature?.width || 200,
      height: documentPreparation.signature_height || config.signature?.height || 100,
      mode: documentPreparation.page_mode || config.page_mode || 'all',
      pages: documentPreparation.applied_pages || config.applied_pages || [],
      positions: config.signature?.positions || {}
    }

    return {
      qr_code: qrConfig,
      signature: signatureConfig,
      page_mode: documentPreparation.page_mode || 'all',
      applied_pages: documentPreparation.applied_pages || []
    }
  }

  /**
   * Récupère le certificat actif de l'organisation depuis Firestore
   */
  async fetchOrganizationCertificate(organizationId) {
    const { db } = this.getFirebase()
    const certsRef = collection(db, 'certificates')
    
    // Rechercher le certificat de l'organisation
    const q = query(certsRef, where('organizationId', '==', organizationId), where('status', '==', 'active'))
    const querySnapshot = await getDocs(q)
    
    if (querySnapshot.empty) {
      throw new Error('Aucun certificat actif trouvé pour cette organisation.')
    }
    
    const certDoc = querySnapshot.docs[0]
    const cert = { id: certDoc.id, ...certDoc.data() }

    if (!cert.private_key_pem || !cert.public_key_pem) {
      throw new Error('Le certificat ne contient pas les clés cryptographiques nécessaires')
    }

    let privateKey, publicKey

    try {
      privateKey = forge.pki.privateKeyFromPem(cert.private_key_pem)
      publicKey = forge.pki.publicKeyFromPem(cert.public_key_pem)
    } catch (error) {
      console.error('❌ Erreur forge PEM:', error)
      throw new Error('Impossible de convertir les clés PEM via forge')
    }

    return {
      certificateData: cert,
      privateKey,
      publicKey,
      privateKeyPem: cert.private_key_pem,
      publicKeyPem: cert.public_key_pem,
      certificatePem: cert.certificate_pem
    }
  }

  /**
   * Extrait les informations du workflow
   */
  extractWorkflowInfo(documentPreparation) {
    const workflow = documentPreparation.signature_workflow || []
    const currentStep = documentPreparation.current_step || 0
    const totalSteps = documentPreparation.total_steps || workflow.length

    let nextSigner = null
    if (currentStep < totalSteps - 1) {
      nextSigner = workflow[currentStep + 1] || null
    }

    const currentSigner = workflow[currentStep] || null

    return {
      workflow,
      currentStep,
      totalSteps,
      currentSigner,
      nextSigner,
      isLastStep: currentStep >= totalSteps - 1,
      progressPercentage: totalSteps > 0 ? Math.round(((currentStep + 1) / totalSteps) * 100) : 0
    }
  }

  /**
   * ÉTAPE 2 : Préparer les métadonnées pour le service de signature
   */
  prepareSignatureMetadata(elementsConfig, workflowInfo, userInfo, certificateData) {
    return {
      qr_position: { ...elementsConfig.qr_code },
      signature_position: {
        signature_image: null,
        positions: {
          default: { x: elementsConfig.signature.x, y: elementsConfig.signature.y },
          ...elementsConfig.signature.positions
        },
        pages: elementsConfig.signature.mode === 'all' ? 'all' : elementsConfig.signature.pages,
        signature_size: 50
      },
      workflow_info: {
        current_step: workflowInfo.currentStep,
        total_steps: workflowInfo.totalSteps,
        is_last_step: workflowInfo.isLastStep,
        signer_info: {
          user_id: userInfo.uid || userInfo.id,
          user_name: userInfo.displayName || userInfo.full_name,
          user_email: userInfo.email
        }
      },
      certificate_info: {
        certificate_id: certificateData.id,
        certificate_name: certificateData.name,
        subject_common_name: certificateData.subject_common_name,
        subject_organization: certificateData.subject_organization,
        fingerprint: certificateData.fingerprint,
        serial_number: certificateData.serial_number
      }
    }
  }

  /**
   * ÉTAPE 3 : Signer le document avec toutes les données
   */
  async signDocument(preparationId, organizationId, userInfo) {
    try {
      const signingData = await this.fetchSigningData(preparationId, organizationId)

      const metadata = this.prepareSignatureMetadata(
        signingData.elementsConfig,
        signingData.workflowInfo,
        userInfo,
        signingData.certificate.certificateData
      )

      const signatureResult = await this.signatureService.signDocumentComplete(
        signingData.pdfData,
        signingData.certificate.privateKey,
        signingData.certificate.publicKey,
        metadata
      )

      const saveResult = await this.saveSignatureToBackend(
        preparationId,
        signatureResult,
        signingData.certificate.certificateData,
        signingData.workflowInfo
      )
      
      return {
        success: true,
        documentPreparation: signingData.documentPreparation,
        signatureResult: signatureResult,
        metadata: metadata,
        workflowInfo: signingData.workflowInfo,
        saveResult: saveResult,
        message: 'Document signé et enregistré avec succès'
      }
    } catch (error) {
      throw new Error(`Erreur lors de la signature du document: ${error.message}`)
    }
  }

  /**
   * Vérifie si l'utilisateur peut signer ce document
   */
  canUserSignDocument(documentPreparation, userId) {
    const currentSignerId = documentPreparation.current_signer?.id
    
    if (!currentSignerId) {
      const workflow = documentPreparation.signature_workflow || []
      const currentStep = documentPreparation.current_step || 0
      
      if (workflow.length > 0 && currentStep < workflow.length) {
        const currentStepData = workflow[currentStep]
        if (currentStepData?.user_id !== userId) return false
      } else {
        return false
      }
    } else if (currentSignerId !== userId) {
      return false
    }

    const signableStatuses = ['prepared', 'pending_signature', 'in_progress']
    return signableStatuses.includes(documentPreparation.status)
  }

  /**
   * Vérifie si l'organisation a un certificat valide
   */
  async hasOrganizationCertificate(organizationId) {
    try {
      const { db } = this.getFirebase()
      const certsRef = collection(db, 'certificates')
      const q = query(certsRef, where('organizationId', '==', organizationId), where('status', '==', 'active'))
      const querySnapshot = await getDocs(q)
      return !querySnapshot.empty
    } catch (error) {
      console.error('Erreur lors de la vérification du certificat:', error)
      return false
    }
  }

  /**
   * Enregistre le résultat de signature dans Firestore (mise à jour de la préparation)
   */
  async saveSignatureToBackend(preparationId, signatureResult, certificateData, workflowInfo) {
    try {
      const { db } = this.getFirebase()
      
      // Convertir le document signé en base64 pour data URL
      const signedDocumentBase64 = btoa(String.fromCharCode(...signatureResult.signedDocument))
      const dataUrl = `data:application/pdf;base64,${signedDocumentBase64}`
      
      const docRef = doc(db, 'document_preparations', preparationId)
      
      // Gérer l'avancement du workflow
      const nextStep = workflowInfo.currentStep + 1
      const isComplete = nextStep >= workflowInfo.totalSteps
      const nextSigner = isComplete ? null : workflowInfo.workflow[nextStep]

      await updateDoc(docRef, {
        current_document: dataUrl,
        current_step: nextStep,
        status: isComplete ? 'completed' : 'in_progress',
        current_signer: nextSigner,
        updatedAt: serverTimestamp(),
        // Ajouter un log de signature dans un tableau
        signatures_history: arrayUnion({
          signatureId: signatureResult.signature,
          timestamp: signatureResult.timestamp,
          step: workflowInfo.currentStep,
          signer_name: workflowInfo.currentSigner?.name || 'Utilisateur',
          hash: signatureResult.originalHash
        })
      })

      return {
        success: true,
        signature_id: signatureResult.signature,
        workflow_advanced: !isComplete,
        is_complete: isComplete,
        next_signer: nextSigner
      }
    } catch (error) {
      console.error('Erreur lors de l\'enregistrement de la signature Firestore:', error)
      throw new Error(`Erreur d'enregistrement: ${error.message}`)
    }
  }
}
