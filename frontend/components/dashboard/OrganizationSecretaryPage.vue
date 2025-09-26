<template>
  <div class="organization-secretary-page">
    <!-- Bouton de fermeture -->
    <button class="close-organization-btn" @click="closeOrganizationDashboard" title="Fermer et retourner à la sélection d'organisation">
      <i class="bi bi-x"></i>
    </button>
    
    <!-- Header avec titre de la section -->
    <div class="organization-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="display-4 fw-bold mb-3 text-dark header-title">
            <span class="text-dark">Espace Secrétaire de </span>
            <span class="text-primary-blue">l'organisation </span> 
            <span class="text-primary-blue" v-if="organizationName"> {{ organizationName }}</span>
          </h1>
          <p class="lead mb-0 text-dark sections-subtitle" v-if="organizationName">
            Gérez les documents, les signatures et l'organisation {{ organizationName }}.
          </p>
          <p class="lead mb-0 text-dark sections-subtitle" v-else>
            Vous êtes secrétaire d'une organisation. Gérez les documents et les signatures.
          </p>
          <div class="header-actions mt-4">
            <button class="btn btn-primary-custom create-doc-btn" @click="toggleCreateDocumentModal" ref="createDocBtn">
              <i class="bi bi-file-earmark-plus me-2"></i>
              Créer un document
            </button>
            <button class="btn btn-outline-primary manage-docs-btn" @click="toggleManageDocuments">
              <i class="bi bi-gear me-2"></i>
              Gérer les documents
            </button>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Organisation Secrétaire" class="header-image">
        </div>
      </div>
    </div>

    <!-- Section statistiques avancées -->
    <div class="docs-stats-section">
      <div class="row g-4">
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ secretaryStats.totalDocuments || 0 }}</h4>
              <p class="stat-label">Total documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ secretaryStats.signedDocuments || 0 }}</h4>
              <p class="stat-label">Signés</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ secretaryStats.pendingDocuments || 0 }}</h4>
              <p class="stat-label">En attente</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ secretaryStats.organizationMembers || 0 }}</h4>
              <p class="stat-label">Membres</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sections de gestion en deux colonnes -->
    <div v-if="!showAllDocuments" class="documents-sections">
      <!-- En-tête de section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Gestion</span> 
              <span class="text-primary-blue"> Documentaire</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Gérez les documents de l'organisation et supervisez les signatures.
            </p>
          </div>
        </div>
      </div>

      <!-- Système d'onglets pour la gestion documentaire -->
      <div class="tabs-container">
        <div class="tabs-header">
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'models' }"
            @click="setActiveDocumentTab('models')"
          >
            <i class="bi bi-file-earmark-text me-2"></i>
            Modèles
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'prepared-with-model' }"
            @click="setActiveDocumentTab('prepared-with-model')"
          >
            <i class="bi bi-file-earmark-check me-2"></i>
            Documents préparés avec modèle
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'prepared-immediate' }"
            @click="setActiveDocumentTab('prepared-immediate')"
          >
            <i class="bi bi-file-earmark-arrow-up me-2"></i>
            Documents préparés immédiatement
          </button>
        </div>

        <!-- Contenu de l'onglet "Modèles" -->
        <div v-if="activeDocumentTab === 'models'" class="tab-content">
          <div class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-text fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Gestion des Modèles</h4>
              <p class="text-muted mb-4">Créez et gérez vos modèles de documents réutilisables</p>
              <button class="btn btn-primary-blue">
                <i class="bi bi-plus-circle me-2"></i>
                Créer un modèle
              </button>
            </div>
          </div>
        </div>

        <!-- Contenu de l'onglet "Documents préparés avec modèle" -->
        <div v-if="activeDocumentTab === 'prepared-with-model'" class="tab-content">
          <div class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-check fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Documents Préparés avec Modèle</h4>
              <p class="text-muted mb-4">Documents créés à partir de vos modèles personnalisés</p>
              <button class="btn btn-primary-blue">
                <i class="bi bi-file-earmark-plus me-2"></i>
                Nouveau document avec modèle
              </button>
            </div>
          </div>
        </div>

        <!-- Contenu de l'onglet "Documents préparés immédiatement" -->
        <div v-if="activeDocumentTab === 'prepared-immediate'" class="tab-content">
          <!-- En-tête avec barre de recherche et bouton d'action -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <!-- Barre de recherche -->
            <div class="search-container">
              <div class="search-input-wrapper">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  class="search-input" 
                  placeholder="Rechercher dans les documents..."
                  v-model="searchQuery"
                  @input="searchDocuments"
                >
                <button 
                  v-if="searchQuery" 
                  class="clear-search-btn"
                  @click="clearSearch"
                >
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <button class="btn btn-primary-blue" @click="navigateToDocumentPreparation">
              <i class="bi bi-upload me-2"></i>
              Nouvelle préparation
            </button>
          </div>

          <!-- Loading state -->
          <div v-if="isLoadingDocuments" class="text-center py-5">
            <div class="spinner-border text-primary-blue" role="status">
              <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="text-muted mt-3">Chargement des documents...</p>
          </div>

          <!-- Error state -->
          <div v-else-if="documentsError" class="text-center py-5">
            <div class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ documentsError }}
            </div>
            <button class="btn btn-outline-primary" @click="fetchPreparedDocuments">
              <i class="bi bi-arrow-clockwise me-2"></i>
              Réessayer
            </button>
          </div>

          <!-- Documents grid -->
          <div v-else-if="filteredDocuments.length > 0" class="documents-grid">
            <div 
              class="document-card" 
              v-for="(document, index) in filteredDocuments" 
              :key="document.id"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <!-- Header de la carte -->
              <div class="card-header">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf"></i>
                </div>
                <div class="document-name">{{ document.document_title || document.original_filename }}</div>
                <div class="document-header-content">
                  <div class="organization-badge">
                    <span>{{ document.organization_name }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Contenu de la carte -->
              <div class="card-content">
                <p class="document-description">{{ document.document_description || 'Aucune description' }}</p>
                
                <!-- Hiérarchie de signature -->
                <div class="signature-hierarchy">
                  <h6 class="hierarchy-title">
                    <i class="bi bi-diagram-3 me-2"></i>
                    Hiérarchie de signature
                  </h6>
                  <div class="signature-steps">
                    <!-- Étapes précédentes (complétées) -->
                    <div class="signature-step completed" v-if="document.current_step > 1">
                      <div class="step-indicator">
                        <i class="bi bi-check-circle-fill"></i>
                      </div>
                      <div class="step-content">
                        <span class="step-title">Préparé par</span>
                        <span class="step-person">{{ document.prepared_by_name }}</span>
                      </div>
                    </div>
                    
                    <!-- Étape actuelle -->
                    <div class="signature-step current">
                      <div class="step-indicator">
                        <i class="bi bi-clock"></i>
                      </div>
                      <div class="step-content">
                        <span class="step-title">En attente de signature</span>
                        <span class="step-person">{{ document.current_signer_name || 'Non assigné' }}</span>
                      </div>
                    </div>
                    
                    <!-- Étapes restantes -->
                    <div class="signature-step pending" v-if="document.current_step < document.total_steps">
                      <div class="step-indicator">
                        <i class="bi bi-circle"></i>
                      </div>
                      <div class="step-content">
                        <span class="step-title">Étapes restantes</span>
                        <span class="step-person">{{ document.total_steps - document.current_step }} étape(s)</span>
                      </div>
                    </div>
                  </div>
                </div>
                
              </div>
              
              <!-- Footer de la carte -->
              <div class="card-footer">
                <div class="document-info">
                  <div class="document-meta">
                    <div class="meta-item">
                      <i class="bi bi-calendar"></i>
                      <span>{{ formatDate(document.created_at) }}</span>
                    </div>
                    <div class="meta-item">
                      <i class="bi bi-bar-chart"></i>
                      <span>{{ document.progress_percentage || 0 }}% complété</span>
                    </div>
                  </div>
                  <span class="document-step">Étape {{ document.current_step || 1 }}/{{ document.total_steps || 1 }}</span>
                </div>
                 <div class="document-actions">
                   <button 
                     class="btn btn-sm btn-outline-primary" 
                     title="Aperçu du document"
                     @click="showDocumentPreview(document, 'current', $event)"
                   >
                     <i class="bi bi-eye"></i>
                   </button>
                   <button 
                     class="btn btn-sm btn-outline-info" 
                     title="Aperçu final (PDF généré)" 
                     v-if="document.generated_pdf"
                     @click="showDocumentPreview(document, 'generated', $event)"
                   >
                     <i class="bi bi-file-earmark-pdf"></i>
                   </button>
                   <button 
                     class="btn btn-sm btn-outline-success" 
                     title="Télécharger"
                     @click="downloadDocument(document)"
                   >
                     <i class="bi bi-download"></i>
                   </button>
                 </div>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else-if="preparedDocuments.length === 0" class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-arrow-up fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Aucun document préparé</h4>
              <p class="text-muted mb-4">Vous n'avez pas encore préparé de documents immédiatement</p>
              <button class="btn btn-primary-blue" @click="navigateToDocumentPreparation">
                <i class="bi bi-upload me-2"></i>
                Créer votre premier document
              </button>
            </div>
          </div>

          <!-- No search results state -->
          <div v-else-if="searchQuery && filteredDocuments.length === 0" class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-search fs-1 text-muted mb-3"></i>
              <h4 class="text-dark mb-3">Aucun document trouvé</h4>
              <p class="text-muted mb-4">Aucun document ne correspond à votre recherche "{{ searchQuery }}".</p>
              <button class="btn btn-outline-primary" @click="clearSearch">
                <i class="bi bi-arrow-left me-2"></i>
                Effacer la recherche
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vue complète des documents -->
    <div v-else class="all-documents-view">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">Gestion des documents</h3>
            <div class="d-flex gap-2">
              <button class="btn btn-primary" @click="toggleCreateDocumentModal">
                <i class="bi bi-plus me-2"></i>
                Nouveau document
              </button>
              <button class="btn btn-outline-primary" @click="toggleAllDocuments">
                <i class="bi bi-arrow-left me-2"></i>
                Retour aux sections
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tableau des documents -->
      <div class="documents-table-container">
        <div class="documents-table">
          <!-- En-tête du tableau -->
          <div class="table-header">
            <div class="table-row header-row">
              <div class="table-cell document-cell">Document</div>
              <div class="table-cell">Assigné à</div>
              <div class="table-cell">Date</div>
              <div class="table-cell">Statut</div>
              <div class="table-cell">Actions</div>
      </div>
    </div>

          <!-- Lignes des documents -->
          <div class="table-body">
            <div class="table-row document-row" v-for="(document, index) in allDocuments" :key="index" @click="viewDocument(document)">
              <div class="table-cell document-cell">
                <div class="document-info-full">
                  <div class="document-icon-full">
                    <i class="bi bi-file-earmark-pdf"></i>
            </div>
                  <div class="document-details-full">
                    <h6 class="document-name-full">{{ document.name }}</h6>
                    <span class="document-type">{{ document.type }}</span>
                  </div>
                </div>
              </div>
              <div class="table-cell">{{ document.assignedTo }}</div>
              <div class="table-cell">{{ document.date }}</div>
              <div class="table-cell">
                <span class="status-badge" :class="document.status">{{ document.statusText }}</span>
              </div>
              <div class="table-cell">
                <div class="document-actions-full">
                  <button class="btn btn-sm btn-outline-primary" @click.stop="viewDocument(document)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-success" @click.stop="editDocument(document)" title="Éditer">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-warning" @click.stop="assignDocument(document)" title="Assigner">
                    <i class="bi bi-person-plus"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click.stop="deleteDocument(document)" title="Supprimer">
                    <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Modale contextuelle de création de document -->
    <div v-if="showCreateDocumentModal" class="signature-modal-overlay" @click="closeCreateDocumentModal">
      <div class="signature-modal" @click.stop ref="createDocumentModal">
        <div class="signature-modal-header">
          <h5>
            <i class="bi bi-file-earmark-plus"></i>
            Créer un Document
          </h5>
          <button class="close-btn" @click="closeCreateDocumentModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="signature-modal-content">
          <div class="signature-option" @click="selectDocumentOption('immediate')">
            <div class="option-icon">
              <i class="bi bi-lightning-fill"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Créer immédiatement</span>
              <span class="option-desc">Créez un nouveau document à partir de zéro</span>
            </div>
          </div>
          
          <div class="signature-option" @click="selectDocumentOption('template')">
            <div class="option-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="option-content">
              <span class="option-title">À partir d'un modèle</span>
              <span class="option-desc">Choisissez parmi nos modèles de documents</span>
            </div>
          </div>
        </div>
      </div>
     </div>
   </div>

   <!-- Tooltip de prévisualisation des documents -->
   <div 
     v-if="showPreviewTooltip" 
     class="document-preview-tooltip" 
     :style="{ top: tooltipPosition.top + 'px', left: tooltipPosition.left + 'px' }" 
     @click.stop 
     @mouseenter="cancelCloseTooltip" 
     @mouseleave="closePreviewTooltip"
   >
     <div class="tooltip-arrow" :class="'arrow-' + tooltipDirection"></div>
     <div class="tooltip-content">
       <div class="tooltip-header">
          <h4 class="tooltip-title">
            <i class="bi bi-file-earmark-pdf me-2"></i>
            {{ previewType === 'current' ? 'Document actuel (workflow)' : 'PDF généré (avec éléments)' }} - {{ currentPreviewDocument?.document_title || currentPreviewDocument?.original_filename }}
          </h4>
         <button class="tooltip-close" @click="closePreviewTooltip">
           <i class="bi bi-x"></i>
         </button>
       </div>
       
       <div class="tooltip-body">
         <div class="preview-container">
           <!-- Aperçu PDF exactement comme dans DocumentPreparationPage -->
           <div class="pdf-preview-content">
             <div v-if="previewPdfSource && !pdfLoadError" class="pdf-container">
               <!-- Solution simple avec iframe native -->
               <iframe
                 :src="previewPdfSource"
                 class="pdf-iframe"
                 frameborder="0"
                 @load="onPreviewPdfLoaded"
                 @error="onPreviewPdfLoadError"
               ></iframe>
             </div>
             
             <!-- Fallback si iframe ne fonctionne pas -->
             <div v-else-if="previewPdfSource && pdfLoadError" class="pdf-fallback">
               <div class="fallback-content">
                 <i class="bi bi-file-earmark-pdf-fill"></i>
                 <h3>{{ currentPreviewDocument?.document_title || currentPreviewDocument?.original_filename || 'Document PDF' }}</h3>
                 <p class="fallback-description">
                   <i class="bi bi-info-circle me-2"></i>
                   Aperçu non disponible dans cette vue
                 </p>
                 <p class="fallback-subtitle">
                   Cliquez sur "Ouvrir dans un nouvel onglet" pour voir le contenu complet
                 </p>
                 <div class="fallback-actions">
                   <button 
                     class="btn btn-primary me-2" 
                     @click="openDocumentDirectly"
                   >
                     <i class="bi bi-box-arrow-up-right me-2"></i>
                     Ouvrir le PDF
                   </button>
                   <a 
                     :href="previewPdfSource" 
                     :download="currentPreviewDocument?.original_filename || 'document.pdf'"
                     class="btn btn-outline-primary"
                   >
                     <i class="bi bi-download me-2"></i>
                     Télécharger
                   </a>
                 </div>
               </div>
             </div>
             
             <!-- État de chargement -->
             <div v-else-if="!previewPdfSource && !pdfLoadError" class="pdf-loading-state">
               <i class="bi bi-file-earmark-pdf-fill fs-1 text-primary mb-3"></i>
               <p>Chargement du document...</p>
             </div>
             
             <!-- État d'erreur -->
             <div v-else-if="pdfLoadError" class="pdf-error-state">
               <i class="bi bi-exclamation-triangle fs-1 text-warning mb-3"></i>
               <p>Impossible de charger le PDF</p>
               <button class="btn btn-sm btn-outline-primary mt-2" @click="retryPdfLoad">
                 <i class="bi bi-arrow-clockwise me-1"></i>
                 Réessayer
               </button>
             </div>
           </div>
         </div>
         
       </div>
     </div>
   </div>
 </template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Store d'authentification
const authStore = useAuthStore()

// État des données
const userOrganization = ref(null)
const selectedOrganization = ref(null)
const showAllDocuments = ref(false)
const showCreateDocumentModal = ref(false)
const isCreatingDocument = ref(false)

// Gestion des onglets de gestion documentaire
const activeDocumentTab = ref('models')

// Données pour les documents préparés
const preparedDocuments = ref([])
const filteredDocuments = ref([])
const isLoadingDocuments = ref(false)
  const documentsError = ref(null)
  const searchQuery = ref('')

  // Variables pour les tooltips de prévisualisation
  const showPreviewTooltip = ref(false)
  const previewType = ref('') // 'current' ou 'generated'
  const tooltipPosition = ref({ top: 0, left: 0 })
  const tooltipDirection = ref('right')
  const currentPreviewDocument = ref(null)
  const closeTooltipTimeout = ref(null)

  // Variables pour la prévisualisation PDF
  const previewPdfSource = ref(null)
  const pdfLoadError = ref(false)

// Références pour la modale
const createDocBtn = ref(null)
const createDocumentModal = ref(null)

// Computed pour l'organisation
const organizationName = computed(() => {
  console.log('🔍 Computed organizationName - userOrganization:', userOrganization.value)
  console.log('🔍 Computed organizationName - structure:', userOrganization.value?.organization)
  console.log('🔍 Computed organizationName - name:', userOrganization.value?.organization?.name)
  console.log('🔍 Computed organizationName - direct name:', userOrganization.value?.name)
  
  // Essayer les deux structures possibles
  return userOrganization.value?.organization?.name || userOrganization.value?.name || ''
})

// Statistiques du secrétaire
const secretaryStats = ref({
  totalDocuments: 0,
  signedDocuments: 0,
  pendingDocuments: 0,
  organizationMembers: 0
})

// Membres de l'organisation
const organizationMembers = ref([
  { id: 1, name: 'Jean Dupont', role: 'Membre' },
  { id: 2, name: 'Marie Martin', role: 'Membre' },
  { id: 3, name: 'Pierre Durand', role: 'Chef' }
])

// Documents à gérer
const documentsToManage = ref([
  {
    name: 'Contrat de service 2024',
    date: '15 Jan 2024',
    status: 'signed',
    statusText: 'Signé',
    type: 'PDF',
    assignedTo: 'Jean Dupont'
  },
  {
    name: 'Accord de confidentialité',
    date: '12 Jan 2024',
    status: 'pending',
    statusText: 'En attente',
    type: 'PDF',
    assignedTo: 'Marie Martin'
  },
  {
    name: 'Rapport mensuel',
    date: '10 Jan 2024',
    status: 'draft',
    statusText: 'Brouillon',
    type: 'PDF',
    assignedTo: 'Pierre Durand'
  }
])

// Tous les documents
const allDocuments = ref([
  ...documentsToManage.value,
  {
    name: 'Facture janvier 2024',
    date: '08 Jan 2024',
    status: 'signed',
    statusText: 'Signé',
    type: 'PDF',
    assignedTo: 'Jean Dupont'
  },
  {
    name: 'Contrat de maintenance',
    date: '05 Jan 2024',
    status: 'pending',
    statusText: 'En attente',
    type: 'PDF',
    assignedTo: 'Marie Martin'
  }
])

// Nouveau document
const newDocument = ref({
  name: '',
  type: '',
  assignedTo: '',
  description: ''
})

// Fonctions de navigation
const closeOrganizationDashboard = () => {
  // Émettre un événement pour retourner à la page de sélection d'organisation
  window.dispatchEvent(new CustomEvent('navigateToOrganizationSelection'))
}

const toggleAllDocuments = () => {
  showAllDocuments.value = !showAllDocuments.value
}

const toggleCreateDocumentModal = () => {
  showCreateDocumentModal.value = !showCreateDocumentModal.value
  
  if (showCreateDocumentModal.value) {
    // Bloquer le défilement du contenu arrière
    document.body.style.overflow = 'hidden'
    
    nextTick(() => {
      if (createDocBtn.value && createDocumentModal.value && window.innerWidth > 768) {
        const buttonRect = createDocBtn.value.getBoundingClientRect()
        const modal = createDocumentModal.value
        
        // Dimensions de la modale
        const modalWidth = 320
        const modalHeight = 200
        
        // Marge de sécurité
        const margin = 20
        
        // Calculer l'espace disponible dans chaque direction
        const spaceRight = window.innerWidth - buttonRect.right
        const spaceLeft = buttonRect.left
        const spaceBelow = window.innerHeight - buttonRect.bottom
        const spaceAbove = buttonRect.top
        
        let leftPosition, topPosition
        
        // Positionner horizontalement selon l'espace disponible
        if (spaceRight >= modalWidth + margin) {
          // Plus d'espace à droite
          leftPosition = buttonRect.right + 10
        } else if (spaceLeft >= modalWidth + margin) {
          // Plus d'espace à gauche
          leftPosition = buttonRect.left - modalWidth - 10
        } else {
          // Pas assez d'espace, centrer horizontalement
          leftPosition = (window.innerWidth - modalWidth) / 2
        }
        
        // Positionner verticalement selon l'espace disponible
        if (spaceBelow >= modalHeight + margin) {
          // Plus d'espace en bas
          topPosition = buttonRect.bottom + 10
        } else if (spaceAbove >= modalHeight + margin) {
          // Plus d'espace en haut
          topPosition = buttonRect.top - modalHeight - 10
        } else {
          // Pas assez d'espace, centrer verticalement
          topPosition = (window.innerHeight - modalHeight) / 2
        }
        
        // Appliquer les positions
        modal.style.left = `${leftPosition}px`
        modal.style.top = `${topPosition}px`
        modal.style.transform = 'none'
      } else {
        // Sur mobile ou si les éléments ne sont pas trouvés, centrer la modale
        const modal = createDocumentModal.value
        if (modal) {
          modal.style.left = '50%'
          modal.style.top = '50%'
          modal.style.transform = 'translate(-50%, -50%)'
        }
      }
    })
  }
}

// Gestion des événements pour fermer le tooltip
const handleDocumentClick = (event) => {
  // Fermer le tooltip si on clique en dehors
  if (showPreviewTooltip.value && !event.target.closest('.document-preview-tooltip') && !event.target.closest('.document-actions button')) {
    closePreviewTooltip()
  }
}

const handleKeyDown = (event) => {
  // Fermer le tooltip si on appuie sur Échap
  if (event.key === 'Escape' && showPreviewTooltip.value) {
    closePreviewTooltip()
  }
}

// Fonctions pour les tooltips de prévisualisation
const showDocumentPreview = (document, type, event) => {
  // Vérifier que nous sommes dans un environnement client
  if (typeof window === 'undefined') return
  
  // Annuler le délai de fermeture si la souris revient
  if (closeTooltipTimeout.value) {
    clearTimeout(closeTooltipTimeout.value)
    closeTooltipTimeout.value = null
  }
  
  // Calculer la position du tooltip par rapport au bouton cliqué
  if (event && event.target) {
    const button = event.target.closest('button')
    const rect = button ? button.getBoundingClientRect() : event.target.getBoundingClientRect()
    const scrollTop = window.pageYOffset || (document.documentElement ? document.documentElement.scrollTop : 0)
    const scrollLeft = window.pageXOffset || (document.documentElement ? document.documentElement.scrollLeft : 0)
    
    const tooltipWidth = 550 // Largeur du tooltip de prévisualisation
    const tooltipHeight = 750 // Hauteur du tooltip de prévisualisation
    const windowWidth = window.innerWidth
    const windowHeight = window.innerHeight
    
    // Calculer l'espace disponible de chaque côté
    const spaceLeft = rect.left
    const spaceRight = windowWidth - rect.right
    const spaceTop = rect.top
    const spaceBottom = windowHeight - rect.bottom
    
    let top, left, direction
    
    // Déterminer la meilleure position en fonction de l'espace disponible
    const horizontalSpace = Math.max(spaceLeft, spaceRight)
    const verticalSpace = Math.max(spaceTop, spaceBottom)
    
    if (horizontalSpace > verticalSpace) {
      // Plus d'espace horizontal, positionner à gauche ou à droite
      if (spaceLeft > spaceRight) {
        // Plus d'espace à gauche
        left = rect.left + scrollLeft - tooltipWidth - 10
        top = rect.top + scrollTop + (rect.height / 2) - (tooltipHeight / 2)
        direction = 'right' // Flèche pointant vers la droite
      } else {
        // Plus d'espace à droite
        left = rect.right + scrollLeft + 10
        top = rect.top + scrollTop + (rect.height / 2) - (tooltipHeight / 2)
        direction = 'left' // Flèche pointant vers la gauche
      }
    } else {
      // Plus d'espace vertical, positionner en haut ou en bas
      if (spaceTop > spaceBottom) {
        // Plus d'espace en haut
        top = rect.top + scrollTop - tooltipHeight - 10
        left = rect.left + scrollLeft + (rect.width / 2) - (tooltipWidth / 2)
        direction = 'bottom' // Flèche pointant vers le bas
      } else {
        // Plus d'espace en bas
        top = rect.bottom + scrollTop + 10
        left = rect.left + scrollLeft + (rect.width / 2) - (tooltipWidth / 2)
        direction = 'top' // Flèche pointant vers le haut
      }
    }
    
    tooltipDirection.value = direction
    
    // Ajustements finaux pour éviter de sortir de l'écran
    const margin = 20
    
    // Ajustement horizontal
    if (left < margin) {
      left = margin
    } else if (left + tooltipWidth > windowWidth - margin) {
      left = windowWidth - tooltipWidth - margin
    }
    
    // Ajustement vertical
    if (top < scrollTop + margin) {
      top = scrollTop + margin
    } else if (top + tooltipHeight > windowHeight + scrollTop - margin) {
      top = windowHeight + scrollTop - tooltipHeight - margin
    }
    
    // Vérification finale pour s'assurer que la bulle est entièrement visible
    const finalLeft = Math.max(margin, Math.min(left, windowWidth - tooltipWidth - margin))
    const finalTop = Math.max(scrollTop + margin, Math.min(top, windowHeight + scrollTop - tooltipHeight - margin))
    
    tooltipPosition.value = { top: finalTop, left: finalLeft }
  }
  
  currentPreviewDocument.value = document
  previewType.value = type
  pdfLoadError.value = false // Réinitialiser l'erreur PDF
  
  // Utiliser l'endpoint spécial pour l'aperçu PDF (sans restrictions X-Frame-Options)
  let pdfUrl = null
  if (type === 'current' && document.current_document) {
    // Document à l'état actuel du workflow (avec signatures partielles)
    pdfUrl = `http://127.0.0.1:8000/api/signatures/pdf-preview/${document.id}/current/`
    console.log('📄 Aperçu du document actuel (état du workflow)')
  } else if (type === 'generated' && document.generated_pdf) {
    // PDF généré avec éléments positionnés (QR code, signature)
    pdfUrl = `http://127.0.0.1:8000/api/signatures/pdf-preview/${document.id}/generated/`
    console.log('📄 Aperçu du PDF généré (avec éléments)')
  }
  
  previewPdfSource.value = pdfUrl
  showPreviewTooltip.value = true
  
  console.log('🔄 Utilisation de l\'endpoint spécial pour l\'aperçu PDF:', pdfUrl)
}

const closePreviewTooltip = () => {
  closeTooltipTimeout.value = setTimeout(() => {
    showPreviewTooltip.value = false
    currentPreviewDocument.value = null
    previewType.value = ''
    previewPdfSource.value = null
  }, 150) // Légèrement plus long pour éviter les fermetures accidentelles
}

const cancelCloseTooltip = () => {
  if (closeTooltipTimeout.value) {
    clearTimeout(closeTooltipTimeout.value)
    closeTooltipTimeout.value = null
  }
}

// Fonctions de gestion du PDF
const onPreviewPdfLoaded = () => {
  pdfLoadError.value = false
  console.log('PDF chargé avec succès')
}

const onPreviewPdfLoadError = () => {
  pdfLoadError.value = true
  console.error('Erreur lors du chargement du PDF (X-Frame-Options probable)')
  console.log('🔄 Affichage du fallback avec téléchargement direct')
}

// Fonction pour formater la taille des fichiers
const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Fonction pour formater les dates
const formatDate = (dateString) => {
  if (!dateString) return 'Date inconnue'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return 'Date inconnue'
  }
}

const retryPdfLoad = () => {
  pdfLoadError.value = false
  // Recharger la source PDF avec l'endpoint spécial
  if (currentPreviewDocument.value && previewType.value) {
    let pdfUrl = null
    if (previewType.value === 'current' && currentPreviewDocument.value.current_document) {
      // Document à l'état actuel du workflow (avec signatures partielles)
      pdfUrl = `http://127.0.0.1:8000/api/signatures/pdf-preview/${currentPreviewDocument.value.id}/current/`
    } else if (previewType.value === 'generated' && currentPreviewDocument.value.generated_pdf) {
      // PDF généré avec éléments positionnés (QR code, signature)
      pdfUrl = `http://127.0.0.1:8000/api/signatures/pdf-preview/${currentPreviewDocument.value.id}/generated/`
    }
    previewPdfSource.value = pdfUrl
    console.log('🔄 Retry avec endpoint spécial:', pdfUrl)
  }
}

// Fonction pour ouvrir le document directement
const openDocumentDirectly = () => {
  if (currentPreviewDocument.value && previewPdfSource.value) {
    window.open(previewPdfSource.value, '_blank')
  }
}

// Fonction pour télécharger le document depuis le tooltip
const downloadCurrentPreviewDocument = () => {
  if (currentPreviewDocument.value) {
    downloadDocument(currentPreviewDocument.value)
  }
}

// Fonction pour télécharger le document
const downloadDocument = (document) => {
  // Vérifier que nous sommes dans un environnement client
  if (typeof window === 'undefined') return
  
  try {
    // Utiliser l'endpoint spécial pour télécharger le document actuel selon l'état du workflow
    const downloadUrl = `http://127.0.0.1:8000/api/signatures/pdf-preview/${document.id}/current/?download=true`
    const filename = document.original_filename || document.document_title || 'document.pdf'
    
    console.log('📥 Téléchargement du document actuel via endpoint spécial:', downloadUrl)
    
    // Créer un lien de téléchargement
    const link = window.document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    link.target = '_blank'
    
    // Déclencher le téléchargement
    window.document.body.appendChild(link)
    link.click()
    window.document.body.removeChild(link)
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error)
  }
}

const closeCreateDocumentModal = () => {
  showCreateDocumentModal.value = false
  // Restaurer le défilement du contenu arrière
  document.body.style.overflow = ''
  newDocument.value = {
    name: '',
    type: '',
    assignedTo: '',
    description: ''
  }
}

// Événements
const emit = defineEmits(['navigate-to', 'open-settings'])

// Fonction pour sélectionner une option de création de document
const selectDocumentOption = (option) => {
  console.log('Option de création sélectionnée:', option)
  closeCreateDocumentModal()
  
  switch (option) {
    case 'immediate':
      // Créer un document immédiatement
      console.log('Création immédiate de document')
      // Rediriger vers la page de préparation de document
      emit('navigate-to', 'document-preparation')
      break
    case 'template':
      // Créer à partir d'un modèle
      console.log('Création à partir d\'un modèle')
      // TODO: Implémenter la logique de sélection de modèle
      break
  }
}

// Actions sur les documents
const viewDocument = (document) => {
  console.log('Voir le document:', document)
  // Logique pour voir le document
}

const editDocument = (document) => {
  console.log('Éditer le document:', document)
  // Logique pour éditer le document
}

const assignDocument = (document) => {
  console.log('Assigner le document:', document)
  // Logique pour assigner le document
}

const deleteDocument = (document) => {
  console.log('Supprimer le document:', document)
  // Logique pour supprimer le document
}

// Actions de gestion
const manageMembers = () => {
  console.log('Gérer les membres')
  // Logique pour gérer les membres
}

const viewReports = () => {
  console.log('Voir les rapports')
  // Logique pour voir les rapports
}

const openSettings = () => {
  console.log('Ouvrir les paramètres')
  // Émettre un événement pour ouvrir les paramètres
  emit('open-settings')
}

// Gestion des onglets de gestion documentaire
const setActiveDocumentTab = (tab) => {
  activeDocumentTab.value = tab
  console.log('Onglet actif changé:', tab)
  
  // Charger les documents préparés quand on clique sur l'onglet correspondant
  if (tab === 'prepared-immediate') {
    fetchPreparedDocuments()
  }
}

// Navigation vers la préparation de document
const navigateToDocumentPreparation = () => {
  console.log('Navigation vers la préparation de document')
  emit('navigate-to', 'document-preparation')
}

// Récupérer les documents préparés depuis l'API
const fetchPreparedDocuments = async () => {
  isLoadingDocuments.value = true
  documentsError.value = null
  
  try {
    // Récupérer le token CSRF depuis les cookies
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    };
    
    const csrfToken = getCookie('csrftoken');
    
    // Construire l'URL avec l'ID de l'organisation
    const organizationId = userOrganization.value?.organization?.id
    if (!organizationId) {
      throw new Error('Organisation non trouvée')
    }
    
    const url = `http://127.0.0.1:8000/api/signatures/document-preparation/?organization_id=${organizationId}`
    
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
    })
    
    if (!response.ok) {
      throw new Error(`Erreur ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    
    if (data.success) {
      preparedDocuments.value = data.preparations || []
      filteredDocuments.value = data.preparations || []
      console.log('Documents préparés récupérés:', preparedDocuments.value)
    } else {
      throw new Error(data.error || 'Erreur lors de la récupération des documents')
    }
    
  } catch (error) {
    console.error('Erreur lors de la récupération des documents préparés:', error)
    documentsError.value = error.message
  } finally {
    isLoadingDocuments.value = false
  }
}

// Fonctions de recherche
const searchDocuments = () => {
  if (!searchQuery.value.trim()) {
    filteredDocuments.value = preparedDocuments.value
    return
  }
  
  const query = searchQuery.value.toLowerCase().trim()
  filteredDocuments.value = preparedDocuments.value.filter(doc => 
    (doc.document_title && doc.document_title.toLowerCase().includes(query)) ||
    (doc.original_filename && doc.original_filename.toLowerCase().includes(query)) ||
    (doc.document_description && doc.document_description.toLowerCase().includes(query)) ||
    (doc.organization_name && doc.organization_name.toLowerCase().includes(query))
  )
}

// Effacer la recherche
const clearSearch = () => {
  searchQuery.value = ''
  filteredDocuments.value = preparedDocuments.value
}


// Obtenir le texte du statut
const getStatusText = (status) => {
  const statusMap = {
    'prepared': 'Préparé',
    'pending_signature': 'En attente de signature',
    'in_progress': 'En cours',
    'completed': 'Terminé',
    'rejected': 'Rejeté',
    'cancelled': 'Annulé'
  }
  return statusMap[status] || status
}

// Obtenir la classe CSS du statut
const getStatusClass = (status) => {
  const classMap = {
    'prepared': 'status-prepared',
    'pending_signature': 'status-pending',
    'in_progress': 'status-progress',
    'completed': 'status-completed',
    'rejected': 'status-rejected',
    'cancelled': 'status-cancelled'
  }
  return classMap[status] || 'status-unknown'
}

// Créer un document
const createDocument = async () => {
  isCreatingDocument.value = true
  try {
    console.log('Création du document:', newDocument.value)
    // Ici on peut faire un appel API pour créer le document
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulation
    
    // Ajouter le nouveau document à la liste
    const document = {
      name: newDocument.value.name,
      date: new Date().toLocaleDateString('fr-FR'),
      status: 'draft',
      statusText: 'Brouillon',
      type: newDocument.value.type,
      assignedTo: organizationMembers.value.find(m => m.id == newDocument.value.assignedTo)?.name || 'Non assigné'
    }
    
    documentsToManage.value.unshift(document)
    allDocuments.value.unshift(document)
    
    closeCreateDocumentModal()
    console.log('✅ Document créé avec succès')
  } catch (error) {
    console.error('❌ Erreur lors de la création du document:', error)
  } finally {
    isCreatingDocument.value = false
  }
}

// Fonction pour écouter l'événement de sélection d'organisation
const handleOrganizationSelected = (event) => {
  console.log('🎯 handleOrganizationSelected appelé dans OrganizationSecretaryPage')
  console.log('📦 Event detail:', event.detail)
  
  const { organization, role } = event.detail
  console.log('🏢 Organisation sélectionnée pour secrétaire:', organization.name, 'Rôle:', role)
  
  selectedOrganization.value = organization
  userOrganization.value = {
    organization: organization,
    role: role
  }
  
  console.log('📝 userOrganization mis à jour:', userOrganization.value)
  console.log('📝 Nom de l\'organisation:', userOrganization.value?.organization?.name)
  
  // Nettoyer le localStorage après utilisation
  localStorage.removeItem('selectedOrganization')
  
  // Charger les statistiques avec la nouvelle organisation
  loadSecretaryStats()
}

// Charger les données de l'organisation
const loadOrganizationData = async () => {
  try {
    // Vérifier d'abord le localStorage pour une organisation sélectionnée
    const storedOrganization = localStorage.getItem('selectedOrganization')
    if (storedOrganization) {
      const organization = JSON.parse(storedOrganization)
      console.log('🏢 Organisation trouvée dans localStorage:', organization.name)
      userOrganization.value = {
        organization: organization,
        role: organization.role || 'secretaire'
      }
      selectedOrganization.value = organization
      return
    }
    
    // Si une organisation est déjà sélectionnée en mémoire, l'utiliser
    if (selectedOrganization.value) {
      console.log('🏢 Organisation sélectionnée en mémoire:', selectedOrganization.value.name)
      userOrganization.value = {
        organization: selectedOrganization.value,
        role: selectedOrganization.value.role || 'secretaire'
      }
      return
    }
    
    // Sinon, essayer de charger depuis l'API (organisation par défaut)
    console.log('🔄 Chargement de l\'organisation par défaut depuis l\'API')
    const response = await fetch('http://127.0.0.1:8000/api/organizations/my-organization/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.organization) {
        userOrganization.value = data.organization
        console.log('✅ Organisation par défaut chargée:', data.organization.name)
      }
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement de l\'organisation:', error)
  }
}

// Charger les statistiques du secrétaire
const loadSecretaryStats = async () => {
  try {
    // Ici on peut faire un appel API pour récupérer les vraies statistiques
    // Pour l'instant, on utilise des données simulées
    secretaryStats.value = {
      totalDocuments: allDocuments.value.length,
      signedDocuments: allDocuments.value.filter(doc => doc.status === 'signed').length,
      pendingDocuments: allDocuments.value.filter(doc => doc.status === 'pending').length,
      organizationMembers: organizationMembers.value.length
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des statistiques:', error)
  }
}

// Initialisation
onMounted(async () => {
  console.log('🔧 OrganisationSecretaryPage montée')
  
  // Écouter l'événement de sélection d'organisation
  window.addEventListener('organizationSelected', handleOrganizationSelected)
  console.log('👂 Event listener organizationSelected ajouté')
  
  // Écouter les clics pour fermer le tooltip
  document.addEventListener('click', handleDocumentClick)
  
  // Écouter la touche Échap pour fermer le tooltip
  document.addEventListener('keydown', handleKeyDown)
  
  await loadOrganizationData()
  console.log('📊 userOrganization après loadOrganizationData:', userOrganization.value)
  console.log('📊 organizationName computed:', organizationName.value)
  
  await loadSecretaryStats()
})

// Nettoyage
onUnmounted(() => {
  window.removeEventListener('organizationSelected', handleOrganizationSelected)
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleKeyDown)
  // S'assurer que le défilement est restauré si le composant est détruit
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Variables CSS intégrées */
:root {
  --primary-blue: #0066cc;
  --primary-blue-dark: #0056b3;
  --text-dark: #2c3e50;
  --dark-gray: #6c757d;
  --light-gray: #f8f9fa;
  --success: #28a745;
  --warning: #ffc107;
  --danger: #dc3545;
}

/* STYLES GÉNÉRAUX */
.organization-secretary-page {
  min-height: 100vh;
  position: relative;
}

/* BOUTON DE FERMETURE */
.close-organization-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #666;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.close-organization-btn:hover {
  background: rgba(255, 255, 255, 1);
  color: #333;
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.close-organization-btn:active {
  transform: scale(0.95);
}

/* BARRE DE RECHERCHE */
.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-container {
  flex: 1;
  max-width: 500px;
  min-width: 300px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.5rem 0.5rem 2.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: var(--text-dark);
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 
    0 0 0 3px rgba(0, 102, 204, 0.1),
    0 4px 16px rgba(0, 102, 204, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.search-input::placeholder {
  color: var(--dark-gray);
  opacity: 0.7;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  color: var(--primary-blue);
  font-size: 1rem;
  z-index: 2;
}

.clear-search-btn {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-search-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

/* Responsive pour mobile */
@media (max-width: 768px) {
  .close-organization-btn {
    position: fixed;
    top: 70px;
    right: 20px;
    width: 40px;
    height: 40px;
    font-size: 18px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    color: #666;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .close-organization-btn:hover {
    background: rgba(255, 255, 255, 1);
    color: #333;
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  }
}

/* CODES COULEURS POUR LES RÔLES */
.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-badge.admin {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.role-badge.secretaire {
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
  border: 1px solid rgba(0, 123, 255, 0.2);
}

.role-badge.chef,
.role-badge.manager,
.role-badge[class*="chef+"] {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.role-badge.member {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

/* HEADER */
.organization-header {
  padding: 2rem 0;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  gap: 3rem;
}

.header-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-title {
  font-family: 'Raleway', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.sections-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.sections-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.5;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
  font-family: 'Raleway', sans-serif;
}

.section-subtitle {
  font-size: 1.2rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.header-image {
  flex-shrink: 0;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
  position: relative;
  width: 400px;
  height: 300px;
}

.organization-illustration {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.organization-illustration:hover {
  transform: translateY(-4px);
  filter: drop-shadow(0 8px 20px rgba(0, 102, 204, 0.15));
}

/* Bulles décoratives */
.bubble {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 102, 204, 0.1);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 90px;
  height: 90px;
  top: -5%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 110px;
  height: 110px;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.4s forwards, float 6s ease-in-out infinite 1.4s;
}

.bubble-3 {
  width: 70px;
  height: 70px;
  bottom: 5%;
  right: 20%;
  animation: fadeInScale 1s ease-out 1.6s forwards, float 6s ease-in-out infinite 1.6s;
}

.bubble-4 {
  width: 80px;
  height: 80px;
  top: 40%;
  left: 10%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

/* BOUTONS PRINCIPAUX */
.create-doc-btn {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  font-size: 1rem;
}

.create-doc-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

.manage-docs-btn {
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  background: transparent;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  font-weight: 500;
  border-radius: 8px;
  font-size: 0.875rem;
}

.manage-docs-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

/* STATISTIQUES */
.docs-stats-section {
  margin-bottom: 4rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.08);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.stat-card:nth-child(1) { animation-delay: 0.9s; }
.stat-card:nth-child(2) { animation-delay: 1s; }
.stat-card:nth-child(3) { animation-delay: 1.1s; }
.stat-card:nth-child(4) { animation-delay: 1.2s; }

.stat-icon {
  width: 50px;
  height: 50px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.25rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--dark-gray);
  margin: 0;
}

/* SECTIONS DES DOCUMENTS */
.documents-sections {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.sections-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.sections-title {
  font-family: 'Raleway', sans-serif;
  font-weight: 800;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.5s forwards;
}

.sections-subtitle {
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.6s forwards;
}

.documents-section-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  height: 100%;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.05);
}

.documents-section-card:nth-child(1) { animation-delay: 1.3s; }
.documents-section-card:nth-child(2) { animation-delay: 1.4s; }

.documents-section-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 8px 16px rgba(0, 102, 204, 0.08);
}

.section-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.section-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.section-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.section-card-subtitle {
  color: var(--dark-gray);
  margin: 0;
  font-size: 0.9rem;
}

/* LISTE DES DOCUMENTS */
.documents-list {
  margin-bottom: 1.5rem;
}

.document-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  background: rgba(248, 249, 250, 0.5);
}

.document-item:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.document-icon {
  width: 40px;
  height: 40px;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.2rem;
  color: #dc3545;
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.document-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-size: 0.85rem;
  color: var(--dark-gray);
  flex-wrap: wrap;
}

.document-date {
  color: var(--dark-gray);
}

.document-status {
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.document-status.signed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.document-status.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.document-status.draft {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
}

.document-assigned {
  font-size: 0.8rem;
  color: var(--primary-blue);
  font-weight: 500;
}

.document-actions {
  display: flex;
  gap: 0.5rem;
}

.document-actions .btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 0.8rem;
}

/* ACTIONS RAPIDES */
.documents-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item-doc {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.action-item-doc:nth-child(1) { animation-delay: 1.5s; }
.action-item-doc:nth-child(2) { animation-delay: 1.6s; }
.action-item-doc:nth-child(3) { animation-delay: 1.7s; }
.action-item-doc:nth-child(4) { animation-delay: 1.8s; }

.action-card-doc {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-card-doc:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.action-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.1rem;
  color: var(--primary-blue);
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.action-description {
  font-size: 0.85rem;
  color: var(--dark-gray);
  margin: 0;
}

.action-arrow {
  color: var(--primary-blue);
  opacity: 0.6;
  transition: all 0.3s ease;
}

.action-card-doc:hover .action-arrow {
  opacity: 1;
  transform: translateX(3px);
}

/* BOUTONS */
.btn-primary-blue {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  color: white;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary-blue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* MODALE DE CRÉATION */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(1px);
  animation: fadeInOverlay 0.3s ease-out;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  z-index: 10000;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--dark-gray);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  transform: scale(1.1);
}

/* FORMULAIRES */
.form-label {
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border: 2px solid rgba(0, 102, 204, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 0.2rem rgba(0, 102, 204, 0.25);
}

/* VUE COMPLÈTE DES DOCUMENTS */
.all-documents-view {
  animation: fadeInUp 0.5s ease-out;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.documents-table-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.05);
  overflow: hidden;
}

.documents-table {
  width: 100%;
}

.table-header {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 123, 255, 0.08) 100%);
  border-bottom: 2px solid rgba(0, 102, 204, 0.1);
}

.table-row {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  transition: all 0.3s ease;
}

.header-row {
  font-weight: 600;
  color: var(--text-dark);
  font-family: 'Raleway', sans-serif;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-align: center;
}

.document-row {
  border-bottom: 1px solid rgba(0, 102, 204, 0.05);
  cursor: pointer;
}

.document-row:hover {
  background: rgba(0, 102, 204, 0.02);
  transform: translateX(5px);
}

.document-row:last-child {
  border-bottom: none;
}

.table-cell {
  flex: 1;
  padding: 0 0.5rem;
}

.document-cell {
  flex: 2;
}

.document-info-full {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.document-icon-full {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 8px;
  font-size: 1.2rem;
  color: #dc3545;
}

.document-details-full {
  flex: 1;
}

.document-name-full {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.document-type {
  font-size: 0.75rem;
  color: #6c757d;
  background: rgba(0, 102, 204, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.signed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.status-badge.draft {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
}

.document-actions-full {
  display: flex;
  gap: 0.5rem;
}

.document-actions-full .btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 0.8rem;
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

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modalSlideUp {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.8) rotateX(-10deg);
  }
  50% {
    opacity: 0.8;
    transform: translateY(-5px) scale(1.05) rotateX(2deg);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1) rotateX(0deg);
  }
}

/* MODALE CONTEXTUELLE DE CRÉATION DE DOCUMENT */
.signature-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(1px);
  animation: fadeInOverlay 0.3s ease-out;
}

.signature-modal {
  position: fixed;
  width: 320px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  z-index: 10000;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
}

.signature-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  background: rgba(0, 102, 204, 0.02);
  border-radius: 16px 16px 0 0;
}

.signature-modal-header h5 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.signature-modal-header h5 i {
  color: var(--primary-blue);
  font-size: 1rem;
}

.close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6c757d;
}

.close-btn:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  transform: scale(1.1);
}

.signature-modal-content {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.signature-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: rgba(248, 249, 250, 0.5);
  border: 1px solid rgba(0, 102, 204, 0.05);
  opacity: 0;
  animation: fadeInOption 0.4s ease-out forwards;
}

.signature-option:nth-child(1) { animation-delay: 0.1s; }
.signature-option:nth-child(2) { animation-delay: 0.2s; }

.signature-option:hover {
  background: rgba(0, 102, 204, 0.08);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(3px) scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
}

.option-icon {
  width: 36px;
  height: 36px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 0.9rem;
  flex-shrink: 0;
}

.option-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.option-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-dark);
  line-height: 1.2;
}

.option-desc {
  font-size: 0.75rem;
  color: #6c757d;
  line-height: 1.3;
}

@keyframes fadeInOption {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }
  
  .header-image {
    width: 320px;
    height: 240px;
  }
  
  .header-title {
    font-size: 2.5rem;
  }
  
  .sections-title {
    font-size: 2.5rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .create-doc-btn, .manage-docs-btn {
    width: 100%;
  }
  
  .documents-sections {
    padding: 0 1rem;
  }
  
  .table-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .table-cell {
    width: 100%;
    padding: 0;
  }
  
  .document-actions-full {
    justify-content: flex-start;
  }
  
  .header-row {
    display: none;
  }
  
  .document-row {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(0, 102, 204, 0.08);
    background: rgba(255, 255, 255, 0.5);
    margin: 0.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 102, 204, 0.05);
  }
  
  .document-row:hover {
    background: rgba(255, 255, 255, 0.8);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
  }
  
  .document-info-full {
    margin-bottom: 0.75rem;
  }
  
  .document-name-full {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .document-type {
    font-size: 0.8rem;
    padding: 0.3rem 0.8rem;
  }
  
  .modal-content {
    margin: 1rem;
    padding: 1.5rem;
  }
}

/* ===== STYLES POUR LE SYSTÈME D'ONGLETS ===== */
/* ONGLETS */
.tabs-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(0, 102, 204, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(0, 102, 204, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

.tabs-header {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
}

.tab-button {
  flex: 1;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.tab-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--primary-blue);
}

.tab-button.active {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border-bottom: 2px solid var(--primary-blue);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-blue);
}

.tab-content {
  padding: 2rem;
  min-height: 400px;
}

.tab-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.tab-placeholder i {
  opacity: 0.8;
  transition: all 0.3s ease;
}

.tab-placeholder:hover i {
  opacity: 1;
  transform: scale(1.1);
}

.tab-placeholder h4 {
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
}

.tab-placeholder p {
  max-width: 400px;
  line-height: 1.6;
}

.tab-placeholder .btn {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.tab-placeholder .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

/* ===== STYLES POUR LES CARTES DE DOCUMENTS ===== */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.document-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.08);
  position: relative;
  overflow: hidden;
}

.document-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 10px 25px rgba(0, 102, 204, 0.08),
    0 5px 15px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
}

/* HEADER DE LA CARTE DE DOCUMENT */
.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.document-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--dark-gray);
  margin: 0;
  flex: 1;
}

.document-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.1) 0%, rgba(220, 53, 69, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #dc3545;
  flex-shrink: 0;
}

.document-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
  font-family: 'Raleway', sans-serif;
  line-height: 1.3;
}

.organization-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 102, 204, 0.15) 100%);
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--primary-blue);
  text-align: center;
  flex-shrink: 0;
}

.document-status-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Utiliser exactement la même classe que les organisations pour le badge de statut */
.approval-status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.approval-status-badge.prepared {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.approval-status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.approval-status-badge.signed {
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
  border: 1px solid rgba(0, 123, 255, 0.2);
}

.approval-status-badge.completed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.status-badge.status-pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.status-badge.status-progress {
  background: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
  border: 1px solid rgba(23, 162, 184, 0.2);
}

.status-badge.status-completed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.status-badge.status-rejected {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.status-badge.status-cancelled {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  border: 1px solid rgba(108, 117, 125, 0.2);
}

.document-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 0.6rem;
  transition: all 0.3s ease;
}

.document-status.status-prepared {
  color: #007bff;
}

.document-status.status-pending {
  color: #ffc107;
}

.document-status.status-progress {
  color: #17a2b8;
}

.document-status.status-completed {
  color: #28a745;
}

.document-status.status-rejected {
  color: #dc3545;
}

.document-status.status-cancelled {
  color: #6c757d;
}

/* CONTENU DE LA CARTE DE DOCUMENT */
.document-description {
  color: var(--dark-gray);
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* HIÉRARCHIE DE SIGNATURE */
.signature-hierarchy {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.03);
  border-radius: 8px;
}

.hierarchy-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
}

.signature-steps {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.signature-step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.signature-step.completed {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.signature-step.current {
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.signature-step.pending {
  background: rgba(108, 117, 125, 0.05);
  border: 1px solid rgba(108, 117, 125, 0.1);
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.signature-step.completed .step-indicator {
  color: #28a745;
  background: rgba(40, 167, 69, 0.1);
}

.signature-step.current .step-indicator {
  color: #ffc107;
  background: rgba(255, 193, 7, 0.1);
}

.signature-step.pending .step-indicator {
  color: #6c757d;
  background: rgba(108, 117, 125, 0.1);
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.step-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-dark);
}

.step-person {
  font-size: 0.75rem;
  color: var(--dark-gray);
}

.document-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--dark-gray);
}

.meta-item i {
  width: 16px;
  text-align: center;
  color: var(--primary-blue);
}

/* FOOTER DE LA CARTE DE DOCUMENT */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.document-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-step {
  font-size: 0.8rem;
  color: var(--dark-gray);
  font-weight: 500;
  padding: 0.25rem 0.75rem;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 15px;
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.document-actions {
  display: flex;
  gap: 0.5rem;
}

.document-actions .btn {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.document-actions .btn:hover {
  transform: translateY(-1px);
}

.document-actions .btn-outline-info {
  border-color: #17a2b8;
  color: #17a2b8;
}

.document-actions .btn-outline-info:hover {
  background-color: #17a2b8;
  color: white;
}

/* Responsive pour les onglets */
@media (max-width: 768px) {
  .search-container {
    max-width: none;
    min-width: auto;
    flex: 1;
  }
  
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .tab-content {
    padding: 1.5rem 1rem;
    min-height: 300px;
  }
  
  .tab-placeholder {
    padding: 2rem 1rem;
  }
  
  .tab-placeholder h4 {
    font-size: 1.25rem;
  }
  
  .tab-placeholder p {
    font-size: 0.9rem;
  }
  
  .documents-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .document-card {
    padding: 1rem;
  }
  
  .card-header {
    flex-direction: row;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .document-name {
    font-size: 1rem;
  }
  
  .document-header-content {
    gap: 0.25rem;
  }
  
  .organization-badge {
    align-self: flex-start;
  }
  
  .signature-hierarchy {
    padding: 0.75rem;
  }
  
  .hierarchy-title {
    font-size: 0.85rem;
  }
  
  .signature-step {
    padding: 0.375rem;
    gap: 0.5rem;
  }
  
  .step-indicator {
    width: 20px;
    height: 20px;
    font-size: 0.7rem;
  }
  
  .step-title {
    font-size: 0.75rem;
  }
  
  .step-person {
    font-size: 0.7rem;
  }
}

/* TOOLTIP DE PRÉVISUALISATION DES DOCUMENTS */
.document-preview-tooltip {
  position: absolute;
  z-index: 1000;
  animation: tooltipFadeIn 0.3s ease-out;
}

/* Transform selon la direction */
.document-preview-tooltip[class*="arrow-top"],
.document-preview-tooltip[class*="arrow-bottom"] {
  transform: translateX(-50%);
}

.document-preview-tooltip[class*="arrow-left"],
.document-preview-tooltip[class*="arrow-right"] {
  transform: translateY(-50%);
}

.tooltip-arrow {
  position: absolute;
  width: 0;
  height: 0;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers le haut (bulle en bas) */
.arrow-top {
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid rgba(255, 255, 255, 0.95);
  filter: drop-shadow(0 -2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers le bas (bulle en haut) */
.arrow-bottom {
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid rgba(255, 255, 255, 0.95);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers la gauche (bulle à droite) */
.arrow-left {
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid rgba(255, 255, 255, 0.95);
  filter: drop-shadow(-2px 0 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers la droite (bulle à gauche) */
.arrow-right {
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-left: 8px solid rgba(255, 255, 255, 0.95);
  filter: drop-shadow(2px 0 4px rgba(0, 0, 0, 0.1));
}

.tooltip-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(0, 102, 204, 0.2);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  overflow: hidden;
  width: 550px;
  max-height: 520px;
  display: flex;
  flex-direction: column;
}

.tooltip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 123, 255, 0.08) 100%);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.tooltip-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0;
  display: flex;
  align-items: center;
  flex: 1;
}

.tooltip-close {
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tooltip-close:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.tooltip-body {
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.preview-container {
  flex: 1;
  border-radius: 0;
  overflow: hidden;
  background: #f8f9fa;
  border: none;
  display: flex;
  flex-direction: column;
  max-height: 450px;
}

.pdf-preview-content {
  flex: 1;
  display: flex;
  align-items: stretch;
  justify-content: center;
  min-height: 400px;
  position: relative;
}

/* Styles exactement comme dans DocumentPreparationPage */
.pdf-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: stretch;
  background: white;
  border-radius: 0;
  box-shadow: none;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-height: 400px;
  max-height: 450px;
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
  max-width: 400px;
  margin: 0 auto;
}

.fallback-content i {
  font-size: 3rem;
  color: var(--primary-blue);
  margin-bottom: 1rem;
}

.fallback-content h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.fallback-description {
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fallback-subtitle {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  font-size: 0.85rem;
  line-height: 1.4;
}

.fallback-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--primary-blue);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.download-btn:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-1px);
}


.pdf-loading-state,
.pdf-error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  height: 100%;
}

.pdf-loading-state i,
.pdf-error-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.pdf-loading-state p,
.pdf-error-state p {
  font-size: 1rem;
  color: var(--dark-gray);
  margin-bottom: 1rem;
}


@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-5px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Animation d'entrée contextuelle selon la direction */
.document-preview-tooltip[class*="arrow-left"] {
  animation: tooltipSlideInRight 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-right"] {
  animation: tooltipSlideInLeft 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-top"] {
  animation: tooltipSlideInUp 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-bottom"] {
  animation: tooltipSlideInDown 0.3s ease-out;
}

@keyframes tooltipSlideInRight {
  from {
    opacity: 0;
    transform: translateX(20px) translateY(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0) translateY(-50%);
  }
}

@keyframes tooltipSlideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px) translateY(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0) translateY(-50%);
  }
}

@keyframes tooltipSlideInUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

@keyframes tooltipSlideInDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Responsive pour le tooltip */
@media (max-width: 768px) {
  .tooltip-content {
    width: 95vw;
    max-width: 500px;
    max-height: 80vh;
  }
  
  .pdf-preview-content {
    min-height: 250px;
  }
  
  .pdf-iframe {
    min-height: 250px;
    max-height: 300px;
  }
  
  .pdf-fallback {
    padding: 2rem;
  }
  
  .fallback-content {
    padding: 1rem;
  }
  
  .tooltip-header {
    padding: 0.75rem 1rem;
  }
  
  .tooltip-body {
    padding: 0;
  }
  
  .tooltip-title {
    font-size: 0.9rem;
  }
}
</style>
