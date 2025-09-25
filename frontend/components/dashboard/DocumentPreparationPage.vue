<template>
  <div class="document-preparation-container">
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
            <div class="page-header">
              <h1 class="page-title">
                <span class="title-main">Préparation</span>
                <span class="title-accent"> de Document</span>
              </h1>
              <p class="page-subtitle">
                Préparez votre document pour la signature hiérarchique et soumettez-le au chef
              </p>
            </div>
          </div>
          <div class="header-bottom-row">
            <button @click="goBack" class="mobile-back-btn">
              <i class="bi bi-arrow-left"></i>
              <span>Retour</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Indicateur de progression -->
    <div class="progress-stepper">
      <!-- Desktop: Jauge circulaire -->
      <div class="stepper-container desktop-only">
        <div class="stepper-line stepper-line-left"></div>
        <div class="stepper-circular-progress">
          <svg class="stepper-progress-ring" width="120" height="120">
            <defs>
              <linearGradient id="stepperGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#0066cc;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#007bff;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#0056b3;stop-opacity:1" />
              </linearGradient>
            </defs>
            <circle
              class="stepper-progress-ring-bg"
              stroke="rgba(255, 255, 255, 0.2)"
              stroke-width="8"
              fill="transparent"
              r="52"
              cx="60"
              cy="60"
            />
            <circle
              class="stepper-progress-ring-fill"
              stroke="url(#stepperGradient)"
              stroke-width="8"
              fill="transparent"
              r="52"
              cx="60"
              cy="60"
              :stroke-dasharray="stepperCircumference"
              :stroke-dashoffset="stepperStrokeDashoffset"
              stroke-linecap="round"
            />
          </svg>
          <div class="stepper-progress-content">
            <div class="stepper-progress-number">{{ currentStep }}</div>
            <div class="stepper-progress-total">/ {{ steps.length }}</div>
          </div>
        </div>
        <div class="stepper-info">
          <div class="stepper-title">
            {{ steps[currentStep - 1]?.title || 'Étape' }}
          </div>
          <div class="stepper-description">
            {{ steps[currentStep - 1]?.description || 'Description de l\'étape' }}
          </div>
        </div>
        <div class="stepper-line stepper-line-right"></div>
      </div>

      <!-- Mobile: Indicateur de progression simple -->
      <div class="mobile-stepper mobile-only">
        <div class="mobile-stepper-header">
          <div class="mobile-step-indicator">
            <span class="mobile-step-number">{{ currentStep }}</span>
            <span class="mobile-step-separator">/</span>
            <span class="mobile-step-total">{{ steps.length }}</span>
          </div>
          <div class="mobile-progress-bar">
            <div 
              class="mobile-progress-fill" 
              :style="{ width: `${(currentStep / steps.length) * 100}%` }"
            ></div>
          </div>
        </div>
        <div class="mobile-step-info">
          <h3 class="mobile-step-title">{{ steps[currentStep - 1]?.title || 'Étape' }}</h3>
          <p class="mobile-step-description">{{ steps[currentStep - 1]?.description || 'Description de l\'étape' }}</p>
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
          <p>Sélectionnez le document PDF que vous souhaitez préparer pour la signature</p>
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
            <span>Positionner les éléments</span>
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Étape 3: Positionnement avec SignBase -->
      <div v-if="currentStep === 3" class="step-content full-height" :key="currentStep">
        <div class="step-header compact">
          <h2>
            <i class="bi bi-pen-fill"></i>
            Positionnement des éléments
          </h2>
          <p>Positionnez la signature et le QR code sur chaque document</p>
          
          <!-- Indicateur de progrès -->
          <div class="progress-indicator" v-if="uploadedFiles.length > 1">
            <div class="circular-progress-container">
              <div class="circular-progress">
                <svg class="progress-ring" width="120" height="120">
                  <defs>
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#0066cc;stop-opacity:1" />
                      <stop offset="50%" style="stop-color:#007bff;stop-opacity:1" />
                      <stop offset="100%" style="stop-color:#0056b3;stop-opacity:1" />
                    </linearGradient>
                  </defs>
                  <circle
                    class="progress-ring-bg"
                    stroke="rgba(255, 255, 255, 0.2)"
                    stroke-width="8"
                    fill="transparent"
                    r="52"
                    cx="60"
                    cy="60"
                  />
                  <circle
                    class="progress-ring-fill"
                    stroke="url(#progressGradient)"
                    stroke-width="8"
                    fill="transparent"
                    r="52"
                    cx="60"
                    cy="60"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="strokeDashoffset"
                    stroke-linecap="round"
                  />
                </svg>
                <div class="progress-content">
                  <div class="progress-number">{{ processedDocuments.size }}</div>
                  <div class="progress-total">/ {{ uploadedFiles.length }}</div>
                </div>
              </div>
              <div class="progress-info">
                <div class="progress-text">
                  Document {{ activeSignBaseTabIndex + 1 }} sur {{ uploadedFiles.length }}
                </div>
                <div class="progress-status">
                  {{ processedDocuments.size }} document(s) traité(s)
                </div>
              </div>
            </div>
          </div>
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
                <p>Chargement de l'outil de positionnement...</p>
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
            :disabled="!allDocumentsProcessed"
            class="action-btn primary"
          >
            <span v-if="allDocumentsProcessed">Finaliser la préparation</span>
            <span v-else>Traitement en cours... ({{ processedDocuments.size }}/{{ uploadedFiles.length }})</span>
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Étape 4: Configuration du workflow -->
      <div v-if="currentStep === 4" class="step-content" :key="currentStep">
        <div class="step-header">
          <h2>
            <i class="bi bi-diagram-3-fill"></i>
            Configuration du workflow
          </h2>
          <p>Configurez le workflow de signature hiérarchique</p>
        </div>

        <div class="workflow-configuration-section">
          <!-- Résumé du document -->
          <div class="summary-status-card">
            <div class="summary-header">
              <div class="summary-status-icon">
                <i class="bi bi-file-earmark-pdf-fill"></i>
              </div>
              <div class="summary-title">
                <h6 class="mb-0">Documents préparés</h6>
                <span class="summary-subtitle text-primary">
                  {{ uploadedFiles.length }} document(s) sélectionné(s)
                </span>
              </div>
              <div class="summary-status-badge">
                <span class="badge bg-primary">{{ currentSignBaseFile?.pages || 1 }} page(s)</span>
              </div>
            </div>

            <div class="summary-content">
              <div class="summary-section">
                <div class="documents-grid">
                  <div v-for="(config, index) in Object.values(documentsConfiguration)" :key="index" class="document-item">
                    <div class="document-header">
                      <i class="bi bi-file-earmark-pdf-fill text-primary"></i>
                      <span class="document-name" :title="config.file.name">{{ truncateFileName(config.file.name, 25) }}</span>
                      <span class="document-pages">{{ config.file.pages || 1 }} page(s)</span>
                    </div>
                    <div class="document-details">
                      <span class="detail-item">
                        <strong>Taille:</strong> {{ formatFileSize(config.file.size) }}
                      </span>
                      <span class="detail-item">
                        <strong>Mode:</strong> {{ getPositionModeLabel(config.positionMode) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Configuration du workflow -->
          <div class="workflow-config-card">
            <div class="workflow-header">
              <h5>
                <i class="bi bi-diagram-3-fill"></i>
                Chaîne de signature
              </h5>
              <p>Définissez l'ordre des signatures</p>
            </div>
            
            <div class="workflow-steps">
              <div class="workflow-step current">
                <div class="step-icon">
                  <i class="bi bi-person-fill"></i>
                </div>
                <div class="step-content">
                  <h6>Secrétaire (Vous)</h6>
                  <p>Préparation du document</p>
                  <span class="step-status completed">Terminé</span>
                </div>
              </div>
              
              <div class="workflow-arrow">
                <i class="bi bi-arrow-down"></i>
              </div>
              
              <div class="workflow-step next">
                <div class="step-icon">
                  <i class="bi bi-person-badge-fill"></i>
                </div>
                <div class="step-content">
                  <h6>Chef+1</h6>
                  <p>Première signature</p>
                  <span class="step-status pending">En attente</span>
                </div>
              </div>
              
              <div class="workflow-arrow">
                <i class="bi bi-arrow-down"></i>
              </div>
              
              <div class="workflow-step future">
                <div class="step-icon">
                  <i class="bi bi-person-gear"></i>
                </div>
                <div class="step-content">
                  <h6>Chef+2</h6>
                  <p>Signature finale</p>
                  <span class="step-status future">À venir</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button @click="previousStep" class="action-btn secondary">
            <i class="bi bi-arrow-left"></i>
            <span>Retour</span>
          </button>
          <button @click="submitForSignature" class="action-btn primary" :disabled="isSubmitting">
            <span v-if="!isSubmitting">Soumettre pour signature</span>
            <span v-else>{{ submissionProgress }}</span>
            <i v-if="!isSubmitting" class="bi bi-send-fill"></i>
            <i v-else class="bi bi-arrow-clockwise spin"></i>
          </button>
        </div>
      </div>

      <!-- Étape 5: Confirmation de soumission -->
      <div v-if="currentStep === 5" class="step-content" :key="currentStep">
        <div class="step-header">
          <h2>
            <i class="bi bi-check-circle-fill"></i>
            Document soumis avec succès
          </h2>
          <p>Votre document a été préparé et soumis au chef pour signature</p>
        </div>

        <div class="submission-success-section">
          <div class="success-card">
            <div class="success-icon">
              <i class="bi bi-check-circle-fill"></i>
            </div>
            <div class="success-content">
              <h3>Document soumis avec succès</h3>
              <p>Votre document a été préparé et transmis au chef pour signature</p>
            </div>
          </div>

          <div class="workflow-status">
            <h4>Statut du workflow</h4>
            <div class="status-timeline">
              <div class="timeline-item completed">
                <div class="timeline-icon">
                  <i class="bi bi-check-circle-fill"></i>
                </div>
                <div class="timeline-content">
                  <h6>Préparation terminée</h6>
                  <p>Document préparé par le secrétaire</p>
                  <span class="timeline-time">{{ new Date().toLocaleString() }}</span>
                </div>
              </div>
              
              <div class="timeline-item pending">
                <div class="timeline-icon">
                  <i class="bi bi-clock-fill"></i>
                </div>
                <div class="timeline-content">
                  <h6>En attente de signature</h6>
                  <p>En attente de signature par le chef</p>
                  <span class="timeline-time">En attente</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button @click="goBackToDocuments" class="action-btn primary">
            <i class="bi bi-arrow-left"></i>
            <span>Retour aux documents</span>
          </button>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '../../stores/auth'
import SignBase from './SignBase.vue'

// Store d'authentification
const authStore = useAuthStore()

// État du stepper
const currentStep = ref(1)
const steps = [
  {
    title: 'Documents',
    description: 'Sélectionnez vos documents PDF'
  },
  {
    title: 'Aperçu',
    description: 'Prévisualisez les documents'
  },
  {
    title: 'Positionner',
    description: 'Placez la signature et le QR code'
  },
  {
    title: 'Workflow',
    description: 'Configurez la chaîne de signature'
  },
  {
    title: 'Soumettre',
    description: 'Transmettez au chef pour signature'
  }
]

// État des fichiers PDF
const uploadedFiles = ref([])
const activeTabIndex = ref(-1)
const activeSignBaseTabIndex = ref(0) // Onglet actif pour SignBase
const isDragging = ref(false)
const hoveredTabIndex = ref(-1) // Index de l'onglet survolé pour l'aperçu
const previewStyle = ref({}) // Style de positionnement de l'aperçu

// État de la préparation
const isPositionConfigured = ref(false)
const signatureData = ref(null)
const positionData = ref(null)

// État pour le traitement multiple des documents
const processedDocuments = ref(new Set()) // Documents traités (index)
const currentDocumentIndex = ref(0) // Index du document en cours de traitement
const allDocumentsProcessed = computed(() => {
  return processedDocuments.value.size === uploadedFiles.value.length
})

// Structure pour stocker la configuration complète de tous les documents
const documentsConfiguration = ref({}) // Stockage des configurations par document
const currentDocumentConfig = ref(null) // Configuration du document en cours

// État pour la soumission
const isSubmitting = ref(false)
const submissionProgress = ref('')
const submissionResults = ref([])

// Propriétés pour la jauge circulaire
const circumference = computed(() => 2 * Math.PI * 52) // 2πr avec r=52
const strokeDashoffset = computed(() => {
  const progress = uploadedFiles.value.length > 0 ? processedDocuments.value.size / uploadedFiles.value.length : 0
  return circumference.value * (1 - progress)
})

// Propriétés pour la jauge circulaire du stepper
const stepperCircumference = computed(() => 2 * Math.PI * 52) // 2πr avec r=52
const stepperStrokeDashoffset = computed(() => {
  const progress = steps.length > 0 ? (currentStep.value - 1) / (steps.length - 1) : 0
  return stepperCircumference.value * (1 - progress)
})

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

const currentSignBaseFile = computed(() => {
  if (activeSignBaseTabIndex.value >= 0 && uploadedFiles.value[activeSignBaseTabIndex.value]) {
    return uploadedFiles.value[activeSignBaseTabIndex.value]
  }
  return null
})

// Événements
const emit = defineEmits(['go-back'])

// Navigation
const goBack = () => {
  emit('go-back')
}

const goBackToDocuments = () => {
  emit('go-back')
}

// Navigation entre étapes
const nextStep = () => {
  if (currentStep.value < steps.length) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

// Gestion des fichiers
const handleDragEnter = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragOver = (e) => {
  e.preventDefault()
}

const handleDragLeave = (e) => {
  e.preventDefault()
  isDragging.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragging.value = false
  
  const files = Array.from(e.dataTransfer.files)
  handleFiles(files)
}

const handleFileSelect = (e) => {
  const files = Array.from(e.target.files)
  handleFiles(files)
}

const handleFiles = async (files) => {
  for (const file of files) {
    if (file.type === 'application/pdf') {
      const fileObj = {
        file: file,
        name: file.name,
        size: file.size,
        url: URL.createObjectURL(file),
        pages: null // Sera calculé plus tard
      }
      
      // Calculer le nombre de pages (simulation)
      fileObj.pages = Math.floor(Math.random() * 10) + 1
      
      uploadedFiles.value.push(fileObj)
    }
  }
  
  // Activer le premier onglet
  if (uploadedFiles.value.length > 0) {
    activeTabIndex.value = 0
    activeSignBaseTabIndex.value = 0
  }
}

const removeFile = (index) => {
  // Libérer l'URL de l'objet
  if (uploadedFiles.value[index]?.url) {
    URL.revokeObjectURL(uploadedFiles.value[index].url)
  }
  
  uploadedFiles.value.splice(index, 1)
  
  // Ajuster les index actifs
  if (activeTabIndex.value >= uploadedFiles.value.length) {
    activeTabIndex.value = uploadedFiles.value.length - 1
  }
  if (activeSignBaseTabIndex.value >= uploadedFiles.value.length) {
    activeSignBaseTabIndex.value = uploadedFiles.value.length - 1
  }
  
  // Si plus de fichiers, réinitialiser
  if (uploadedFiles.value.length === 0) {
    activeTabIndex.value = -1
    activeSignBaseTabIndex.value = 0
  }
}

// Gestion des onglets
const switchTab = (index) => {
  activeTabIndex.value = index
}

const switchSignBaseTab = (index) => {
  activeSignBaseTabIndex.value = index
}

// Aperçu des onglets
const showTabPreview = (index, event) => {
  hoveredTabIndex.value = index
  const rect = event.target.getBoundingClientRect()
  previewStyle.value = {
    position: 'fixed',
    top: `${rect.bottom + 10}px`,
    left: `${rect.left}px`,
    zIndex: 1000
  }
}

const hideTabPreview = () => {
  hoveredTabIndex.value = -1
}

const getFilePreviewUrl = (file) => {
  return file?.url || ''
}

// Gestion PDF
const onPdfLoaded = () => {
  pdfLoaded.value = true
}

const onPdfLoadError = () => {
  console.error('Erreur lors du chargement du PDF')
}

// Gestion SignBase
const handlePositionConfirmed = (data) => {
  console.log('Position confirmée:', data)
  isPositionConfigured.value = true
  positionData.value = data
}

const handlePositionChanged = (data) => {
  console.log('Position changée:', data)
}

const handleSignatureUploaded = (data) => {
  console.log('Signature uploadée:', data)
  signatureData.value = data
}

const handlePdfGenerated = (data) => {
  console.log('PDF généré:', data)
  
  // Marquer le document comme traité
  processedDocuments.value.add(activeSignBaseTabIndex.value)
  
  // Stocker la configuration
  documentsConfiguration.value[activeSignBaseTabIndex.value] = {
    file: uploadedFiles.value[activeSignBaseTabIndex.value],
    positionMode: data.positionMode,
    qrCode: data.qrCode,
    signature: data.signature,
    generatedPdf: data.generatedPdf
  }
  
  // Passer au document suivant si disponible
  if (activeSignBaseTabIndex.value < uploadedFiles.value.length - 1) {
    activeSignBaseTabIndex.value++
  }
}

// Utilitaires
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const truncateFileName = (fileName, maxLength) => {
  if (fileName.length <= maxLength) return fileName
  return fileName.substring(0, maxLength) + '...'
}

const getPositionModeLabel = (mode) => {
  const modes = {
    'manual': 'Manuel',
    'auto': 'Automatique',
    'template': 'Modèle'
  }
  return modes[mode] || 'Inconnu'
}

// Soumission du document
const submitForSignature = async () => {
  isSubmitting.value = true
  submissionProgress.value = 'Préparation de la soumission...'
  
  try {
    // Simuler la soumission
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    submissionProgress.value = 'Document soumis avec succès'
    
    // Passer à l'étape suivante
    nextStep()
  } catch (error) {
    console.error('Erreur lors de la soumission:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Initialisation
onMounted(() => {
  console.log('DocumentPreparationPage montée')
})

// Nettoyage
onUnmounted(() => {
  // Libérer les URLs des objets
  uploadedFiles.value.forEach(file => {
    if (file.url) {
      URL.revokeObjectURL(file.url)
    }
  })
})
</script>

<style scoped>
/* Variables CSS */
:root {
  --primary-blue: #0066cc;
  --primary-blue-dark: #0056b3;
  --text-dark: #2c3e50;
  --text-muted: #6c757d;
  --success: #28a745;
  --warning: #ffc107;
  --danger: #dc3545;
  --light-gray: #f8f9fa;
  --border-color: #dee2e6;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* STYLES GÉNÉRAUX */
.document-preparation-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  position: relative;
  overflow-x: hidden;
}

/* Bouton de fermeture */
.close-button-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
}

.close-btn-round {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-dark);
  font-size: 1.2rem;
}

.close-btn-round:hover {
  background: rgba(220, 53, 69, 0.1);
  color: var(--danger);
  transform: scale(1.1);
}

/* HEADER */
.documents-header {
  padding: 2rem 0;
  margin-bottom: 2rem;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.header-content {
  text-align: center;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 3.5rem;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.title-main {
  color: var(--text-dark);
}

.title-accent {
  color: var(--primary-blue);
}

.page-subtitle {
  font-size: 1.2rem;
  color: var(--text-muted);
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

.mobile-back-btn {
  display: none;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-dark);
  text-decoration: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.mobile-back-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Stepper moderne - Jauge circulaire */
.progress-stepper {
  padding: 0;
  margin-bottom: 1rem;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.5s forwards;
}

.stepper-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  justify-content: center;
  position: relative;
}

.stepper-line {
  width: 20vw;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(0, 102, 204, 0.3) 50%, transparent 100%);
  border-radius: 1px;
  position: relative;
}

.stepper-line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 0%, rgba(0, 102, 204, 0.6) 50%, transparent 100%);
  border-radius: 1px;
  animation: stepperLineGlow 2s ease-in-out infinite alternate;
}

.stepper-line {
  animation: stepperLineFloat 4s ease-in-out infinite;
}

.stepper-line-left {
  animation-delay: 0s;
}

.stepper-line-right {
  animation-delay: 2s;
}

@keyframes stepperLineFloat {
  0%, 100% {
    transform: translateX(0px);
  }
  50% {
    transform: translateX(5px);
  }
}

.stepper-line-left {
  transform: translateX(-10px);
}

.stepper-line-right {
  transform: translateX(10px);
}

@keyframes stepperLineGlow {
  0% {
    opacity: 0.3;
    transform: scaleX(0.8);
  }
  100% {
    opacity: 0.8;
    transform: scaleX(1.2);
  }
}

.stepper-circular-progress {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: stepperContainerFloat 3s ease-in-out infinite;
  overflow: hidden;
  border-radius: 50%;
}

@keyframes stepperContainerFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

.stepper-progress-ring {
  transform: rotate(-90deg);
  filter: drop-shadow(0 4px 8px rgba(0, 102, 204, 0.3));
}

.stepper-progress-ring-bg {
  transition: stroke 0.3s ease;
}

.stepper-progress-ring-fill {
  transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 2px 4px rgba(0, 102, 204, 0.4));
  animation: stepperProgressPulse 2s ease-in-out infinite;
  transform-origin: center;
}

@keyframes stepperProgressPulse {
  0%, 100% {
    filter: drop-shadow(0 2px 4px rgba(0, 102, 204, 0.4));
    stroke-width: 8;
    transform: scale(1);
  }
  50% {
    filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.6));
    stroke-width: 10;
    transform: scale(1.02);
  }
}

.stepper-progress-content {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.stepper-progress-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary-blue);
  line-height: 1;
  text-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
  animation: stepperNumberGlow 2s ease-in-out infinite;
}

@keyframes stepperNumberGlow {
  0%, 100% {
    text-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
    transform: scale(1);
  }
  50% {
    text-shadow: 0 4px 12px rgba(0, 102, 204, 0.5);
    transform: scale(1.05);
  }
}

.stepper-progress-total {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-muted);
  opacity: 0.8;
}

.stepper-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 250px;
}

.stepper-title {
  font-weight: 600;
  color: var(--primary-blue);
  font-size: 1.2rem;
  text-align: left;
}

.stepper-description {
  font-size: 0.9rem;
  color: var(--text-muted);
  opacity: 0.8;
  text-align: left;
  line-height: 1.4;
}

/* Mobile stepper */
.mobile-stepper {
  display: none;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  margin: 0 1rem;
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
}

.mobile-stepper-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.mobile-step-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 600;
  color: var(--primary-blue);
}

.mobile-step-number {
  font-size: 1.2rem;
}

.mobile-step-separator {
  font-size: 0.9rem;
  opacity: 0.6;
}

.mobile-step-total {
  font-size: 1rem;
  opacity: 0.8;
}

.mobile-progress-bar {
  flex: 1;
  height: 4px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.mobile-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-blue), #007bff);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.mobile-step-info {
  text-align: left;
}

.mobile-step-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.mobile-step-description {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
}

/* CONTENU PRINCIPAL */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}

.step-content {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.step-content.full-height {
  min-height: 70vh;
}

.step-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-header.compact {
  margin-bottom: 1rem;
}

.step-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.step-header h2 i {
  color: var(--primary-blue);
  font-size: 1.8rem;
}

.step-header p {
  font-size: 1.1rem;
  color: var(--text-muted);
  margin: 0;
  line-height: 1.5;
}

/* SECTION UPLOAD */
.upload-section {
  margin-bottom: 2rem;
}

.upload-dropzone {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.upload-dropzone:hover,
.upload-dropzone.dragover {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.05);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.file-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}

.upload-icon {
  font-size: 3rem;
  color: var(--primary-blue);
  opacity: 0.8;
}

.upload-text h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.upload-text p {
  font-size: 1.1rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.upload-text .link {
  color: var(--primary-blue);
  text-decoration: underline;
  cursor: pointer;
}

.upload-text small {
  font-size: 0.9rem;
  color: var(--text-muted);
  opacity: 0.8;
}

.files-preview {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.file-icon {
  font-size: 1.5rem;
  color: var(--danger);
}

.file-details h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.file-details p {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
}

.remove-file-btn {
  margin-left: auto;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(220, 53, 69, 0.1);
  color: var(--danger);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  background: var(--danger);
  color: white;
  transform: scale(1.1);
}

/* SECTION PREVIEW */
.preview-section {
  margin-bottom: 2rem;
}

.pdf-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.pdf-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(248, 249, 250, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 200px;
}

.pdf-tab:hover {
  background: rgba(0, 102, 204, 0.05);
  border-color: var(--primary-blue);
  transform: translateY(-1px);
}

.pdf-tab.active {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
}

.tab-title {
  font-weight: 500;
  font-size: 0.9rem;
}

.tab-pages {
  font-size: 0.8rem;
  opacity: 0.8;
}

.tab-close-btn {
  margin-left: auto;
  width: 20px;
  height: 20px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: inherit;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
}

.tab-close-btn:hover {
  background: rgba(220, 53, 69, 0.8);
  color: white;
}

.document-viewer {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.pdf-container {
  position: relative;
  width: 100%;
  height: 600px;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.pdf-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: var(--light-gray);
}

.fallback-content {
  text-align: center;
  padding: 2rem;
}

.fallback-content i {
  font-size: 3rem;
  color: var(--danger);
  margin-bottom: 1rem;
}

.fallback-content h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.fallback-content p {
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary-blue);
  color: white;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.download-btn:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.no-files-message {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}

.no-files-message i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* SECTION SIGNBASE */
.signbase-container {
  margin-bottom: 2rem;
}

.signbase-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.signbase-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(248, 249, 250, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 200px;
}

.signbase-tab:hover {
  background: rgba(0, 102, 204, 0.05);
  border-color: var(--primary-blue);
  transform: translateY(-1px);
}

.signbase-tab.active {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
}

.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* PROGRESS INDICATOR */
.progress-indicator {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.circular-progress-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.circular-progress {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-ring {
  transform: rotate(-90deg);
  filter: drop-shadow(0 2px 4px rgba(0, 102, 204, 0.3));
}

.progress-ring-bg {
  transition: stroke 0.3s ease;
}

.progress-ring-fill {
  transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 2px 4px rgba(0, 102, 204, 0.4));
}

.progress-content {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.progress-number {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary-blue);
  line-height: 1;
}

.progress-total {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
  opacity: 0.8;
}

.progress-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.progress-text {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.9rem;
}

.progress-status {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* WORKFLOW CONFIGURATION */
.workflow-configuration-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-status-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.summary-status-icon {
  width: 48px;
  height: 48px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.5rem;
}

.summary-title h6 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.summary-subtitle {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.summary-status-badge {
  margin-left: auto;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.bg-primary {
  background: var(--primary-blue);
  color: white;
}

.bg-success {
  background: var(--success);
  color: white;
}

.bg-warning {
  background: var(--warning);
  color: var(--text-dark);
}

.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.document-item {
  padding: 1rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.document-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.document-name {
  font-weight: 600;
  color: var(--text-dark);
  flex: 1;
}

.document-pages {
  font-size: 0.8rem;
  color: var(--text-muted);
  background: rgba(0, 102, 204, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.document-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.detail-item strong {
  color: var(--text-dark);
}

/* WORKFLOW CONFIG */
.workflow-config-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.workflow-header {
  text-align: center;
  margin-bottom: 2rem;
}

.workflow-header h5 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.workflow-header h5 i {
  color: var(--primary-blue);
}

.workflow-header p {
  color: var(--text-muted);
  margin: 0;
}

.workflow-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.workflow-step.current {
  background: rgba(0, 102, 204, 0.05);
  border-color: var(--primary-blue);
}

.workflow-step.next {
  background: rgba(255, 193, 7, 0.05);
  border-color: var(--warning);
}

.workflow-step.future {
  background: rgba(108, 117, 125, 0.05);
  border-color: var(--text-muted);
}

.step-icon {
  width: 48px;
  height: 48px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.2rem;
}

.workflow-step.next .step-icon {
  background: rgba(255, 193, 7, 0.1);
  color: var(--warning);
}

.workflow-step.future .step-icon {
  background: rgba(108, 117, 125, 0.1);
  color: var(--text-muted);
}

.step-content {
  flex: 1;
}

.step-content h6 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.step-status {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.step-status.completed {
  background: rgba(40, 167, 69, 0.1);
  color: var(--success);
}

.step-status.pending {
  background: rgba(255, 193, 7, 0.1);
  color: var(--warning);
}

.step-status.future {
  background: rgba(108, 117, 125, 0.1);
  color: var(--text-muted);
}

.workflow-arrow {
  display: flex;
  justify-content: center;
  color: var(--text-muted);
  font-size: 1.2rem;
}

/* SUBMISSION SUCCESS */
.submission-success-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.success-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  background: rgba(40, 167, 69, 0.05);
  border: 1px solid rgba(40, 167, 69, 0.2);
  border-radius: 12px;
}

.success-icon {
  font-size: 3rem;
  color: var(--success);
}

.success-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.success-content p {
  color: var(--text-muted);
  margin: 0;
}

.workflow-status h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.status-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.timeline-item.completed {
  border-color: var(--success);
  background: rgba(40, 167, 69, 0.05);
}

.timeline-item.pending {
  border-color: var(--warning);
  background: rgba(255, 193, 7, 0.05);
}

.timeline-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.timeline-item.completed .timeline-icon {
  background: var(--success);
  color: white;
}

.timeline-item.pending .timeline-icon {
  background: var(--warning);
  color: var(--text-dark);
}

.timeline-content h6 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.timeline-content p {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.timeline-time {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* ACTIONS */
.step-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.action-btn.primary {
  background: var(--primary-blue);
  color: white;
}

.action-btn.primary:hover:not(:disabled) {
  background: var(--primary-blue-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.action-btn.secondary {
  background: rgba(108, 117, 125, 0.1);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.action-btn.secondary:hover {
  background: rgba(108, 117, 125, 0.2);
  transform: translateY(-2px);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* APERÇU ONGLET */
.tab-preview {
  position: fixed;
  width: 300px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(10px);
  z-index: 1000;
  overflow: hidden;
}

.preview-content {
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(0, 102, 204, 0.05);
  border-bottom: 1px solid var(--border-color);
  font-weight: 500;
  color: var(--text-dark);
}

.preview-header i {
  color: var(--danger);
}

.preview-body {
  display: flex;
  flex-direction: column;
}

.preview-pdf {
  height: 200px;
  border-bottom: 1px solid var(--border-color);
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-info {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  background: rgba(248, 249, 250, 0.5);
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

.spin {
  animation: spin 1s linear infinite;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }
  
  .mobile-only {
    display: block;
  }
  
  .mobile-back-btn {
    display: flex;
  }
  
  .page-title {
    font-size: 2.5rem;
  }
  
  .step-content {
    padding: 1.5rem;
  }
  
  .step-actions {
    flex-direction: column;
  }
  
  .action-btn {
    justify-content: center;
  }
  
  .workflow-steps {
    gap: 0.5rem;
  }
  
  .workflow-step {
    padding: 0.75rem;
  }
  
  .step-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .documents-grid {
    grid-template-columns: 1fr;
  }
  
  .success-card {
    flex-direction: column;
    text-align: center;
  }
  
  .timeline-item {
    flex-direction: column;
    text-align: center;
  }
}

@media (min-width: 769px) {
  .desktop-only {
    display: flex;
  }
  
  .mobile-only {
    display: none;
  }
}
</style>
