import { ref, computed } from 'vue'
import fr from '../locales/fr.js'
import en from '../locales/en.js'

const messages = { fr, en }

// État partagé réactif global (singleton entre tous les composants Nuxt)
const currentLocale = ref('fr')
const isInitialized = ref(false)

export const useI18n = () => {
  // Initialisation côté client au premier appel
  if (process.client && !isInitialized.value) {
    try {
      const savedLocale = localStorage.getItem('gvb_locale')
      if (savedLocale && (savedLocale === 'fr' || savedLocale === 'en')) {
        currentLocale.value = savedLocale
      } else {
        // Détecter la langue du navigateur si aucune préférence n'est enregistrée
        const browserLang = navigator.language || navigator.userLanguage || ''
        if (browserLang.toLowerCase().startsWith('en')) {
          currentLocale.value = 'en'
        } else {
          currentLocale.value = 'fr'
        }
        localStorage.setItem('gvb_locale', currentLocale.value)
      }
      
      if (document.documentElement) {
        document.documentElement.lang = currentLocale.value
      }
    } catch (e) {
      console.warn('Erreur lors de la lecture de la langue locale:', e)
    }
    isInitialized.value = true
  }

  /**
   * Traduire une clé avec remplacement optionnel de paramètres
   * Exemple : t('common.save') ou t('signBase.pageIndicator', { current: 1, total: 5 })
   */
  const t = (key, replacements = {}) => {
    if (!key || typeof key !== 'string') return ''

    const keys = key.split('.')
    
    // Recherche dans la langue active
    let translation = keys.reduce((obj, k) => (obj && obj[k] !== undefined) ? obj[k] : null, messages[currentLocale.value])

    // Repli (fallback) sur l'autre langue si la clé est absente
    if (translation === null || translation === undefined) {
      const fallbackLang = currentLocale.value === 'fr' ? 'en' : 'fr'
      translation = keys.reduce((obj, k) => (obj && obj[k] !== undefined) ? obj[k] : null, messages[fallbackLang])
    }

    // Si la traduction est introuvable, retourner la clé
    if (translation === null || translation === undefined) {
      return key
    }

    // Remplacement des paramètres dynamiques {variable}
    if (typeof translation === 'string' && replacements && Object.keys(replacements).length > 0) {
      return Object.keys(replacements).reduce((acc, paramKey) => {
        const regex = new RegExp(`\\{${paramKey}\\}`, 'g')
        return acc.replace(regex, replacements[paramKey])
      }, translation)
    }

    return translation
  }

  /**
   * Définir la langue active
   */
  const setLocale = (newLocale) => {
    if (newLocale !== 'fr' && newLocale !== 'en') return
    currentLocale.value = newLocale

    if (process.client) {
      try {
        localStorage.setItem('gvb_locale', newLocale)
        if (document.documentElement) {
          document.documentElement.lang = newLocale
        }
      } catch (e) {
        console.warn('Erreur lors de la sauvegarde de la langue:', e)
      }
    }
  }

  /**
   * Basculer entre Français et Anglais
   */
  const toggleLocale = () => {
    setLocale(currentLocale.value === 'fr' ? 'en' : 'fr')
  }

  return {
    locale: currentLocale,
    currentLocale: computed(() => currentLocale.value),
    isEnglish: computed(() => currentLocale.value === 'en'),
    isFrench: computed(() => currentLocale.value === 'fr'),
    locales: ['fr', 'en'],
    t,
    setLocale,
    toggleLocale
  }
}
