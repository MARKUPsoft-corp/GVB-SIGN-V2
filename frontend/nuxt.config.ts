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
        { rel: 'apple-touch-icon', href: '/gvb_icon.png' }
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
  modules: [],
  
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
