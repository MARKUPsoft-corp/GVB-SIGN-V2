<template>
  <div class="organizations-page">
    <!-- Header avec titre de la section -->
    <div class="organizations-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Gestion des</span>
            <span class="text-primary-blue"> Organisations</span>
          </h1>
          <p class="section-subtitle">Créez et gérez vos organisations pour collaborer efficacement</p>
          <div class="header-actions">
            <button class="btn btn-primary-custom create-org-btn" @click="toggleCreateModal" ref="createBtn">
              <i class="bi bi-building-add me-2"></i>
              Créer une organisation
            </button>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organizations.svg" alt="Organisations" class="organizations-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques des organisations -->
    <div class="orgs-stats-section">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-building"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ totalOrganizations }}</h4>
              <p class="stat-label">Total organisations</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ activeOrganizations }}</h4>
              <p class="stat-label">Actives</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ pendingOrganizations }}</h4>
              <p class="stat-label">En attente</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sections des organisations en deux colonnes -->
    <div v-if="!showAllOrganizations" class="organizations-sections">
      <!-- En-tête de section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Gestion</span> 
              <span class="text-primary-blue"> Organisationnelle</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Gérez vos organisations et collaborez avec votre équipe.
            </p>
          </div>
        </div>
      </div>

      <div class="row align-items-center">
        <!-- Colonne gauche - Mes Organisations Récentes -->
        <div class="col-lg-6 mb-4">
          <div class="organizations-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-building text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Organisations Récentes</h3>
                <p class="section-card-subtitle">Vos dernières organisations créées</p>
              </div>
            </div>
            
            <div class="organizations-list">
              <!-- Organisation 1 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-primary-blue"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">TechCorp Solutions</h5>
                  <p class="organization-details">
                    <span class="organization-date">15 Jan 2024</span>
                    <span class="organization-status active">Active</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(1)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>

              <!-- Organisation 2 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-warning"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">Startup Innovante</h5>
                  <p class="organization-details">
                    <span class="organization-date">12 Jan 2024</span>
                    <span class="organization-status pending">En attente</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(2)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>

              <!-- Organisation 3 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-success"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">Digital Agency</h5>
                  <p class="organization-details">
                    <span class="organization-date">10 Jan 2024</span>
                    <span class="organization-status active">Active</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(3)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="section-footer">
              <button class="btn btn-primary-blue btn-sm" @click="toggleAllOrganizations">
                Voir toutes les organisations
                <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Colonne droite - Actions sur les Organisations -->
        <div class="col-lg-6 mb-4">
          <div class="organizations-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-plus-circle text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Actions Rapides</h3>
                <p class="section-card-subtitle">Créez et gérez vos organisations</p>
              </div>
            </div>
            
            <div class="organizations-actions">
              <!-- Action 1 - Nouvelle organisation -->
              <div class="action-item-org">
                <div class="action-card-org" @click="toggleCreateModal()">
                  <div class="action-icon-org">
                    <i class="bi bi-building-add text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Nouvelle Organisation</h5>
                    <p class="action-description">Créer une nouvelle organisation</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Rejoindre -->
              <div class="action-item-org">
                <div class="action-card-org" @click="toggleJoinModal()">
                  <div class="action-icon-org">
                    <i class="bi bi-person-plus text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Rejoindre</h5>
                    <p class="action-description">Rejoindre une organisation existante</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Invitations -->
              <div class="action-item-org">
                <div class="action-card-org">
                  <div class="action-icon-org">
                    <i class="bi bi-envelope text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Invitations</h5>
                    <p class="action-description">Gérer vos invitations</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Paramètres -->
              <div class="action-item-org">
                <div class="action-card-org">
                  <div class="action-icon-org">
                    <i class="bi bi-gear text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Paramètres</h5>
                    <p class="action-description">Configurer vos organisations</p>
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

    <!-- Vue de toutes les organisations -->
    <div v-if="showAllOrganizations" class="all-organizations-view">
      <!-- Header de la vue complète -->
      <div class="all-organizations-header">
        <div class="row mb-4">
          <div class="col-12">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <h2 class="display-6 fw-bold mb-2 text-dark">
                  <span class="text-dark">Mes</span>
                  <span class="text-primary-blue"> Organisations</span>
                </h2>
                <p class="lead mb-0 text-muted">
                  Toutes vos organisations et invitations
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

      <!-- Liste complète des organisations -->
      <div class="all-organizations-list">
        <div class="row">
          <div class="col-12">
            <div class="organizations-table-container">
              <div class="organizations-table">
                <div class="table-header">
                  <div class="table-row">
                    <div class="table-cell">Organisation</div>
                    <div class="table-cell">Statut</div>
                    <div class="table-cell">Rôle</div>
                    <div class="table-cell">Date de création</div>
                    <div class="table-cell">Actions</div>
                  </div>
                </div>
                <div class="table-body">
                  <div v-for="org in organizations" :key="org.id" class="table-row">
                    <div class="table-cell">
                      <div class="organization-cell">
                        <div class="organization-icon">
                          <i class="bi bi-building"></i>
                        </div>
                        <div class="organization-details">
                          <h6 class="organization-name">{{ org.name }}</h6>
                          <p class="organization-description">{{ org.description }}</p>
                        </div>
                      </div>
                    </div>
                    <div class="table-cell">
                      <span :class="`status-badge ${org.status}`">
                        {{ getStatusText(org.status) }}
                      </span>
                    </div>
                    <div class="table-cell">
                      <span class="role-badge">{{ org.role }}</span>
                    </div>
                    <div class="table-cell">
                      <span class="date-text">{{ org.createdAt }}</span>
                    </div>
                    <div class="table-cell">
                      <div class="action-buttons">
                        <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(org.id)" title="Voir">
                          <i class="bi bi-eye"></i>
                        </button>
                        <button v-if="org.status === 'active'" class="btn btn-sm btn-outline-success" @click="manageOrganization(org.id)" title="Gérer">
                          <i class="bi bi-gear"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modale de création d'organisation -->
    <div v-if="isCreateModalOpen" class="organization-modal-overlay" @click="closeCreateModal">
      <div class="organization-modal" @click.stop ref="createModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-building-add"></i>
            Créer une Organisation
          </h5>
          <button class="close-btn" @click="closeCreateModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-modal-content">
          <form @submit.prevent="createOrganization">
            <div class="form-group">
              <label for="orgName">Nom de l'organisation</label>
              <input 
                type="text" 
                id="orgName" 
                v-model="newOrganization.name" 
                class="form-control" 
                placeholder="Ex: TechCorp Solutions"
                required
              >
            </div>
            <div class="form-group">
              <label for="orgDescription">Description</label>
              <textarea 
                id="orgDescription" 
                v-model="newOrganization.description" 
                class="form-control" 
                rows="3"
                placeholder="Décrivez votre organisation..."
              ></textarea>
            </div>
            <div class="form-group">
              <label for="orgType">Type d'organisation</label>
              <select id="orgType" v-model="newOrganization.type" class="form-control">
                <option value="company">Entreprise</option>
                <option value="association">Association</option>
                <option value="ngo">ONG</option>
                <option value="government">Gouvernement</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-outline-secondary" @click="closeCreateModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isCreating">
                <span v-if="isCreating" class="spinner-border spinner-border-sm me-2"></span>
                Créer l'organisation
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Modale de rejoindre une organisation -->
    <div v-if="isJoinModalOpen" class="organization-modal-overlay" @click="closeJoinModal">
      <div class="organization-modal" @click.stop ref="joinModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-person-plus"></i>
            Rejoindre une Organisation
          </h5>
          <button class="close-btn" @click="closeJoinModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-modal-content">
          <form @submit.prevent="joinOrganization">
            <div class="form-group">
              <label for="inviteCode">Code d'invitation</label>
              <input 
                type="text" 
                id="inviteCode" 
                v-model="inviteCode" 
                class="form-control" 
                placeholder="Entrez le code d'invitation"
                required
              >
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-outline-secondary" @click="closeJoinModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isJoining">
                <span v-if="isJoining" class="spinner-border spinner-border-sm me-2"></span>
                Rejoindre
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, defineEmits } from 'vue'

// Émissions
const emit = defineEmits(['navigate-to-organization', 'open-profile-modal'])

// État pour afficher la liste complète des organisations
const showAllOrganizations = ref(false)

// État pour les modales
const isCreateModalOpen = ref(false)
const isJoinModalOpen = ref(false)
const createBtn = ref(null)
const createModal = ref(null)
const joinModal = ref(null)

// État pour les formulaires
const isCreating = ref(false)
const isJoining = ref(false)

// Données des organisations (simulées)
const organizations = ref([
  {
    id: 1,
    name: 'TechCorp Solutions',
    description: 'Entreprise de solutions technologiques',
    type: 'company',
    status: 'active',
    role: 'Administrateur',
    createdAt: '15 Jan 2024'
  },
  {
    id: 2,
    name: 'Startup Innovante',
    description: 'Startup dans le domaine de l\'innovation',
    type: 'company',
    status: 'pending',
    role: 'Créateur',
    createdAt: '12 Jan 2024'
  },
  {
    id: 3,
    name: 'Digital Agency',
    description: 'Agence digitale spécialisée',
    type: 'company',
    status: 'active',
    role: 'Membre',
    createdAt: '10 Jan 2024'
  },
  {
    id: 4,
    name: 'Association Tech',
    description: 'Association des professionnels du tech',
    type: 'association',
    status: 'active',
    role: 'Modérateur',
    createdAt: '08 Jan 2024'
  },
  {
    id: 5,
    name: 'ONG Humanitaire',
    description: 'Organisation non gouvernementale',
    type: 'ngo',
    status: 'pending',
    role: 'Créateur',
    createdAt: '05 Jan 2024'
  }
])

// Nouvelle organisation
const newOrganization = ref({
  name: '',
  description: '',
  type: 'company'
})

// Code d'invitation
const inviteCode = ref('')

// Computed properties
const totalOrganizations = computed(() => organizations.value.length)
const activeOrganizations = computed(() => 
  organizations.value.filter(org => org.status === 'active').length
)
const pendingOrganizations = computed(() => 
  organizations.value.filter(org => org.status === 'pending').length
)

// Fonctions pour les modales
const toggleCreateModal = () => {
  isCreateModalOpen.value = !isCreateModalOpen.value
  if (isCreateModalOpen.value) {
    nextTick(() => {
      positionModal(createModal.value, createBtn.value)
    })
  }
}

const closeCreateModal = () => {
  isCreateModalOpen.value = false
  // Réinitialiser le formulaire
  newOrganization.value = {
    name: '',
    description: '',
    type: 'company'
  }
}

const toggleJoinModal = () => {
  isJoinModalOpen.value = !isJoinModalOpen.value
  if (isJoinModalOpen.value) {
    nextTick(() => {
      positionModal(joinModal.value, createBtn.value)
    })
  }
}

const closeJoinModal = () => {
  isJoinModalOpen.value = false
  inviteCode.value = ''
}

// Fonctions pour les organisations
const toggleAllOrganizations = () => {
  showAllOrganizations.value = true
}

const backToMainView = () => {
  showAllOrganizations.value = false
}

const viewOrganization = (orgId) => {
  console.log('Voir organisation:', orgId)
  // Émettre un événement pour naviguer vers l'organisation
  emit('navigate-to-organization', orgId)
}

const manageOrganization = (orgId) => {
  console.log('Gérer organisation:', orgId)
  // Émettre un événement pour gérer l'organisation
  emit('navigate-to-organization', orgId, 'manage')
}

const createOrganization = async () => {
  if (!newOrganization.value.name.trim()) {
    return
  }
  
  isCreating.value = true
  
  try {
    // Simuler la création d'organisation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newOrg = {
      id: organizations.value.length + 1,
      name: newOrganization.value.name,
      description: newOrganization.value.description,
      type: newOrganization.value.type,
      status: 'pending',
      role: 'Créateur',
      createdAt: new Date().toLocaleDateString('fr-FR', { 
        day: '2-digit', 
        month: 'short', 
        year: 'numeric' 
      })
    }
    
    organizations.value.unshift(newOrg)
    closeCreateModal()
    
    console.log('Organisation créée:', newOrg)
  } catch (error) {
    console.error('Erreur lors de la création:', error)
  } finally {
    isCreating.value = false
  }
}

const joinOrganization = async () => {
  if (!inviteCode.value.trim()) {
    return
  }
  
  isJoining.value = true
  
  try {
    // Simuler la jointure d'organisation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('Code d\'invitation:', inviteCode.value)
    closeJoinModal()
    
    // Ici on pourrait ajouter l'organisation à la liste
  } catch (error) {
    console.error('Erreur lors de la jointure:', error)
  } finally {
    isJoining.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'active': 'Active',
    'pending': 'En attente',
    'inactive': 'Inactive'
  }
  return statusMap[status] || status
}

// Fonction pour positionner les modales
const positionModal = (modal, button) => {
  if (!modal || !button) return
  
  const buttonRect = button.getBoundingClientRect()
  const modalWidth = 400
  const modalHeight = 500
  const margin = 20
  
  // Calculer l'espace disponible
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

onMounted(() => {
  // Ici on pourrait charger les vraies organisations depuis l'API
  console.log('Organizations page loaded')
})
</script>

<style scoped>
.organizations-page {
  padding: 0;
  background: #f8f9fa;
  min-height: 100vh;
}

/* HEADER */
.organizations-header {
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

.organizations-illustration {
  width: 380px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.organizations-illustration:hover {
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

/* Titres et sous-titres */
.section-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* Boutons */
.btn-primary-custom {
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0052a3 0%, #003366 100%);
}

.create-org-btn {
  font-size: 1.1rem;
  padding: 14px 28px;
}

/* STATISTIQUES */
.orgs-stats-section {
  padding: 2rem 0;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  opacity: 0;
  animation: slideInUp 0.8s ease-out forwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 102, 204, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #0066cc;
  margin: 0;
  line-height: 1;
}

.stat-label {
  color: #6c757d;
  font-size: 1rem;
  margin: 0.5rem 0 0 0;
  font-weight: 500;
}

/* SECTIONS */
.organizations-sections {
  padding: 2rem 0;
}

.sections-header {
  margin-bottom: 3rem;
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.4s forwards;
}

.sections-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.sections-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  line-height: 1.5;
}

/* CARTES DE SECTION */
.organizations-section-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  opacity: 0;
  animation: slideInUp 0.8s ease-out forwards;
}

.organizations-section-card:nth-child(1) { animation-delay: 0.5s; }
.organizations-section-card:nth-child(2) { animation-delay: 0.6s; }

.organizations-section-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15);
}

.section-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.3rem;
}

.section-header-content {
  flex: 1;
}

.section-card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.section-card-subtitle {
  color: #6c757d;
  margin: 0;
  font-size: 1rem;
}

/* LISTE DES ORGANISATIONS */
.organizations-list {
  margin-bottom: 2rem;
}

.organization-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.organization-item:hover {
  background: rgba(0, 102, 204, 0.05);
  transform: translateX(4px);
}

.organization-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(0, 102, 204, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0066cc;
  font-size: 1.2rem;
}

.organization-info {
  flex: 1;
}

.organization-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.organization-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-size: 0.9rem;
}

.organization-date {
  color: #6c757d;
}

.organization-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.organization-status.active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.organization-status.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.organization-actions {
  display: flex;
  gap: 0.5rem;
}

/* ACTIONS RAPIDES */
.organizations-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item-org {
  transition: all 0.3s ease;
}

.action-card-org {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card-org:hover {
  background: rgba(0, 102, 204, 0.1);
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
}

.action-icon-org {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.action-content-org {
  flex: 1;
}

.action-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.action-description {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

.action-arrow {
  color: #0066cc;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.action-card-org:hover .action-arrow {
  transform: translateX(4px);
}

/* FOOTER DE SECTION */
.section-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.btn-primary-blue {
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary-blue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* VUE COMPLÈTE */
.all-organizations-view {
  padding: 2rem 0;
}

.all-organizations-header {
  margin-bottom: 2rem;
}

.all-organizations-list {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.organizations-table-container {
  overflow-x: auto;
}

.organizations-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px 12px 0 0;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  align-items: center;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.table-body .table-row:hover {
  background: rgba(0, 102, 204, 0.05);
}

.table-cell {
  font-size: 0.9rem;
  color: #2c3e50;
}

.organization-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.organization-cell .organization-icon {
  width: 35px;
  height: 35px;
  font-size: 1rem;
}

.organization-cell .organization-name {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.organization-cell .organization-description {
  font-size: 0.85rem;
  color: #6c757d;
  margin: 0;
}

.status-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
}

.status-badge.active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.role-badge {
  background: rgba(0, 102, 204, 0.1);
  color: #0066cc;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.date-text {
  color: #6c757d;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* MODALES */
.organization-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.organization-modal {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: modalSlideIn 0.3s ease-out;
}

.organization-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.organization-modal-header h5 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #6c757d;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: #0066cc;
}

.organization-modal-content {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

/* ANIMATIONS */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
  }
  
  .organizations-illustration {
    width: 280px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .sections-title {
    font-size: 2rem;
  }
  
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .table-cell {
    text-align: left;
  }
  
  .organization-modal {
    width: 95%;
    margin: 1rem;
  }
}
</style>
