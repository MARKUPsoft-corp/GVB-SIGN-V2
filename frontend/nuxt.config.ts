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
    host: 'localhost'
  },
  
  // Configuration Vite
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
