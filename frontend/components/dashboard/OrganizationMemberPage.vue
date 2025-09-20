<template>
  <div class="organization-member-page">
    <!-- Bouton de fermeture -->
    <button class="close-organization-btn" @click="closeOrganizationDashboard" title="Fermer et retourner à la sélection d'organisation">
      <i class="bi bi-x"></i>
    </button>
    
    <!-- Header avec titre de la section -->
    <div class="organization-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Espace Membre de l'</span>
            <span class="text-primary-blue">organisation </span>
            <span class="text-primary-blue" v-if="userOrganization && userOrganization.organization"> {{ userOrganization.organization.name }}</span>
          </h1>
          <p class="section-subtitle" v-if="userOrganization && userOrganization.organization">
            Bienvenue dans l'organisation {{ userOrganization.organization.name }}. Gérez vos documents et signatures.
          </p>
          <p class="section-subtitle" v-else>
            Vous êtes membre d'une organisation. Accédez à vos documents et signatures.
          </p>
          <div class="header-actions">
            <button class="btn btn-primary-custom sign-now-btn" @click="toggleSignatureModal" ref="signBtn">
              <i class="bi bi-pen me-2"></i>
              Signer un document
            </button>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Organisation Membre" class="organization-illustration">
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
              <h4 class="stat-number">{{ memberStats.totalDocuments || 0 }}</h4>
              <p class="stat-label">Mes documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ memberStats.signedDocuments || 0 }}</h4>
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
              <h4 class="stat-number">{{ memberStats.pendingDocuments || 0 }}</h4>
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
              <span class="text-dark">Mes</span> 
              <span class="text-primary-blue"> Documents</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Gérez vos documents personnels et suivez vos signatures.
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
                <p class="section-card-subtitle">Vos derniers documents</p>
              </div>
            </div>
            
            <div class="documents-list">
              <!-- Document 1 -->
              <div class="document-item" v-for="(document, index) in recentDocuments" :key="index">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h5 class="document-name">{{ document.name }}</h5>
                  <p class="document-details">
                    <span class="document-date">{{ document.date }}</span>
                    <span class="document-status" :class="document.status">{{ document.statusText }}</span>
                  </p>
                </div>
                <div class="document-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewDocument(document)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="section-footer">
              <button class="btn btn-primary-blue btn-sm" @click="toggleAllDocuments">
                Voir tous mes documents
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
              <!-- Action 1 - Signer un document -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="toggleSignatureModal">
                  <div class="action-icon">
                    <i class="bi bi-pen"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Signer un document</h5>
                    <p class="action-description">Signez un document existant</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Télécharger un document -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="downloadDocument">
                  <div class="action-icon">
                    <i class="bi bi-download"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Télécharger</h5>
                    <p class="action-description">Téléchargez vos documents</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Historique des signatures -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="viewSignatureHistory">
                  <div class="action-icon">
                    <i class="bi bi-clock-history"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Historique</h5>
                    <p class="action-description">Consultez vos signatures</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Profil -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="openProfile">
                  <div class="action-icon">
                    <i class="bi bi-person"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Mon Profil</h5>
                    <p class="action-description">Gérez vos informations</p>
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

    <!-- Vue complète des documents -->
    <div v-else class="all-documents-view">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">Tous mes documents</h3>
            <button class="btn btn-outline-primary" @click="toggleAllDocuments">
              <i class="bi bi-arrow-left me-2"></i>
              Retour aux sections
            </button>
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
              <div class="table-cell">{{ document.date }}</div>
              <div class="table-cell">
                <span class="status-badge" :class="document.status">{{ document.statusText }}</span>
              </div>
              <div class="table-cell">
                <div class="document-actions-full">
                  <button class="btn btn-sm btn-outline-primary" @click.stop="viewDocument(document)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-success" @click.stop="downloadDocument(document)" title="Télécharger">
                    <i class="bi bi-download"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale de signature -->
    <div v-if="showSignatureModal" class="modal-overlay" @click="closeSignatureModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Choisir le type de signature</h5>
          <button class="btn-close" @click="closeSignatureModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="signature-options">
            <div class="signature-option" @click="selectSignatureType('upload')">
              <div class="option-icon">
                <i class="bi bi-upload"></i>
              </div>
              <div class="option-content">
                <h6 class="option-title">Télécharger un document</h6>
                <p class="option-description">Signez un document existant</p>
              </div>
            </div>
            <div class="signature-option" @click="selectSignatureType('create')">
              <div class="option-icon">
                <i class="bi bi-file-earmark-plus"></i>
              </div>
              <div class="option-content">
                <h6 class="option-title">Créer un document</h6>
                <p class="option-description">Créez un nouveau document à signer</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Store d'authentification
const authStore = useAuthStore()

// État des données
const userOrganization = ref(null)
const showAllDocuments = ref(false)
const showSignatureModal = ref(false)

// Statistiques du membre
const memberStats = ref({
  totalDocuments: 0,
  signedDocuments: 0,
  pendingDocuments: 0
})

// Documents récents
const recentDocuments = ref([
  {
    name: 'Contrat de service 2024',
    date: '15 Jan 2024',
    status: 'signed',
    statusText: 'Signé',
    type: 'PDF'
  },
  {
    name: 'Accord de confidentialité',
    date: '12 Jan 2024',
    status: 'signed',
    statusText: 'Signé',
    type: 'PDF'
  },
  {
    name: 'Facture janvier 2024',
    date: '10 Jan 2024',
    status: 'pending',
    statusText: 'En attente',
    type: 'PDF'
  }
])

// Tous les documents
const allDocuments = ref([
  ...recentDocuments.value,
  {
    name: 'Rapport mensuel',
    date: '08 Jan 2024',
    status: 'signed',
    statusText: 'Signé',
    type: 'PDF'
  },
  {
    name: 'Contrat de maintenance',
    date: '05 Jan 2024',
    status: 'pending',
    statusText: 'En attente',
    type: 'PDF'
  }
])

// Fonctions de navigation
const closeOrganizationDashboard = () => {
  // Émettre un événement pour retourner à la page de sélection d'organisation
  window.dispatchEvent(new CustomEvent('navigateToOrganizationSelection'))
}

const toggleAllDocuments = () => {
  showAllDocuments.value = !showAllDocuments.value
}

const toggleSignatureModal = () => {
  showSignatureModal.value = !showSignatureModal.value
}

const closeSignatureModal = () => {
  showSignatureModal.value = false
}

const selectSignatureType = (type) => {
  console.log('Type de signature sélectionné:', type)
  closeSignatureModal()
  // Ici on peut rediriger vers la page de signature appropriée
}

// Actions sur les documents
const viewDocument = (document) => {
  console.log('Voir le document:', document)
  // Logique pour voir le document
}

const downloadDocument = (document = null) => {
  console.log('Télécharger le document:', document)
  // Logique pour télécharger le document
}

const viewSignatureHistory = () => {
  console.log('Voir l\'historique des signatures')
  // Logique pour voir l'historique
}

const openProfile = () => {
  console.log('Ouvrir le profil')
  // Émettre un événement pour ouvrir le profil
  emit('open-profile')
}

// Charger les données de l'organisation
const loadOrganizationData = async () => {
  try {
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
        console.log('✅ Organisation chargée:', data.organization.name)
      }
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement de l\'organisation:', error)
  }
}

// Charger les statistiques du membre
const loadMemberStats = async () => {
  try {
    // Ici on peut faire un appel API pour récupérer les vraies statistiques
    // Pour l'instant, on utilise des données simulées
    memberStats.value = {
      totalDocuments: recentDocuments.value.length,
      signedDocuments: recentDocuments.value.filter(doc => doc.status === 'signed').length,
      pendingDocuments: recentDocuments.value.filter(doc => doc.status === 'pending').length
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des statistiques:', error)
  }
}

// Initialisation
onMounted(async () => {
  await loadOrganizationData()
  await loadMemberStats()
})

// Émettre les événements
const emit = defineEmits(['open-profile'])
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
.organization-member-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem 0;
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
  margin-bottom: 3rem;
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
  flex-wrap: wrap;
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
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 60px;
  height: 60px;
  top: -5%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 40px;
  height: 40px;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.4s forwards, float 6s ease-in-out infinite 1.4s;
}

.bubble-3 {
  width: 80px;
  height: 80px;
  bottom: 5%;
  right: 20%;
  animation: fadeInScale 1s ease-out 1.6s forwards, float 6s ease-in-out infinite 1.6s;
}

.bubble-4 {
  width: 50px;
  height: 50px;
  top: 40%;
  left: 10%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

/* BOUTON PRINCIPAL */
.sign-now-btn {
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

.sign-now-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

/* STATISTIQUES */
.docs-stats-section {
  margin-bottom: 4rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.1);
  border: 1px solid rgba(0, 102, 204, 0.08);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.stat-card:nth-child(1) { animation-delay: 0.9s; }
.stat-card:nth-child(2) { animation-delay: 1s; }
.stat-card:nth-child(3) { animation-delay: 1.1s; }

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
  color: var(--primary-blue);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  font-family: 'Raleway', sans-serif;
}

.stat-label {
  color: var(--dark-gray);
  font-weight: 500;
  margin: 0;
  font-size: 1rem;
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

.documents-section-card:nth-child(1) { animation-delay: 1.2s; }
.documents-section-card:nth-child(2) { animation-delay: 1.3s; }

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

.action-item-doc:nth-child(1) { animation-delay: 1.4s; }
.action-item-doc:nth-child(2) { animation-delay: 1.5s; }
.action-item-doc:nth-child(3) { animation-delay: 1.6s; }
.action-item-doc:nth-child(4) { animation-delay: 1.7s; }

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

/* MODALE DE SIGNATURE */
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
  max-width: 500px;
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

.signature-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.signature-option {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
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
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.2rem;
  color: var(--primary-blue);
}

.option-content {
  flex: 1;
}

.option-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.option-description {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin: 0;
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

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }
  
  .header-image {
    width: 300px;
    height: 200px;
  }
  
  .section-title {
    font-size: 2rem;
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
  
  .signature-option {
    padding: 1rem;
  }
  
  .option-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
