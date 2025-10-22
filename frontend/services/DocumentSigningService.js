/**
 * Service de gestion de la signature des documents
 * Orchestre la récupération des données et la signature
 */
import { SignatureService } from './SignatureService'
import { CertificateService } from './CertificateService'
import forge from 'node-forge'

export class DocumentSigningService {
  constructor() {
    this.signatureService = new SignatureService()
    this.certificateService = new CertificateService()
    this.baseURL = 'http://127.0.0.1:8000/api/signatures'
  }

  /**
   * Initialise le service
   */
  initialize() {
    console.log('🔧 Initialisation du DocumentSigningService')
    this.signatureService.initialize()
  }

  /**
   * Récupère le token CSRF depuis les cookies
   */
  getCSRFToken() {
    const cookies = document.cookie.split(';')
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=')
      if (name === 'csrftoken') {
        return value
      }
    }
    return ''
  }

  /**
   * ÉTAPE 1 : Récupérer toutes les données nécessaires depuis la BDD
   * @param {string} preparationId - ID de la préparation de document
   * @param {string} organizationId - ID de l'organisation
   * @returns {Promise<Object>} Toutes les données nécessaires pour la signature
   */
  async fetchSigningData(preparationId, organizationId) {
    try {
      console.log('📥 === RÉCUPÉRATION DES DONNÉES DE SIGNATURE ===')
      console.log('📥 Preparation ID:', preparationId)
      console.log('📥 Organization ID:', organizationId)

      // 1. Récupérer les détails complets du document préparé
      const documentPreparation = await this.fetchDocumentPreparation(preparationId)
      console.log('✅ Document préparation récupéré:', documentPreparation)

      // 2. Télécharger le PDF actuel (avec signatures partielles éventuelles)
      const pdfData = await this.downloadCurrentPDF(documentPreparation)
      console.log('✅ PDF téléchargé, taille:', pdfData.byteLength, 'octets')

      // 3. Récupérer la configuration des éléments (QR + Signature)
      const elementsConfig = this.extractElementsConfiguration(documentPreparation)
      console.log('✅ Configuration des éléments extraite:', elementsConfig)

      // 4. Récupérer le certificat et les clés cryptographiques depuis la BDD
      const certificate = await this.fetchOrganizationCertificate(organizationId)
      console.log('✅ Certificat chargé depuis la BDD:', certificate.certificateData.subject_common_name)

      // 5. Extraire les informations du workflow
      const workflowInfo = this.extractWorkflowInfo(documentPreparation)
      console.log('✅ Informations workflow extraites:', workflowInfo)

      console.log('✅ === TOUTES LES DONNÉES RÉCUPÉRÉES AVEC SUCCÈS ===')

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
   * Récupère les détails complets du document préparé depuis l'API
   */
  async fetchDocumentPreparation(preparationId) {
    console.log('📡 Récupération du document préparation ID:', preparationId)

    const response = await fetch(
      `${this.baseURL}/document-preparation/${preparationId}/`,
      {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      console.error('❌ Erreur API:', errorText)
      throw new Error(`Erreur ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.error || 'Erreur lors de la récupération du document')
    }

    return data.preparation
  }

  /**
   * Télécharge le PDF actuel du document
   */
  async downloadCurrentPDF(documentPreparation) {
    console.log('📄 Téléchargement du PDF actuel')

    // Déterminer l'URL du PDF à télécharger
    // Utiliser current_document en priorité (avec signatures partielles)
    // Sinon utiliser original_document
    let pdfUrl = documentPreparation.current_document || documentPreparation.original_document

    if (!pdfUrl) {
      throw new Error('Aucun document PDF disponible')
    }

    // Si l'URL est relative, l'ajuster pour pointer vers le backend Django
    if (pdfUrl.startsWith('/media/')) {
      pdfUrl = `http://127.0.0.1:8000${pdfUrl}`
    }

    console.log('📄 URL du PDF:', pdfUrl)

    const response = await fetch(pdfUrl, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Erreur lors du téléchargement du PDF: ${response.statusText}`)
    }

    const arrayBuffer = await response.arrayBuffer()
    return new Uint8Array(arrayBuffer)
  }

  /**
   * Extrait la configuration des éléments (QR Code + Signature)
   */
  extractElementsConfiguration(documentPreparation) {
    console.log('⚙️ Extraction de la configuration des éléments')

    const config = documentPreparation.elements_configuration || {}

    // Configuration du QR Code
    const qrConfig = {
      x: documentPreparation.qr_code_x || config.qr_code?.x || 85,
      y: documentPreparation.qr_code_y || config.qr_code?.y || 10,
      size: documentPreparation.qr_code_size || config.qr_code?.size || 'medium',
      mode: documentPreparation.page_mode || config.page_mode || 'all',
      pages: documentPreparation.applied_pages || config.applied_pages || [],
      positions: config.qr_code?.positions || {}
    }

    // Configuration de la signature
    const signatureConfig = {
      x: documentPreparation.signature_x || config.signature?.x || 50,
      y: documentPreparation.signature_y || config.signature?.y || 80,
      width: documentPreparation.signature_width || config.signature?.width || 200,
      height: documentPreparation.signature_height || config.signature?.height || 100,
      mode: documentPreparation.page_mode || config.page_mode || 'all',
      pages: documentPreparation.applied_pages || config.applied_pages || [],
      positions: config.signature?.positions || {}
    }

    console.log('⚙️ QR Config:', qrConfig)
    console.log('⚙️ Signature Config:', signatureConfig)

    return {
      qr_code: qrConfig,
      signature: signatureConfig,
      page_mode: documentPreparation.page_mode || 'all',
      applied_pages: documentPreparation.applied_pages || []
    }
  }

  /**
   * Récupère le certificat actif de l'organisation depuis la BDD
   * @param {string} organizationId - ID de l'organisation
   * @returns {Promise<Object>} Données du certificat avec les clés
   */
  async fetchOrganizationCertificate(organizationId) {
    console.log('🔐 Récupération du certificat de l\'organisation depuis la BDD')
    console.log('🔐 Organization ID:', organizationId)

    const response = await fetch(
      `http://127.0.0.1:8000/api/organizations/${organizationId}/certificates/active-for-signing/`,
      {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
      }
    )

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('❌ Erreur API certificat:', errorData)
      
      if (response.status === 404) {
        throw new Error('Aucun certificat actif trouvé pour cette organisation. Veuillez d\'abord importer un certificat.')
      } else if (response.status === 400 && errorData.is_expired) {
        throw new Error('Le certificat de l\'organisation est expiré. Veuillez importer un nouveau certificat.')
      } else if (response.status === 403) {
        throw new Error('Vous n\'êtes pas autorisé à récupérer le certificat de cette organisation.')
      }
      
      throw new Error(`Erreur ${response.status}: ${errorData.message || response.statusText}`)
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.message || 'Erreur lors de la récupération du certificat')
    }

    const cert = data.certificate

    // Vérifier que le certificat a les clés nécessaires
    if (!cert.private_key_pem || !cert.public_key_pem) {
      throw new Error('Le certificat ne contient pas les clés cryptographiques nécessaires')
    }

    // Convertir les clés PEM en objets forge
    console.log('🔧 Utilisation de node-forge importé:', !!forge)

    let privateKey, publicKey

    try {
      // Convertir la clé privée PEM en objet forge
      privateKey = forge.pki.privateKeyFromPem(cert.private_key_pem)
      console.log('✅ Clé privée convertie depuis PEM')
    } catch (error) {
      console.error('❌ Erreur lors de la conversion de la clé privée:', error)
      throw new Error('Impossible de convertir la clé privée PEM')
    }

    try {
      // Convertir la clé publique PEM en objet forge
      publicKey = forge.pki.publicKeyFromPem(cert.public_key_pem)
      console.log('✅ Clé publique convertie depuis PEM')
    } catch (error) {
      console.error('❌ Erreur lors de la conversion de la clé publique:', error)
      throw new Error('Impossible de convertir la clé publique PEM')
    }

    console.log('🔐 Certificat de l\'organisation:', cert.name)
    console.log('🔐 Propriétaire du certificat:', cert.subject_common_name)
    console.log('🔐 Sujet:', cert.subject_common_name)
    console.log('🔐 Organisation:', cert.subject_organization)
    console.log('🔐 Validité:', cert.not_before, '-', cert.not_after)
    console.log('🔐 Jours restants:', cert.days_until_expiry)

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
    console.log('📋 Extraction des informations du workflow')

    const workflow = documentPreparation.signature_workflow || []
    const currentStep = documentPreparation.current_step || 0
    const totalSteps = documentPreparation.total_steps || 0

    // Déterminer le prochain signataire
    let nextSigner = null
    if (currentStep < totalSteps - 1) {
      nextSigner = workflow[currentStep + 1] || null
    }

    // Informations du signataire actuel
    const currentSigner = workflow[currentStep] || null

    console.log('📋 Étape actuelle:', currentStep + 1, '/', totalSteps)
    console.log('📋 Signataire actuel:', currentSigner)
    console.log('📋 Prochain signataire:', nextSigner)

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
    console.log('🔧 Préparation des métadonnées de signature')

    const metadata = {
      // Configuration du QR Code
      qr_position: {
        x: elementsConfig.qr_code.x,
        y: elementsConfig.qr_code.y,
        size: elementsConfig.qr_code.size,
        mode: elementsConfig.qr_code.mode,
        pages: elementsConfig.qr_code.pages,
        positions: elementsConfig.qr_code.positions
      },

      // Configuration de la signature
      // Note: Pour le chef, pas d'image de signature dessinée
      // La signature est purement cryptographique
      signature_position: {
        signature_image: null, // Pas d'image dessinée pour le chef
        positions: {
          default: {
            x: elementsConfig.signature.x,
            y: elementsConfig.signature.y
          },
          ...elementsConfig.signature.positions
        },
        pages: elementsConfig.signature.mode === 'all' ? 'all' : elementsConfig.signature.pages,
        signature_size: 50 // Taille par défaut
      },

      // Informations du workflow
      workflow_info: {
        current_step: workflowInfo.currentStep,
        total_steps: workflowInfo.totalSteps,
        is_last_step: workflowInfo.isLastStep,
        signer_info: {
          user_id: userInfo.id,
          user_name: userInfo.full_name,
          user_email: userInfo.email,
          role: userInfo.role
        }
      },

      // Informations du certificat
      certificate_info: {
        certificate_id: certificateData.id,
        certificate_name: certificateData.name,
        subject_common_name: certificateData.subject_common_name,
        subject_organization: certificateData.subject_organization,
        fingerprint: certificateData.fingerprint,
        serial_number: certificateData.serial_number
      }
    }

    console.log('✅ Métadonnées préparées:', metadata)
    return metadata
  }

  /**
   * ÉTAPE 3 : Signer le document avec toutes les données
   * @param {string} preparationId - ID de la préparation
   * @param {string} organizationId - ID de l'organisation
   * @param {Object} userInfo - Informations de l'utilisateur connecté
   * @returns {Promise<Object>} Résultat de la signature
   */
  async signDocument(preparationId, organizationId, userInfo) {
    try {
      console.log('✍️ === DÉBUT DU PROCESSUS DE SIGNATURE ===')
      console.log('✍️ Preparation ID:', preparationId)
      console.log('✍️ Organization ID:', organizationId)
      console.log('✍️ User:', userInfo.full_name)

      // ÉTAPE 1: Récupérer toutes les données nécessaires
      console.log('\n📥 ÉTAPE 1: Récupération des données...')
      const signingData = await this.fetchSigningData(preparationId, organizationId)

      // ÉTAPE 2: Préparer les métadonnées
      console.log('\n🔧 ÉTAPE 2: Préparation des métadonnées...')
      const metadata = this.prepareSignatureMetadata(
        signingData.elementsConfig,
        signingData.workflowInfo,
        userInfo,
        signingData.certificate.certificateData
      )

      // ÉTAPE 3: Signer le document avec SignatureService
      console.log('\n✍️ ÉTAPE 3: Signature du document...')
      const signatureResult = await this.signatureService.signDocumentComplete(
        signingData.pdfData,
        signingData.certificate.privateKey,
        signingData.certificate.publicKey,
        metadata
      )

      console.log('✅ Document signé avec succès!')
      console.log('✅ Document ID:', signatureResult.documentId)
      console.log('✅ Hash original:', signatureResult.originalHash.substring(0, 20) + '...')
      console.log('✅ Signature:', signatureResult.signature.substring(0, 50) + '...')
      console.log('✅ Temps d\'exécution:', signatureResult.executionTime, 'secondes')

      console.log('\n✅ === SIGNATURE TERMINÉE AVEC SUCCÈS ===')

      // ÉTAPE 4: Enregistrer le résultat dans la base de données
      console.log('\n💾 ÉTAPE 4: Enregistrement dans la base de données...')
      const saveResult = await this.saveSignatureToBackend(
        preparationId,
        signatureResult,
        signingData.certificate.certificateData
      )
      
      console.log('✅ Signature enregistrée dans la BDD:', saveResult)

      // Retourner le résultat complet
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
      console.error('❌ === ERREUR LORS DE LA SIGNATURE ===')
      console.error('❌ Message:', error.message)
      console.error('❌ Stack:', error.stack)

      throw new Error(`Erreur lors de la signature du document: ${error.message}`)
    }
  }

  /**
   * Vérifie si l'utilisateur peut signer ce document
   */
  canUserSignDocument(documentPreparation, userId) {
    console.log('🔍 Vérification des permissions de signature...')
    console.log('🔍 Document ID:', documentPreparation.id)
    console.log('🔍 Document preparation complet:', documentPreparation)
    console.log('🔍 Current signer:', documentPreparation.current_signer)
    console.log('🔍 Current signer ID:', documentPreparation.current_signer?.id)
    console.log('🔍 User ID:', userId)
    console.log('🔍 Document status:', documentPreparation.status)
    
    // Vérifier que l'utilisateur est le signataire actuel
    const currentSignerId = documentPreparation.current_signer?.id
    
    // Si current_signer n'est pas défini, vérifier dans le workflow
    if (!currentSignerId) {
      console.log('🔍 Current signer non défini, vérification dans le workflow...')
      const workflow = documentPreparation.signature_workflow || []
      const currentStep = documentPreparation.current_step || 0
      
      if (workflow.length > 0 && currentStep < workflow.length) {
        const currentStepData = workflow[currentStep]
        console.log('🔍 Étape actuelle du workflow:', currentStepData)
        
        if (currentStepData && currentStepData.user_id === userId) {
          console.log('✅ Utilisateur trouvé dans le workflow comme signataire actuel')
        } else {
          console.warn('⚠️ Utilisateur non trouvé dans le workflow comme signataire actuel')
          console.warn('⚠️ Workflow step user_id:', currentStepData?.user_id, 'vs User ID:', userId)
          return false
        }
      } else {
        console.warn('⚠️ Workflow vide ou étape invalide')
        return false
      }
    } else if (currentSignerId !== userId) {
      console.warn('⚠️ Utilisateur non autorisé à signer ce document')
      console.warn('⚠️ Current signer ID:', currentSignerId, 'vs User ID:', userId)
      return false
    }

    console.log('✅ Utilisateur est le signataire actuel')

    // Vérifier que le document est dans un état signable
    const signableStatuses = ['prepared', 'pending_signature', 'in_progress']
    console.log('🔍 Statuts signables autorisés:', signableStatuses)
    console.log('🔍 Statut actuel du document:', documentPreparation.status)
    
    if (!signableStatuses.includes(documentPreparation.status)) {
      console.warn('⚠️ Document dans un état non signable:', documentPreparation.status)
      console.warn('⚠️ Statuts autorisés:', signableStatuses)
      return false
    }

    console.log('✅ Document dans un état signable')
    console.log('✅ Toutes les vérifications passées - utilisateur autorisé')
    return true
  }

  /**
   * Vérifie si l'organisation a un certificat valide
   * @param {string} organizationId - ID de l'organisation
   * @returns {Promise<boolean>} True si un certificat actif existe
   */
  async hasOrganizationCertificate(organizationId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/organizations/${organizationId}/certificates/active-for-signing/`,
        {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken(),
          },
        }
      )

      if (response.ok) {
        const data = await response.json()
        return data.success && data.has_certificate
      }

      return false
    } catch (error) {
      console.error('❌ Erreur lors de la vérification du certificat:', error)
      return false
    }
  }

  /**
   * Enregistre le résultat de signature dans la base de données
   * @param {string} preparationId - ID de la préparation
   * @param {Object} signatureResult - Résultat de la signature
   * @param {Object} certificateData - Données du certificat
   * @returns {Promise<Object>} Résultat de l'enregistrement
   */
  async saveSignatureToBackend(preparationId, signatureResult, certificateData) {
    console.log('💾 Enregistrement de la signature dans la BDD...')
    console.log('💾 Preparation ID:', preparationId)
    console.log('💾 Document ID:', signatureResult.documentId)
    console.log('💾 Signature ID:', signatureResult.signature.substring(0, 20) + '...')

    try {
      // Convertir le document signé en base64
      const signedDocumentBase64 = btoa(String.fromCharCode(...signatureResult.signedDocument))
      
      // Préparer les données à envoyer
      const payload = {
        document_id: signatureResult.documentId,
        document_hash: signatureResult.originalHash,
        signature: signatureResult.signature,
        public_key: signatureResult.publicKeyPem,
        signed_document_data: signedDocumentBase64,
        signature_timestamp: signatureResult.timestamp,
        // Champs requis supplémentaires
        file_size_original: signatureResult.originalDocumentSize || 0,
        file_size_signed: signatureResult.signedDocument.length,
        execution_time: signatureResult.executionTime
      }

      console.log('💾 Données à envoyer:', {
        document_id: payload.document_id,
        document_hash: payload.document_hash.substring(0, 20) + '...',
        signature: payload.signature.substring(0, 20) + '...',
        signed_document_size: signedDocumentBase64.length
      })

      // Envoyer au backend
      const response = await fetch(
        `http://127.0.0.1:8000/api/signatures/document-preparation/${preparationId}/save-signature/`,
        {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken(),
          },
          body: JSON.stringify(payload)
        }
      )

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        console.error('❌ Erreur API enregistrement:', errorData)
        throw new Error(`Erreur ${response.status}: ${errorData.error || response.statusText}`)
      }

      const data = await response.json()

      if (!data.success) {
        throw new Error(data.error || 'Erreur lors de l\'enregistrement de la signature')
      }

      console.log('✅ Signature enregistrée avec succès!')
      console.log('✅ Signature ID:', data.signature_id)
      console.log('✅ Workflow avancé:', data.workflow_advanced)
      
      if (data.next_signer) {
        console.log('⏭️ Prochain signataire:', data.next_signer.name, `(${data.next_signer.role})`)
      }
      
      if (data.is_complete) {
        console.log('🎉 Workflow terminé - Document complètement signé!')
      }

      return data

    } catch (error) {
      console.error('❌ Erreur lors de l\'enregistrement de la signature:', error)
      throw new Error(`Erreur d'enregistrement: ${error.message}`)
    }
  }
}

