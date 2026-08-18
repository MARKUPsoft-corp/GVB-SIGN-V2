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

      const data = await response.json()

      if (!data.success) {
        throw new Error(data.error || 'Erreur lors de l\'upload')
      }

      console.log('✅ Upload Cloudinary réussi:', data.url)
      return data.url
    } catch (error) {
      console.error('❌ Erreur CloudinaryService:', error)
      throw error
    }
  }
}
