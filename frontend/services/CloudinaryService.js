export default class CloudinaryService {
  /**
   * Uploade un fichier Base64 vers Cloudinary via l'API interne Nuxt
   * @param {string} base64Data - Les données du fichier en Base64 (doit commencer par 'data:...')
   * @param {string} filename - Le nom de fichier souhaité
   * @param {string} folder - (Optionnel) Le sous-dossier dans lequel uploader
   * @returns {Promise<string>} L'URL sécurisée Cloudinary du fichier
   */
  static async uploadPdf(base64Data, filename, folder = 'gvb_sign_documents') {
    try {
      console.log(`🚀 Upload vers Cloudinary en cours pour: ${filename}`)
      
      const response = await fetch('/api/cloudinary/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          file: base64Data,
          filename: filename,
          folder: folder
        })
      })

      const textData = await response.text()
      let data
      try {
        data = JSON.parse(textData)
      } catch (e) {
        throw new Error(`Server returned non-JSON (${response.status}): ${textData.substring(0, 100)}...`)
      }

      if (!response.ok || !data.success) {
        const errorMsg = data.error || data.statusMessage || `Erreur serveur HTTP ${response.status}`
        if (errorMsg.includes('429')) {
          throw new Error("Limite d'utilisation Cloudinary atteinte (Quota dépassé). Veuillez patienter ou vérifier votre compte Cloudinary.")
        }
        throw new Error(errorMsg)
      }

      console.log('✅ Upload Cloudinary réussi:', data.url)
      return data.url
    } catch (error) {
      console.error('❌ Erreur CloudinaryService:', error)
      throw error
    }
  }
}
