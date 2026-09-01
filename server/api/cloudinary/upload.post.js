import { defineEventHandler, readBody } from 'h3'
import { v2 as cloudinary } from 'cloudinary'

export default defineEventHandler(async (event) => {
  try {
    const config = useRuntimeConfig()
    const body = await readBody(event)
    
    // Configurer Cloudinary avec les variables d'environnement (y compris le secret côté serveur)
    cloudinary.config({
      cloud_name: config.public.cloudinaryCloudName,
      api_key: config.public.cloudinaryApiKey,
      api_secret: config.cloudinaryApiSecret
    })

    const { file, folder, filename } = body

    if (!file) {
      return {
        success: false,
        error: 'Aucun fichier fourni'
      }
    }

    // Paramètres d'upload pour Cloudinary
    const uploadOptions = {
      folder: folder || 'gvb_sign_documents',
      resource_type: 'auto'
    }

    // Ajouter le nom de fichier personnalisé si fourni
    if (filename) {
      // Cloudinary prend public_id pour le nom du fichier
      uploadOptions.public_id = filename.replace(/\.[^/.]+$/, "") // Enlever l'extension
    }

    // Effectuer l'upload vers Cloudinary
    const result = await cloudinary.uploader.upload(file, uploadOptions)

    return {
      success: true,
      url: result.secure_url,
      public_id: result.public_id,
      format: result.format,
      bytes: result.bytes
    }
  } catch (error) {
    console.error('Erreur lors de l\'upload vers Cloudinary:', error)
    return {
      success: false,
      error: error.message || 'Erreur lors de l\'upload'
    }
  }
})
