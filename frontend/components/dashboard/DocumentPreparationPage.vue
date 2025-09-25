<template>
  <div class="document-preparation-container">
    <!-- Bouton retour rond style fermer -->
    <div class="close-button-container">
      <button @click="goBack" class="close-btn-round">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <!-- Notifications -->
    <div class="notifications-container">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification', `notification-${notification.type}`]"
      >
        <div class="notification-icon">
          <i :class="notification.type === 'warning' ? 'bi bi-exclamation-triangle' : 'bi bi-info-circle'"></i>
        </div>
        <div class="notification-content">
          <p class="notification-message">{{ notification.message }}</p>
        </div>
        <button @click="removeNotification(notification.id)" class="notification-close">
          <i class="bi bi-x"></i>
        </button>
      </div>
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
            @click="openFileExplorer"
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
            <div class="upload-label">
              <div class="upload-icon">
                <i class="bi bi-file-earmark-pdf-fill"></i>
              </div>
              <div class="upload-text">
                <h3>Glissez-déposez vos PDF ici</h3>
                <p>ou <span class="link">cliquez pour sélectionner</span></p>
                <small>Formats acceptés: PDF uniquement • Taille max: 50MB par fichier</small>
              </div>
            </div>
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
              ref="signBaseRef"
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
            <i class="bi bi-person-check-fill"></i>
            Validation du destinataire
          </h2>
          <p>Vérification de la présence d'un chef pour signer le document</p>
        </div>

        <div class="workflow-validation-section">
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

          <!-- Validation du chef -->
          <div class="chief-validation-card">
            <div class="validation-header">
              <h5>
                <i class="bi bi-person-check"></i>
                Validation du destinataire
              </h5>
              <p>Vérification de la présence d'un chef pour signer le document</p>
            </div>
            
            <!-- Loading state -->
            <div v-if="workflowValidation.isLoading" class="validation-loading">
              <div class="loading-spinner"></div>
              <p>Vérification de la présence d'un chef...</p>
            </div>
            
            <!-- Chef trouvé -->
            <div v-else-if="workflowValidation.hasChief && workflowValidation.chiefInfo" class="chief-info">
              <div class="chief-card">
                <div class="chief-avatar">
                  <i class="bi bi-person-fill"></i>
                </div>
                <div class="chief-details">
                  <h6 class="chief-name">{{ workflowValidation.chiefInfo.name }}</h6>
                  <p class="chief-email">{{ workflowValidation.chiefInfo.email }}</p>
                  <span class="chief-role">
                    <i class="bi bi-award-fill"></i>
                    {{ workflowValidation.chiefInfo.role }}
                  </span>
                </div>
                <div class="chief-status">
                  <i class="bi bi-check-circle-fill text-success"></i>
                  <span>Disponible pour signature</span>
                </div>
              </div>
              
              <div class="workflow-info">
                <div class="workflow-step">
                  <div class="step-icon">
                    <i class="bi bi-person-fill"></i>
                  </div>
                  <div class="step-content">
                    <h6>Secrétaire (Vous)</h6>
                    <p>Préparation du document et positionnement des éléments</p>
                    <span class="step-status completed">Terminé</span>
                  </div>
                </div>
                <div class="workflow-arrow">
                  <i class="bi bi-arrow-down"></i>
                </div>
                <div class="workflow-step">
                  <div class="step-icon">
                    <i class="bi bi-person-fill"></i>
                  </div>
                  <div class="step-content">
                    <h6>{{ workflowValidation.chiefInfo.name }}</h6>
                    <p>Signature et validation du document</p>
                    <span class="step-status pending">En attente</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Aucun chef trouvé -->
            <div v-else-if="!workflowValidation.hasChief" class="no-chief-error">
              <div class="error-icon">
                <i class="bi bi-exclamation-triangle-fill"></i>
              </div>
              <div class="error-content">
                <h6>Impossible de préparer le document</h6>
                <p>{{ workflowValidation.error || 'Aucun chef trouvé dans cette organisation' }}</p>
                <p class="error-solution">
                  <i class="bi bi-info-circle"></i>
                  Le document ne peut pas être préparé car il n'y a personne pour le signer.
                  Contactez l'administrateur de l'organisation pour ajouter un chef.
                </p>
              </div>
            </div>
            
            <!-- Erreur de validation -->
            <div v-else-if="workflowValidation.error" class="validation-error">
              <div class="error-icon">
                <i class="bi bi-x-circle-fill"></i>
              </div>
              <div class="error-content">
                <h6>Erreur de validation</h6>
                <p>{{ workflowValidation.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Barre de progression globale -->
        <div v-if="isSubmitting" class="submission-progress-section">
          <div class="progress-header">
            <h4>Préparation en cours...</h4>
            <span class="progress-counter">{{ completedDocuments }}/{{ totalDocuments }} documents</span>
          </div>
          
          <div class="global-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${totalDocuments > 0 ? (completedDocuments / totalDocuments) * 100 : 0}%` }"
              ></div>
            </div>
            <span class="progress-text">{{ submissionProgress }}</span>
          </div>
          
          <!-- Progression détaillée par document -->
          <div class="documents-progress">
            <div 
              v-for="(file, index) in uploadedFiles" 
              :key="index"
              class="document-progress-item"
            >
              <div class="document-info">
                <i class="bi bi-file-earmark-pdf-fill"></i>
                <span class="document-name">{{ file.name }}</span>
              </div>
              
              <div class="document-progress">
                <div class="mini-progress-bar">
                  <div 
                    class="mini-progress-fill" 
                    :class="{
                      'progress-success': documentProgress[index] === 100,
                      'progress-error': documentProgress[index] === 0 && completedDocuments > 0,
                      'progress-active': documentProgress[index] > 0 && documentProgress[index] < 100
                    }"
                    :style="{ width: `${documentProgress[index] || 0}%` }"
                  ></div>
                </div>
                <span class="mini-progress-text">{{ documentProgress[index] || 0 }}%</span>
              </div>
              
              <div class="document-status">
                <i v-if="documentProgress[index] === 100" class="bi bi-check-circle-fill status-success"></i>
                <i v-else-if="documentProgress[index] === 0 && completedDocuments > 0" class="bi bi-x-circle-fill status-error"></i>
                <i v-else-if="documentProgress[index] > 0" class="bi bi-arrow-clockwise spin status-active"></i>
                <i v-else class="bi bi-clock status-pending"></i>
              </div>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button @click="previousStep" class="action-btn secondary" :disabled="isSubmitting">
            <i class="bi bi-arrow-left"></i>
            <span>Retour</span>
          </button>
          <button 
            @click="submitForSignature" 
            class="action-btn primary" 
            :disabled="isSubmitting || !workflowValidation.hasChief"
          >
            <span v-if="!isSubmitting">Soumettre pour signature</span>
            <span v-else>Préparation en cours...</span>
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
          <!-- Carte de succès principale -->
          <div class="document-success-card">
            <div class="document-success-header">
              <div class="document-info">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-check-fill"></i>
                </div>
                <div class="document-details">
                  <h3 class="document-name">{{ uploadedFiles[0]?.name || 'Document' }}</h3>
                  <span class="document-size">{{ formatFileSize(uploadedFiles[0]?.size || 0) }}</span>
                </div>
              </div>
              <div class="document-status">
                <span class="status-badge success">
                  <i class="bi bi-check-circle-fill"></i>
                  Préparé
                </span>
              </div>
            </div>
            <div class="document-success-content">
              <div class="success-message">
                <i class="bi bi-check-circle-fill"></i>
                <span>Votre document a été préparé et transmis au chef pour signature</span>
              </div>
            </div>
          </div>

          <!-- Statut du workflow - Cartes sur la même ligne -->
          <div class="workflow-status-section">
            <div class="section-header">
              <h4 class="section-title">Statut du workflow</h4>
            </div>
            
            <div class="workflow-cards-grid">
              <!-- Carte étape terminée -->
              <div class="workflow-status-card completed">
                <div class="workflow-card-header">
                  <div class="workflow-info">
                    <div class="workflow-icon">
                      <i class="bi bi-check-circle-fill"></i>
                    </div>
                    <div class="workflow-details">
                      <h5 class="workflow-title">Préparation terminée</h5>
                      <p class="workflow-description">Document préparé par le secrétaire</p>
                    </div>
                  </div>
                  <div class="workflow-status">
                    <span class="status-badge completed">
                      <i class="bi bi-check-circle-fill"></i>
                      Terminé
                    </span>
                  </div>
                </div>
                <div class="workflow-meta">
                  <div class="meta-item">
                    <i class="bi bi-calendar3"></i>
                    <span>{{ new Date().toLocaleDateString() }}</span>
                  </div>
                  <div class="meta-item">
                    <i class="bi bi-clock"></i>
                    <span>{{ new Date().toLocaleTimeString() }}</span>
                  </div>
                </div>
              </div>

              <!-- Carte étape en attente -->
              <div class="workflow-status-card pending">
                <div class="workflow-card-header">
                  <div class="workflow-info">
                    <div class="workflow-icon">
                      <i class="bi bi-hourglass-split"></i>
                    </div>
                    <div class="workflow-details">
                      <h5 class="workflow-title">En attente de signature</h5>
                      <p class="workflow-description">En attente de signature par le chef</p>
                    </div>
                  </div>
                  <div class="workflow-status">
                    <span class="status-badge pending">
                      <i class="bi bi-hourglass-split"></i>
                      En attente
                    </span>
                  </div>
                </div>
                <div class="workflow-meta">
                  <div class="meta-item">
                    <i class="bi bi-person"></i>
                    <span>{{ workflowValidation.chiefInfo?.name || 'Chef' }}</span>
                  </div>
                  <div class="meta-item">
                    <i class="bi bi-envelope"></i>
                    <span>{{ workflowValidation.chiefInfo?.email || 'N/A' }}</span>
                  </div>
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
import { useAuthHeaders } from '../../composables/useAuthHeaders'
import SignBase from './SignBase.vue'

// Store d'authentification
const authStore = useAuthStore()

// Composable pour les headers d'authentification
const { getAuthHeaders, authenticatedFetch } = useAuthHeaders()

// Référence vers le composant SignBase
const signBaseRef = ref(null)

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
const documentProgress = ref({}) // Progression par document
const totalDocuments = ref(0)
const completedDocuments = ref(0)

// État pour les notifications
const notifications = ref([])

// État pour la validation du workflow
const workflowValidation = ref({
  isLoading: false,
  hasChief: false,
  chiefInfo: null,
  error: null
})

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
    
    // Si on arrive à l'étape de configuration du workflow, valider la présence d'un chef
    if (currentStep.value === 4) {
      validateWorkflow()
    }
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

const openFileExplorer = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// Fonction pour afficher une notification
const showNotification = (message, type = 'warning') => {
  const notification = {
    id: Date.now(),
    message,
    type,
    timestamp: new Date()
  }
  
  notifications.value.push(notification)
  
  // Supprimer la notification après 5 secondes (ou plus pour les erreurs)
  const timeout = type === 'error' ? 8000 : 5000
  setTimeout(() => {
    const index = notifications.value.findIndex(n => n.id === notification.id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }, timeout)
}

// Fonction pour supprimer une notification
const removeNotification = (notificationId) => {
  const index = notifications.value.findIndex(n => n.id === notificationId)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const handleFiles = async (files) => {
  for (const file of files) {
    if (file.type === 'application/pdf') {
      // Vérifier si le fichier existe déjà
      const isDuplicate = uploadedFiles.value.some(existingFile => 
        existingFile.name === file.name && existingFile.size === file.size
      )
      
      if (isDuplicate) {
        showNotification(`Le fichier "${file.name}" est déjà importé`, 'warning')
        continue
      }
      
      const fileObj = {
        file: file,
        name: file.name,
        size: file.size,
        url: URL.createObjectURL(file),
        pages: null // Sera détecté automatiquement par SignBase
      }
      
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
  
  // Sauvegarder les positions pour le document actuel
  const docKey = activeSignBaseTabIndex.value.toString()
  if (!documentsConfiguration.value[docKey]) {
    documentsConfiguration.value[docKey] = {}
  }
  
  // Sauvegarder les positions de signature (gérer différentes structures)
  if (data.signature) {
    let signatureX, signatureY, signaturePage, signatureWidth, signatureHeight
    
    // Structure directe
    if (data.signature.x !== undefined && data.signature.y !== undefined) {
      signatureX = data.signature.x
      signatureY = data.signature.y
      signaturePage = data.signature.page || 1
      signatureWidth = data.signature.width || 150
      signatureHeight = data.signature.height || 50
    }
    // Structure imbriquée (comme SignImmediatelyPage)
    else if (data.signature.positions?.default) {
      signatureX = data.signature.positions.default.x
      signatureY = data.signature.positions.default.y
      signaturePage = data.signature.positions.default.page || 1
      signatureWidth = data.signature.positions.default.width || 150
      signatureHeight = data.signature.positions.default.height || 50
    }
    
    if (signatureX !== undefined && signatureY !== undefined) {
      documentsConfiguration.value[docKey].signaturePosition = {
        x: signatureX,
        y: signatureY,
        page: signaturePage,
        width: signatureWidth,
        height: signatureHeight
      }
    }
  }
  
  // Sauvegarder les positions QR (gérer différentes structures)
  if (data.qr) {
    let qrX, qrY, qrPage, qrSize
    
    // Structure directe
    if (data.qr.x !== undefined && data.qr.y !== undefined) {
      qrX = data.qr.x
      qrY = data.qr.y
      qrPage = data.qr.page || 1
      qrSize = data.qr.size || 100
    }
    // Structure imbriquée (comme SignImmediatelyPage)
    else if (data.qr.positions?.default) {
      qrX = data.qr.positions.default.x
      qrY = data.qr.positions.default.y
      qrPage = data.qr.positions.default.page || 1
      qrSize = data.qr.positions.default.size || 100
    }
    
    if (qrX !== undefined && qrY !== undefined) {
      documentsConfiguration.value[docKey].qrPosition = {
        x: qrX,
        y: qrY,
        page: qrPage,
        size: qrSize
      }
    }
  }
  
  // Sauvegarder le mode de positionnement
  documentsConfiguration.value[docKey].positionMode = data.mode
  
  console.log(`✅ Positions sauvegardées pour le document ${docKey}:`, documentsConfiguration.value[docKey])
}

const handlePositionChanged = (data) => {
  console.log('Position changée:', data)
  
  // Mettre à jour les données de position en temps réel
  positionData.value = data
  
  // Sauvegarder aussi dans documentsConfiguration pour persistence
  const docKey = activeSignBaseTabIndex.value.toString()
  if (!documentsConfiguration.value[docKey]) {
    documentsConfiguration.value[docKey] = {}
  }
  
  // Sauvegarder les positions de signature (gérer différentes structures)
  if (data.signature) {
    let signatureX, signatureY, signaturePage, signatureWidth, signatureHeight
    
    // Structure directe
    if (data.signature.x !== undefined && data.signature.y !== undefined) {
      signatureX = data.signature.x
      signatureY = data.signature.y
      signaturePage = data.signature.page || 1
      signatureWidth = data.signature.width || 150
      signatureHeight = data.signature.height || 50
    }
    // Structure imbriquée (comme SignImmediatelyPage)
    else if (data.signature.positions?.default) {
      signatureX = data.signature.positions.default.x
      signatureY = data.signature.positions.default.y
      signaturePage = data.signature.positions.default.page || 1
      signatureWidth = data.signature.positions.default.width || 150
      signatureHeight = data.signature.positions.default.height || 50
    }
    
    if (signatureX !== undefined && signatureY !== undefined) {
      documentsConfiguration.value[docKey].signaturePosition = {
        x: signatureX,
        y: signatureY,
        page: signaturePage,
        width: signatureWidth,
        height: signatureHeight
      }
    }
  }
  
  // Sauvegarder les positions QR (gérer différentes structures)
  if (data.qr) {
    let qrX, qrY, qrPage, qrSize
    
    // Structure directe
    if (data.qr.x !== undefined && data.qr.y !== undefined) {
      qrX = data.qr.x
      qrY = data.qr.y
      qrPage = data.qr.page || 1
      qrSize = data.qr.size || 100
    }
    // Structure imbriquée (comme SignImmediatelyPage)
    else if (data.qr.positions?.default) {
      qrX = data.qr.positions.default.x
      qrY = data.qr.positions.default.y
      qrPage = data.qr.positions.default.page || 1
      qrSize = data.qr.positions.default.size || 100
    }
    
    if (qrX !== undefined && qrY !== undefined) {
      documentsConfiguration.value[docKey].qrPosition = {
        x: qrX,
        y: qrY,
        page: qrPage,
        size: qrSize
      }
    }
  }
  
  // Sauvegarder le mode de positionnement
  documentsConfiguration.value[docKey].positionMode = data.mode
}

const handleSignatureUploaded = (data) => {
  console.log('Signature uploadée:', data)
  signatureData.value = data
  
  // Sauvegarder l'image de signature pour le document actuel
  const docKey = activeSignBaseTabIndex.value.toString()
  if (!documentsConfiguration.value[docKey]) {
    documentsConfiguration.value[docKey] = {}
  }
  documentsConfiguration.value[docKey].signatureImage = data.dataUrl
  
  console.log(`✅ Image de signature sauvegardée pour le document ${docKey}`)
}

const handlePdfGenerated = (data) => {
  console.log('PDF généré:', data)
  
  // Marquer le document comme traité
  processedDocuments.value.add(activeSignBaseTabIndex.value)
  
  // Sauvegarder la configuration complète
  const docKey = activeSignBaseTabIndex.value.toString()
  if (!documentsConfiguration.value[docKey]) {
    documentsConfiguration.value[docKey] = {}
  }
  
  // Merger les nouvelles données avec les positions déjà sauvegardées
  documentsConfiguration.value[docKey] = {
    ...documentsConfiguration.value[docKey], // Garder les positions et images déjà sauvegardées
    file: uploadedFiles.value[activeSignBaseTabIndex.value],
    positionMode: data.positionMode || documentsConfiguration.value[docKey].positionMode,
    qrCode: data.qrCode,
    signature: data.signature,
    generatedPdf: {
      file: data.file,
      dataUrl: data.dataUrl,
      blob: data.blob
    }
  }
  
  console.log(`✅ Configuration complète sauvegardée pour le document ${docKey}:`, documentsConfiguration.value[docKey])
  
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

// Validation du workflow
const validateWorkflow = async () => {
  workflowValidation.value.isLoading = true
  workflowValidation.value.error = null
  
  try {
    // Récupérer l'organisation actuelle depuis le localStorage
    const selectedOrganizationData = localStorage.getItem('selectedOrganization')
    let currentOrganization = null
    
    if (selectedOrganizationData) {
      try {
        currentOrganization = JSON.parse(selectedOrganizationData)
      } catch (error) {
        console.error('Erreur lors du parsing de l\'organisation:', error)
      }
    }
    
    console.log('Organisation actuelle:', currentOrganization)
    
    if (!currentOrganization || !currentOrganization.id) {
      throw new Error('Aucune organisation sélectionnée')
    }
    
    console.log('URL de la requête:', `http://127.0.0.1:8000/api/organizations/${currentOrganization.id}/members/`)
    
    // Faire une requête pour récupérer les membres de l'organisation
    const response = await authenticatedFetch(`http://127.0.0.1:8000/api/organizations/${currentOrganization.id}/members/`, {
      method: 'GET'
    })
    
    console.log('Réponse de l\'API:', response.status, response.statusText)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Erreur API:', errorText)
      throw new Error(`Erreur lors de la récupération des membres: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('Données reçues:', data)
    console.log('Membres disponibles:', data.members)
    
    // Afficher les rôles disponibles
    if (data.members && data.members.length > 0) {
      console.log('Rôles disponibles:', data.members.map(member => ({ 
        name: member.user_name || member.name, 
        role: member.role,
        user_role: member.user_role 
      })))
    }
    
    // Chercher un membre avec le rôle "chef" (essayer différentes variantes)
    const chief = data.members?.find(member => 
      member.role === 'chef' || 
      member.user_role === 'chef' ||
      member.role === 'Chef' ||
      member.user_role === 'Chef'
    )
    console.log('Chef trouvé:', chief)
    
    if (chief) {
      workflowValidation.value.hasChief = true
      workflowValidation.value.chiefInfo = {
        name: chief.user_name || chief.name || 'Nom non disponible',
        email: chief.user_email || chief.email || 'Email non disponible',
        role: chief.role,
        joinedDate: chief.joined_date || chief.date_joined
      }
    } else {
      workflowValidation.value.hasChief = false
      workflowValidation.value.error = 'Aucun chef trouvé dans cette organisation'
    }
    
  } catch (error) {
    console.error('Erreur lors de la validation du workflow:', error)
    workflowValidation.value.error = error.message || 'Erreur lors de la validation du workflow'
    workflowValidation.value.hasChief = false
  } finally {
    workflowValidation.value.isLoading = false
  }
}

// Soumission de tous les documents
const submitForSignature = async () => {
  isSubmitting.value = true
  submissionProgress.value = 'Initialisation de la préparation...'
  
  try {
    // Récupérer l'organisation actuelle
    const selectedOrganizationData = localStorage.getItem('selectedOrganization')
    let currentOrganization = null
    
    if (selectedOrganizationData) {
      try {
        currentOrganization = JSON.parse(selectedOrganizationData)
      } catch (error) {
        console.error('Erreur lors du parsing de l\'organisation:', error)
        throw new Error('Organisation invalide')
      }
    }
    
    if (!currentOrganization) {
      throw new Error('Aucune organisation sélectionnée')
    }
    
    if (uploadedFiles.value.length === 0) {
      throw new Error('Aucun fichier sélectionné')
    }
    
    // Initialiser les compteurs de progression
    totalDocuments.value = uploadedFiles.value.length
    completedDocuments.value = 0
    documentProgress.value = {}
    submissionResults.value = []
    
    console.log(`🚀 Début de la préparation de ${totalDocuments.value} document(s)`)
    
    // Traiter tous les documents en parallèle
    const documentPromises = uploadedFiles.value.map(async (fileData, index) => {
      return await processDocument(fileData, index, currentOrganization)
    })
    
    // Attendre que tous les documents soient traités
    submissionProgress.value = 'Traitement de tous les documents en cours...'
    const results = await Promise.allSettled(documentPromises)
    
    // Analyser les résultats
    const successfulResults = []
    const failedResults = []
    
    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        successfulResults.push(result.value)
        documentProgress.value[index] = 100
      } else {
        failedResults.push({
          index,
          fileName: uploadedFiles.value[index]?.name || `Document ${index + 1}`,
          error: result.reason?.message || 'Erreur inconnue'
        })
        documentProgress.value[index] = 0
      }
    })
    
    // Mettre à jour les résultats
    submissionResults.value = successfulResults
    completedDocuments.value = successfulResults.length
    
    console.log(`✅ Préparation terminée: ${successfulResults.length}/${totalDocuments.value} documents préparés`)
    
    if (successfulResults.length > 0) {
      // Stocker les informations de la dernière préparation
      localStorage.setItem('lastDocumentPreparation', JSON.stringify(successfulResults[0].document_preparation))
      
      if (failedResults.length > 0) {
        // Succès partiel
        submissionProgress.value = `${successfulResults.length}/${totalDocuments.value} documents préparés avec succès`
        showNotification(
          `${failedResults.length} document(s) n'ont pas pu être préparés: ${failedResults.map(f => f.fileName).join(', ')}`,
          'warning'
        )
      } else {
        // Succès total
        submissionProgress.value = 'Tous les documents ont été préparés avec succès'
      }
      
      // Passer à l'étape suivante
      nextStep()
    } else {
      // Échec total
      throw new Error('Aucun document n\'a pu être préparé')
    }
    
  } catch (error) {
    console.error('Erreur lors de la soumission:', error)
    showNotification(error.message || 'Erreur lors de la préparation des documents', 'error')
  } finally {
    isSubmitting.value = false
  }
}

// Traiter un document individuel
const processDocument = async (fileData, index, currentOrganization) => {
  console.log(`📄 Traitement du document ${index + 1}: ${fileData.name}`)
  
  // Mettre à jour la progression de ce document
  documentProgress.value[index] = 0
  
  try {
    // Extraire les positions pour ce document spécifique
    documentProgress.value[index] = 10
    const { signaturePositions, qrCodePositions, signatureImage, generatedPdf } = await extractDocumentPositions(index)
    
    console.log(`Positions extraites pour ${fileData.name}:`, {
      signaturePositions,
      qrCodePositions,
      hasSignatureImage: !!signatureImage,
      hasGeneratedPdf: !!generatedPdf
    })
    
    // Convertir le fichier en base64
    documentProgress.value[index] = 30
    const originalBase64 = await fileToBase64(fileData.file)
    
    // Générer le PDF avec les éléments positionnés si nécessaire
    documentProgress.value[index] = 50
    let currentDocumentBase64 = originalBase64
    let finalPdfBase64 = null
    
    // Vérifier s'il y a des éléments à positionner
    const hasElements = Object.keys(signaturePositions).length > 0 || Object.keys(qrCodePositions).length > 0
    
    if (hasElements) {
      try {
        // Utiliser le PDF généré extrait directement
        if (generatedPdf && generatedPdf.blob) {
          console.log(`🔍 PDF généré trouvé pour ${fileData.name}`)
          finalPdfBase64 = await blobToBase64(generatedPdf.blob)
          currentDocumentBase64 = finalPdfBase64
          console.log(`✅ PDF récupéré depuis extractDocumentPositions pour ${fileData.name}`)
        } else if (generatedPdf && generatedPdf.dataUrl && generatedPdf.dataUrl.startsWith('data:application/pdf;base64,')) {
          finalPdfBase64 = generatedPdf.dataUrl.split(',')[1]
          currentDocumentBase64 = finalPdfBase64
          console.log(`✅ PDF Base64 récupéré depuis extractDocumentPositions pour ${fileData.name}`)
        } else if (index === activeSignBaseTabIndex.value && signBaseRef.value) {
          // Fallback: Si pas de PDF extrait ET c'est le document actif, essayer de générer
          console.log(`🔄 Fallback: Tentative de génération PDF pour le document actif ${fileData.name}`)
          const generatedPdfBlob = await generateDocumentPdf()
          if (generatedPdfBlob) {
            finalPdfBase64 = await blobToBase64(generatedPdfBlob)
            currentDocumentBase64 = finalPdfBase64
            console.log(`✅ PDF généré avec SignBase pour ${fileData.name}`)
          } else {
            console.log(`❌ Aucun PDF généré par SignBase pour ${fileData.name}`)
          }
        }
      } catch (error) {
        console.warn(`⚠️ Erreur récupération PDF pour ${fileData.name}:`, error)
        // Continuer avec le PDF original
      }
    }
    
    console.log(`📄 Document ${fileData.name} - Éléments: ${hasElements ? 'OUI' : 'NON'}, PDF généré: ${!!finalPdfBase64}`)
    
    // Préparer les données pour l'API
    documentProgress.value[index] = 70
    // Créer la configuration simplifiée des éléments
    const elementsConfig = {}
    
    // Récupérer le mode de page depuis les données de position
    let pageMode = 'all' // valeur par défaut
    
    // Option 1: Si c'est le document actif, utiliser positionData global
    if (index === activeSignBaseTabIndex.value && positionData.value?.mode) {
      pageMode = positionData.value.mode
      console.log(`📋 Mode de page détecté depuis positionData global: ${pageMode}`)
    } 
    // Option 2: Récupérer depuis documentsConfiguration
    else {
      const docKey = index.toString()
      if (documentsConfiguration.value[docKey]?.positionData?.mode) {
        pageMode = documentsConfiguration.value[docKey].positionData.mode
        console.log(`📋 Mode de page détecté depuis documentsConfiguration: ${pageMode}`)
      } else {
        console.log(`⚠️ Mode de page non trouvé, utilisation du défaut: ${pageMode}`)
      }
    }
    
    // Ajouter le mode de page à la configuration
    elementsConfig.page_mode = pageMode
    
    // Extraire les pages appliquées selon le mode
    let appliedPages = []
    if (pageMode === 'current' && positionData.value?.qr?.pages) {
      appliedPages = Array.isArray(positionData.value.qr.pages) ? positionData.value.qr.pages : [positionData.value.qr.pages]
    } else if (pageMode === 'custom' && positionData.value?.qr?.pages) {
      appliedPages = Array.isArray(positionData.value.qr.pages) ? positionData.value.qr.pages : []
    } else if (pageMode === 'individual') {
      // En mode individual, les pages sont les clés des positions
      const qrPages = positionData.value?.qr?.pages || []
      const sigPages = positionData.value?.signature?.pages || []
      appliedPages = [...new Set([...qrPages, ...sigPages])] // Unique pages
    } else if (pageMode === 'all') {
      appliedPages = [] // Toutes les pages, pas besoin de liste
    }
    
    elementsConfig.applied_pages = appliedPages
    console.log(`📋 Pages appliquées pour le mode ${pageMode}:`, appliedPages)
    
    // Ajouter la configuration de signature si elle existe
    if (Object.keys(signaturePositions).length > 0) {
      const firstSignaturePos = Object.values(signaturePositions)[0]
      elementsConfig.signature = {
        x: firstSignaturePos.x,
        y: firstSignaturePos.y,
        width: firstSignaturePos.width,
        height: firstSignaturePos.height,
        page: firstSignaturePos.page
      }
    }
    
    // Ajouter la configuration QR si elle existe
    if (Object.keys(qrCodePositions).length > 0) {
      const firstQrPos = Object.values(qrCodePositions)[0]
      
      // Convertir la taille numérique en choix textuel
      let qrSize = 'medium' // par défaut
      console.log(`🔄 Conversion taille QR: ${firstQrPos.size} (type: ${typeof firstQrPos.size})`)
      
      if (firstQrPos.size) {
        if (typeof firstQrPos.size === 'number') {
          // Convertir la taille numérique en choix
          if (firstQrPos.size <= 50) {
            qrSize = 'small'
          } else if (firstQrPos.size <= 100) {
            qrSize = 'medium'
          } else {
            qrSize = 'large'
          }
          console.log(`✅ Taille numérique ${firstQrPos.size} convertie en: ${qrSize}`)
        } else if (typeof firstQrPos.size === 'string') {
          // Vérifier que c'est un choix valide
          if (['small', 'medium', 'large'].includes(firstQrPos.size)) {
            qrSize = firstQrPos.size
            console.log(`✅ Taille string valide: ${qrSize}`)
          } else {
            console.log(`⚠️ Taille string invalide: ${firstQrPos.size}, utilisation du défaut: ${qrSize}`)
          }
        }
      } else {
        console.log(`⚠️ Aucune taille QR fournie, utilisation du défaut: ${qrSize}`)
      }
      
      elementsConfig.qr_code = {
        x: firstQrPos.x,
        y: firstQrPos.y,
        size: qrSize,
        page: firstQrPos.page
      }
    }
    
    const submissionData = {
      organization: currentOrganization,
      document_title: fileData.name,
      document_description: 'Document préparé pour signature hiérarchique',
      original_filename: fileData.name,
      elements_configuration: elementsConfig,
      signature_image: signatureImage || '',
      file_size_original: fileData.size,
      preparation_notes: `Document préparé via l'interface secrétaire (${index + 1}/${totalDocuments.value})`,
      original_document_data: originalBase64,
      current_document_data: currentDocumentBase64 || originalBase64,
      final_document_data: finalPdfBase64 || '',
      has_positioned_elements: hasElements
    }
    
    console.log(`📋 Données de soumission pour ${fileData.name}:`, {
      document_title: submissionData.document_title,
      has_signature_positions: Object.keys(signaturePositions).length > 0,
      has_qr_positions: Object.keys(qrCodePositions).length > 0,
      has_signature_image: !!signatureImage,
      has_final_pdf: !!finalPdfBase64,
      has_positioned_elements: hasElements
    })
    
    console.log(`📋 Configuration des éléments finale:`, elementsConfig)
    
    // Envoyer vers l'API
    documentProgress.value[index] = 90
    const response = await authenticatedFetch('http://127.0.0.1:8000/api/signatures/document-preparation/create/', {
      method: 'POST',
      body: JSON.stringify(submissionData)
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Erreur API (${response.status}): ${errorText}`)
    }
    
    const result = await response.json()
    
    if (!result.success) {
      throw new Error(result.error || 'Erreur lors de la préparation')
    }
    
    // Succès
    documentProgress.value[index] = 100
    completedDocuments.value++
    
    console.log(`✅ Document ${fileData.name} préparé avec succès`)
    
    return {
      fileName: fileData.name,
      index,
      success: true,
      document_preparation: result.document_preparation
    }
    
  } catch (error) {
    console.error(`❌ Erreur pour ${fileData.name}:`, error)
    documentProgress.value[index] = 0
    throw error
  }
}

// Extraire les positions pour un document spécifique
const extractDocumentPositions = async (documentIndex) => {
  const signaturePositions = {}
  const qrCodePositions = {}
  let signatureImage = null
  let generatedPdf = null
  const docKey = documentIndex.toString()
  
  console.log(`🔍 Extraction des positions pour le document ${documentIndex}`)
  console.log('📊 documentsConfiguration:', documentsConfiguration.value)
  console.log('📍 positionData actuel:', positionData.value)
  console.log('🖊️ signatureData actuel:', signatureData.value)
  
  // Priorité 1: Si c'est le document actuellement affiché dans SignBase, utiliser les données en temps réel
  if (documentIndex === activeSignBaseTabIndex.value && positionData.value && positionData.value.mode) {
    console.log(`✅ Document ${documentIndex} est actif dans SignBase, utilisation des données temps réel`)
    console.log(`🎯 Mode de position: ${positionData.value.mode}`)
    console.log(`📍 Données signature:`, positionData.value.signature)
    console.log(`📍 Données QR:`, positionData.value.qr)
    
    // Traiter les positions de signature selon le mode
    if (positionData.value.mode === 'signature' || positionData.value.mode === 'all' || positionData.value.mode === 'current' || positionData.value.mode === 'custom' || positionData.value.mode === 'individual') {
      // Essayer plusieurs structures possibles pour les positions de signature
      let signatureX, signatureY, signaturePage, signatureWidth, signatureHeight
      
      if (positionData.value.signature) {
        // Mode individual : positions par page
        if (positionData.value.mode === 'individual' && positionData.value.signature.positions) {
          console.log(`🔍 Mode individual détecté, extraction des positions par page:`, positionData.value.signature.positions)
          
          // Parcourir toutes les pages avec positions
          Object.entries(positionData.value.signature.positions).forEach(([page, pos]) => {
            if (pos.x !== undefined && pos.y !== undefined) {
              const pageKey = `${docKey}_page_${page}`
              signaturePositions[pageKey] = {
                x: pos.x,
                y: pos.y,
                page: parseInt(page),
                width: pos.width || 150,
                height: pos.height || 50
              }
              console.log(`✅ Position signature page ${page}:`, signaturePositions[pageKey])
            }
          })
        }
        // Autres modes : position unique
        else {
          // Structure directe: data.signature.x
          if (positionData.value.signature.x !== undefined && positionData.value.signature.y !== undefined) {
            signatureX = positionData.value.signature.x
            signatureY = positionData.value.signature.y
            signaturePage = positionData.value.signature.page || 1
            signatureWidth = positionData.value.signature.width || 150
            signatureHeight = positionData.value.signature.height || 50
          }
          // Structure imbriquée: data.signature.positions.default.x (comme dans SignImmediatelyPage)
          else if (positionData.value.signature.positions?.default) {
            signatureX = positionData.value.signature.positions.default.x
            signatureY = positionData.value.signature.positions.default.y
            signaturePage = positionData.value.signature.positions.default.page || 1
            signatureWidth = positionData.value.signature.positions.default.width || 150
            signatureHeight = positionData.value.signature.positions.default.height || 50
          }
          
          if (signatureX !== undefined && signatureY !== undefined) {
            signaturePositions[docKey] = {
              x: signatureX,
              y: signatureY,
              page: signaturePage,
              width: signatureWidth,
              height: signatureHeight
            }
            console.log(`✅ Position signature temps réel trouvée:`, signaturePositions[docKey])
          } else {
            console.log(`❌ Position signature manquante ou incomplète:`, positionData.value.signature)
          }
        }
      } else {
        console.log(`❌ Aucune donnée de signature dans positionData`)
      }
    }
    
    if (positionData.value.mode === 'qr' || positionData.value.mode === 'all' || positionData.value.mode === 'current' || positionData.value.mode === 'custom' || positionData.value.mode === 'individual') {
      // Essayer plusieurs structures possibles pour les positions QR
      let qrX, qrY, qrPage, qrSize
      
      if (positionData.value.qr) {
        // Mode individual : positions par page
        if (positionData.value.mode === 'individual' && positionData.value.qr.positions) {
          console.log(`🔍 Mode individual QR détecté, extraction des positions par page:`, positionData.value.qr.positions)
          
          // Parcourir toutes les pages avec positions QR
          Object.entries(positionData.value.qr.positions).forEach(([page, pos]) => {
            if (pos.x !== undefined && pos.y !== undefined) {
              const pageKey = `${docKey}_page_${page}`
              qrCodePositions[pageKey] = {
                x: pos.x,
                y: pos.y,
                page: parseInt(page),
                size: pos.size || positionData.value.qr.size || 100
              }
              console.log(`✅ Position QR page ${page}:`, qrCodePositions[pageKey])
            }
          })
        }
        // Autres modes : position unique
        else {
          // Structure directe: data.qr.x
          if (positionData.value.qr.x !== undefined && positionData.value.qr.y !== undefined) {
            qrX = positionData.value.qr.x
            qrY = positionData.value.qr.y
            qrPage = positionData.value.qr.page || 1
            qrSize = positionData.value.qr.size || 100
          }
          // Structure imbriquée: data.qr.positions.default.x (comme dans SignImmediatelyPage)
          else if (positionData.value.qr.positions?.default) {
            qrX = positionData.value.qr.positions.default.x
            qrY = positionData.value.qr.positions.default.y
            qrPage = positionData.value.qr.positions.default.page || 1
            qrSize = positionData.value.qr.positions.default.size || 100
          }
          
          if (qrX !== undefined && qrY !== undefined) {
            qrCodePositions[docKey] = {
              x: qrX,
              y: qrY,
              page: qrPage,
              size: qrSize
            }
            console.log(`✅ Position QR temps réel trouvée:`, qrCodePositions[docKey])
          } else {
            console.log(`❌ Position QR manquante ou incomplète:`, positionData.value.qr)
          }
        }
      } else {
        console.log(`❌ Aucune donnée QR dans positionData`)
      }
    }
    
    // Récupérer l'image de signature temps réel - gérer différents formats
    if (signatureData.value) {
      console.log(`🖊️ Type de signatureData:`, typeof signatureData.value, signatureData.value)
      
      if (signatureData.value.dataUrl) {
        // Format attendu : { dataUrl: "data:image/png;base64,..." }
        signatureImage = signatureData.value.dataUrl
        console.log(`✅ Image signature temps réel trouvée (dataUrl)`)
      } else if (signatureData.value instanceof File) {
        // Si c'est un File object, on doit le convertir
        console.log(`🔄 Conversion du File object en dataUrl...`)
        try {
          signatureImage = await fileToDataUrl(signatureData.value)
          console.log(`✅ Image signature convertie depuis File`)
        } catch (error) {
          console.error(`❌ Erreur conversion File:`, error)
        }
      } else if (typeof signatureData.value === 'string') {
        // Si c'est déjà une string (dataUrl)
        signatureImage = signatureData.value
        console.log(`✅ Image signature temps réel trouvée (string)`)
      }
    }
  }
  
  // Priorité 2: Utiliser les données sauvegardées dans documentsConfiguration (toujours vérifier)
  if (documentsConfiguration.value[docKey]) {
    const docConfig = documentsConfiguration.value[docKey]
    console.log(`📋 Configuration trouvée pour le document ${docKey}:`, docConfig)
    console.log(`📋 signaturePosition:`, docConfig.signaturePosition)
    console.log(`📋 qrPosition:`, docConfig.qrPosition)
    console.log(`📋 signatureImage:`, docConfig.signatureImage ? 'PRÉSENTE' : 'ABSENTE')
    console.log(`📋 positionMode:`, docConfig.positionMode)
    
    // Si on n'a pas encore de position signature, essayer de la récupérer
    if (!signaturePositions[docKey] && docConfig.signaturePosition) {
      if (docConfig.signaturePosition.x !== undefined && docConfig.signaturePosition.y !== undefined) {
        signaturePositions[docKey] = {
          x: docConfig.signaturePosition.x,
          y: docConfig.signaturePosition.y,
          page: docConfig.signaturePosition.page || 1,
          width: docConfig.signaturePosition.width || 150,
          height: docConfig.signaturePosition.height || 50
        }
        console.log(`✅ Position signature depuis config:`, signaturePositions[docKey])
      }
    }
    
    // Si on n'a pas encore de position QR, essayer de la récupérer
    if (!qrCodePositions[docKey] && docConfig.qrPosition) {
      if (docConfig.qrPosition.x !== undefined && docConfig.qrPosition.y !== undefined) {
        qrCodePositions[docKey] = {
          x: docConfig.qrPosition.x,
          y: docConfig.qrPosition.y,
          page: docConfig.qrPosition.page || 1,
          size: docConfig.qrPosition.size || 100
        }
        console.log(`✅ Position QR depuis config:`, qrCodePositions[docKey])
      }
    }
    
    // Si on n'a pas encore d'image signature, essayer de la récupérer
    if (!signatureImage && docConfig.signatureImage) {
      signatureImage = docConfig.signatureImage
      console.log(`✅ Image signature depuis config trouvée`)
    }
    
    // Récupérer le PDF généré si disponible
    if (docConfig.generatedPdf) {
      generatedPdf = docConfig.generatedPdf
      console.log(`✅ PDF généré depuis config trouvé:`, {
        hasFile: !!generatedPdf.file,
        hasBlob: !!generatedPdf.blob,
        hasDataUrl: !!generatedPdf.dataUrl
      })
    }
  }
  
  const result = { signaturePositions, qrCodePositions, signatureImage, generatedPdf }
  console.log(`🎯 Résultat final de l'extraction pour le document ${documentIndex}:`, result)
  
  return result
}

// Générer le PDF avec SignBase
const generateDocumentPdf = async () => {
  console.log('🎯 Tentative de génération PDF via SignBase...')
  
  if (!signBaseRef.value) {
    console.log('❌ SignBase ref non disponible')
    return null
  }
  
  console.log('✅ SignBase ref disponible, méthodes:', Object.keys(signBaseRef.value))
  
  try {
    // Essayer d'abord de récupérer un PDF déjà généré
    if (typeof signBaseRef.value.getGeneratedPdfBlob === 'function') {
      const existingBlob = signBaseRef.value.getGeneratedPdfBlob()
      if (existingBlob) {
        console.log('✅ PDF déjà généré récupéré')
        return existingBlob
      }
    }
    
    // Sinon, générer un nouveau PDF
    if (typeof signBaseRef.value.generatePreviewPdf === 'function') {
      console.log('🔄 Génération via generatePreviewPdf...')
      const result = await signBaseRef.value.generatePreviewPdf()
      console.log('📄 Résultat generatePreviewPdf:', !!result)
      return result
    } else if (typeof signBaseRef.value.generateFinalPdf === 'function') {
      console.log('🔄 Génération via generateFinalPdf...')
      const result = await signBaseRef.value.generateFinalPdf()
      console.log('📄 Résultat generateFinalPdf:', !!result)
      return result
    } else if (typeof signBaseRef.value.forceGeneratePdf === 'function') {
      console.log('🔄 Génération via forceGeneratePdf...')
      const result = await signBaseRef.value.forceGeneratePdf()
      console.log('📄 Résultat forceGeneratePdf:', !!result)
      return result
    } else {
      console.log('❌ Aucune méthode de génération PDF trouvée')
      console.log('Méthodes disponibles:', Object.keys(signBaseRef.value).filter(key => typeof signBaseRef.value[key] === 'function'))
    }
  } catch (error) {
    console.error('❌ Erreur lors de la génération PDF:', error)
  }
  
  return null
}

// Fonction utilitaire pour convertir un fichier en base64
const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      // Retourner seulement la partie base64 (sans le préfixe data:type;base64,)
      const base64 = reader.result.split(',')[1]
      resolve(base64)
    }
    reader.onerror = error => reject(error)
  })
}

const fileToDataUrl = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      // Retourner le dataUrl complet (data:type;base64,...)
      resolve(reader.result)
    }
    reader.onerror = error => reject(error)
  })
}

// Fonction utilitaire pour convertir un blob en base64
const blobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(blob)
    reader.onload = () => {
      // Retourner seulement la partie base64 (sans le préfixe data:type;base64,)
      const base64 = reader.result.split(',')[1]
      resolve(base64)
    }
    reader.onerror = error => reject(error)
  })
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
  background: #f8f9fa;
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

/* Notifications */
.notifications-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
}

.notification {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 4px solid;
  animation: slideInLeft 0.3s ease-out;
}

.notification-warning {
  border-left-color: #f59e0b;
  background: #fef3c7;
}

.notification-error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.notification-success {
  border-left-color: #10b981;
  background: #d1fae5;
}

.notification-error {
  border-left-color: #ef4444;
  background: #fee2e2;
}

.notification-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.notification-warning .notification-icon {
  color: #f59e0b;
}

.notification-success .notification-icon {
  color: #10b981;
}

.notification-error .notification-icon {
  color: #ef4444;
}

.notification-content {
  flex: 1;
}

.notification-message {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-dark);
}

.notification-close {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.notification-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-dark);
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
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
  font-size: 2.8rem;
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
  cursor: pointer;
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
  opacity: 0;
  pointer-events: none;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  width: 100%;
  height: 100%;
  justify-content: center;
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
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
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
  font-size: 1rem;
  color: var(--text-muted);
  margin: 0 0 8px 0;
}

.upload-text .link {
  color: var(--primary-blue);
  text-decoration: underline;
  cursor: pointer;
}

.upload-text small {
  font-size: 0.875rem;
  color: var(--text-muted);
  opacity: 0.7;
}

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
  border-radius: 8px;
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
  color: var(--text-muted);
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

/* SECTION PREVIEW */
.preview-section {
  margin-bottom: 2rem;
}

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
  color: var(--text-muted);
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

/* SECTION VALIDATION WORKFLOW */
.workflow-validation-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chief-validation-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.validation-header {
  margin-bottom: 1.5rem;
}

.validation-header h5 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.validation-header p {
  color: var(--text-muted);
  margin: 0;
}

/* Loading state */
.validation-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top: 3px solid var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Chef info */
.chief-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chief-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 12px;
}

.chief-avatar {
  width: 60px;
  height: 60px;
  background: var(--primary-blue);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.chief-details {
  flex: 1;
}

.chief-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.chief-email {
  color: var(--text-muted);
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.chief-role {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.chief-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  color: var(--success);
  font-size: 0.8rem;
  font-weight: 500;
}

.chief-status i {
  font-size: 1.2rem;
}

/* Workflow info */
.workflow-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.step-icon {
  width: 40px;
  height: 40px;
  background: var(--primary-blue);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h6 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.step-content p {
  color: var(--text-muted);
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.step-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.step-status.completed {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.step-status.pending {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.workflow-arrow {
  display: flex;
  justify-content: center;
  color: var(--text-muted);
  font-size: 1.2rem;
}

/* Error states */
.no-chief-error,
.validation-error {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 12px;
}

.error-icon {
  color: #dc2626;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.error-content h6 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.5rem 0;
}

.error-content p {
  color: var(--text-muted);
  margin: 0 0 0.5rem 0;
}

.error-solution {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  color: #1d4ed8;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.error-solution i {
  flex-shrink: 0;
  margin-top: 0.1rem;
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

/* SUBMISSION SUCCESS - Style homogène avec DocumentsPage */
.submission-success-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-top: 2rem;
}

/* Carte de succès principale - Style DocumentsPage */
.document-success-card {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px) saturate(120%);
  -webkit-backdrop-filter: blur(10px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Suppression de la barre de couleur au-dessus */

.document-success-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.document-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.document-icon {
  width: 45px;
  height: 45px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.25rem;
  flex-shrink: 0;
}

.document-details {
  flex: 1;
  min-width: 0;
}

.document-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Raleway', sans-serif;
}

.document-size {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-family: 'Raleway', sans-serif;
}

.document-status {
  flex-shrink: 0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  font-family: 'Raleway', sans-serif;
}

.status-badge.success {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.status-badge.completed {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.status-badge.pending {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
  border: 1px solid rgba(249, 115, 22, 0.2);
}

.document-success-content {
  text-align: center;
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  font-size: 0.95rem;
  font-weight: 500;
  font-family: 'Raleway', sans-serif;
}

.success-message i {
  font-size: 1.1rem;
}

/* Section workflow - Style homogène avec DocumentsPage */
.workflow-status-section {
  margin-top: 2rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.workflow-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.workflow-status-card {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px) saturate(120%);
  -webkit-backdrop-filter: blur(10px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Suppression des barres de couleur au-dessus des cartes de workflow */

.workflow-status-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.workflow-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.workflow-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.workflow-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.workflow-status-card.completed .workflow-icon {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.workflow-status-card.pending .workflow-icon {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

.workflow-details {
  flex: 1;
  min-width: 0;
}

.workflow-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
  font-family: 'Raleway', sans-serif;
}

.workflow-description {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.workflow-status {
  flex-shrink: 0;
}

.workflow-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  font-family: 'Raleway', sans-serif;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 0.5rem 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.meta-item i {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Responsive */
@media (max-width: 768px) {
  .workflow-cards-grid {
    grid-template-columns: 1fr;
  }
  
  .workflow-card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .workflow-meta {
    justify-content: center;
  }
}

/* SUBMISSION PROGRESS - Barre de progression pour la préparation multiple */
.submission-progress-section {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px) saturate(120%);
  -webkit-backdrop-filter: blur(10px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.progress-header h4 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-dark);
  font-family: 'Raleway', sans-serif;
}

.progress-counter {
  font-size: 1rem;
  font-weight: 500;
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid rgba(0, 102, 204, 0.2);
  font-family: 'Raleway', sans-serif;
}

.global-progress {
  margin-bottom: 2rem;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-blue), #4a90e2);
  border-radius: 6px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-text {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-family: 'Raleway', sans-serif;
  text-align: center;
  display: block;
}

.documents-progress {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.document-progress-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.document-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.document-info i {
  color: #dc3545;
  font-size: 1.1rem;
}

.document-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-dark);
  font-family: 'Raleway', sans-serif;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.document-progress {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.mini-progress-bar {
  width: 100px;
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.mini-progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.mini-progress-fill.progress-success {
  background: #22c55e;
}

.mini-progress-fill.progress-error {
  background: #ef4444;
}

.mini-progress-fill.progress-active {
  background: linear-gradient(90deg, var(--primary-blue), #4a90e2);
}

.mini-progress-text {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-muted);
  font-family: 'Raleway', sans-serif;
  min-width: 35px;
  text-align: right;
}

.document-status {
  flex-shrink: 0;
}

.document-status i {
  font-size: 1.2rem;
}

.status-success {
  color: #22c55e;
}

.status-error {
  color: #ef4444;
}

.status-active {
  color: var(--primary-blue);
}

.status-pending {
  color: #6b7280;
}

/* Responsive pour la progression */
@media (max-width: 768px) {
  .progress-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .document-progress-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .document-progress {
    width: 100%;
    justify-content: space-between;
  }
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
}

.preview-pdf {
  height: calc(100% - 40px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  background: white;
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
  font-size: 0.75rem;
  color: var(--text-muted);
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
