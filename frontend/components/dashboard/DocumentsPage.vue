<template>
  <div class="documents-page">
    <!-- Page de signature immédiate -->
    <SignImmediatelyPage 
      v-if="showSignaturePage" 
      @go-back="backFromSignature"
    />
    
    <!-- Éditeur de documents -->
    <DocumentEditor 
      v-else-if="showEditor" 
      @back="closeEditor"
      @save="saveDocument"
      @share="shareDocument"
    />
    
    <!-- Contenu principal (masqué quand l'éditeur ou la signature est ouvert) -->
    <div v-else>
      <!-- Header avec titre de la section -->
      <div class="documents-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Espace de Gestion et Signature</span>
            <span class="text-primary-blue"> Électronique de vos documents</span>
          </h1>
          <p class="section-subtitle">Simplifiez vos processus de signature avec notre plateforme sécurisée et intuitive</p>
                      <div class="header-actions">
              <button class="btn btn-primary-custom sign-now-btn" @click="toggleSignatureModal" ref="signBtn">
                <i class="bi bi-pen me-2"></i>
                Signer maintenant
              </button>
            </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/My_documents.svg" alt="Mes Documents" class="documents-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques des documents -->
    <div class="docs-stats-section">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">24</h4>
              <p class="stat-label">Total documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">18</h4>
              <p class="stat-label">Signés</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">6</h4>
              <p class="stat-label">En attente</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sections des documents en deux colonnes -->
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
              Accédez rapidement à vos documents par catégorie et gérez-les efficacement.
            </p>
          </div>
        </div>
      </div>

      <div class="row align-items-center">
        <!-- Colonne gauche - Mes Documents Récents -->
        <div class="col-lg-6 mb-4">
          <div class="documents-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-file-earmark-text text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Documents Récents</h3>
                <p class="section-card-subtitle">Vos derniers documents signés</p>
              </div>
            </div>
            
            <div class="documents-list">
              <!-- Document 1 -->
              <div class="document-item">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h5 class="document-name">Contrat de service 2024</h5>
                  <p class="document-details">
                    <span class="document-date">15 Jan 2024</span>
                    <span class="document-status signed">Signé</span>
                  </p>
                </div>
                <div class="document-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="openEditor()" title="Éditer">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                </div>
              </div>

              <!-- Document 2 -->
              <div class="document-item">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h5 class="document-name">Accord de confidentialité</h5>
                  <p class="document-details">
                    <span class="document-date">12 Jan 2024</span>
                    <span class="document-status signed">Signé</span>
                  </p>
                </div>
                <div class="document-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="openEditor()" title="Éditer">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                </div>
              </div>

              <!-- Document 3 -->
              <div class="document-item">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h5 class="document-name">Facture janvier 2024</h5>
                  <p class="document-details">
                    <span class="document-date">10 Jan 2024</span>
                    <span class="document-status pending">En attente</span>
                  </p>
                </div>
                <div class="document-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="openEditor()" title="Éditer">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="section-footer">
              <button class="btn btn-primary-blue btn-sm" @click="toggleAllDocuments">
                Voir tous les documents
                <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Colonne droite - Actions sur les Documents -->
        <div class="col-lg-6 mb-4">
          <div class="documents-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-plus-circle text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Actions Rapides</h3>
                <p class="section-card-subtitle">Créez et gérez vos documents</p>
              </div>
            </div>
            
            <div class="documents-actions">
              <!-- Action 1 - Nouveau document -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="openEditor()">
                  <div class="action-icon-doc">
                    <i class="bi bi-file-earmark-plus text-primary-blue"></i>
                  </div>
                  <div class="action-content-doc">
                    <h5 class="action-title">Nouveau Document</h5>
                    <p class="action-description">Créer un nouveau document à signer</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Éditer -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="openEditor()">
                  <div class="action-icon-doc">
                    <i class="bi bi-pencil-square text-primary-blue"></i>
                  </div>
                  <div class="action-content-doc">
                    <h5 class="action-title">Éditer</h5>
                    <p class="action-description">Modifier vos documents existants</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Modèles -->
              <div class="action-item-doc">
                <div class="action-card-doc">
                  <div class="action-icon-doc">
                    <i class="bi bi-file-earmark-text text-primary-blue"></i>
                  </div>
                  <div class="action-content-doc">
                    <h5 class="action-title">Modèles</h5>
                    <p class="action-description">Utiliser un modèle prédéfini</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Organiser -->
              <div class="action-item-doc">
                <div class="action-card-doc">
                  <div class="action-icon-doc">
                    <i class="bi bi-folder2-open text-primary-blue"></i>
                  </div>
                  <div class="action-content-doc">
                    <h5 class="action-title">Organiser</h5>
                    <p class="action-description">Créer des dossiers et catégories</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vue de tous les documents -->
    <div v-if="showAllDocuments" class="all-documents-view">
      <!-- Header de la vue complète -->
      <div class="all-documents-header">
        <div class="row mb-4">
          <div class="col-12">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <h2 class="display-6 fw-bold mb-2 text-dark">
                  <span class="text-dark">Mes</span>
                  <span class="text-primary-blue"> Documents</span>
                </h2>
                <p class="lead mb-0 text-muted">
                  Tous vos documents signés et en attente de signature
                </p>
              </div>
              <button class="btn btn-outline-primary" @click="backToMainView">
                <i class="bi bi-arrow-left me-2"></i>
                Retour
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Liste complète des documents -->
      <div class="all-documents-list">
        <div class="row">
          <div class="col-12">
            <div class="documents-table-container">
              <div class="documents-table">
                <div class="table-header">
                  <div class="table-row header-row">
                    <div class="table-cell">Document</div>
                    <div class="table-cell">Date</div>
                    <div class="table-cell">Statut</div>
                    <div class="table-cell">Taille</div>
                    <div class="table-cell">Actions</div>
                  </div>
                </div>
                <div class="table-body">
                  <div 
                    v-for="document in paginatedDocuments" 
                    :key="document.id" 
                    class="table-row document-row"
                  >
                    <div class="table-cell document-cell">
                      <div class="document-info-full">
                        <div class="document-icon-full">
                          <i class="bi bi-file-earmark-pdf text-danger"></i>
                        </div>
                        <div class="document-details-full">
                          <h6 class="document-name-full">{{ document.name }}</h6>
                          <span class="document-type">PDF</span>
                        </div>
                      </div>
                    </div>
                    <div class="table-cell" data-label="Date">{{ document.date }}</div>
                    <div class="table-cell" data-label="Statut">
                      <span 
                        class="status-badge" 
                        :class="document.status === 'signed' ? 'signed' : 'pending'"
                      >
                        {{ document.status === 'signed' ? 'Signé' : 'En attente' }}
                      </span>
                    </div>
                    <div class="table-cell" data-label="Taille">{{ document.size }}</div>
                    <div class="table-cell" data-label="Actions">
                      <div class="document-actions-full">
                        <button class="btn btn-sm btn-outline-primary me-2" @click="openEditor(document)" title="Éditer">
                          <i class="bi bi-pencil-square"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info me-2" title="Voir">
                          <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary me-2" title="Télécharger">
                          <i class="bi bi-download"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" title="Supprimer">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Contrôles de pagination -->
        <div class="pagination-container">
          <div class="pagination-info">
            <span class="pagination-text">
              Page {{ currentPage }} sur {{ totalPages }} 
              ({{ documents.length }} documents au total)
            </span>
          </div>
          
          <div class="pagination-controls">
            <button 
              class="btn btn-outline-primary pagination-btn" 
              :disabled="currentPage === 1"
              @click="prevPage"
            >
              <i class="bi bi-chevron-left"></i>
              Précédent
            </button>
            
            <div class="pagination-numbers">
              <button 
                v-for="page in totalPages" 
                :key="page"
                class="btn pagination-number"
                :class="page === currentPage ? 'btn-primary' : 'btn-outline-primary'"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
            </div>
            
            <button 
              class="btn btn-outline-primary pagination-btn" 
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              Suivant
              <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>
      </div>
    
    <!-- Modale contextuelle de signature -->
    <div v-if="isSignatureModalOpen" class="signature-modal-overlay" @click="closeSignatureModal">
      <div class="signature-modal" @click.stop ref="signatureModal">
        <div class="signature-modal-header">
          <h5>
            <i class="bi bi-pen"></i>
            Options de Signature
          </h5>
          <button class="close-btn" @click="closeSignatureModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="signature-modal-content">
          <div class="signature-option" @click="selectSignatureOption('immediate')">
            <div class="option-icon">
              <i class="bi bi-lightning-fill"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Signature Immédiate</span>
              <span class="option-desc">Signez directement votre document actuel</span>
            </div>
          </div>
          
          <div class="signature-option" @click="selectSignatureOption('template')">
            <div class="option-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Signer à partir d'un modèle</span>
              <span class="option-desc">Choisissez parmi nos modèles de signature</span>
            </div>
          </div>
          
          <div class="signature-option" @click="selectSignatureOption('upload')">
            <div class="option-icon">
              <i class="bi bi-cloud-upload"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Importer un document</span>
              <span class="option-desc">Uploadez un document à signer</span>
            </div>
          </div>
          
          <div class="signature-option" @click="selectSignatureOption('batch')">
            <div class="option-icon">
              <i class="bi bi-stack"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Signature en lot</span>
              <span class="option-desc">Signez plusieurs documents à la fois</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Popup d'erreur de certificat -->
    <div v-if="isCertificateErrorModalOpen" class="signature-modal-overlay" @click="closeCertificateErrorModal">
      <div class="signature-modal certificate-error-modal" @click.stop ref="certificateErrorModal">
        <div class="signature-modal-header">
          <h5>
            <i class="bi bi-exclamation-triangle-fill text-warning"></i>
            Certificat non valide
          </h5>
          <button class="close-btn" @click="closeCertificateErrorModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="signature-modal-content">
          <div class="certificate-error-content">
            <div class="error-header">
              <div class="error-icon">
                <i class="bi bi-shield-x text-danger"></i>
              </div>
              <div class="error-text">
                <h6 class="error-title">Certificat invalide</h6>
                <p class="error-message">
                  Votre certificat n'est pas valide ou a expiré. Importez un certificat valide pour signer.
                </p>
              </div>
            </div>
            <div class="error-actions">
              <button class="btn btn-primary btn-sm" @click="goToCertificateImport">
                <i class="bi bi-shield-fill-check me-2"></i>
                Importer
              </button>
              <button class="btn btn-outline-secondary btn-sm" @click="closeCertificateErrorModal">
                Annuler
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script setup>
import { ref, computed, onMounted, nextTick, defineEmits } from 'vue'
import DocumentEditor from './DocumentEditor.vue'
import SignImmediatelyPage from './SignImmediatelyPage.vue'
import { CertificateService } from '../../services/CertificateService'

// Émissions
const emit = defineEmits(['navigate-to-signature', 'open-profile-modal'])

// État pour afficher la liste complète des documents
const showAllDocuments = ref(false)

// État pour l'éditeur
const showEditor = ref(false)

// État pour la page de signature
const showSignaturePage = ref(false)
const currentDocument = ref(null)

// Service de certificat
const certificateService = new CertificateService()

// État pour la modale de signature
const isSignatureModalOpen = ref(false)
const signBtn = ref(null)
const signatureModal = ref(null)

// État pour la popup d'erreur de certificat
const isCertificateErrorModalOpen = ref(false)
const certificateErrorModal = ref(null)

// Pagination
const currentPage = ref(1)
const documentsPerPage = 7

// Données des documents (simulées)
const documents = ref([
  {
    id: 1,
    name: 'Contrat de service 2024',
    type: 'pdf',
    date: '15 Jan 2024',
    status: 'signed',
    size: '2.3 MB'
  },
  {
    id: 2,
    name: 'Accord de confidentialité',
    type: 'pdf',
    date: '12 Jan 2024',
    status: 'signed',
    size: '1.8 MB'
  },
  {
    id: 3,
    name: 'Facture janvier 2024',
    type: 'pdf',
    date: '10 Jan 2024',
    status: 'pending',
    size: '0.9 MB'
  },
  {
    id: 4,
    name: 'Devis projet web',
    type: 'pdf',
    date: '08 Jan 2024',
    status: 'signed',
    size: '1.2 MB'
  },
  {
    id: 5,
    name: 'Convention de stage',
    type: 'pdf',
    date: '05 Jan 2024',
    status: 'signed',
    size: '3.1 MB'
  },
  {
    id: 6,
    name: 'Bon de commande #2024-001',
    type: 'pdf',
    date: '03 Jan 2024',
    status: 'pending',
    size: '1.5 MB'
  },
  {
    id: 7,
    name: 'Contrat de location',
    type: 'pdf',
    date: '01 Jan 2024',
    status: 'signed',
    size: '2.7 MB'
  },
  {
    id: 8,
    name: 'Devis rénovation',
    type: 'pdf',
    date: '28 Dec 2023',
    status: 'signed',
    size: '1.9 MB'
  }
])

// Fonction pour afficher tous les documents
const toggleAllDocuments = () => {
  showAllDocuments.value = !showAllDocuments.value
}

// Fonction pour revenir à la vue principale
const backToMainView = () => {
  showAllDocuments.value = false
  currentPage.value = 1 // Reset à la première page
}

// Fonctions de l'éditeur
const openEditor = (document = null) => {
  currentDocument.value = document
  showEditor.value = true
}

const closeEditor = () => {
  showEditor.value = false
  currentDocument.value = null
}

const saveDocument = (data) => {
  console.log('Document sauvegardé:', data)
  // Ici on pourrait envoyer les données au backend
}

const shareDocument = (data) => {
  console.log('Document partagé:', data)
  // Ici on pourrait implémenter le partage
}

// Computed properties pour la pagination
const totalPages = computed(() => Math.ceil(documents.value.length / documentsPerPage))

const paginatedDocuments = computed(() => {
  const startIndex = (currentPage.value - 1) * documentsPerPage
  const endIndex = startIndex + documentsPerPage
  return documents.value.slice(startIndex, endIndex)
})

// Fonctions de pagination
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// Fonctions pour la modale de signature
const toggleSignatureModal = () => {
  // Vérifier la validité du certificat avant d'ouvrir la modale
  certificateService.initialize()
  
  if (!certificateService.canUseCertificate()) {
    // Afficher directement la popup d'erreur de certificat avec positionnement contextuel
    openCertificateErrorModal()
    return
  }
  
  isSignatureModalOpen.value = !isSignatureModalOpen.value
  
  if (isSignatureModalOpen.value) {
    nextTick(() => {
      if (signBtn.value && signatureModal.value && window.innerWidth > 768) {
        const buttonRect = signBtn.value.getBoundingClientRect()
        const modal = signatureModal.value
        
        // Dimensions de la modale
        const modalWidth = 320
        const modalHeight = 280
        
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
        
        // GARANTIR que la modale reste entièrement dans les limites de l'écran
        // Vérification horizontale
        if (leftPosition < margin) {
          leftPosition = margin
        } else if (leftPosition + modalWidth > window.innerWidth - margin) {
          leftPosition = window.innerWidth - modalWidth - margin
        }
        
        // Vérification verticale
        if (topPosition < margin) {
          topPosition = margin
        } else if (topPosition + modalHeight > window.innerHeight - margin) {
          topPosition = window.innerHeight - modalHeight - margin
        }
        
        // Vérification finale - si la modale est encore trop grande pour l'écran
        if (modalWidth > window.innerWidth - 2 * margin) {
          // Modale trop large, centrer et réduire la largeur
          leftPosition = margin
          modal.style.width = (window.innerWidth - 2 * margin) + 'px'
        } else {
          modal.style.width = modalWidth + 'px'
        }
        
        if (modalHeight > window.innerHeight - 2 * margin) {
          // Modale trop haute, centrer et réduire la hauteur
          topPosition = margin
          modal.style.height = (window.innerHeight - 2 * margin) + 'px'
          modal.style.overflowY = 'auto'
        } else {
          modal.style.height = 'auto'
          modal.style.overflowY = 'visible'
        }
        
        modal.style.left = leftPosition + 'px'
        modal.style.top = topPosition + 'px'
      }
    })
    
    // Bloquer le scroll en arrière-plan
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeSignatureModal = () => {
  isSignatureModalOpen.value = false
  document.body.style.overflow = ''
}

const closeCertificateErrorModal = () => {
  isCertificateErrorModalOpen.value = false
  document.body.style.overflow = ''
}

// Fonction pour ouvrir la popup d'erreur de certificat avec positionnement contextuel
const openCertificateErrorModal = () => {
  isCertificateErrorModalOpen.value = true
  
  nextTick(() => {
    if (signBtn.value && certificateErrorModal.value && window.innerWidth > 768) {
      const buttonRect = signBtn.value.getBoundingClientRect()
      const modal = certificateErrorModal.value
      
      // Dimensions de la modale (même que la modale de signature)
      const modalWidth = 320
      const modalHeight = 280
      
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
      
      // GARANTIR que la modale reste entièrement dans les limites de l'écran
      // Vérification horizontale
      if (leftPosition < margin) {
        leftPosition = margin
      } else if (leftPosition + modalWidth > window.innerWidth - margin) {
        leftPosition = window.innerWidth - modalWidth - margin
      }
      
      // Vérification verticale
      if (topPosition < margin) {
        topPosition = margin
      } else if (topPosition + modalHeight > window.innerHeight - margin) {
        topPosition = window.innerHeight - modalHeight - margin
      }
      
      // Vérification finale - si la modale est encore trop grande pour l'écran
      if (modalWidth > window.innerWidth - 2 * margin) {
        // Modale trop large, centrer et réduire la largeur
        leftPosition = margin
        modal.style.width = (window.innerWidth - 2 * margin) + 'px'
      } else {
        modal.style.width = modalWidth + 'px'
      }
      
      if (modalHeight > window.innerHeight - 2 * margin) {
        // Modale trop haute, centrer et réduire la hauteur
        topPosition = margin
        modal.style.height = (window.innerHeight - 2 * margin) + 'px'
        modal.style.overflowY = 'auto'
      } else {
        modal.style.height = 'auto'
        modal.style.overflowY = 'visible'
      }
      
      modal.style.left = leftPosition + 'px'
      modal.style.top = topPosition + 'px'
    }
  })
  
  // Bloquer le scroll en arrière-plan
  document.body.style.overflow = 'hidden'
}

const goToCertificateImport = () => {
  closeCertificateErrorModal()
  // Émettre un événement pour ouvrir la modale de profil sur l'onglet certificat
  emit('open-profile-modal', 'certificate')
}

const selectSignatureOption = (option) => {
  console.log('Option sélectionnée:', option)
  closeSignatureModal()
  
  switch (option) {
    case 'immediate':
      // Afficher la page de signature immédiate
      showSignaturePage.value = true
      break
    case 'template':
      // Rediriger vers les modèles
      console.log('Ouverture des modèles de signature')
      break
    case 'upload':
      // Ouvrir l'éditeur pour upload
      openEditor()
      break
    case 'batch':
      // Ouvrir l'interface de signature en lot
      console.log('Ouverture de la signature en lot')
      break
  }
}

// Fonction pour revenir de la page de signature
const backFromSignature = () => {
  showSignaturePage.value = false
}

onMounted(() => {
  // Ici on pourrait charger les vrais documents depuis l'API
  console.log('Documents page loaded')
})
</script>

<style scoped>
.documents-page {
  padding: 0;
  background: #f8f9fa;
  min-height: 100vh;
}

/* HEADER */
.documents-header {
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 2rem;
}

.header-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-image {
  flex-shrink: 0;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
}

.documents-illustration {
  width: 380px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.documents-illustration:hover {
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

.section-title {
  font-size: 3rem;
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

.header-actions {
  margin-top: 1.5rem;
}

.sign-now-btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

.sign-now-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

/* MODALE CONTEXTUELLE DE SIGNATURE */
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

/* Styles pour la popup d'erreur de certificat */
.certificate-error-modal {
  max-width: 320px;
  width: 320px;
  height: auto;
  min-height: 280px;
}

.certificate-error-content {
  padding: 0.75rem;
}

.error-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.error-icon {
  font-size: 2rem;
  color: #dc3545;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.error-text {
  flex: 1;
}

.error-title {
  color: var(--text-dark);
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  text-align: left;
}

.error-message {
  color: #6c757d;
  line-height: 1.4;
  font-size: 0.85rem;
  text-align: left;
  margin-bottom: 0;
}

.error-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.error-actions .btn {
  min-width: 120px;
  padding: 0.5rem 1rem;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.error-actions .btn-primary {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
}

.error-actions .btn-primary:hover {
  background: var(--primary-blue-dark);
  border-color: var(--primary-blue-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.error-actions .btn-outline-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
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
.signature-option:nth-child(3) { animation-delay: 0.3s; }
.signature-option:nth-child(4) { animation-delay: 0.4s; }

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

/* Animations */
@keyframes fadeInOverlay {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(1px);
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

@keyframes modalSlideUpMobile {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.7) rotateY(-15deg);
  }
  50% {
    opacity: 0.9;
    transform: translate(-50%, -50%) scale(1.1) rotateY(3deg);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotateY(0deg);
  }
}

@keyframes fadeInOption {
  from {
    opacity: 0;
    transform: translateX(-20px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

/* Responsive pour mobile */
@media (max-width: 768px) {
  .signature-modal {
    width: 90%;
    max-width: 350px;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    animation: modalSlideUpMobile 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    transform-origin: center center;
  }
  
  .signature-modal-content {
    padding: 1rem;
  }
  
  .signature-option {
    padding: 1rem;
  }
  
  .option-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .option-title {
    font-size: 0.9rem;
  }
  
  .option-desc {
    font-size: 0.8rem;
  }
}

/* SECTION STATISTIQUES */
.docs-stats-section {
  margin-bottom: 3rem;
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
  font-family: 'Raleway', sans-serif;
}

.stat-label {
  color: #6c757d;
  font-size: 0.875rem;
  margin-bottom: 0;
  font-weight: 500;
}

/* SECTIONS DES DOCUMENTS */
.documents-sections {
  margin-bottom: 3rem;
}

/* En-tête de section */
.sections-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.sections-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.5s forwards;
}

.sections-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.6s forwards;
}

.documents-section-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  height: 100%;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.documents-section-card:nth-child(1) { animation-delay: 1.2s; }
.documents-section-card:nth-child(2) { animation-delay: 1.3s; }

.documents-section-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 10px 25px rgba(0, 102, 204, 0.08),
    0 5px 15px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
}

.section-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 102, 204, 0.08);
}

.section-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  border: 1px solid rgba(0, 102, 204, 0.15);
}

.section-header-content {
  flex: 1;
}

.section-card-title {
  font-family: 'Raleway', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.section-card-subtitle {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
}

/* LISTE DES DOCUMENTS */
.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.document-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
}

.document-item:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.document-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
  font-size: 1.25rem;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.document-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0;
}

.document-date {
  font-size: 0.8rem;
  color: #6c757d;
}

.document-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
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

.document-actions {
  display: flex;
  gap: 0.5rem;
}

/* ACTIONS DES DOCUMENTS */
.documents-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-item-doc {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.action-item-doc:nth-child(1) { animation-delay: 1.4s; }
.action-item-doc:nth-child(2) { animation-delay: 1.5s; }
.action-item-doc:nth-child(3) { animation-delay: 1.6s; }
.action-item-doc:nth-child(4) { animation-delay: 1.7s; }

.action-card-doc {
  display: flex;
  align-items: center;
  gap: 1rem;
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

.action-icon-doc {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 10px;
  font-size: 1.2rem;
  border: 1px solid rgba(0, 102, 204, 0.15);
}

.action-content-doc {
  flex: 1;
}

.action-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.action-description {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 0;
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

/* FOOTER DE SECTION */
.section-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.08);
}

.btn-primary-blue {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  border: none;
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

/* RESPONSIVE */
@media (max-width: 768px) {
  .documents-header {
    padding: 1.5rem 0;
  }
  
  .header-container {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  
  .header-content {
    text-align: center;
  }
  
  .documents-illustration {
    width: 280px;
  }
  
  .section-title {
    font-size: 2.5rem;
  }
  
  .section-subtitle {
    font-size: 1.25rem;
  }
  
  .sections-title {
    font-size: 2rem;
  }
  
  .sections-subtitle {
    font-size: 1.1rem;
  }
  
  .documents-section-card {
    margin-bottom: 1.5rem;
  }
  
  .document-item {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .document-details {
    justify-content: center;
  }
}

/* VUE COMPLÈTE DES DOCUMENTS */
.all-documents-view {
  animation: fadeInUp 0.5s ease-out;
}

.all-documents-header {
  margin-bottom: 2rem;
}

/* TABLEAU DES DOCUMENTS */
.documents-table-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
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

.header-row .table-cell {
  text-align: center;
}

.header-row .table-cell:nth-child(2) {
  text-align: right;
}

.header-row .table-cell:nth-child(3) {
  text-align: center;
  padding-left: 5rem;
}

.header-row .table-cell:nth-child(4) {
  text-align: center;
  padding-right: 1rem;
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

/* RESPONSIVE */
@media (max-width: 768px) {
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
  
  /* Amélioration mobile pour la liste des documents */
  .documents-table-container {
    border-radius: 12px;
    margin: 0 0.5rem;
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
  
  .table-cell {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(0, 102, 204, 0.05);
  }
  
  .table-cell:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .table-cell:first-child {
    padding-top: 0;
  }
  
  .table-cell:not(.document-cell)::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--primary-blue);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-right: 1rem;
    min-width: 60px;
  }
  
  .document-actions-full {
    gap: 0.75rem;
  }
  
  .document-actions-full .btn {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }
  
  .status-badge {
    font-size: 0.8rem;
    padding: 0.4rem 1rem;
  }
}

/* PAGINATION */
.pagination-container {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
}

.pagination-info {
  text-align: center;
  margin-bottom: 1.5rem;
}

.pagination-text {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-numbers {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.pagination-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.pagination-number:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
}

.pagination-number.btn-primary {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  border: none;
  color: white;
}

.pagination-number.btn-primary:hover {
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

/* Responsive pagination */
@media (max-width: 768px) {
  .pagination-container {
    margin: 1rem 0.5rem;
    padding: 1rem;
  }
  
  .pagination-controls {
    flex-direction: column;
    gap: 1rem;
  }
  
  .pagination-numbers {
    order: -1;
  }
  
  .pagination-btn {
    width: 100%;
    justify-content: center;
  }
  
  .pagination-number {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.75rem;
  }
  
  .documents-actions {
    gap: 0.5rem;
  }
  
  .action-card-doc {
    padding: 0.75rem;
  }
  
  .all-documents-header .d-flex {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
