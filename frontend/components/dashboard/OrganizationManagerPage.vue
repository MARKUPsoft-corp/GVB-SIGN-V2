<template>
  <div class="organization-manager-page">
    <!-- Bouton de fermeture -->
    <button class="close-organization-btn" @click="closeOrganizationDashboard" title="Fermer et retourner à la sélection d'organisation">
      <i class="bi bi-x"></i>
    </button>
    
    <!-- Header avec titre de la section -->
    <div class="organization-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Espace Direction de l'</span>
            <span class="text-primary-blue">organisation </span>
            <span class="text-primary-blue" v-if="userOrganization && userOrganization.organization"> {{ userOrganization.organization.name }}</span>
          </h1>
          <p class="section-subtitle" v-if="userOrganization && userOrganization.organization">
            Supervisez et gérez l'organisation {{ userOrganization.organization.name }} avec des outils de direction avancés.
          </p>
          <p class="section-subtitle" v-else>
            Vous êtes directeur d'une organisation. Supervisez et gérez avec des outils avancés.
          </p>
          <div class="header-actions">
            <button class="btn btn-primary-custom analytics-btn" @click="toggleAnalyticsModal" ref="analyticsBtn">
              <i class="bi bi-graph-up me-2"></i>
              Tableau de bord
            </button>
            <button class="btn btn-outline-primary team-btn" @click="toggleTeamManagement">
              <i class="bi bi-people me-2"></i>
              Gérer l'équipe
            </button>
            <button class="btn btn-outline-secondary settings-btn" @click="openOrganizationSettings">
              <i class="bi bi-gear me-2"></i>
              Paramètres
            </button>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Organisation Direction" class="organization-illustration">
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
              <h4 class="stat-number">{{ managerStats.totalDocuments || 0 }}</h4>
              <p class="stat-label">Total documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.totalMembers || 0 }}</h4>
              <p class="stat-label">Membres actifs</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-graph-up"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.productivityScore || 0 }}%</h4>
              <p class="stat-label">Productivité</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.pendingTasks || 0 }}</h4>
              <p class="stat-label">Tâches en cours</p>
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
              <span class="text-dark">Direction</span> 
              <span class="text-primary-blue"> & Supervision</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Supervisez l'organisation, gérez les équipes et analysez les performances.
            </p>
          </div>
        </div>
      </div>

      <div class="row align-items-center">
        <!-- Colonne gauche - Vue d'ensemble -->
        <div class="col-lg-6 mb-4">
          <div class="documents-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-graph-up text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Vue d'ensemble</h3>
                <p class="section-card-subtitle">Analysez les performances de l'organisation</p>
              </div>
            </div>
            
            <div class="overview-list">
              <!-- Performance générale -->
              <div class="overview-item">
                <div class="overview-icon">
                  <i class="bi bi-speedometer2 text-success"></i>
                </div>
                <div class="overview-info">
                  <h5 class="overview-title">Performance générale</h5>
                  <p class="overview-details">
                    <span class="overview-value">{{ managerStats.overallPerformance || 0 }}%</span>
                    <span class="overview-trend positive">+5% ce mois</span>
                  </p>
                </div>
              </div>

              <!-- Documents en cours -->
              <div class="overview-item">
                <div class="overview-icon">
                  <i class="bi bi-file-earmark-check text-warning"></i>
                </div>
                <div class="overview-info">
                  <h5 class="overview-title">Documents en cours</h5>
                  <p class="overview-details">
                    <span class="overview-value">{{ managerStats.documentsInProgress || 0 }}</span>
                    <span class="overview-trend neutral">Stable</span>
                  </p>
                </div>
              </div>

              <!-- Équipe active -->
              <div class="overview-item">
                <div class="overview-icon">
                  <i class="bi bi-people text-info"></i>
                </div>
                <div class="overview-info">
                  <h5 class="overview-title">Équipe active</h5>
                  <p class="overview-details">
                    <span class="overview-value">{{ managerStats.activeTeamMembers || 0 }}/{{ managerStats.totalMembers || 0 }}</span>
                    <span class="overview-trend positive">Tous actifs</span>
                  </p>
                </div>
              </div>
            </div>

            <div class="section-footer">
              <button class="btn btn-primary-blue btn-sm" @click="toggleAllDocuments">
                Voir le tableau de bord complet
                <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Colonne droite - Actions de Direction -->
        <div class="col-lg-6 mb-4">
          <div class="documents-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-gear text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Actions de Direction</h3>
                <p class="section-card-subtitle">Gérez et supervisez l'organisation</p>
              </div>
            </div>
            
            <div class="documents-actions">
              <!-- Action 1 - Tableau de bord -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="toggleAnalyticsModal">
                  <div class="action-icon">
                    <i class="bi bi-graph-up"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Tableau de bord</h5>
                    <p class="action-description">Analyses et rapports avancés</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Gestion d'équipe -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="toggleTeamManagement">
                  <div class="action-icon">
                    <i class="bi bi-people"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Gestion d'équipe</h5>
                    <p class="action-description">Supervisez les membres</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Rapports -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="generateReports">
                  <div class="action-icon">
                    <i class="bi bi-file-earmark-bar-graph"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Rapports</h5>
                    <p class="action-description">Générez des rapports détaillés</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Paramètres avancés -->
              <div class="action-item-doc">
                <div class="action-card-doc" @click="openAdvancedSettings">
                  <div class="action-icon">
                    <i class="bi bi-gear"></i>
                  </div>
                  <div class="action-content">
                    <h5 class="action-title">Paramètres avancés</h5>
                    <p class="action-description">Configuration complète</p>
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

    <!-- Vue complète du tableau de bord -->
    <div v-else class="all-documents-view">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">Tableau de bord de direction</h3>
            <div class="d-flex gap-2">
              <button class="btn btn-primary" @click="toggleAnalyticsModal">
                <i class="bi bi-graph-up me-2"></i>
                Analyses avancées
              </button>
              <button class="btn btn-outline-primary" @click="toggleAllDocuments">
                <i class="bi bi-arrow-left me-2"></i>
                Retour aux sections
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tableau de bord complet -->
      <div class="dashboard-grid">
        <!-- Graphique de performance -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Performance de l'organisation</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="refreshPerformance">
                <i class="bi bi-arrow-clockwise"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="performance-chart">
              <div class="chart-placeholder">
                <i class="bi bi-graph-up fs-1 text-primary-blue"></i>
                <p class="text-muted">Graphique de performance</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Membres de l'équipe -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Membres de l'équipe</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="toggleTeamManagement">
                <i class="bi bi-people"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="team-members">
              <div class="team-member" v-for="member in teamMembers" :key="member.id">
                <div class="member-avatar">
                  <i class="bi bi-person-circle"></i>
                </div>
                <div class="member-info">
                  <h6 class="member-name">{{ member.name }}</h6>
                  <p class="member-role">{{ member.role }}</p>
                </div>
                <div class="member-status" :class="member.status">
                  <i class="bi bi-circle-fill"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Documents récents -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Documents récents</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="viewAllDocuments">
                <i class="bi bi-eye"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="recent-documents">
              <div class="document-item" v-for="(document, index) in recentDocuments" :key="index">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h6 class="document-name">{{ document.name }}</h6>
                  <p class="document-meta">{{ document.author }} • {{ document.date }}</p>
                </div>
                <div class="document-status" :class="document.status">
                  <span class="status-badge" :class="document.status">{{ document.statusText }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Activité récente -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Activité récente</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="viewActivityLog">
                <i class="bi bi-clock-history"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="activity-feed">
              <div class="activity-item" v-for="(activity, index) in recentActivity" :key="index">
                <div class="activity-icon" :class="activity.type">
                  <i :class="activity.icon"></i>
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.description }}</p>
                  <span class="activity-time">{{ activity.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale d'analyses avancées -->
    <div v-if="showAnalyticsModal" class="modal-overlay" @click="closeAnalyticsModal">
      <div class="modal-content analytics-modal" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Analyses avancées</h5>
          <button class="btn-close" @click="closeAnalyticsModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="analytics-tabs">
            <button class="tab-btn" :class="{ active: activeTab === 'performance' }" @click="activeTab = 'performance'">
              Performance
            </button>
            <button class="tab-btn" :class="{ active: activeTab === 'team' }" @click="activeTab = 'team'">
              Équipe
            </button>
            <button class="tab-btn" :class="{ active: activeTab === 'documents' }" @click="activeTab = 'documents'">
              Documents
            </button>
          </div>
          
          <div class="analytics-content">
            <div v-if="activeTab === 'performance'" class="analytics-panel">
              <h6>Analyse de performance</h6>
              <p class="text-muted">Graphiques et métriques de performance de l'organisation.</p>
            </div>
            <div v-if="activeTab === 'team'" class="analytics-panel">
              <h6>Analyse d'équipe</h6>
              <p class="text-muted">Statistiques et performances des membres de l'équipe.</p>
            </div>
            <div v-if="activeTab === 'documents'" class="analytics-panel">
              <h6>Analyse de documents</h6>
              <p class="text-muted">Métriques et tendances des documents de l'organisation.</p>
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
const showAnalyticsModal = ref(false)
const activeTab = ref('performance')

// Statistiques du manager
const managerStats = ref({
  totalDocuments: 0,
  totalMembers: 0,
  productivityScore: 0,
  pendingTasks: 0,
  overallPerformance: 0,
  documentsInProgress: 0,
  activeTeamMembers: 0
})

// Membres de l'équipe
const teamMembers = ref([
  { id: 1, name: 'Jean Dupont', role: 'Secrétaire', status: 'active' },
  { id: 2, name: 'Marie Martin', role: 'Membre', status: 'active' },
  { id: 3, name: 'Pierre Durand', role: 'Chef d\'équipe', status: 'active' },
  { id: 4, name: 'Sophie Bernard', role: 'Membre', status: 'inactive' }
])

// Documents récents
const recentDocuments = ref([
  {
    name: 'Rapport mensuel Q1',
    author: 'Jean Dupont',
    date: '15 Jan 2024',
    status: 'signed',
    statusText: 'Signé'
  },
  {
    name: 'Contrat de service',
    author: 'Marie Martin',
    date: '12 Jan 2024',
    status: 'pending',
    statusText: 'En attente'
  },
  {
    name: 'Accord de confidentialité',
    author: 'Pierre Durand',
    date: '10 Jan 2024',
    status: 'draft',
    statusText: 'Brouillon'
  }
])

// Activité récente
const recentActivity = ref([
  {
    type: 'success',
    icon: 'bi bi-check-circle',
    description: 'Document "Rapport mensuel" signé par Jean Dupont',
    time: 'Il y a 2 heures'
  },
  {
    type: 'info',
    icon: 'bi bi-person-plus',
    description: 'Nouveau membre ajouté à l\'équipe',
    time: 'Il y a 4 heures'
  },
  {
    type: 'warning',
    icon: 'bi bi-exclamation-triangle',
    description: 'Document "Contrat de service" en attente depuis 3 jours',
    time: 'Il y a 1 jour'
  },
  {
    type: 'primary',
    icon: 'bi bi-file-earmark-plus',
    description: 'Nouveau document créé par Marie Martin',
    time: 'Il y a 2 jours'
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

const toggleAnalyticsModal = () => {
  showAnalyticsModal.value = !showAnalyticsModal.value
}

const closeAnalyticsModal = () => {
  showAnalyticsModal.value = false
}

// Actions de direction
const toggleTeamManagement = () => {
  console.log('Gestion d\'équipe')
  // Logique pour gérer l'équipe
}

const generateReports = () => {
  console.log('Génération de rapports')
  // Logique pour générer des rapports
}

const openOrganizationSettings = () => {
  console.log('Paramètres de l\'organisation')
  // Émettre un événement pour ouvrir les paramètres
  emit('open-organization-settings')
}

const openAdvancedSettings = () => {
  console.log('Paramètres avancés')
  // Logique pour les paramètres avancés
}

// Actions du tableau de bord
const refreshPerformance = () => {
  console.log('Actualisation des performances')
  // Logique pour actualiser les performances
}

const viewAllDocuments = () => {
  console.log('Voir tous les documents')
  // Logique pour voir tous les documents
}

const viewActivityLog = () => {
  console.log('Voir le journal d\'activité')
  // Logique pour voir le journal d'activité
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

// Charger les statistiques du manager
const loadManagerStats = async () => {
  try {
    // Ici on peut faire un appel API pour récupérer les vraies statistiques
    // Pour l'instant, on utilise des données simulées
    managerStats.value = {
      totalDocuments: 45,
      totalMembers: teamMembers.value.length,
      productivityScore: 87,
      pendingTasks: 12,
      overallPerformance: 92,
      documentsInProgress: 8,
      activeTeamMembers: teamMembers.value.filter(m => m.status === 'active').length
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des statistiques:', error)
  }
}

// Initialisation
onMounted(async () => {
  await loadOrganizationData()
  await loadManagerStats()
})

// Émettre les événements
const emit = defineEmits(['open-organization-settings'])
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
  --info: #17a2b8;
}

/* STYLES GÉNÉRAUX */
.organization-manager-page {
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

/* BOUTONS PRINCIPAUX */
.analytics-btn {
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

.analytics-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

.team-btn, .settings-btn {
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  background: transparent;
  transition: all 0.3s ease;
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  font-size: 1rem;
}

.team-btn:hover, .settings-btn:hover {
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
.stat-card:nth-child(4) { animation-delay: 1.2s; }

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

/* VUE D'ENSEMBLE */
.overview-list {
  margin-bottom: 1.5rem;
}

.overview-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  background: rgba(248, 249, 250, 0.5);
}

.overview-item:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.overview-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.overview-info {
  flex: 1;
}

.overview-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.overview-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-size: 0.85rem;
  color: var(--dark-gray);
}

.overview-value {
  font-weight: 700;
  color: var(--primary-blue);
  font-size: 1.1rem;
}

.overview-trend {
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.overview-trend.positive {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.overview-trend.neutral {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
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

/* TABLEAU DE BORD */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.card-content {
  padding: 0.5rem 0;
}

/* PERFORMANCE CHART */
.performance-chart {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px;
}

.chart-placeholder {
  text-align: center;
  color: var(--dark-gray);
}

/* TEAM MEMBERS */
.team-members {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.team-member {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.team-member:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.member-avatar {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 1.5rem;
  color: var(--primary-blue);
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.member-role {
  font-size: 0.8rem;
  color: var(--dark-gray);
  margin: 0;
}

.member-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 0.6rem;
}

.member-status.active {
  color: var(--success);
}

.member-status.inactive {
  color: var(--dark-gray);
}

/* RECENT DOCUMENTS */
.recent-documents {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.document-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.document-item:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.document-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 1rem;
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.document-meta {
  font-size: 0.8rem;
  color: var(--dark-gray);
  margin: 0;
}

.document-status {
  display: flex;
  align-items: center;
}

.status-badge {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  text-transform: uppercase;
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

/* ACTIVITY FEED */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.activity-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 0.9rem;
  border-radius: 50%;
}

.activity-icon.success {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.activity-icon.info {
  background: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
}

.activity-icon.warning {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.activity-icon.primary {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 0.85rem;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.activity-time {
  font-size: 0.75rem;
  color: var(--dark-gray);
}

/* MODALE D'ANALYSES */
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

.analytics-modal {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 800px;
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

/* ONGLETS D'ANALYSES */
.analytics-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px 8px 0 0;
  font-weight: 600;
  color: var(--dark-gray);
  transition: all 0.3s ease;
  cursor: pointer;
}

.tab-btn:hover {
  background: rgba(0, 102, 204, 0.05);
  color: var(--primary-blue);
}

.tab-btn.active {
  background: var(--primary-blue);
  color: white;
}

.analytics-content {
  min-height: 300px;
}

.analytics-panel {
  padding: 1rem 0;
}

.analytics-panel h6 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
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
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .analytics-btn, .team-btn, .settings-btn {
    width: 100%;
  }
  
  .documents-sections {
    padding: 0 1rem;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .analytics-modal {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .analytics-tabs {
    flex-direction: column;
  }
  
  .tab-btn {
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }
}
</style>
