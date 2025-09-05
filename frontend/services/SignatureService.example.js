/**
 * Exemple d'utilisation du SignatureService
 * Ce fichier montre comment utiliser le service de signature numérique
 */

import { SignatureService } from './SignatureService.js'
import { CertificateService } from './CertificateService.js'

// Exemple d'utilisation complète
async function exempleSignatureComplete() {
  try {
    // 1. Initialiser les services
    const signatureService = new SignatureService()
    const certificateService = new CertificateService()
    
    signatureService.initialize()
    certificateService.initialize()
    
    // 2. Récupérer le certificat depuis la session storage
    const certificateInfo = certificateService.getCertificateInfo()
    if (!certificateInfo) {
      throw new Error('Aucun certificat disponible')
    }
    
    // 3. Récupérer les clés privée et publique
    const privateKeyPem = certificateService.getPrivateKeyPem()
    const publicKeyPem = certificateService.getPublicKeyPem()
    
    if (!privateKeyPem || !publicKeyPem) {
      throw new Error('Clés manquantes')
    }
    
    // 4. Convertir les clés PEM en objets node-forge
    const privateKey = forge.pki.privateKeyFromPem(privateKeyPem)
    const publicKey = forge.pki.publicKeyFromPem(publicKeyPem)
    
    // 5. Préparer les données du document (exemple avec un fichier)
    const fileInput = document.getElementById('pdf-file')
    const file = fileInput.files[0]
    const documentData = await file.arrayBuffer()
    
    // 6. Préparer les métadonnées (positions depuis l'étape 3)
    const metadata = {
      qr_position: {
        x: 85,        // Position X en pourcentage
        y: 10,        // Position Y en pourcentage
        size: 'medium', // Taille du QR code
        pages: 'all', // Pages où appliquer
        mode: 'all'   // Mode d'application
      },
      signature_position: {
        signature_image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...', // Image base64
        positions: [
          {
            page: 1,
            x: 50,    // Position X en pourcentage
            y: 80,    // Position Y en pourcentage
          }
        ],
        signature_size: 60 // Taille en pourcentage
      }
    }
    
    // 7. Signer le document
    console.log('Début de la signature...')
    const result = await signatureService.signDocumentComplete(
      documentData,
      privateKey,
      publicKey,
      metadata
    )
    
    // 8. Traiter le résultat
    if (result.success) {
      console.log('Signature réussie!')
      console.log(`ID du document: ${result.documentId}`)
      console.log(`Hash original: ${result.originalHash}`)
      console.log(`Temps d'exécution: ${result.executionTime}s`)
      
      // 9. Télécharger le PDF signé
      const blob = new Blob([result.signedDocument], { type: 'application/pdf' })
      const url = URL.createObjectURL(blob)
      
      const a = document.createElement('a')
      a.href = url
      a.download = `document_signé_${result.documentId}.pdf`
      a.click()
      
      URL.revokeObjectURL(url)
    }
    
  } catch (error) {
    console.error('Erreur lors de la signature:', error)
    alert(`Erreur: ${error.message}`)
  }
}

export { exempleSignatureComplete }
