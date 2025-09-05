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
            <div class="page-header">
              <h1 class="page-title">
                <span class="title-main">Signature</span>
                <span class="title-accent"> Immédiate</span>
            </h1>
              <p class="page-subtitle">
                Signez vos documents rapidement et en toute sécurité avec votre certificat personnel
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
          <p>Positionnez votre signature et le QR code sur chaque document</p>
          
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
            :disabled="!allDocumentsProcessed"
            class="action-btn primary"
          >
            <span v-if="allDocumentsProcessed">Finaliser la signature</span>
            <span v-else>Traitement en cours... ({{ processedDocuments.size }}/{{ uploadedFiles.length }})</span>
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

        <div class="signature-summary-section">
          
          <!-- Résumé du document -->
          <div class="summary-status-card">
            <div class="summary-header">
              <div class="summary-status-icon">
                <i class="bi bi-file-earmark-pdf-fill"></i>
            </div>
              <div class="summary-title">
                <h6 class="mb-0">Documents à signer</h6>
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

          <!-- Résumé du positionnement -->
          <div class="summary-status-card">
            <div class="summary-header">
              <div class="summary-status-icon">
                <i class="bi bi-geo-alt-fill"></i>
        </div>
              <div class="summary-title">
                <h6 class="mb-0">Positionnement des éléments</h6>
                <span class="summary-subtitle" :class="isPositionConfigured ? 'text-success' : 'text-warning'">
                  {{ isPositionConfigured ? 'Éléments positionnés avec succès' : 'Aucun élément positionné' }}
                </span>
      </div>
              <div class="summary-status-badge">
                <span class="badge" :class="isPositionConfigured ? 'bg-success' : 'bg-warning'">
                  {{ isPositionConfigured ? 'Prêt' : 'En attente' }}
                </span>
              </div>
        </div>

                                                  <div class="summary-content">
          <div class="summary-section">
            <div class="positioning-grid">
              <!-- Résumé par document -->
              <div v-for="(config, index) in Object.values(documentsConfiguration)" :key="index" class="document-positioning">
                <h6 class="document-title">
                  <i class="bi bi-file-earmark-pdf-fill text-primary me-2"></i>
                  <span :title="config.file.name">{{ truncateFileName(config.file.name, 25) }}</span>
                </h6>
                
                <!-- QR Code -->
                <div v-if="config.qrCode" class="positioning-item qr-item">
                  <div class="positioning-icon">
                    <i class="bi bi-qr-code text-success"></i>
                </div>
                  <div class="positioning-details">
                    <span class="positioning-title">QR Code de vérification</span>
                    <div class="positioning-info-grid">
                      <span class="info-label">Taille:</span>
                      <span class="info-value">{{ config.qrCode.size }}</span>
                      <span class="info-label">Mode:</span>
                      <span class="info-value">{{ getPositionModeLabel(config.qrCode.mode) }}</span>
                      <span class="info-label">Pages:</span>
                      <span class="info-value">{{ formatPages(config.qrCode.pages) }}</span>
              </div>
            </div>
          </div>

                <!-- Signature manuscrite -->
                <div v-if="config.signature" class="positioning-item signature-item">
                  <div class="positioning-icon">
                    <i class="bi bi-pen-fill text-primary"></i>
                  </div>
                  <div class="positioning-details">
                    <span class="positioning-title">Signature manuscrite</span>
                    <div class="positioning-info-grid">
                      <span class="info-label">Taille:</span>
                      <span class="info-value">{{ config.signature.size }}%</span>
                      <span class="info-label">Pages:</span>
                      <span class="info-value">{{ formatPages(config.signature.pages) }}</span>
                    </div>
                    <!-- Aperçu de la signature -->
                    <div class="signature-preview">
                      <img :src="config.signature.imageUrl" alt="Signature" class="signature-thumbnail">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

          <!-- Résumé du certificat -->
          <div class="summary-status-card">
            <div class="summary-header">
              <div class="summary-status-icon">
              <i class="bi bi-shield-check"></i>
                </div>
              <div class="summary-title">
                <h6 class="mb-0">Certificat de signature</h6>
                <span class="summary-subtitle" :class="certificateInfo ? 'text-success' : 'text-warning'">
                  {{ certificateInfo ? 'Certificat valide et prêt' : 'Aucun certificat importé' }}
                </span>
              </div>
              <div class="summary-status-badge">
                <span class="badge" :class="certificateInfo ? 'bg-success' : 'bg-warning'">
                  {{ certificateInfo ? 'Valide' : 'Manquant' }}
                </span>
            </div>
          </div>

            <div class="summary-content">
          <div class="summary-section">
            <div v-if="certificateInfo" class="info-grid">
              <div class="info-item">
                <span class="info-label">Titulaire</span>
                <span class="info-value">{{ certificateInfo.subject?.commonName || 'N/A' }}</span>
                </div>
              <div class="info-item">
                <span class="info-label">Organisation</span>
                <span class="info-value">{{ certificateInfo.subject?.organization || 'N/A' }}</span>
                </div>
              <div class="info-item">
                <span class="info-label">Numéro de série</span>
                <span class="info-value serial-number">{{ certificateInfo.serialNumber || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Validité</span>
                <span class="info-value" :class="certificateInfo.validity?.isValid ? 'text-success' : 'text-danger'">
                  {{ certificateInfo.validity?.isValid ? 'Valide' : 'Expiré' }}
                </span>
            </div>
          </div>
                        <div v-else class="no-certificate-message">
              <i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>
              <span>Aucun certificat n'est disponible. Veuillez importer un certificat valide pour procéder à la signature.</span>
              <button @click="refreshCertificate" class="refresh-btn">
                <i class="bi bi-arrow-clockwise"></i>
                Actualiser
              </button>
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
          <button @click="proceedToSignature" class="action-btn primary" :disabled="isSigning">
            <span v-if="!isSigning">Signer le document</span>
            <span v-else>{{ signatureProgress }}</span>
            <i v-if="!isSigning" class="bi bi-lightning-charge-fill"></i>
            <i v-else class="bi bi-arrow-clockwise spin"></i>
            </button>
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
import { CertificateService } from '../../services/CertificateService.js'
import { SignatureService } from '../../services/SignatureService.js'
import JSZip from 'jszip'
import forge from 'node-forge'

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

// État pour le traitement multiple des documents
const processedDocuments = ref(new Set()) // Documents traités (index)
const currentDocumentIndex = ref(0) // Index du document en cours de traitement
const allDocumentsProcessed = computed(() => {
  return processedDocuments.value.size === uploadedFiles.value.length
})

// Structure pour stocker la configuration complète de tous les documents
const documentsConfiguration = ref({}) // Stockage des configurations par document
const currentDocumentConfig = ref(null) // Configuration du document en cours

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

// Service de gestion des certificats
const certificateService = new CertificateService()

// Service de signature numérique
const signatureService = new SignatureService()

// État de la signature
const isSigning = ref(false)
const signatureProgress = ref('')

// Données du certificat depuis la session storage
const certificateInfo = ref(null)

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
  // Retourner des données de test pour l'étape 4 si aucun fichier n'est sélectionné
  if (currentStep.value === 4) {
    return {
      name: 'document-test.pdf',
      size: 1024000,
      pages: 2
    }
  }
  return null
})



// Navigation du stepper
function nextStep() {
  if (currentStep.value < steps.length) {
    currentStep.value++
    
    // Réinitialiser l'état quand on entre dans l'étape 3
    if (currentStep.value === 3) {
      processedDocuments.value.clear()
      activeSignBaseTabIndex.value = 0
      isPositionConfigured.value = false
      positionData.value = null
      signatureData.value = null
      documentsConfiguration.value = {}
      currentDocumentConfig.value = null
    }
    
    // Préparer les données finales quand on passe à l'étape 4
    if (currentStep.value === 4) {
      prepareFinalConfiguration()
    }
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
  
  // Collecter toutes les informations de configuration du document actuel
  const currentFile = uploadedFiles.value[activeSignBaseTabIndex.value]
  
  // Récupérer les positions par défaut ou spécifiques selon le mode
  let defaultX = 85, defaultY = 10
  if (data.qr?.positions?.default) {
    defaultX = data.qr.positions.default.x
    defaultY = data.qr.positions.default.y
  }
  
  const documentConfig = {
    file: currentFile,
    qrCode: {
      size: data.qr?.size || 'medium',
      pages: data.qr?.pages || 'all',
      positions: data.qr?.positions || {},
      mode: data.qr?.mode || 'all',
      x: defaultX,  // Position par défaut
      y: defaultY   // Position par défaut
    },
    signature: data.signature ? {
      imageUrl: data.signature.imageUrl,
      size: data.signature.size,
      pages: data.signature.pages,
      positions: data.signature.positions,
      // Récupérer les positions depuis la structure correcte
      x: data.signature.positions?.default?.x || data.signature.positions?.[currentPage.value]?.x || 50,
      y: data.signature.positions?.default?.y || data.signature.positions?.[currentPage.value]?.y || 50
    } : null,
    positionMode: data.mode || 'all',
    timestamp: new Date().toISOString()
  }
  
  // Stocker la configuration du document actuel
  documentsConfiguration.value[activeSignBaseTabIndex.value] = documentConfig
  currentDocumentConfig.value = documentConfig
  
  // Log pour déboguer les positions
  console.log('Configuration QR Code stockée:', {
    size: documentConfig.qrCode.size,
    pages: documentConfig.qrCode.pages,
    positions: documentConfig.qrCode.positions,
    mode: documentConfig.qrCode.mode,
    x: documentConfig.qrCode.x,
    y: documentConfig.qrCode.y
  })
  
  // Log pour déboguer la signature
  if (documentConfig.signature) {
    console.log('Configuration Signature stockée:', {
      imageUrl: documentConfig.signature.imageUrl,
      size: documentConfig.signature.size,
      pages: documentConfig.signature.pages,
      positions: documentConfig.signature.positions,
      x: documentConfig.signature.x,
      y: documentConfig.signature.y
    })
  } else {
    console.log('Aucune signature configurée')
  }
  
  // Marquer le document actuel comme traité
  processedDocuments.value.add(activeSignBaseTabIndex.value)
  
  // Passer automatiquement au document suivant
  moveToNextDocument()
}

// Fonction pour passer au document suivant
function moveToNextDocument() {
  const nextIndex = activeSignBaseTabIndex.value + 1
  
  if (nextIndex < uploadedFiles.value.length) {
    // Passer au document suivant
    activeSignBaseTabIndex.value = nextIndex
    // Réinitialiser l'état pour le nouveau document
    isPositionConfigured.value = false
    positionData.value = null
    signatureData.value = null
  } else {
    // Tous les documents ont été traités
    console.log('Tous les documents ont été traités')
  }
}

// Fonction pour préparer la configuration finale de tous les documents
function prepareFinalConfiguration() {
  console.log('Préparation de la configuration finale...')
  console.log('Configuration des documents:', documentsConfiguration.value)
  
  // Vérifier que tous les documents ont été configurés
  const allConfigured = uploadedFiles.value.every((_, index) => 
    documentsConfiguration.value[index] && processedDocuments.value.has(index)
  )
  
  if (!allConfigured) {
    console.warn('Certains documents ne sont pas encore configurés')
  }
}

// Fonction pour formater le label du mode de positionnement
function getPositionModeLabel(mode) {
  const labels = {
    'all': 'Toutes les pages',
    'current': 'Page actuelle',
    'custom': 'Pages sélectionnées',
    'individual': 'Pages individuelles'
  }
  return labels[mode] || mode
}

// Fonction pour formater l'affichage des pages
function formatPages(pages) {
  if (pages === 'all') return 'Toutes les pages'
  if (Array.isArray(pages)) {
    if (pages.length === 1) return `Page ${pages[0]}`
    return `Pages ${pages.join(', ')}`
  }
  return 'Page spécifique'
}

// Fonction pour rafraîchir les informations du certificat
function refreshCertificate() {
  console.log('Rafraîchissement des informations du certificat...')
  certificateInfo.value = certificateService.getCertificateInfo()
  console.log('Certificat rafraîchi:', certificateInfo.value)
}

// Fonction pour tronquer les noms de fichiers trop longs
function truncateFileName(fileName, maxLength) {
  if (!fileName) return 'Document'
  if (fileName.length <= maxLength) return fileName
  
  const extension = fileName.split('.').pop()
  const nameWithoutExt = fileName.substring(0, fileName.lastIndexOf('.'))
  const truncatedName = nameWithoutExt.substring(0, maxLength - 3) + '...'
  
  return extension ? `${truncatedName}.${extension}` : truncatedName
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
      return allDocumentsProcessed.value
    case 4:
      return true // Dernière étape
    default:
      return false
  }
})

// Fonction utilitaire pour convertir un File en data URL base64
async function convertFileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// Fonction utilitaire pour convertir un Blob URL en data URL base64
async function convertBlobUrlToDataUrl(blobUrl) {
  return new Promise((resolve, reject) => {
    fetch(blobUrl)
      .then(response => response.blob())
      .then(blob => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
      })
      .catch(reject)
  })
}

// Fonction pour procéder à la signature
async function proceedToSignature() {
  try {
    // Activer l'indicateur de chargement
    isSigning.value = true
    signatureProgress.value = 'Vérification des prérequis...'
    
    console.log('=== DÉBUT DE LA SIGNATURE FINALE ===')
    
    // Vérifier que le certificat est disponible et valide
    if (!certificateInfo.value) {
      throw new Error('Aucun certificat disponible. Veuillez importer un certificat valide.')
    }
    
    if (!certificateService.canUseCertificate()) {
      throw new Error('Le certificat n\'est pas valide ou a expiré. Veuillez importer un nouveau certificat.')
    }
    
    // Vérifier que des documents ont été configurés
    if (Object.keys(documentsConfiguration.value).length === 0) {
      throw new Error('Aucun document configuré pour la signature.')
    }
    
    signatureProgress.value = 'Préparation des documents...'
    console.log('Vérifications préliminaires passées')
    console.log('Documents configurés:', documentsConfiguration.value)
    
    // Récupérer les clés du certificat
    const privateKeyPem = certificateService.getPrivateKeyPem()
    const publicKeyPem = certificateService.getPublicKeyPem()
    
    console.log('Clé privée PEM récupérée:', privateKeyPem ? 'OUI' : 'NON')
    console.log('Clé publique PEM récupérée:', publicKeyPem ? 'OUI' : 'NON')
    
    if (!privateKeyPem || !publicKeyPem) {
      throw new Error('Impossible de récupérer les clés du certificat.')
    }
    
    console.log('Clés du certificat récupérées')
    console.log('Longueur clé privée PEM:', privateKeyPem.length)
    console.log('Longueur clé publique PEM:', publicKeyPem.length)
    
    // Convertir les clés PEM en objets node-forge
    console.log('Conversion de la clé privée...')
    const privateKey = forge.pki.privateKeyFromPem(privateKeyPem)
    console.log('Clé privée convertie:', privateKey ? 'OUI' : 'NON')
    
    console.log('Conversion de la clé publique...')
    const publicKey = forge.pki.publicKeyFromPem(publicKeyPem)
    console.log('Clé publique convertie:', publicKey ? 'OUI' : 'NON')
    
    console.log('Clés converties en objets node-forge')
    
    // Traiter chaque document configuré
    const signatureResults = []
    const totalDocuments = Object.keys(documentsConfiguration.value).length
    
    for (const [index, config] of Object.entries(documentsConfiguration.value)) {
      const documentNumber = parseInt(index) + 1
      signatureProgress.value = `Signature du document ${documentNumber}/${totalDocuments}...`
      
      console.log(`\n--- Traitement du document ${documentNumber} ---`)
      console.log('Configuration:', config)
      
      // Récupérer le fichier PDF original
      const file = config.file
      if (!file) {
        console.warn(`Document ${index} sans fichier, passage au suivant`)
        continue
      }
      
      // Utiliser directement les données du fichier si disponibles
      let documentData
      if (file.dataUrl) {
        // Convertir data URL en ArrayBuffer
        const base64Data = file.dataUrl.split(',')[1]
        const binaryString = atob(base64Data)
        const bytes = new Uint8Array(binaryString.length)
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i)
        }
        documentData = bytes.buffer
      } else if (file.blob) {
        // Convertir Blob en ArrayBuffer
        documentData = await file.blob.arrayBuffer()
      } else if (file.url) {
        // Fallback: convertir l'URL en ArrayBuffer
        const response = await fetch(file.url)
        documentData = await response.arrayBuffer()
      } else {
        console.warn(`Document ${index} sans données, passage au suivant`)
        continue
      }
      
      console.log(`Document ${index} chargé, taille: ${documentData.byteLength} octets`)
      console.log('Type de documentData:', typeof documentData)
      console.log('Instance de ArrayBuffer:', documentData instanceof ArrayBuffer)
      console.log('Instance de Uint8Array:', documentData instanceof Uint8Array)
      
              // Préparer les métadonnées pour la signature
        let processedSignatureImage = null
        
        // Traiter l'image de signature si elle existe
        if (config.signature && (config.signature.imageUrl || signatureData.value)) {
          let signatureImage = null
          
          // Priorité au File original stocké dans signatureData.value
          if (signatureData.value) {
            console.log('Utilisation du File original pour l\'image de signature')
            try {
              signatureImage = await convertFileToDataUrl(signatureData.value)
              console.log('File converti en data URL avec succès:', signatureImage.substring(0, 100) + '...')
            } catch (error) {
              console.error('Erreur lors de la conversion du File:', error)
              processedSignatureImage = null
              return // Arrêter le traitement si la conversion échoue
            }
          }
          // Fallback sur l'URL si pas de File original
          else if (config.signature.imageUrl) {
            signatureImage = config.signature.imageUrl
            
            console.log('DEBUG SIGNATURE IMAGE - État initial:', {
              'image_exists': !!signatureImage,
              'image_type': typeof signatureImage,
              'image_length': signatureImage?.length || 0,
              'image_starts_with_data': signatureImage?.startsWith('data:image'),
              'is_blob_url': signatureImage?.startsWith('blob:'),
              'image_preview': signatureImage?.substring(0, 100) + '...'
            })
            
            // Si c'est un Blob URL, le convertir en data URL base64
            if (signatureImage && signatureImage.startsWith('blob:')) {
              console.log('Conversion du Blob URL en data URL base64...')
              try {
                signatureImage = await convertBlobUrlToDataUrl(signatureImage)
                console.log('Blob URL converti avec succès:', signatureImage.substring(0, 100) + '...')
              } catch (error) {
                console.error('Erreur lors de la conversion du Blob URL:', error)
                processedSignatureImage = null
                return // Arrêter le traitement si la conversion échoue
              }
            }
            // S'assurer que l'image est au bon format (comme dans SignWithTemplateMultiple.vue)
            else if (signatureImage && !signatureImage.startsWith('data:image')) {
              console.warn('Format d\'image incorrect, tentative de correction')
              let imageType = 'png'
              if (signatureImage.startsWith('/9j/')) {
                imageType = 'jpeg'
              }
              signatureImage = `data:image/${imageType};base64,${signatureImage}`
              console.log('Image corrigée:', signatureImage.substring(0, 100) + '...')
            }
          }
          
          processedSignatureImage = signatureImage
        }
        
        const metadata = {
          qr_position: {
            x: config.qrCode?.x || 85,
            y: config.qrCode?.y || 10,
            size: config.qrCode?.size || 'medium',
            pages: config.qrCode?.pages || 'all',
            mode: config.qrCode?.mode || 'all',
            positions: config.qrCode?.positions || {}
          },
          signature_position: config.signature && processedSignatureImage ? {
            signature_image: processedSignatureImage,
            positions: config.signature.positions || {},
            pages: config.signature.pages || 'all',
          signature_size: config.signature.size || 50
        } : null
      }
      
      console.log('Métadonnées préparées:', metadata)
      console.log('QR Code - Taille configurée:', config.qrCode?.size)
      console.log('QR Code - Positions:', config.qrCode?.positions)
      if (config.signature) {
        console.log('Signature - Taille configurée:', config.signature?.size)
        console.log('Signature - Pages configurées:', config.signature?.pages)
        console.log('Signature - Positions:', config.signature?.positions)
      }
      
      // Signer le document
      console.log(`Signature du document ${index}...`)
      const result = await signatureService.signDocumentComplete(
        documentData,
        privateKey,
        publicKey,
        metadata
      )
      
      if (result.success) {
        console.log(`Document ${index} signé avec succès!`)
        console.log(`ID: ${result.documentId}`)
        console.log(`Hash: ${result.originalHash}`)
        console.log(`Temps: ${result.executionTime}s`)
        
        // Ajouter le résultat à la liste
        signatureResults.push({
          documentIndex: parseInt(index),
          fileName: file.name,
          documentId: result.documentId,
          originalHash: result.originalHash,
          signature: result.signature,
          publicKeyPem: result.publicKeyPem,
          signedDocument: result.signedDocument,
          timestamp: result.timestamp
        })
      } else {
        throw new Error(`Échec de la signature du document ${index}`)
      }
    }
    
    // Tous les documents ont été signés avec succès
    console.log('\n=== SIGNATURE TERMINÉE AVEC SUCCÈS ===')
    console.log(`${signatureResults.length} document(s) signé(s)`)
    
    signatureProgress.value = 'Création du fichier ZIP...'
    
    // Créer un fichier ZIP avec tous les documents signés
    const zip = new JSZip()
    
    signatureResults.forEach((result, index) => {
      const fileName = result.fileName.replace('.pdf', '') || `document_${index + 1}`
      const signedFileName = `${fileName}_signé_${result.documentId}.pdf`
      
      zip.file(signedFileName, result.signedDocument)
      
      // Ajouter un fichier de métadonnées
      const metadata = {
        documentId: result.documentId,
        originalHash: result.originalHash,
        signature: result.signature,
        publicKeyPem: result.publicKeyPem,
        timestamp: result.timestamp,
        originalFileName: result.fileName
      }
      
      zip.file(`${fileName}_metadata.json`, JSON.stringify(metadata, null, 2))
    })
    
    // Générer le ZIP
    const zipBlob = await zip.generateAsync({ type: 'blob' })
    
    // Télécharger le ZIP
    const zipUrl = URL.createObjectURL(zipBlob)
    const a = document.createElement('a')
    a.href = zipUrl
    a.download = `documents_signés_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.zip`
    a.click()
    
    // Nettoyer
    URL.revokeObjectURL(zipUrl)
    
    // Afficher un message de succès
    alert(`Signature terminée avec succès !\n${signatureResults.length} document(s) signé(s) et téléchargé(s).`)
    
    // Rediriger vers la page des documents ou autre action
    // emit('go-back')
    
  } catch (error) {
    console.error('Erreur lors de la signature:', error)
    alert(`Erreur lors de la signature: ${error.message}`)
  } finally {
    // Désactiver l'indicateur de chargement
    isSigning.value = false
    signatureProgress.value = ''
  }
}

// Cycle de vie
onMounted(() => {
  console.log('SignImmediatelyPage monté')
  
  // Charger les informations du certificat via le service
  certificateService.initialize()
  certificateInfo.value = certificateService.getCertificateInfo()
  console.log('Certificat chargé via le service:', certificateInfo.value)
  
  // Initialiser le service de signature
  signatureService.initialize()
  
  // Surveiller les changements de certificat (si l'utilisateur en importe un nouveau)
  if (process.client) {
    // Vérifier périodiquement les changements
    const checkCertificateInterval = setInterval(() => {
      const currentCert = certificateService.getCertificateInfo()
      if (currentCert !== certificateInfo.value) {
        console.log('Changement de certificat détecté, mise à jour...')
        certificateInfo.value = currentCert
      }
    }, 2000) // Vérifier toutes les 2 secondes
    
    // Nettoyer l'intervalle lors du démontage
    onUnmounted(() => {
      clearInterval(checkCertificateInterval)
    })
  }
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
  font-family: 'Raleway', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
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

/* Classes de visibilité */
.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

/* Titre de la page */
.page-header {
  text-align: center;
  margin-bottom: 0.5rem;
}

.page-title {
  font-size: 2.8rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  line-height: 1.2;
  font-family: 'Raleway', sans-serif;
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
  text-align: center;
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

/* Mobile Stepper */
.mobile-stepper {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  margin: 0 1rem;
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
  background: rgba(0, 102, 204, 0.1);
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.mobile-step-number {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-blue);
}

.mobile-step-separator {
  font-weight: 500;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.mobile-step-total {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 1rem;
}

.mobile-progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.mobile-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-blue) 0%, #007bff 100%);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.mobile-step-info {
  text-align: center;
}

.mobile-step-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-blue);
  margin: 0 0 0.5rem 0;
}

.mobile-step-description {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
  line-height: 1.4;
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

/* Indicateur de progrès - Jauge circulaire */
.progress-indicator {
  margin-top: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.circular-progress-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  justify-content: center;
}

.circular-progress {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-ring {
  transform: rotate(-90deg);
  filter: drop-shadow(0 4px 8px rgba(0, 102, 204, 0.3));
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
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary-blue);
  line-height: 1;
  text-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
}

.progress-total {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-muted);
  opacity: 0.8;
}

.progress-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.progress-text {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 1rem;
  text-align: left;
}

.progress-status {
  font-size: 0.9rem;
  color: var(--text-muted);
  opacity: 0.8;
  text-align: left;
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





/* Section de résumé de signature */
.signature-summary-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.signature-summary-section h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.summary-status-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  flex-direction: column;
  align-items: stretch;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.summary-status-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 15px 40px rgba(0, 0, 0, 0.15),
    inset 1px 0 0 rgba(255, 255, 255, 0.2);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 1rem;
}

.summary-status-icon {
  width: 48px;
  height: 48px;
  background: rgba(0, 102, 204, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 102, 204, 0.3);
  color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.summary-title {
  flex: 1;
}

.summary-title h6 {
  color: var(--text-dark);
  font-weight: 600;
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.summary-subtitle {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 400;
  font-family: 'Raleway', sans-serif;
}

.summary-status-badge {
  flex-shrink: 0;
}

.summary-content {
  width: 100%;
}

.summary-section {
  margin-bottom: 1.5rem;
}

.summary-section:last-child {
  margin-bottom: 0;
}

.section-title {
  color: var(--text-dark);
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Raleway', sans-serif;
}

.section-title i {
  color: var(--primary-blue);
  margin-right: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-label {
  font-size: 0.8rem;
  color: var(--primary-blue);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Raleway', sans-serif;
}

.info-value {
  font-size: 0.9rem;
  color: var(--text-dark);
  font-weight: 500;
  word-break: break-word;
  font-family: 'Raleway', sans-serif;
}

.serial-number {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  background: rgba(0, 0, 0, 0.05);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.positioning-info {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
  flex-wrap: wrap;
}

.positioning-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  font-size: 0.9rem;
  color: var(--text-dark);
  transition: all 0.3s ease;
  font-family: 'Raleway', sans-serif;
}

.positioning-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
}

.positioning-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-left: 0.5rem;
}

.positioning-title {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.9rem;
}

.positioning-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
  opacity: 0.8;
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
  
  .page-header {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .page-title {
    font-size: 2.5rem;
    text-align: center;
  }
  
  .page-subtitle {
    font-size: 1rem;
    text-align: center;
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
  
  .desktop-only {
    display: none;
  }
  
  .mobile-only {
    display: block;
  }
  
  .mobile-stepper {
    margin: 0 0.5rem;
  }
  
  .mobile-stepper-header {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .mobile-step-indicator {
    align-self: center;
  }
  
  .mobile-progress-bar {
    width: 100%;
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
  
  /* Responsive pour la jauge circulaire */
  .circular-progress-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .progress-ring {
    width: 100px;
    height: 100px;
  }
  
  .progress-ring circle {
    r: 42;
    cx: 50;
    cy: 50;
    stroke-width: 6;
  }
  
  .progress-number {
    font-size: 1.5rem;
  }
  
  .progress-total {
    font-size: 0.9rem;
  }
  
  .progress-info {
    min-width: auto;
    text-align: center;
  }
  
  .progress-text,
  .progress-status {
    text-align: center;
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

/* Styles pour les nouveaux éléments de l'étape 4 */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 100%;
}

.positioning-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 100%;
}

.document-item {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.document-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.document-name {
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.document-pages {
  background: var(--primary-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.document-details {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.detail-item {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.detail-item strong {
  color: var(--text-primary);
}

.positioning-summary {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.document-positioning {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.document-title {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.positioning-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.positioning-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  flex-shrink: 0;
}

.positioning-details {
  flex: 1;
}

.positioning-title {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.positioning-info-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem 1rem;
  align-items: center;
}

.info-label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.info-value {
  color: var(--text-primary);
  font-size: 0.9rem;
}

.signature-preview {
  margin-top: 0.75rem;
}

.signature-thumbnail {
  width: 80px;
  height: 40px;
  object-fit: contain;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background: white;
}

.no-certificate-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 8px;
  color: var(--warning-color);
  font-size: 0.9rem;
}

/* Animation de rotation pour l'icône de chargement */
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--warning-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: auto;
}

.refresh-btn:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .documents-grid,
  .positioning-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .documents-header {
    padding: 0.5rem 0;
  }
  
  .header-top-row {
    gap: 12px;
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
