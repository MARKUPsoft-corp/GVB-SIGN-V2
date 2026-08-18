// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // CSS global
  css: [
    'bootstrap/dist/css/bootstrap.min.css',
    'bootstrap-icons/font/bootstrap-icons.css'
  ],
  
  // Configuration de l'application
  app: {
    head: {
      title: 'GVB Sign - Signature Électronique',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Application de signature électronique avec authentification QR Code' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/gvb-favicon-1755744029.png' },
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'shortcut icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/gvb_icon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800&display=swap' }
      ]
    }
  },
  
  // Auto-import des composants
  components: {
    dirs: [
      '~/components'
    ]
  },
  
  // Configuration des modules
  modules: [
    '@pinia/nuxt'
  ],
  
  // Configuration du serveur de développement
  devServer: {
    port: 3000,
    host: '127.0.0.1'
  },
  
  // Configuration Vite
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/styles/main.scss" as *;'
        }
      }
    }
  },
  
  // Configuration d'environnement
  runtimeConfig: {
    public: {
      // Firebase configuration
      firebaseApiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY,
      firebaseAuthDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
      firebaseProjectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID,
      firebaseStorageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
      firebaseMessagingSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
      firebaseAppId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID,
      firebaseMeasurementId: process.env.NUXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
      // Cloudinary (Public)
      cloudinaryCloudName: process.env.NUXT_PUBLIC_CLOUDINARY_CLOUD_NAME,
      cloudinaryApiKey: process.env.NUXT_PUBLIC_CLOUDINARY_API_KEY
    },
    // Cloudinary (Secret - Utilisable uniquement côté serveur)
    cloudinaryApiSecret: process.env.NUXT_CLOUDINARY_API_SECRET
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "~/assets/styles/main.scss";'
        }
      }
    }
  },
  
  // Configuration du build
  build: {
    transpile: ['bootstrap']
  },
  
  // Configuration des alias
  alias: {
    '@': '~/',
    '~': '~/'
  }
})
