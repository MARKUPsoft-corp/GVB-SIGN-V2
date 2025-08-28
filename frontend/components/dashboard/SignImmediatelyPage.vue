<template>
  <div class="sign-immediately-container">
    <!-- Bouton retour rond style fermer -->
    <div class="close-button-container">
      <button @click="goBack" class="close-btn-round">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <!-- Header avec titre de la section -->
    <div class="documents-header">
      <div class="header-container">
        <div class="header-content">
          <div class="header-top-row">
            <h1 class="section-title">
              <span class="text-dark">Signature</span>
              <span class="text-primary-blue"> Immédiate</span>
            </h1>
          </div>
          <p class="section-subtitle">Signez vos documents rapidement et en toute sécurité</p>
          <div class="header-bottom-row">
            <button @click="goBack" class="mobile-back-btn">
              <i class="bi bi-arrow-left"></i>
              <span>Retour</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Indicateur de progression (Stepper) -->
    <div class="progress-stepper">
      <div class="stepper-container">
        <!-- Ligne de fond pour le stepper -->
        <div class="stepper-background-line"></div>
        
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          :class="['step-item', {
            'active': currentStep === index + 1,
            'completed': currentStep > index + 1,
            'disabled': currentStep < index + 1,
            'mobile-hidden': currentStep !== index + 1
          }]"
        >
          <div class="step-circle">
            <i v-if="currentStep > index + 1" class="bi bi-check-lg"></i>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="step-content">
            <h4>{{ step.title }}</h4>
            <p>{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenu principal avec les étapes -->
    <div class="main-content">
      <!-- Étape 1: Upload du PDF -->
      <div v-if="currentStep === 1" class="step-content" :key="currentStep">
        <div class="step-header">
          <h2>
            <i class="bi bi-cloud-upload-fill"></i>
            Upload votre document
          </h2>
          <p>Sélectionnez le document PDF que vous souhaitez signer</p>
        </div>

        <div class="upload-section">
          <div 
            :class="['upload-dropzone', { 'dragover': isDragging }]"
            @dragenter.prevent="handleDragEnter"
            @dragover.prevent="handleDragOver"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleDrop"
          >
            <input 
              type="file" 
              id="pdf-upload" 
              accept=".pdf" 
              multiple
              @change="handleFileSelect" 
              class="file-input"
              ref="fileInput"
            >
            <label for="pdf-upload" class="upload-label">
              <div class="upload-icon">
                <i class="bi bi-file-earmark-pdf-fill"></i>
              </div>
              <div class="upload-text">
                <h3>Glissez-déposez vos PDF ici</h3>
                <p>ou <span class="link">cliquez pour sélectionner</span></p>
                <small>Formats acceptés: PDF uniquement • Taille max: 50MB par fichier</small>
              </div>
            </label>
          </div>

          <div v-if="uploadedFiles.length > 0" class="files-preview">
            <div v-for="(file, index) in uploadedFiles" :key="index" class="file-info">
              <div class="file-icon">
                <i class="bi bi-file-earmark-pdf-fill"></i>
              </div>
              <div class="file-details">
                <h4>{{ file.name }}</h4>
                <p>{{ formatFileSize(file.size) }} • {{ file.pages || 'Calcul...' }} page(s)</p>
              </div>
              <button @click="removeFile(index)" class="remove-file-btn">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button 
            @click="nextStep" 
            :disabled="uploadedFiles.length === 0"
            class="action-btn primary"
          >
            <span>Continuer</span>
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Étape 2: Prévisualisation du PDF -->
      <div v-if="currentStep === 2" class="step-content" :key="currentStep">
        <div class="step-header">
          <h2>
            <i class="bi bi-eye-fill"></i>
            Aperçu du document
          </h2>
          <p>Vérifiez le contenu de votre document avant de continuer</p>
        </div>

        <div class="preview-section">
          <!-- Onglets des fichiers -->
          <div class="pdf-tabs">
            <div 
              v-for="(file, index) in uploadedFiles" 
              :key="index"
              :class="['pdf-tab', { 'active': activeTabIndex === index }]"
              @click="switchTab(index)"
              @mouseenter="showTabPreview(index, $event)"
              @mouseleave="hideTabPreview"
            >
              <i class="bi bi-file-earmark-pdf-fill"></i>
              <span class="tab-title">{{ file.name }}</span>
              <span class="tab-pages" v-if="file.pages">{{ file.pages }} pages</span>
              <button 
                @click.stop="removeFile(index)" 
                class="tab-close-btn"
                title="Fermer cet onglet"
              >
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>

          <!-- Visualiseur PDF -->
          <div class="document-viewer" v-if="activeTabIndex >= 0 && uploadedFiles[activeTabIndex]">
            <div class="pdf-container" ref="pdfContainer">
              <!-- Solution simple avec iframe native -->
              <iframe
                v-if="currentPdfSource"
                :src="currentPdfSource"
                class="pdf-iframe"
                frameborder="0"
                @load="onPdfLoaded"
                @error="onPdfLoadError"
              ></iframe>
              
              <!-- Fallback si iframe ne fonctionne pas -->
              <div v-else class="pdf-fallback">
                <div class="fallback-content">
                  <i class="bi bi-file-earmark-pdf-fill"></i>
                  <h3>{{ uploadedFiles[activeTabIndex]?.name }}</h3>
                  <p>Cliquez pour télécharger le PDF</p>
                  <a 
                    :href="currentPdfSource" 
                    :download="uploadedFiles[activeTabIndex]?.name"
                    class="download-btn"
                  >
                    <i class="bi bi-download"></i>
                    Télécharger le PDF
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Message si aucun fichier sélectionné -->
          <div v-if="uploadedFiles.length === 0" class="no-files-message">
            <i class="bi bi-file-earmark-pdf"></i>
            <p>Aucun fichier PDF sélectionné</p>
          </div>
        </div>

        <div class="step-actions">
          <button @click="previousStep" class="action-btn secondary">
            <i class="bi bi-arrow-left"></i>
            <span>Retour</span>
          </button>
          <button @click="nextStep" class="action-btn primary">
            <span>Positionner la signature</span>
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Étape 3: Positionnement avec SignBase -->
      <div v-if="currentStep === 3" class="step-content full-height" :key="currentStep">
        <div class="step-header compact">
          <h2>
            <i class="bi bi-pen-fill"></i>
            Positionnement de la signature
          </h2>
          <p>Positionnez votre signature et le QR code sur le document</p>
        </div>

        <div class="signbase-container">
          <!-- Onglets des fichiers pour SignBase -->
          <div class="signbase-tabs" v-if="uploadedFiles.length > 1">
            <div 
              v-for="(file, index) in uploadedFiles" 
              :key="index"
              :class="['signbase-tab', { 'active': activeSignBaseTabIndex === index }]"
              @click="switchSignBaseTab(index)"
              @mouseenter="showTabPreview(index, $event)"
              @mouseleave="hideTabPreview"
            >
              <i class="bi bi-file-earmark-pdf-fill"></i>
              <span class="tab-title">{{ file.name }}</span>
              <span class="tab-pages" v-if="file.pages">{{ file.pages }} pages</span>
              <button 
                @click.stop="removeFile(index)" 
                class="tab-close-btn"
                title="Fermer cet onglet"
              >
                <i class="bi bi-x"></i>
              </button>
            </div>
          </div>

          <ClientOnly>
                          <SignBase
                v-if="currentSignBaseFile"
                :pdf-file="currentSignBaseFile.file"
                :total-pages="currentSignBaseFile.pages || 1"
                @position-confirmed="handlePositionConfirmed"
                @position-changed="handlePositionChanged"
                @signature-uploaded="handleSignatureUploaded"
                @pdf-generated="handlePdfGenerated"
              />
            <template #fallback>
              <div class="loading-placeholder">
                <div class="loading-spinner"></div>
                <p>Chargement de l'outil de signature...</p>
              </div>
            </template>
          </ClientOnly>
        </div>

        <div class="step-actions">
          <button @click="previousStep" class="action-btn secondary">
            <i class="bi bi-arrow-left"></i>
            <span>Retour</span>
          </button>
          <button 
            @click="nextStep" 
            :disabled="!isPositionConfigured"
            class="action-btn primary"
          >
            <span>Configurer le certificat</span>
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>



      <!-- Étape 4: Signature finale -->
      <div v-if="currentStep === 4" class="step-content" :key="currentStep">
        <div class="step-header">
          <h2>
            <i class="bi bi-pen-fill"></i>
            Finaliser la signature
          </h2>
          <p>Vérifiez les informations et procédez à la signature du document</p>
        </div>

        <div class="signature-summary">
          <div class="summary-section">
            <h3>
              <i class="bi bi-file-earmark-text"></i>
              Document à signer
            </h3>
            <div class="document-info">
              <div class="doc-preview">
                <i class="bi bi-file-earmark-pdf-fill"></i>
                <div class="doc-details">
                  <h4>{{ currentSignBaseFile?.name }}</h4>
                  <p>{{ currentSignBaseFile?.pages || 1 }} page(s) • {{ formatFileSize(currentSignBaseFile?.size || 0) }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="summary-section">
            <h3>
              <i class="bi bi-shield-check"></i>
              Certificat utilisé
            </h3>
            <div class="certificate-info">
              <div class="cert-preview">
                <i class="bi bi-award-fill"></i>
                <div class="cert-details">
                  <h4>{{ certificateFile?.name }}</h4>
                  <p>Certificat de signature électronique</p>
                </div>
              </div>
            </div>
          </div>

          <div class="summary-section">
            <h3>
              <i class="bi bi-geo-alt-fill"></i>
              Positionnement
            </h3>
            <div class="position-info">
              <div class="position-details">
                <div class="position-item">
                  <i class="bi bi-pen"></i>
                  <span>Signature manuscrite positionnée</span>
                </div>
                <div class="position-item">
                  <i class="bi bi-qr-code"></i>
                  <span>QR code de vérification ajouté</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="signature-actions">
          <div class="final-warning">
            <div class="warning-icon">
              <i class="bi bi-exclamation-triangle-fill"></i>
            </div>
            <div class="warning-content">
              <h4>Attention</h4>
              <p>La signature électronique aura la même valeur juridique qu'une signature manuscrite. Cette action est irréversible.</p>
            </div>
          </div>

          <div class="step-actions">
            <button @click="previousStep" class="action-btn secondary">
              <i class="bi bi-arrow-left"></i>
              <span>Retour</span>
            </button>
            <button @click="proceedSignature" class="action-btn signature">
              <i class="bi bi-lightning-charge-fill"></i>
              <span>Signer le document</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Aperçu de l'onglet survolé -->
  <div v-if="hoveredTabIndex >= 0" class="tab-preview" :style="previewStyle">
    <div class="preview-content">
      <div class="preview-header">
        <i class="bi bi-file-earmark-pdf-fill"></i>
        <span>{{ uploadedFiles[hoveredTabIndex]?.name }}</span>
      </div>
      <div class="preview-body">
        <div class="preview-pdf">
          <iframe 
            :src="getFilePreviewUrl(uploadedFiles[hoveredTabIndex])"
            class="preview-iframe"
            frameborder="0"
          ></iframe>
        </div>
        <div class="preview-info">
          <span>{{ uploadedFiles[hoveredTabIndex]?.pages || 1 }} pages</span>
          <span>{{ formatFileSize(uploadedFiles[hoveredTabIndex]?.size || 0) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, defineEmits } from 'vue'
import SignBase from './SignBase.vue'

// Émissions
const emit = defineEmits(['go-back'])

// État du stepper
const currentStep = ref(1)
const steps = [
  {
    title: 'Télécharger',
    description: 'Sélectionnez votre document PDF'
  },
  {
    title: 'Aperçu',
    description: 'Prévisualisez le document'
  },
  {
    title: 'Positionner',
    description: 'Placez la signature et le QR code'
  },
  {
    title: 'Signer',
    description: 'Finalisez la signature'
  }
]

// État des fichiers PDF
const uploadedFiles = ref([])
const activeTabIndex = ref(-1)
const activeSignBaseTabIndex = ref(0) // Onglet actif pour SignBase
const isDragging = ref(false)
const hoveredTabIndex = ref(-1) // Index de l'onglet survolé pour l'aperçu
const previewStyle = ref({}) // Style de positionnement de l'aperçu



// État de la signature
const isPositionConfigured = ref(false)
const signatureData = ref(null)
const positionData = ref(null)

// Références DOM
const fileInput = ref(null)
const pdfContainer = ref(null)

// État pour la preview PDF
const pdfLoaded = ref(false)

// Computed properties pour le fichier actif
const currentPdfSource = computed(() => {
  if (activeTabIndex.value >= 0 && uploadedFiles.value[activeTabIndex.value]) {
    return uploadedFiles.value[activeTabIndex.value].url
  }
  return null
})

// Computed property pour le fichier actif dans SignBase
const currentSignBaseFile = computed(() => {
  if (activeSignBaseTabIndex.value >= 0 && uploadedFiles.value[activeSignBaseTabIndex.value]) {
    return uploadedFiles.value[activeSignBaseTabIndex.value]
  }
  return null
})



// Navigation du stepper
function nextStep() {
  if (currentStep.value < steps.length) {
    currentStep.value++
  }
}

// Gestion des onglets
function switchTab(index) {
  activeTabIndex.value = index
}

// Gestion des onglets SignBase
function switchSignBaseTab(index) {
  activeSignBaseTabIndex.value = index
}

// Fonctions pour l'aperçu des onglets
function showTabPreview(index, event) {
  hoveredTabIndex.value = index
  
  // Positionner l'aperçu par rapport à l'onglet survolé
  const rect = event.target.getBoundingClientRect()
  const previewWidth = 400
  const previewHeight = 300
  
  // Calculer la position optimale
  let left = rect.left + (rect.width / 2) - (previewWidth / 2)
  let top = rect.bottom + 10
  
  // Ajuster si l'aperçu dépasse les bords de l'écran
  if (left < 20) left = 20
  if (left + previewWidth > window.innerWidth - 20) {
    left = window.innerWidth - previewWidth - 20
  }
  if (top + previewHeight > window.innerHeight - 20) {
    top = rect.top - previewHeight - 10
  }
  
  previewStyle.value = {
    position: 'fixed',
    left: `${left}px`,
    top: `${top}px`,
    zIndex: 10000
  }
}

function hideTabPreview() {
  hoveredTabIndex.value = -1
}

function getFilePreviewUrl(file) {
  return file.url
}

function previousStep() {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

function goBack() {
  emit('go-back')
}

// Gestion de l'upload de fichiers
function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  const validFiles = files.filter(file => file.type === 'application/pdf')
  
  if (validFiles.length > 0) {
    validFiles.forEach(file => handleFileUpload(file))
  } else {
    alert('Veuillez sélectionner des fichiers PDF valides.')
  }
}

function handleFileUpload(file) {
  // Vérifier qu'on est côté client
  if (!process.client) return
  
  // Vérifier la taille (50MB max)
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    alert(`Le fichier ${file.name} est trop volumineux. Taille maximum autorisée : 50MB`)
    return
  }

  // Vérifier si le fichier n'est pas déjà uploadé
  const existingFile = uploadedFiles.value.find(f => f.name === file.name && f.size === file.size)
  if (existingFile) {
    alert(`Le fichier ${file.name} est déjà uploadé.`)
    return
  }

  // Ajouter le fichier à la liste
  uploadedFiles.value.push({
    file: file,
    name: file.name,
    size: file.size,
    pages: null, // Sera calculé plus tard
    url: URL.createObjectURL(file)
  })
  
  // Activer le premier onglet si c'est le premier fichier
  if (uploadedFiles.value.length === 1) {
    activeTabIndex.value = 0
    activeSignBaseTabIndex.value = 0
  }
  
  console.log('Fichier PDF ajouté:', file.name)
}

function removeFile(index) {
  if (!process.client) return
  
  const fileToRemove = uploadedFiles.value[index]
  if (fileToRemove && fileToRemove.url) {
    URL.revokeObjectURL(fileToRemove.url)
  }
  
  uploadedFiles.value.splice(index, 1)
  
  // Ajuster l'onglet actif si nécessaire
  if (uploadedFiles.value.length === 0) {
    activeTabIndex.value = -1
    activeSignBaseTabIndex.value = 0
  } else if (activeTabIndex.value >= uploadedFiles.value.length) {
    activeTabIndex.value = uploadedFiles.value.length - 1
  }
  
  // Ajuster l'onglet SignBase si nécessaire
  if (activeSignBaseTabIndex.value >= uploadedFiles.value.length) {
    activeSignBaseTabIndex.value = uploadedFiles.value.length - 1
  }
  
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Gestion du drag & drop
function handleDragEnter(event) {
  event.preventDefault()
  isDragging.value = true
}

function handleDragOver(event) {
  event.preventDefault()
}

function handleDragLeave(event) {
  event.preventDefault()
  // Vérifier si on quitte vraiment la zone de drop
  if (!event.currentTarget.contains(event.relatedTarget)) {
    isDragging.value = false
  }
}

function handleDrop(event) {
  event.preventDefault()
  isDragging.value = false
  
  const files = Array.from(event.dataTransfer.files)
  const validFiles = files.filter(file => file.type === 'application/pdf')
  
  if (validFiles.length > 0) {
    validFiles.forEach(file => handleFileUpload(file))
  } else {
    alert('Veuillez déposer des fichiers PDF valides.')
  }
}

// Gestion du PDF
function onPdfLoaded(event) {
  console.log('PDF chargé via iframe:', event)
  pdfLoaded.value = true
  
  // Pour l'iframe, on ne peut pas facilement détecter le nombre de pages
  // On utilise une valeur par défaut ou on peut implémenter une détection via PDF.js si nécessaire
  if (activeTabIndex.value >= 0 && uploadedFiles.value[activeTabIndex.value]) {
    // Valeur par défaut, peut être améliorée avec PDF.js
    uploadedFiles.value[activeTabIndex.value].pages = 1
  }
}

function onPdfLoadError(error) {
  console.error('Erreur lors du chargement du PDF:', error)
  alert('Erreur lors du chargement du PDF. Veuillez réessayer.')
}





// Gestion de SignBase
function handlePositionConfirmed(data) {
  console.log('Position confirmée:', data)
  positionData.value = data
  isPositionConfigured.value = true
}

// Debug: Log du fichier actuel pour SignBase
console.log('SignImmediatelyPage - currentSignBaseFile:', currentSignBaseFile.value)

function handlePositionChanged(data) {
  console.log('Position changée:', data)
  positionData.value = data
}

function handleSignatureUploaded(file) {
  console.log('Signature uploadée:', file)
  signatureData.value = file
}

function handlePdfGenerated(data) {
  console.log('PDF généré:', data)
  // Le PDF avec la signature et QR code est prêt
}

// Signature finale
function proceedSignature() {
  // TODO: Implémenter la logique de signature avec le backend
  console.log('Procéder à la signature...')
  console.log('Fichier PDF:', currentSignBaseFile.value)
  console.log('Position:', positionData.value)
  console.log('Signature:', signatureData.value)
  
  // Pour l'instant, afficher un message
  alert('Fonctionnalité de signature en cours d\'implémentation. Les données sont prêtes pour le backend.')
}

// Utilitaires
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Propriétés calculées
const canProceedToNext = computed(() => {
  switch (currentStep.value) {
    case 1:
      return uploadedFiles.value.length > 0
    case 2:
      return true // Aperçu toujours accessible
    case 3:
      return isPositionConfigured.value
    case 4:
      return true // Dernière étape
    default:
      return false
  }
})

// Cycle de vie
onMounted(() => {
  console.log('SignImmediatelyPage monté')
})

onUnmounted(() => {
  // Nettoyer les URL d'objets
  uploadedFiles.value.forEach(file => {
    if (file.url) {
      URL.revokeObjectURL(file.url)
    }
  })
})
</script>

<style scoped>
/* Utilisation des variables CSS du dashboard */
/* Les variables sont définies dans main.scss et sont disponibles globalement */

/* Conteneur principal */
.sign-immediately-container {
  background: transparent;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  padding: 0;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Header de la page - Style identique à DocumentsPage */
.documents-header {
  padding: 0.25rem 0;
  margin-bottom: 2rem;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.header-content {
  width: 100%;
  text-align: center;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-top-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 0.5rem;
}

.header-bottom-row {
  display: none;
  justify-content: flex-start;
  margin-top: 1rem;
}

.mobile-back-btn {
  display: none;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--text-dark);
  border: 1px solid #e2e8f0;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  text-decoration: none;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mobile-back-btn:hover {
  background: rgba(255, 255, 255, 1);
  border-color: var(--primary-blue);
  transform: translateX(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.section-title {
  font-size: 2.8rem;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 0;
  font-weight: 400;
}

.close-button-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.close-btn-round {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--text-dark);
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  text-decoration: none;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.close-btn-round:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #dc3545;
  color: #dc3545;
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Stepper moderne - Style cohérent avec le header */
.progress-stepper {
  padding: 1rem 0;
  margin-bottom: 0.5rem;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.5s forwards;
}

.stepper-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.stepper-background-line {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: #e2e8f0;
  z-index: 0;
}

.stepper-background-line::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: #28a745;
  transition: width 0.3s ease;
  width: 0%;
}

/* Progression de la ligne selon l'étape actuelle */
.progress-0 .stepper-background-line::after {
  width: 0%;
}

.progress-1 .stepper-background-line::after {
  width: 25%;
}

.progress-2 .stepper-background-line::after {
  width: 50%;
}

.progress-3 .stepper-background-line::after {
  width: 75%;
}

.progress-4 .stepper-background-line::after {
  width: 100%;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
  z-index: 2;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 12px;
  border: 2px solid #e2e8f0;
  background: #f8f9fa;
  color: #6c757d;
}

.step-item.active .step-circle {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1);
  transform: scale(1.1);
}

.step-item.completed .step-circle {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.step-content {
  text-align: center;
  min-height: 40px;
}

.step-content h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 2px 0;
  transition: color 0.3s ease;
}

.step-content p {
  font-size: 0.75rem;
  color: var(--dark-gray);
  margin: 0;
  line-height: 1.3;
}

.step-item.active .step-content h4 {
  color: var(--primary-blue);
}

.step-item.completed .step-content h4 {
  color: #28a745;
}



/* Contenu principal - Style glassmorphisme comme la modale du profil */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 2rem;
  min-height: 600px;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.7s forwards;
}

/* Style pour la barre de scroll du contenu principal */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Pour Firefox */
.main-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

.full-height {
  min-height: 800px;
}

/* Animation pour les transitions d'étapes */
.step-content {
  animation: stepTransition 0.5s ease-out;
}

@keyframes stepTransition {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.step-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 1.5rem;
  border-radius: 12px;
  margin: 0 0 2rem 0;
}

.step-header.compact {
  margin-bottom: 24px;
  padding-bottom: 16px;
}

.step-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  letter-spacing: -0.025em;
}

.step-header h2 i {
  color: var(--primary-blue);
  font-size: 1.5rem;
}

.step-header p {
  color: var(--dark-gray);
  margin: 0;
  font-size: 1.125rem;
  line-height: 1.6;
}

/* Zone d'upload avec drag & drop */
.upload-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Onglets PDF - Style Dashboard */
.pdf-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  overflow-x: auto;
  padding: 0 8px 0 0;
  justify-content: flex-start;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px 8px 0 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
}

.pdf-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 0;
  flex-shrink: 0;
  position: relative;
  margin-right: 2px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.pdf-tab:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.pdf-tab.active {
  background: rgba(0, 102, 204, 0.2);
  color: var(--primary-blue);
  border-color: rgba(0, 102, 204, 0.5);
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
  z-index: 1;
}

.pdf-tab i {
  font-size: 0.9rem;
  color: var(--text-dark);
}

.pdf-tab.active i {
  color: var(--primary-blue);
}

.tab-title {
  font-weight: 500;
  font-size: 0.8rem;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-dark);
}

.tab-pages {
  font-size: 0.7rem;
  opacity: 0.7;
  background: rgba(0, 0, 0, 0.1);
  padding: 1px 5px;
  border-radius: 10px;
  color: var(--text-dark);
}

.pdf-tab.active .tab-pages {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

/* Bouton de fermeture des onglets */
.tab-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: none;
  background: transparent;
  color: var(--text-dark);
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
  margin-left: 4px;
  opacity: 0.7;
}

.tab-close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-dark);
  opacity: 1;
}

.tab-close-btn i {
  font-size: 0.75rem;
}

/* Aperçu des onglets */
.tab-preview {
  animation: previewFadeIn 0.2s ease-out;
}

.preview-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  width: 400px;
  height: 300px;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(0, 102, 204, 0.1);
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
  font-weight: 600;
  color: var(--text-dark);
}

.preview-header i {
  color: #dc2626;
  font-size: 1rem;
}

.preview-body {
  padding: 12px;
  height: calc(100% - 60px);
  display: flex;
  flex-direction: column;
}

.preview-pdf {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-info {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

@keyframes previewFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Message si aucun fichier */
.no-files-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--dark-gray);
  text-align: center;
}

.no-files-message i {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-files-message p {
  font-size: 1.1rem;
  margin: 0;
}

.upload-dropzone {
  border: 3px dashed #e2e8f0;
  border-radius: 16px;
  padding: 60px 40px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8f9fa;
  position: relative;
  overflow: hidden;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-dropzone:hover {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.04);
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.upload-dropzone.dragover {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.08);
  transform: scale(1.02);
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1);
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  cursor: pointer;
  color: var(--dark-gray);
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.upload-icon {
  width: 80px;
  height: 80px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: var(--primary-blue);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.upload-dropzone:hover .upload-icon {
  transform: scale(1.1) rotate(5deg);
  background: rgba(0, 102, 204, 0.15);
}

.upload-text h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 8px 0;
}

.upload-text p {
  margin: 0 0 16px 0;
  color: var(--dark-gray);
}

.upload-text .link {
  color: var(--primary-blue);
  font-weight: 600;
  text-decoration: underline;
}

.upload-text small {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Prévisualisation de fichiers */
.files-preview {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.file-icon {
  width: 60px;
  height: 60px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #dc2626;
  flex-shrink: 0;
}

.file-details {
  flex: 1;
}

.file-details h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 4px 0;
}

.file-details p {
  color: var(--dark-gray);
  margin: 0;
  font-size: 0.8rem;
}

.remove-file-btn {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.remove-file-btn:hover {
  background: rgba(220, 53, 69, 0.2);
  transform: scale(1.1);
}

/* Section de prévisualisation PDF */
.preview-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.document-viewer {
  flex: 1;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  min-height: 800px;
}



.pdf-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
  min-height: 700px;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-height: 700px;
}

.pdf-fallback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: var(--dark-gray);
  text-align: center;
}

.fallback-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.fallback-content i {
  font-size: 3rem;
  color: #dc2626;
}

.fallback-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0;
}

.fallback-content p {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin: 0;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--primary-blue);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.download-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  color: #6c757d;
  padding: 60px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f8f9fa;
  border-radius: 50%;
  border-top-color: var(--primary-blue);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Conteneur SignBase */
.signbase-container {
  flex: 1;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

/* Onglets SignBase - Style Dashboard */
.signbase-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  overflow-x: auto;
  padding: 0 8px 0 0;
  justify-content: flex-start;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px 8px 0 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
}

.signbase-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px 12px 20px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 0;
  flex-shrink: 0;
  position: relative;
  margin-right: 2px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.signbase-tab:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.signbase-tab.active {
  background: rgba(0, 102, 204, 0.2);
  color: var(--primary-blue);
  border-color: rgba(0, 102, 204, 0.5);
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
  z-index: 1;
}

.signbase-tab i {
  font-size: 1rem;
  color: var(--text-dark);
}

.signbase-tab.active i {
  color: var(--primary-blue);
}

.signbase-tab .tab-title {
  font-weight: 500;
  font-size: 0.875rem;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-dark);
}

.signbase-tab .tab-pages {
  font-size: 0.75rem;
  opacity: 0.7;
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 12px;
  color: var(--text-dark);
}

.signbase-tab.active .tab-pages {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}



/* Résumé de signature */
.signature-summary {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.summary-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.summary-section h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-section h3 i {
  color: var(--primary-blue);
}

.document-info, .certificate-info {
  background: white;
  border-radius: var(--radius-sm);
  padding: 16px;
  border: 1px solid var(--border-color);
}

.doc-preview {
  display: flex;
  align-items: center;
  gap: 16px;
}

.doc-preview i {
  font-size: 2rem;
  color: #dc2626;
}

.doc-details {
  flex: 1;
}

.doc-details h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 4px 0;
}

.doc-details p {
  color: var(--text-secondary);
  margin: 0;
  font-size: 0.9rem;
}

.position-details {
  background: white;
  border-radius: var(--radius-sm);
  padding: 16px;
  border: 1px solid var(--border-color);
}

.position-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  color: var(--text-color);
  font-weight: 500;
}

.position-item i {
  color: var(--success-color);
}

.position-item:not(:last-child) {
  border-bottom: 1px solid var(--border-color);
}

/* Avertissement final */
.final-warning {
  display: flex;
  gap: 16px;
  background: rgba(255, 193, 7, 0.05);
  border: 1px solid rgba(255, 193, 7, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.warning-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 193, 7, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: #ffc107;
  flex-shrink: 0;
}

.warning-content h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 8px 0;
}

.warning-content p {
  color: var(--dark-gray);
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Actions des étapes */
.step-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: auto;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.step-actions:has(.action-btn:only-child) {
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  min-width: 120px;
  justify-content: center;
  text-decoration: none;
}

.action-btn.secondary {
  background: #f8f9fa;
  color: var(--text-dark);
  border: 1px solid #e2e8f0;
}

.action-btn.secondary:hover {
  background: #e9ecef;
  border-color: var(--dark-gray);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.action-btn.primary {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

.action-btn.signature {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
  color: white;
  border: none;
  min-width: 140px;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.action-btn.signature:hover {
  background: linear-gradient(135deg, #1e7e34 0%, #155724 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

.action-btn:disabled {
  background: #6c757d;
  color: white;
  border-color: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
}

.action-btn i {
  font-size: 1rem;
}

/* ANIMATIONS */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.2);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 1024px) {
  .stepper-container {
    flex-direction: column;
    gap: 24px;
  }
  
  .step-item {
    flex-direction: row;
    text-align: left;
    width: 100%;
  }
  
  .step-circle {
    margin-bottom: 0;
    margin-right: 16px;
    flex-shrink: 0;
  }
  
  .step-connector {
    display: none;
  }
  
  .step-panel {
    padding: 32px 24px;
  }
}

@media (max-width: 768px) {
  .sign-immediately-container {
    padding: 0;
  }
  
  .close-button-container {
    display: none;
  }
  
  .header-top-row {
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0;
    text-align: center;
  }
  
  .section-title {
    text-align: center;
    margin-bottom: 0;
  }
  
  .header-bottom-row {
    display: flex;
    justify-content: center;
    width: 100%;
  }
  
  .mobile-back-btn {
    display: flex;
    flex-shrink: 0;
  }
  
  .documents-header {
    padding: 0.5rem 0;
  }
  
  .header-container {
    max-width: 600px;
  }
  
  .header-content {
    text-align: center;
  }
  
  .section-title {
    font-size: 3rem;
  }
  
  .section-subtitle {
    font-size: 1.25rem;
  }
  
  .progress-stepper,
  .main-content {
    margin-bottom: 24px;
  }
  
  .progress-stepper {
    padding: 0.75rem 0;
    margin-bottom: 0.75rem;
  }
  
  .step-item.mobile-hidden {
    display: none;
  }
  
  .stepper-container {
    justify-content: center;
    align-items: center;
  }
  
  .step-item {
    flex: none;
    width: auto;
    text-align: center;
  }
  
  .step-content {
    text-align: center;
    min-width: 200px;
  }
  
  .close-button-container {
    display: none;
  }
  
  .stepper-background-line {
    display: none;
  }
  
  .step-panel {
    padding: 24px 20px;
  }
  
  .step-header h2 {
    font-size: 1.5rem;
    flex-direction: column;
    gap: 12px;
  }
  
  .upload-dropzone {
    padding: 40px 20px;
  }
  
  .upload-icon {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }
  
  .viewer-controls {
    flex-direction: column;
    gap: 16px;
  }
  
  .step-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .action-btn {
    width: 100%;
    min-width: auto;
  }
  
  .file-info {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .final-warning {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .documents-header {
    padding: 0.5rem 0;
  }
  
  .header-top-row {
    gap: 12px;
  }
  
  .section-title {
    font-size: 2.1rem;
  }
  
  .section-subtitle {
    font-size: 1rem;
  }
  
  .mobile-back-btn {
    padding: 4px 8px;
    font-size: 0.8rem;
  }
  
  .progress-stepper {
    padding: 1rem 0;
    margin-bottom: 0.5rem;
  }
  
  .step-panel {
    padding: 20px 16px;
  }
  
  .step-header h2 {
    font-size: 1.25rem;
  }
  
  .upload-dropzone {
    padding: 32px 16px;
    min-height: 250px;
  }
  
  .upload-text h3 {
    font-size: 1.25rem;
  }
  
  .step-circle {
    width: 48px;
    height: 48px;
    font-size: 1rem;
  }
  
  .action-btn {
    padding: 12px 20px;
    font-size: 0.9rem;
  }
}
</style>
