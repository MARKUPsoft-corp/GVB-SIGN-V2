/**
 * Service pour l'API des signatures de documents
 */
export class SignatureApiService {
  constructor() {
    this.baseURL = 'http://localhost:8000/api/signatures'
  }

  /**
   * Convertir un fichier en base64
   */
  async fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        // Enlever le préfixe data:application/pdf;base64,
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
   * Enregistrer une signature de document
   */
  async saveDocumentSignature(signatureData) {
    try {
      const response = await fetch(`${this.baseURL}/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify(signatureData)
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de l\'enregistrement')
      }

      return data
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
      const response = await fetch(`${this.baseURL}/bulk-create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify({ signatures: signaturesData })
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Erreur lors de l\'enregistrement')
      }

      return data
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
      const response = await fetch(`${this.baseURL}/list/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des signatures')
      }

      return data
    } catch (error) {
      console.error('Erreur SignatureApiService.getUserSignatures:', error)
      throw error
    }
  }

  /**
   * Récupérer les détails d'une signature
   */
  async getSignatureDetails(signatureId) {
    try {
      const response = await fetch(`${this.baseURL}/${signatureId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des détails')
      }

      return data
    } catch (error) {
      console.error('Erreur SignatureApiService.getSignatureDetails:', error)
      throw error
    }
  }

  /**
   * Préparer les données de signature pour l'API
   */
  async prepareSignatureData(signatureResult, originalFileData, certificateInfo) {
    try {
      // Convertir les données en base64
      const originalDocumentBase64 = this.uint8ArrayToBase64(originalFileData)
      const signedDocumentBase64 = this.uint8ArrayToBase64(signatureResult.signedDocument)

      // Préparer les données
      const signatureData = {
        document_id: signatureResult.documentId,
        signer_full_name: certificateInfo.subject?.commonName || 'Nom non disponible',
        original_filename: signatureResult.fileName || 'document.pdf',
        document_hash: signatureResult.originalHash,
        public_key: signatureResult.publicKeyPem,
        signature: signatureResult.signature,
        signature_timestamp: signatureResult.timestamp,
        file_size_original: originalFileData.byteLength,
        file_size_signed: signatureResult.signedDocument.byteLength,
        execution_time: parseFloat(signatureResult.executionTime) || 0,
        original_document_base64: originalDocumentBase64,
        signed_document_base64: signedDocumentBase64
      }

      return signatureData
    } catch (error) {
      console.error('Erreur lors de la préparation des données:', error)
      throw error
    }
  }

  /**
   * Récupérer le token CSRF
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
}
