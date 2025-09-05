import forge from 'node-forge'
import QRCode from 'qrcode'
import { v4 as uuidv4 } from 'uuid'
import { PDFDocument } from 'pdf-lib'

/**
 * Service de signature numérique côté client
 * Inspiré des fichiers Python signer.py et main.py
 */
export class SignatureService {
  constructor() {
    this.isInitialized = false
  }

  /**
   * Initialise le service
   */
  initialize() {
    this.isInitialized = true
    console.log('SignatureService initialisé')
  }

  /**
   * Génère un identifiant unique pour le document
   * @returns {string} UUID v4
   */
  generateDocumentId() {
    const documentId = uuidv4()
    console.log(`Identifiant généré pour le document: ${documentId}`)
    return documentId
  }

  /**
   * Calcule le hash SHA-256 d'un document
   * @param {ArrayBuffer|Uint8Array} documentData - Données du document
   * @returns {string} Hash SHA-256 en hexadécimal
   */
  calculateDocumentHash(documentData) {
    try {
      console.log('=== DÉBUT CALCUL HASH ===')
      console.log('Type de documentData:', typeof documentData)
      console.log('Instance de ArrayBuffer:', documentData instanceof ArrayBuffer)
      console.log('Instance de Uint8Array:', documentData instanceof Uint8Array)
      console.log('Taille:', documentData.byteLength || 'N/A')
      
      // Convertir en Uint8Array si nécessaire
      const data = documentData instanceof ArrayBuffer ? new Uint8Array(documentData) : documentData
      console.log('Type de data après conversion:', typeof data)
      console.log('Instance de Uint8Array après conversion:', data instanceof Uint8Array)
      console.log('Taille après conversion:', data.byteLength)
      
      // Vérifier que les données sont valides
      if (!data || data.byteLength === 0) {
        throw new Error('Données du document invalides ou vides')
      }
      
      // Calculer le hash SHA-256 avec node-forge
      const md = forge.md.sha256.create()
      console.log('Hash MD créé')
      
      // Traiter les données binaires directement sans passer par createBuffer
      // car les données PDF contiennent des octets qui ne sont pas du texte UTF-8 valide
      const bytes = new Uint8Array(data)
      console.log('Uint8Array créé, taille:', bytes.length)
      
      // Mettre à jour le hash en utilisant une approche plus efficace
      // mais en évitant createBuffer qui cause des problèmes avec les données binaires
      const chunkSize = 1024 // Traiter par chunks de 1KB
      for (let i = 0; i < bytes.length; i += chunkSize) {
        const chunk = bytes.slice(i, i + chunkSize)
        const chunkString = Array.from(chunk).map(byte => String.fromCharCode(byte)).join('')
        md.update(chunkString)
      }
      console.log('Hash MD mis à jour par chunks')
      
      const hash = md.digest().toHex()
      console.log(`Hash du document calculé: ${hash.substring(0, 10)}...`)
      console.log('=== FIN CALCUL HASH ===')
      return hash
    } catch (error) {
      console.error('Erreur lors du calcul du hash:', error)
      console.error('Stack trace:', error.stack)
      throw new Error(`Erreur lors du calcul du hash: ${error.message}`)
    }
  }

  /**
   * Signe un document avec la clé privée (équivalent de sign_file en Python)
   * @param {ArrayBuffer|Uint8Array} documentData - Données du document
   * @param {Object} privateKey - Clé privée au format node-forge
   * @returns {string} Signature en base64
   */
  signDocument(documentData, privateKey) {
    try {
      console.log('Début de la signature du document')
      
      if (!privateKey) {
        throw new Error('Clé privée manquante')
      }

      // Convertir en Uint8Array si nécessaire
      const data = documentData instanceof ArrayBuffer ? new Uint8Array(documentData) : documentData
      
      // Calculer le hash SHA-256 du document directement avec node-forge
      const md = forge.md.sha256.create()
      
      // Traiter les données binaires par chunks pour éviter les problèmes d'encodage
      const chunkSize = 1024
      for (let i = 0; i < data.length; i += chunkSize) {
        const chunk = data.slice(i, i + chunkSize)
        const chunkString = Array.from(chunk).map(byte => String.fromCharCode(byte)).join('')
        md.update(chunkString)
      }
      
      // Obtenir le digest
      const digest = md.digest()
      console.log('Hash calculé et digest créé pour signature')
      
      // Créer la signature avec PKCS#1 v1.5 en utilisant les primitives RSA
      // Approche alternative : utiliser directement les fonctions RSA de node-forge
      try {
        // Méthode 1: Essayer avec l'objet digest
        const signature = privateKey.sign(digest)
        console.log('Signature créée avec l\'objet digest')
        return forge.util.encode64(signature)
      } catch (digestError) {
        console.log('Échec avec l\'objet digest, essai avec les bytes:', digestError.message)
        
        try {
          // Méthode 2: Essayer avec les bytes du digest
          const signature = privateKey.sign(digest.getBytes())
          console.log('Signature créée avec les bytes du digest')
          return forge.util.encode64(signature)
        } catch (bytesError) {
          console.log('Échec avec les bytes, essai avec signature manuelle:', bytesError.message)
          
          // Méthode 3: Signature RSA manuelle avec PKCS#1 v1.5
          const hashBytes = digest.getBytes()
          
          // Créer le padding PKCS#1 v1.5 pour SHA-256
          const algorithmIdentifier = forge.asn1.create(forge.asn1.Class.UNIVERSAL, forge.asn1.Type.SEQUENCE, true, [
            forge.asn1.create(forge.asn1.Class.UNIVERSAL, forge.asn1.Type.SEQUENCE, true, [
              forge.asn1.create(forge.asn1.Class.UNIVERSAL, forge.asn1.Type.OID, false, forge.asn1.oidToDer(forge.oids.sha256).getBytes()),
              forge.asn1.create(forge.asn1.Class.UNIVERSAL, forge.asn1.Type.NULL, false, '')
            ]),
            forge.asn1.create(forge.asn1.Class.UNIVERSAL, forge.asn1.Type.OCTETSTRING, false, hashBytes)
          ])
          
          const algorithmIdentifierBytes = forge.asn1.toDer(algorithmIdentifier).getBytes()
          
          // Utiliser les primitives RSA de forge
          const signature = forge.pki.rsa.encrypt(algorithmIdentifierBytes, privateKey, 0x01)
          console.log('Signature créée avec RSA manuel')
          return forge.util.encode64(signature)
        }
      }
    } catch (error) {
      console.error('Erreur lors de la signature:', error)
      throw new Error(`Erreur lors de la signature: ${error.message}`)
    }
  }

  /**
   * Génère un QR code contenant l'ID du document (équivalent de add_simple_qr_code_to_pdf)
   * @param {string} documentId - ID unique du document
   * @param {Object} options - Options pour le QR code
   * @returns {Promise<string>} QR code en base64 (data URL)
   */
  async generateQRCode(documentId, options = {}) {
    try {
      console.log(`Génération du QR code pour le document: ${documentId}`)
      
      const qrOptions = {
        errorCorrectionLevel: 'H', // Haute correction d'erreur (comme dans Python)
        type: 'image/png',
        quality: 0.92,
        margin: 4,
        color: {
          dark: '#000000',
          light: '#FFFFFF'
        },
        width: options.width || 256,
        ...options
      }
      
      // Générer le QR code avec seulement l'ID du document (comme dans Python)
      const qrCodeDataURL = await QRCode.toDataURL(documentId, qrOptions)
      
      console.log('QR code généré avec succès')
      return qrCodeDataURL
    } catch (error) {
      console.error('Erreur lors de la génération du QR code:', error)
      throw new Error(`Erreur lors de la génération du QR code: ${error.message}`)
    }
  }



  /**
   * Ajoute un QR code au PDF (équivalent de add_simple_qr_code_to_pdf)
   * @param {ArrayBuffer|Uint8Array} pdfData - Données du PDF original
   * @param {string} documentId - ID du document à encoder dans le QR code
   * @param {Object} qrPosition - Position et configuration du QR code
   * @returns {Promise<Uint8Array>} PDF modifié avec le QR code
   */
  async addQRCodeToPDF(pdfData, documentId, qrPosition = {}) {
    try {
      console.log('Début du processus d\'ajout du QR code au PDF')
      
      // Position par défaut si non spécifiée
      const defaultPosition = { x: 85, y: 10, size: 'medium', pages: 'all' }
      const position = { ...defaultPosition, ...qrPosition }
      
      // Tailles disponibles pour le QR code (en points, 1 inch = 72 points)
      const qrSizes = {
        'small': 43.2,   // 0.6 inch
        'medium': 57.6,  // 0.8 inch
        'large': 72      // 1.0 inch
      }
      
      const qrSize = qrSizes[position.size] || qrSizes['medium']
      console.log(`Taille du QR code: ${qrSize} points (${position.size})`)
      
      // Générer le QR code
      const qrCodeDataURL = await this.generateQRCode(documentId, { width: 256 })
      
      // Convertir le data URL en Uint8Array
      const qrImageBytes = this.dataURLToUint8Array(qrCodeDataURL)
      
      // Charger le PDF
      const pdfDoc = await PDFDocument.load(pdfData)
      
      // Intégrer l'image du QR code
      const qrImage = await pdfDoc.embedPng(qrImageBytes)
      
      // Parcourir les pages selon la configuration
      const pages = pdfDoc.getPages()
      console.log(`Traitement des ${pages.length} pages du PDF`)
      
      for (let i = 0; i < pages.length; i++) {
        const page = pages[i]
        const pageNumber = i + 1
        
        // Vérifier si le QR code doit être appliqué sur cette page
        let shouldApplyQR = false
        
        if (position.pages === 'all') {
          shouldApplyQR = true
        } else if (Array.isArray(position.pages)) {
          shouldApplyQR = position.pages.includes(pageNumber)
        }
        
        if (shouldApplyQR) {
          console.log(`Application du QR code sur la page ${pageNumber}`)
          console.log(`Position reçue:`, position)
          console.log(`Mode: ${position.mode}, Pages: ${position.pages}`)
          console.log(`Positions disponibles:`, position.positions)
          
          const { width: pageWidth, height: pageHeight } = page.getSize()
          
          // Déterminer la position du QR code
          let xPercent = position.x
          let yPercent = position.y
          
          // Gérer les différents modes de positionnement
          if (position.positions && Object.keys(position.positions).length > 0) {
            // Chercher la position pour cette page spécifique
            const pagePosition = position.positions[pageNumber.toString()]
            if (pagePosition) {
              xPercent = pagePosition.x
              yPercent = pagePosition.y
              console.log(`Position trouvée pour page ${pageNumber}: x=${xPercent}%, y=${yPercent}%`)
            }
            // Fallback : position par défaut
            else if (position.positions.default) {
              xPercent = position.positions.default.x
              yPercent = position.positions.default.y
              console.log(`Position par défaut pour page ${pageNumber}: x=${xPercent}%, y=${yPercent}%`)
            }
            // Mode individual : si pas de position définie, ne pas afficher
            else if (position.mode === 'individual') {
              console.log(`En mode individual, aucune position définie pour la page ${pageNumber}, QR non affiché`)
              continue
            }
          }
          
          // Convertir les pourcentages en coordonnées absolues
          // Les pourcentages : 0% = gauche/haut, 100% = droite/bas
          const xPosition = (xPercent / 100) * pageWidth - qrSize / 2
          const yPosition = pageHeight - (yPercent / 100) * pageHeight - qrSize / 2
          
          // S'assurer que le QR code reste dans les limites de la page
          const margin = 20
          const finalX = Math.max(margin, Math.min(pageWidth - qrSize - margin, xPosition))
          const finalY = Math.max(margin, Math.min(pageHeight - qrSize - margin, yPosition))
          
          console.log(`Position finale du QR code: x=${finalX}, y=${finalY}`)
          
          // Dessiner le QR code sur la page
          page.drawImage(qrImage, {
            x: finalX,
            y: finalY,
            width: qrSize,
            height: qrSize
          })
        } else {
          console.log(`Page ${pageNumber} sans QR code`)
        }
      }
      
      // Sauvegarder le PDF modifié
      console.log('Sauvegarde du PDF modifié avec le QR code')
      const modifiedPdfBytes = await pdfDoc.save()
      
      console.log('Processus d\'ajout du QR code terminé avec succès')
      return modifiedPdfBytes
      
    } catch (error) {
      console.error('Erreur lors de l\'ajout du QR code au PDF:', error)
      throw new Error(`Erreur lors de l'ajout du QR code: ${error.message}`)
    }
  }

  /**
   * Ajoute une image de signature au PDF (équivalent de add_signature_image_to_pdf)
   * @param {ArrayBuffer|Uint8Array} pdfData - Données du PDF original
   * @param {string} signatureImageData - Image de signature en base64
   * @param {Array} signaturePositions - Positions où ajouter la signature
   * @param {number} signatureSize - Taille de la signature en pourcentage
   * @returns {Promise<Uint8Array>} PDF modifié avec l'image de signature
   */
  async addSignatureImageToPDF(pdfData, signatureImageData, signaturePositions, signatureSize = 50) {
    try {
      console.log('=== DÉBUT add_signature_image_to_pdf ===')
      console.log(`Taille de signature reçue: ${signatureSize}%`)
      console.log(`Nombre de positions: ${signaturePositions.length}`)
      
      if (!signatureImageData || !signaturePositions || signaturePositions.length === 0) {
        console.warn('Image de signature ou positions manquantes')
        return pdfData
      }
      
      // Nettoyer l'image base64 si nécessaire et déterminer le type
      let cleanImageData = signatureImageData
      let imageType = 'png' // par défaut
      
      if (signatureImageData.startsWith('data:image')) {
        const commaIndex = signatureImageData.indexOf(',')
        if (commaIndex !== -1) {
          // Extraire le type d'image de la data URL
          const mimeType = signatureImageData.substring(5, commaIndex).split(';')[0]
          if (mimeType === 'image/jpeg' || mimeType === 'image/jpg') {
            imageType = 'jpeg'
          }
          cleanImageData = signatureImageData.substring(commaIndex + 1)
        }
      } else {
        // Si pas de data URL, détecter le type par les premiers caractères base64
        if (cleanImageData.startsWith('/9j/')) {
          imageType = 'jpeg'
        }
      }
      
      console.log(`Type d'image détecté: ${imageType}`)
      
      // Convertir en Uint8Array avec le bon type MIME
      const imageBytes = this.dataURLToUint8Array(`data:image/${imageType};base64,${cleanImageData}`)
      
      // Charger le PDF
      const pdfDoc = await PDFDocument.load(pdfData)
      
      // Intégrer l'image de signature avec le bon type
      let signatureImage
      if (imageType === 'jpeg') {
        signatureImage = await pdfDoc.embedJpg(imageBytes)
      } else {
        signatureImage = await pdfDoc.embedPng(imageBytes)
      }
      
      // Parcourir chaque page du PDF
      const pages = pdfDoc.getPages()
      console.log(`Traitement des ${pages.length} pages du PDF`)
      
      for (let i = 0; i < pages.length; i++) {
        const page = pages[i]
        const pageNumber = i + 1
        const { width: pageWidth, height: pageHeight } = page.getSize()
        
        // Vérifier si une signature doit être ajoutée sur cette page
        const signaturesForPage = []
        
        for (const pos of signaturePositions) {
          const posPage = pos.page
          
          // Mode "all": si page="all", appliquer sur toutes les pages
          if (String(posPage).toLowerCase() === 'all') {
            signaturesForPage.push(pos)
            console.log(`Mode 'all' détecté - signature appliquée sur la page ${pageNumber}`)
          }
          // Mode spécifique: appliquer seulement sur la page correspondante
          else if (String(posPage) === String(pageNumber)) {
            signaturesForPage.push(pos)
            console.log(`Mode spécifique - signature appliquée sur la page ${pageNumber}`)
          }
        }
        
        if (signaturesForPage.length > 0) {
          console.log(`Ajout de ${signaturesForPage.length} signature(s) sur la page ${pageNumber}`)
          
          // Ajouter chaque signature à la page
          for (const pos of signaturesForPage) {
            // Obtenir les coordonnées en pourcentage
            const xPercent = parseFloat(pos.x || 50)
            const yPercent = parseFloat(pos.y || 50)
            
            // Calculer les dimensions basées sur le pourcentage de signature_size
            // Ratio d'aspect fixe pour les signatures (environ 2:1)
            const widthPercent = signatureSize * 0.6   // Largeur basée sur signature_size
            const heightPercent = signatureSize * 0.3  // Hauteur basée sur signature_size
            
            console.log(`Position de signature: x=${xPercent}%, y=${yPercent}%, largeur=${widthPercent}%, hauteur=${heightPercent}%`)
            
            // Convertir les pourcentages en coordonnées absolues
            // Pour X: 0% = gauche, 100% = droite
            // Pour Y: 0% = haut, 100% = bas (inverser pour le PDF car Y=0 est en bas)
            const xPosition = (xPercent / 100) * pageWidth
            const yPosition = pageHeight - (yPercent / 100) * pageHeight
            
            // Calculer la largeur et hauteur en points
            const widthPoints = (widthPercent / 100) * pageWidth
            const heightPoints = (heightPercent / 100) * pageHeight
            
            console.log(`Position absolue: x=${xPosition}, y=${yPosition}`)
            console.log(`Dimensions absolues: largeur=${widthPoints}, hauteur=${heightPoints} points`)
            
            // Ajuster la position pour centrer l'image à la position spécifiée
            const finalX = xPosition - (widthPoints / 2)
            const finalY = yPosition - (heightPoints / 2)
            
            // Dessiner l'image de signature
            page.drawImage(signatureImage, {
              x: finalX,
              y: finalY,
              width: widthPoints,
              height: heightPoints
            })
            
            console.log(`Signature ajoutée à la position: x=${finalX}, y=${finalY}, largeur=${widthPoints}, hauteur=${heightPoints}`)
          }
        }
      }
      
      // Sauvegarder le PDF modifié
      const modifiedPdfBytes = await pdfDoc.save()
      
      console.log('Processus d\'ajout de l\'image de signature terminé avec succès')
      return modifiedPdfBytes
      
    } catch (error) {
      console.error('Erreur lors de l\'ajout de l\'image de signature au PDF:', error)
      // En cas d'erreur, retourner le PDF original
      return pdfData
    }
  }

  /**
   * Méthode principale de signature complète (équivalent de l'endpoint /sign)
   * @param {ArrayBuffer|Uint8Array} documentData - Données du document PDF original
   * @param {Object} privateKey - Clé privée du certificat
   * @param {Object} publicKey - Clé publique du certificat
   * @param {Object} metadata - Métadonnées contenant positions QR et signature
   * @returns {Promise<Object>} Résultat avec le PDF signé et les informations
   */
  async signDocumentComplete(documentData, privateKey, publicKey, metadata = {}) {
    try {
      console.log('=== DÉBUT DE LA SIGNATURE COMPLÈTE ===')
      const startTime = Date.now()
      
      // Générer un identifiant unique pour le document
      const documentId = this.generateDocumentId()
      
      // Calculer le hash SHA-256 du document original
      const originalHash = this.calculateDocumentHash(documentData)
      
      // Signer le document avec la clé privée
      const signature = this.signDocument(documentData, privateKey)
      console.log('Document signé avec succès')
      
      // Extraire les métadonnées
      const qrPosition = metadata.qr_position || null
      const signaturePosition = metadata.signature_position || null
      
      let processedPdf = new Uint8Array(documentData)
      
      // Étape 1: Ajouter l'image de signature si disponible
      if (signaturePosition && signaturePosition.signature_image && signaturePosition.positions) {
        console.log('Ajout de l\'image de signature au document')
        
        // Transformer les positions de signature en format compatible
        const transformedPositions = this.transformSignaturePositions(signaturePosition.positions, signaturePosition.pages)
        console.log('Positions de signature transformées:', transformedPositions)
        
        processedPdf = await this.addSignatureImageToPDF(
          processedPdf,
          signaturePosition.signature_image,
          transformedPositions,
          signaturePosition.signature_size || 50
        )
        console.log('Image de signature ajoutée avec succès')
      } else {
        console.log('Aucune image de signature à ajouter')
      }
      
      // Étape 2: Ajouter le QR code avec l'ID du document
      console.log('Ajout du QR code au document')
      processedPdf = await this.addQRCodeToPDF(processedPdf, documentId, qrPosition)
      console.log(`QR code contenant l'ID ${documentId} ajouté au document`)
      
      // Calculer le temps d'exécution
      const executionTime = (Date.now() - startTime) / 1000
      console.log(`Signature terminée en ${executionTime.toFixed(2)} secondes`)
      
      // Retourner le résultat
      return {
        success: true,
        documentId: documentId,
        originalHash: originalHash,
        signature: signature,
        publicKeyPem: this.getPublicKeyPEM(publicKey),
        signedDocument: processedPdf,
        executionTime: executionTime,
        timestamp: new Date().toISOString()
      }
      
    } catch (error) {
      console.error('Erreur lors de la signature complète:', error)
      throw new Error(`Erreur lors de la signature complète: ${error.message}`)
    }
  }

  /**
   * Convertit une clé publique en format PEM
   * @param {Object} publicKey - Clé publique node-forge
   * @returns {string} Clé publique au format PEM
   */
  getPublicKeyPEM(publicKey) {
    try {
      return forge.pki.publicKeyToPem(publicKey)
    } catch (error) {
      console.error('Erreur lors de la conversion de la clé publique en PEM:', error)
      return null
    }
  }

  /**
   * Transforme les positions de signature en format compatible avec addSignatureImageToPDF
   * @param {Object} positions - Positions de signature (format SignBase)
   * @param {string|Array} pages - Pages où appliquer la signature
   * @returns {Array} Positions transformées au format [{page, x, y}, ...]
   */
  transformSignaturePositions(positions, pages) {
    try {
      console.log('Transformation des positions de signature:', { positions, pages })
      
      const transformedPositions = []
      
      if (pages === 'all') {
        // Mode "all" : appliquer sur toutes les pages avec la position par défaut
        if (positions.default) {
          transformedPositions.push({
            page: 'all',
            x: positions.default.x,
            y: positions.default.y
          })
        }
      } else if (Array.isArray(pages)) {
        // Mode "custom" ou "current" : appliquer sur les pages spécifiées
        pages.forEach(pageNum => {
          if (positions[pageNum]) {
            transformedPositions.push({
              page: pageNum,
              x: positions[pageNum].x,
              y: positions[pageNum].y
            })
          } else if (positions.default) {
            // Utiliser la position par défaut si pas de position spécifique
            transformedPositions.push({
              page: pageNum,
              x: positions.default.x,
              y: positions.default.y
            })
          }
        })
      } else if (typeof pages === 'number') {
        // Mode "current" : une seule page
        if (positions[pages]) {
          transformedPositions.push({
            page: pages,
            x: positions[pages].x,
            y: positions[pages].y
          })
        } else if (positions.default) {
          transformedPositions.push({
            page: pages,
            x: positions.default.x,
            y: positions.default.y
          })
        }
      }
      
      console.log('Positions transformées:', transformedPositions)
      return transformedPositions
      
    } catch (error) {
      console.error('Erreur lors de la transformation des positions:', error)
      return []
    }
  }

  /**
   * Convertit un data URL en Uint8Array
   * @param {string} dataURL - Data URL (base64)
   * @returns {Uint8Array} Données binaires
   */
  dataURLToUint8Array(dataURL) {
    // Extraire la partie base64
    const base64 = dataURL.split(',')[1]
    // Décoder en binaire
    const binaryString = atob(base64)
    // Convertir en Uint8Array
    const bytes = new Uint8Array(binaryString.length)
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i)
    }
    return bytes
  }
}
