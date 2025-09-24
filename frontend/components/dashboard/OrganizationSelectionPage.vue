<template>
  <div class="organization-selection-page">
    <!-- Header avec titre de la section -->
    <div class="organization-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Sélectionnez votre</span>
            <span class="text-primary-blue"> organisation</span>
          </h1>
          <p class="section-subtitle">
            Choisissez l'organisation pour laquelle vous souhaitez accéder au tableau de bord.
          </p>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/dashboard.svg" alt="Sélection Organisation" class="dashboard-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques -->
    <div class="stats-section">
      <div class="row g-4">
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-building"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ userOrganizations.length }}</h4>
              <p class="stat-label">Organisations</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ totalMembers }}</h4>
              <p class="stat-label">Membres total</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ totalDocuments }}</h4>
              <p class="stat-label">Documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
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
      </div>
    </div>

    <!-- Section des organisations avec onglets -->
    <div class="organizations-section">
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Vos</span> 
              <span class="text-primary-blue"> Organisations</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Gérez vos organisations et découvrez de nouvelles opportunités.
            </p>
          </div>
        </div>
      </div>

      <!-- Onglets -->
      <div class="tabs-container">
        <div class="tabs-header">
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'my-organizations' }"
            @click="setActiveTab('my-organizations')"
          >
            <i class="bi bi-building me-2"></i>
            Mes Organisations
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'search' }"
            @click="setActiveTab('search')"
          >
            <i class="bi bi-search me-2"></i>
            Rechercher
          </button>
        </div>

        <!-- Contenu de l'onglet "Mes Organisations" -->
        <div v-if="activeTab === 'my-organizations'" class="tab-content">
          <!-- Grille des organisations de l'utilisateur -->
          <div class="organizations-grid" v-if="userOrganizations.length > 0">
            <div 
              class="organization-card" 
              v-for="(org, index) in userOrganizations" 
              :key="org.id"
              @click="selectOrganization(org)"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="card-header">
                <div class="organization-icon">
                  <i class="bi bi-building"></i>
                </div>
                <div class="organization-header-content">
                  <h3 class="organization-name">{{ org.name }}</h3>
                  <p class="organization-subtitle">{{ org.role || 'Membre' }}</p>
                </div>
                <div class="organization-status" :class="org.status">
                  <i class="bi bi-circle-fill"></i>
                </div>
              </div>
              
              <div class="card-content">
                <p class="organization-description">{{ org.description || 'Aucune description' }}</p>
                
                <div class="organization-meta">
                  <div class="meta-item" @mouseenter="showOrganizationMembers(org, $event)" @mouseleave="closeMembersModal" @click="showOrganizationMembers(org, $event)" style="cursor: pointer;" title="Voir les membres">
                    <i class="bi bi-people"></i>
                    <span>{{ org.member_count || 0 }} membres</span>
                  </div>
                  <div class="meta-item">
                    <i class="bi bi-file-earmark-text"></i>
                    <span>{{ org.documentCount || 0 }} documents</span>
                  </div>
                </div>
              </div>
              
              <div class="card-footer">
                <div class="user-role">
                  <span class="role-badge" :class="org.role">{{ getRoleDisplayName(org.role) }}</span>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click.stop="viewOrganizationDetails(org)" @mouseenter="showOrganizationInfo(org, $event)" @mouseleave="closeOrganizationInfo" title="Détails">
                    <i class="bi bi-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click.stop="leaveOrganization(org)" title="Quitter l'organisation">
                    <i class="bi bi-box-arrow-right"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Message si aucune organisation -->
          <div v-else class="no-organizations">
            <div class="no-org-content">
              <div class="no-org-icon">
                <i class="bi bi-building"></i>
              </div>
              <h3 class="no-org-title">Aucune organisation trouvée</h3>
              <p class="no-org-description">
                Vous n'appartenez à aucune organisation pour le moment. 
                Créez-en une ou rejoignez une organisation existante.
              </p>
              <div class="no-org-actions">
                <button class="btn btn-primary" @click="toggleCreateOrganizationModal">
                  <i class="bi bi-plus-circle me-2"></i>
                  Créer une organisation
                </button>
                <button class="btn btn-outline-primary" @click="toggleJoinOrganizationModal">
                  <i class="bi bi-people me-2"></i>
                  Rejoindre une organisation
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Contenu de l'onglet "Rechercher" -->
        <div v-if="activeTab === 'search'" class="tab-content">
          <!-- Barre de recherche -->
          <div class="search-section">
            <div class="search-container">
              <div class="search-input-wrapper">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  class="search-input" 
                  placeholder="Rechercher une organisation..."
                  v-model="searchQuery"
                  @input="searchOrganizations"
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
          </div>

          <!-- Liste des organisations disponibles -->
          <div class="available-organizations">
            <div class="organizations-grid" v-if="filteredOrganizations.length > 0">
              <div 
                class="organization-card search-card" 
                v-for="(org, index) in filteredOrganizations" 
                :key="org.id"
                :style="{ animationDelay: `${index * 0.1}s` }"
              >
                <div class="card-header">
                  <div class="organization-icon">
                    <i class="bi bi-building"></i>
                  </div>
                  <div class="organization-header-content">
                    <h3 class="organization-name">{{ org.name }}</h3>
                    <p class="organization-subtitle">{{ org.organization_type || 'Organisation' }}</p>
                  </div>
                  <div class="organization-status" :class="org.is_active ? 'active' : 'inactive'">
                    <i class="bi bi-circle-fill"></i>
                  </div>
                </div>
                
                <div class="card-content">
                  <p class="organization-description">{{ org.description || 'Aucune description' }}</p>
                  
                  <div class="organization-meta">
                    <div class="meta-item">
                      <i class="bi bi-people"></i>
                      <span>{{ org.member_count || 0 }} membres</span>
                    </div>
                    <div class="meta-item">
                      <i class="bi bi-calendar"></i>
                      <span>{{ formatDate(org.created_at) }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="card-footer">
                  <div class="organization-info">
                    <span class="organization-sector">{{ org.sector || 'Secteur non renseigné' }}</span>
                  </div>
                  <div class="organization-actions">
                    <button class="btn btn-sm btn-outline-primary" @click="viewOrganizationDetails(org)" @mouseenter="showOrganizationInfo(org, $event)" @mouseleave="closeOrganizationInfo" title="Détails">
                      <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-primary" @click="requestToJoin(org, $event)" title="Demander à rejoindre">
                      <i class="bi bi-person-plus"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Message si aucune organisation trouvée -->
            <div v-else-if="searchQuery && !isLoading" class="no-results">
              <div class="no-results-content">
                <div class="no-results-icon">
                  <i class="bi bi-search"></i>
                </div>
                <h3 class="no-results-title">Aucune organisation trouvée</h3>
                <p class="no-results-description">
                  Aucune organisation ne correspond à votre recherche "{{ searchQuery }}".
                </p>
                <button class="btn btn-outline-primary" @click="clearSearch">
                  <i class="bi bi-arrow-left me-2"></i>
                  Effacer la recherche
                </button>
              </div>
            </div>

            <!-- Message d'accueil pour la recherche -->
            <div v-else-if="!searchQuery" class="search-welcome">
              <div class="search-welcome-content">
                <div class="search-welcome-icon">
                  <i class="bi bi-search"></i>
                </div>
                <h3 class="search-welcome-title">Découvrez de nouvelles organisations</h3>
                <p class="search-welcome-description">
                  Utilisez la barre de recherche ci-dessus pour trouver des organisations qui vous intéressent.
                </p>
              </div>
            </div>

            <!-- Indicateur de chargement -->
            <div v-if="isLoading" class="loading-indicator">
              <div class="spinner"></div>
              <p>Recherche en cours...</p>
            </div>
          </div>
        </div>
      </div>
    </div>


  </div>

  <!-- Bulle d'informations des membres -->
  <div v-if="showMembersModal" class="members-tooltip" :style="{ top: tooltipPosition.top + 'px', left: tooltipPosition.left + 'px' }" @click.stop @mouseenter="cancelCloseMembersModal" @mouseleave="closeMembersModal">
    <div class="tooltip-arrow" :class="'arrow-' + tooltipDirection"></div>
    <div class="tooltip-content">
      <div class="tooltip-header">
        <h4 class="tooltip-title">
          <i class="bi bi-people me-2"></i>
          {{ currentOrganization?.name }}
        </h4>
        <button class="tooltip-close" @click="closeMembersModal">
          <i class="bi bi-x"></i>
        </button>
      </div>
      
      <div class="tooltip-body">
        <div v-if="currentOrganizationMembers.length > 0" class="members-list">
          <div 
            v-for="member in currentOrganizationMembers" 
            :key="member.id"
            class="member-item"
          >
            <div class="member-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <div class="member-info">
              <div class="member-name">{{ member.user_name || member.user_email }}</div>
              <div class="member-email">{{ member.user_email }}</div>
            </div>
            <div class="member-role">
              <span class="role-badge" :class="member.role">
                {{ getRoleDisplayName(member.role) }}
              </span>
            </div>
          </div>
        </div>
        
        <div v-else class="no-members">
          <i class="bi bi-people text-muted"></i>
          <p class="text-muted">Aucun membre</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Bulle d'informations de l'organisation -->
  <div v-if="showOrganizationInfoModal" class="organization-info-tooltip" :style="{ top: organizationInfoPosition.top + 'px', left: organizationInfoPosition.left + 'px' }" @click.stop @mouseenter="cancelCloseOrganizationInfo" @mouseleave="closeOrganizationInfo">
    <div class="tooltip-arrow" :class="'arrow-' + organizationInfoDirection"></div>
    <div class="tooltip-content">
      <div class="tooltip-header">
        <h4 class="tooltip-title">
          <i class="bi bi-building me-2"></i>
          {{ currentOrganizationInfo?.name }}
        </h4>
        <button class="tooltip-close" @click="closeOrganizationInfo">
          <i class="bi bi-x"></i>
        </button>
      </div>
      
      <div class="tooltip-body">
        <div class="organization-info-list">
          <div class="info-item">
            <i class="bi bi-envelope me-2"></i>
            <span class="info-label">Email:</span>
            <span class="info-value">{{ currentOrganizationInfo?.email || 'Non renseigné' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-telephone me-2"></i>
            <span class="info-label">Téléphone:</span>
            <span class="info-value">{{ currentOrganizationInfo?.phone || 'Non renseigné' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-geo-alt me-2"></i>
            <span class="info-label">Adresse:</span>
            <span class="info-value">{{ currentOrganizationInfo?.address || 'Non renseignée' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-globe me-2"></i>
            <span class="info-label">Site web:</span>
            <span class="info-value">{{ currentOrganizationInfo?.website || 'Non renseigné' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-tag me-2"></i>
            <span class="info-label">Type:</span>
            <span class="info-value">{{ currentOrganizationInfo?.organization_type || 'Non renseigné' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-briefcase me-2"></i>
            <span class="info-label">Secteur:</span>
            <span class="info-value">{{ currentOrganizationInfo?.sector || 'Non renseigné' }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-people me-2"></i>
            <span class="info-label">Membres:</span>
            <span class="info-value">{{ currentOrganizationInfo?.member_count || 0 }}</span>
          </div>
          
          <div class="info-item">
            <i class="bi bi-check-circle me-2"></i>
            <span class="info-label">Statut:</span>
            <span class="info-value" :class="currentOrganizationInfo?.is_active ? 'text-success' : 'text-danger'">
              {{ currentOrganizationInfo?.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Pop-up de confirmation pour rejoindre une organisation -->
  <div v-if="showJoinConfirmationPopup" class="join-confirmation-popup" :style="{ top: popupPosition.top + 'px', left: popupPosition.left + 'px' }" @click.stop>
    <div v-if="showPopupArrow" class="popup-arrow"></div>
    <div class="popup-content">
      <div class="popup-header">
        <div class="popup-icon">
          <i class="bi bi-people-fill"></i>
        </div>
        <h6 class="popup-title">Rejoindre {{ organizationToJoin?.name }} ?</h6>
        <button class="popup-close" @click="closeJoinConfirmation">
          <i class="bi bi-x"></i>
        </button>
      </div>
      
      <div class="popup-body">
        <p class="popup-message">Vous deviendrez membre de cette organisation.</p>
      </div>
      
      <div class="popup-actions">
        <button class="btn btn-sm btn-outline-secondary" @click="closeJoinConfirmation">
          Annuler
        </button>
        <button class="btn btn-sm btn-primary" @click="confirmJoinOrganization">
          <i class="bi bi-person-plus me-1"></i>
          Rejoindre
        </button>
      </div>
    </div>
  </div>

  <!-- Notification Toast -->
  <div v-if="showNotification" class="notification-toast" :class="`notification-${notificationData.type}`">
    <div class="notification-content">
      <div class="notification-icon">
        <i class="bi" :class="`bi-${getNotificationIcon(notificationData.type)}`"></i>
      </div>
      <div class="notification-text">
        <div class="notification-title">{{ notificationData.title }}</div>
        <div class="notification-message">{{ notificationData.message }}</div>
      </div>
      <button class="notification-close" @click="showNotification = false">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

// Store d'authentification et router
const authStore = useAuthStore()
const router = useRouter()

// État des données
const userOrganizations = ref([])
const showMembersModal = ref(false)
const currentOrganizationMembers = ref([])
const currentOrganization = ref(null)
const tooltipPosition = ref({ top: 0, left: 0 })
const tooltipDirection = ref('bottom') // 'top', 'bottom', 'left', 'right'

// Bulle d'informations de l'organisation
const showOrganizationInfoModal = ref(false)
const currentOrganizationInfo = ref(null)
const organizationInfoPosition = ref({ top: 0, left: 0 })
const organizationInfoDirection = ref('bottom')
const closeOrganizationInfoTimeout = ref(null)

// Gestion des onglets
const activeTab = ref('my-organizations')

// Gestion de la recherche
const searchQuery = ref('')
const allOrganizations = ref([])
const filteredOrganizations = ref([])
const isLoading = ref(false)

// Gestion des notifications et pop-ups
const showJoinConfirmationPopup = ref(false)
const organizationToJoin = ref(null)
const popupPosition = ref({ top: 0, left: 0 })
const showPopupArrow = ref(true)
const showNotification = ref(false)
const notificationData = ref({ type: '', title: '', message: '' })

// Computed pour les statistiques
const totalMembers = computed(() => {
  return userOrganizations.value.reduce((total, org) => total + (org.member_count || 0), 0)
})

const totalDocuments = computed(() => {
  return userOrganizations.value.reduce((total, org) => total + (org.document_count || 0), 0)
})

const activeOrganizations = computed(() => {
  return userOrganizations.value.filter(org => org.is_active).length
})

// Charger les organisations de l'utilisateur
const loadUserOrganizations = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/organizations/user-organizations/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.organizations) {
        userOrganizations.value = data.organizations
        console.log('✅ Organisations chargées:', data.organizations.length)
        console.log('📋 Détails des organisations:', data.organizations)
      } else {
        console.log('ℹ️ Aucune organisation trouvée pour cet utilisateur')
        userOrganizations.value = []
      }
    } else {
      console.error('❌ Erreur lors du chargement des organisations')
      userOrganizations.value = []
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des organisations:', error)
    userOrganizations.value = []
  }
}

// Sélectionner une organisation
const selectOrganization = (organization) => {
  console.log('Organisation sélectionnée:', organization)
  
  // Sauvegarder l'organisation sélectionnée
  localStorage.setItem('selectedOrganization', JSON.stringify(organization))
  
  // Émettre un événement pour changer la page dans le dashboard parent
  const event = new CustomEvent('organizationSelected', {
    detail: {
      organization: organization,
      role: organization.role
    }
  })
  window.dispatchEvent(event)
}

// Obtenir le nom d'affichage du rôle
const getRoleDisplayName = (role) => {
  const roleNames = {
    'admin': 'Administrateur',
    'chef': 'Chef',
    'chef+1': 'Chef+1',
    'chef+2': 'Chef+2',
    'chef+n': 'Chef+n',
    'secretaire': 'Secrétaire',
    'member': 'Membre'
  }
  return roleNames[role] || 'Membre'
}

// Actions sur les organisations
const viewOrganizationDetails = (organization) => {
  console.log('Voir les détails de l\'organisation:', organization)
  // Logique pour voir les détails
}

// Gestion de la bulle d'informations de l'organisation
const showOrganizationInfo = (organization, event) => {
  // Annuler le délai de fermeture si la souris revient
  if (closeOrganizationInfoTimeout.value) {
    clearTimeout(closeOrganizationInfoTimeout.value)
    closeOrganizationInfoTimeout.value = null
  }
  
  if (event && event.target) {
    const rect = event.target.getBoundingClientRect()
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    
    const tooltipWidth = 450 // Largeur approximative de la bulle
    const tooltipHeight = 300 // Hauteur approximative de la bulle
    const windowWidth = window.innerWidth
    const windowHeight = window.innerHeight
    
    const spaceLeft = rect.left
    const spaceRight = windowWidth - rect.right
    const spaceTop = rect.top
    const spaceBottom = windowHeight - rect.bottom
    
    let top, left, direction
    
    // Calculer l'espace total disponible
    const totalHorizontalSpace = spaceLeft + spaceRight
    const totalVerticalSpace = spaceTop + spaceBottom
    
    // Positionner à droite de l'œil, au niveau du début de la carte
    left = rect.right + scrollLeft + 15
    top = rect.top + scrollTop - 80 // Positionner au niveau du début de la carte
    direction = 'left'
    
    organizationInfoDirection.value = direction
    
    // Ajustements finaux pour éviter de sortir de l'écran
    const margin = 20
    
    // Ajustement horizontal
    if (left < margin) {
      left = margin
    } else if (left + tooltipWidth > windowWidth - margin) {
      left = windowWidth - tooltipWidth - margin
    }
    
    // Ajustement vertical - priorité pour garder la bulle entièrement visible
    if (top < scrollTop + margin) {
      top = scrollTop + margin
    } else if (top + tooltipHeight > windowHeight + scrollTop - margin) {
      // Si la bulle dépasse en bas, la repositionner plus haut
      top = windowHeight + scrollTop - tooltipHeight - margin
      
      // Si même en haut elle ne rentre pas, la centrer verticalement
      if (top < scrollTop + margin) {
        top = scrollTop + (windowHeight - tooltipHeight) / 2
      }
    }
    
    // Vérification finale pour s'assurer que la bulle est entièrement visible
    const finalLeft = Math.max(margin, Math.min(left, windowWidth - tooltipWidth - margin))
    const finalTop = Math.max(scrollTop + margin, Math.min(top, windowHeight + scrollTop - tooltipHeight - margin))
    
    organizationInfoPosition.value = { top: finalTop, left: finalLeft }
  }
  
  currentOrganizationInfo.value = organization
  showOrganizationInfoModal.value = true
}

const closeOrganizationInfo = () => {
  closeOrganizationInfoTimeout.value = setTimeout(() => {
    showOrganizationInfoModal.value = false
    currentOrganizationInfo.value = null
  }, 150)
}

const cancelCloseOrganizationInfo = () => {
  if (closeOrganizationInfoTimeout.value) {
    clearTimeout(closeOrganizationInfoTimeout.value)
    closeOrganizationInfoTimeout.value = null
  }
}

// Gestion de la modale des membres
const showOrganizationMembers = async (organization, event) => {
  // Annuler le délai de fermeture si la souris revient
  if (closeTimeout) {
    clearTimeout(closeTimeout)
    closeTimeout = null
  }
  
  // Calculer la position de la bulle par rapport à l'élément survolé
  if (event && event.target) {
    const rect = event.target.getBoundingClientRect()
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    
    const tooltipWidth = 500 // Largeur approximative de la bulle
    const tooltipHeight = 300 // Hauteur approximative de la bulle
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
  
  try {
    currentOrganization.value = organization
    showMembersModal.value = true
    
    // Charger les membres de l'organisation
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/${organization.id}/members/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.members) {
        currentOrganizationMembers.value = data.members
        console.log('✅ Membres chargés:', data.members.length)
      } else {
        console.log('ℹ️ Aucun membre trouvé pour cette organisation')
        currentOrganizationMembers.value = []
      }
    } else if (response.status === 403) {
      console.log('ℹ️ Accès non autorisé aux membres de cette organisation')
      currentOrganizationMembers.value = []
    } else {
      console.error('❌ Erreur lors du chargement des membres')
      currentOrganizationMembers.value = []
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des membres:', error)
    currentOrganizationMembers.value = []
  }
}

let closeTimeout = null

const closeMembersModal = () => {
  // Ajouter un petit délai pour éviter la fermeture trop rapide
  if (closeTimeout) {
    clearTimeout(closeTimeout)
  }
  
  closeTimeout = setTimeout(() => {
    showMembersModal.value = false
    currentOrganizationMembers.value = []
    currentOrganization.value = null
  }, 150) // 150ms de délai
}

const cancelCloseMembersModal = () => {
  // Annuler la fermeture si la souris entre dans la bulle
  if (closeTimeout) {
    clearTimeout(closeTimeout)
    closeTimeout = null
  }
}

// Quitter l'organisation
const leaveOrganization = async (organization) => {
  if (confirm(`Êtes-vous sûr de vouloir quitter l'organisation "${organization.name}" ?\n\nCette action est irréversible.`)) {
    try {
      // Récupérer le token CSRF depuis les cookies
      const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
      };
      
      const csrfToken = getCookie('csrftoken');
      
      const response = await fetch(`http://127.0.0.1:8000/api/organizations/${organization.id}/leave/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          console.log('✅ Organisation quittée avec succès')
          alert('Organisation quittée avec succès !')
          // Recharger la liste des organisations
          await loadUserOrganizations()
        } else {
          console.error('❌ Erreur lors de la sortie de l\'organisation:', data.message)
          alert('Erreur lors de la sortie de l\'organisation: ' + data.message)
        }
      } else {
        const errorData = await response.json().catch(() => ({}))
        console.error('❌ Erreur lors de la sortie de l\'organisation:', errorData)
        alert('Erreur lors de la sortie de l\'organisation: ' + (errorData.message || 'Erreur inconnue'))
      }
    } catch (error) {
      console.error('❌ Erreur lors de la sortie de l\'organisation:', error)
      alert('Erreur lors de la sortie de l\'organisation')
    }
  }
}



// Gestion des onglets
const setActiveTab = (tab) => {
  activeTab.value = tab
  if (tab === 'search' && allOrganizations.value.length === 0) {
    loadAllOrganizations()
  }
}

// Charger toutes les organisations disponibles
const loadAllOrganizations = async () => {
  try {
    isLoading.value = true
    const response = await fetch('http://127.0.0.1:8000/api/organizations/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.organizations) {
        allOrganizations.value = data.organizations
        filteredOrganizations.value = data.organizations
        console.log('✅ Toutes les organisations chargées:', data.organizations.length)
      } else {
        console.log('ℹ️ Aucune organisation trouvée')
        allOrganizations.value = []
        filteredOrganizations.value = []
      }
    } else {
      console.error('❌ Erreur lors du chargement des organisations')
      allOrganizations.value = []
      filteredOrganizations.value = []
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des organisations:', error)
    allOrganizations.value = []
    filteredOrganizations.value = []
  } finally {
    isLoading.value = false
  }
}

// Recherche d'organisations
const searchOrganizations = () => {
  if (!searchQuery.value.trim()) {
    filteredOrganizations.value = allOrganizations.value
    return
  }
  
  const query = searchQuery.value.toLowerCase().trim()
  filteredOrganizations.value = allOrganizations.value.filter(org => 
    org.name.toLowerCase().includes(query) ||
    (org.description && org.description.toLowerCase().includes(query)) ||
    (org.sector && org.sector.toLowerCase().includes(query)) ||
    (org.organization_type && org.organization_type.toLowerCase().includes(query))
  )
}

// Effacer la recherche
const clearSearch = () => {
  searchQuery.value = ''
  filteredOrganizations.value = allOrganizations.value
}

// Formater la date
const formatDate = (dateString) => {
  if (!dateString) return 'Date inconnue'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Fonction pour afficher une notification
const displayNotification = (type, title, message) => {
  notificationData.value = { type, title, message }
  showNotification.value = true
  
  // Masquer automatiquement après 5 secondes
  setTimeout(() => {
    showNotification.value = false
  }, 5000)
}

// Fonction pour obtenir l'icône selon le type de notification
const getNotificationIcon = (type) => {
  const icons = {
    success: 'check-circle-fill',
    error: 'x-circle-fill',
    warning: 'exclamation-triangle-fill',
    info: 'info-circle-fill'
  }
  return icons[type] || 'info-circle-fill'
}

// Ouvrir le pop-up de confirmation pour rejoindre une organisation
const openJoinConfirmation = (organization, event) => {
  console.log('🔍 Ouverture du pop-up pour:', organization.name)
  
  if (event && event.target) {
    const rect = event.target.getBoundingClientRect()
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft
    
    // Dimensions du pop-up
    const popupWidth = 300
    const popupHeight = 200
    const margin = 20
    
    // Position initiale (au-dessus du bouton)
    let top = rect.top + scrollTop - popupHeight - 20
    let left = rect.left + scrollLeft + (rect.width / 2) - (popupWidth / 2)
    
    // Vérifier les limites de l'écran
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight
    
    // Ajuster horizontalement si nécessaire
    if (left < margin) {
      left = margin
    } else if (left + popupWidth > viewportWidth - margin) {
      left = viewportWidth - popupWidth - margin
    }
    
    // Ajuster verticalement si nécessaire
    if (top < margin) {
      // Si pas assez d'espace au-dessus, placer en dessous
      top = rect.bottom + scrollTop + 20
      showPopupArrow.value = false // Masquer la flèche si en dessous
    } else {
      showPopupArrow.value = true // Afficher la flèche si au-dessus
    }
    
    // Vérifier si le pop-up dépasse en bas
    if (top + popupHeight > viewportHeight + scrollTop - margin) {
      // Centrer verticalement si possible
      top = Math.max(margin, (viewportHeight - popupHeight) / 2 + scrollTop)
      showPopupArrow.value = false // Masquer la flèche si centré
    }
    
    popupPosition.value = {
      top: top,
      left: left
    }
    
    console.log('📍 Position du pop-up:', popupPosition.value)
  }
  
  organizationToJoin.value = organization
  showJoinConfirmationPopup.value = true
  console.log('✅ Pop-up ouvert:', showJoinConfirmationPopup.value)
}

// Fermer le pop-up de confirmation
const closeJoinConfirmation = () => {
  showJoinConfirmationPopup.value = false
  organizationToJoin.value = null
  showPopupArrow.value = true // Réinitialiser la flèche
}

// Confirmer et rejoindre l'organisation
const confirmJoinOrganization = async () => {
  if (!organizationToJoin.value) return
  
  try {
    // Récupérer le token CSRF depuis les cookies
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    };
    
    const csrfToken = getCookie('csrftoken');
    
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/${organizationToJoin.value.id}/request-join/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        console.log('✅ Demande de rejoindre l\'organisation envoyée')
        displayNotification('success', 'Succès', data.message)
        // Recharger les organisations de l'utilisateur
        await loadUserOrganizations()
      } else {
        console.error('❌ Erreur lors de la demande:', data.message)
        displayNotification('error', 'Erreur', data.message)
      }
    } else {
      const errorData = await response.json().catch(() => ({}))
      console.error('❌ Erreur lors de la demande:', errorData)
      displayNotification('error', 'Erreur', errorData.message || 'Erreur inconnue')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la demande:', error)
    displayNotification('error', 'Erreur', 'Erreur lors de la demande')
  } finally {
    closeJoinConfirmation()
  }
}

// Demander à rejoindre une organisation (ancienne fonction pour compatibilité)
const requestToJoin = (organization, event) => {
  console.log('🔍 Clic sur le bouton rejoindre:', organization.name)
  // Empêcher la propagation de l'événement pour éviter la fermeture immédiate
  event.stopPropagation()
  openJoinConfirmation(organization, event)
}

// Gestionnaire pour fermer le pop-up en cliquant en dehors
const handleClickOutside = (event) => {
  if (showJoinConfirmationPopup.value && !event.target.closest('.join-confirmation-popup')) {
    closeJoinConfirmation()
  }
}

// Initialisation
onMounted(async () => {
  await loadUserOrganizations()
  // Ajouter le gestionnaire d'événements
  document.addEventListener('click', handleClickOutside)
})

// Nettoyage
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
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
  --info: #17a2b8;
}

/* STYLES GÉNÉRAUX */
.organization-selection-page {
  min-height: 100vh;
}

/* HEADER */
.organization-header {
  margin-bottom: 3rem;
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

.section-title {
  font-size: 3rem;
  font-weight: 700;
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
}

.dashboard-illustration {
  width: 420px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.dashboard-illustration:hover {
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
.create-org-btn {
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

.create-org-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

.join-org-btn {
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  background: transparent;
  transition: all 0.3s ease;
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  font-size: 1rem;
}

.join-org-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

/* SECTIONS DES ORGANISATIONS */
/* ONGLETS */
.tabs-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

.tabs-header {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-button {
  flex: 1;
  padding: 1rem 2rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
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

/* BARRE DE RECHERCHE */
.search-section {
  margin-bottom: 2rem;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  color: var(--text-dark);
  font-size: 1rem;
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
  left: 1rem;
  color: var(--primary-blue);
  font-size: 1.1rem;
  z-index: 2;
}

.clear-search-btn {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-search-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

/* CARTES DE RECHERCHE */
.search-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.search-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.15),
    0 10px 25px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  border-color: rgba(0, 102, 204, 0.3);
}

.organization-info {
  flex: 1;
}

.organization-sector {
  font-size: 0.85rem;
  color: var(--dark-gray);
  background: rgba(255, 255, 255, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* MESSAGES D'ÉTAT */
.no-results, .search-welcome, .loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  padding: 2rem;
}

.no-results-content, .search-welcome-content {
  text-align: center;
  max-width: 400px;
}

.no-results-icon, .search-welcome-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  color: var(--primary-blue);
}

.no-results-title, .search-welcome-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-family: 'Raleway', sans-serif;
}

.no-results-description, .search-welcome-description {
  font-size: 1rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* INDICATEUR DE CHARGEMENT */
.loading-indicator {
  flex-direction: column;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 102, 204, 0.1);
  border-top: 3px solid var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-indicator p {
  color: var(--dark-gray);
  font-size: 1rem;
  margin: 0;
}

/* STATISTIQUES */
.stats-section {
  margin-bottom: 3rem;
  padding: 0 2rem;
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

.organizations-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem 2rem;
}

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
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.5s forwards;
}

.sections-subtitle {
  font-size: 1.2rem;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.6s forwards;
}

/* GRILLE DES ORGANISATIONS */
.organizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.organization-card {
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
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  position: relative;
  overflow: hidden;
}

.organization-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 10px 25px rgba(0, 102, 204, 0.08),
    0 5px 15px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
}


/* HEADER DE LA CARTE */
.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 102, 204, 0.08);
}

.organization-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.organization-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--primary-blue);
  flex-shrink: 0;
}

.organization-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 0.6rem;
}

.organization-status.active {
  color: var(--success);
}

.organization-status.inactive {
  color: var(--dark-gray);
}

/* CONTENU DE LA CARTE */
.card-content {
  margin-bottom: 1.5rem;
}

.organization-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.organization-subtitle {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
  font-weight: 400;
}

.organization-description {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.organization-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--dark-gray);
}

.meta-item i {
  color: var(--primary-blue);
  font-size: 0.9rem;
}

/* FOOTER DE LA CARTE */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.user-role {
  flex: 1;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Codes couleurs pour les rôles */
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

.organization-actions {
  display: flex;
  gap: 0.5rem;
}

.organization-actions .btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 0.8rem;
}

/* MESSAGE AUCUNE ORGANISATION */
.no-organizations {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 3rem;
}

.no-org-content {
  text-align: center;
  max-width: 500px;
}

.no-org-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  color: var(--primary-blue);
}

.no-org-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-family: 'Raleway', sans-serif;
}

.no-org-description {
  font-size: 1rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.no-org-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* MODALES */
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

.form-text {
  font-size: 0.85rem;
  color: var(--dark-gray);
  margin-top: 0.25rem;
}

/* BOUTONS */
.btn-primary {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

.btn-outline-primary {
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  background: transparent;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

.btn-outline-secondary {
  border: 2px solid var(--dark-gray);
  color: var(--dark-gray);
  background: transparent;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  background: var(--dark-gray);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
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

/* BULLE D'INFORMATIONS DES MEMBRES */
.members-tooltip {
  position: absolute;
  z-index: 1000;
  animation: tooltipFadeIn 0.3s ease-out;
}

/* Transform selon la direction */
.members-tooltip[class*="arrow-top"],
.members-tooltip[class*="arrow-bottom"] {
  transform: translateX(-50%);
}

.members-tooltip[class*="arrow-left"],
.members-tooltip[class*="arrow-right"] {
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
  border-bottom: 8px solid rgba(255, 255, 255, 0.2);
  filter: drop-shadow(0 -2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers le bas (bulle en haut) */
.arrow-bottom {
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid rgba(255, 255, 255, 0.2);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers la gauche (bulle à droite) */
.arrow-left {
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid rgba(255, 255, 255, 0.2);
  filter: drop-shadow(-2px 0 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers la droite (bulle à gauche) */
.arrow-right {
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-left: 8px solid rgba(255, 255, 255, 0.2);
  filter: drop-shadow(2px 0 4px rgba(0, 0, 0, 0.1));
}

.tooltip-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  max-width: 500px;
  width: 90vw;
  max-height: 70vh;
  overflow: hidden;
}

.tooltip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.tooltip-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
  display: flex;
  align-items: center;
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
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tooltip-close:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.tooltip-body {
  padding: 1rem 1.5rem;
  max-height: 50vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 102, 204, 0.3) transparent;
}

.tooltip-body::-webkit-scrollbar {
  width: 6px;
}

.tooltip-body::-webkit-scrollbar-track {
  background: transparent;
}

.tooltip-body::-webkit-scrollbar-thumb {
  background: rgba(0, 102, 204, 0.3);
  border-radius: 3px;
}

.tooltip-body::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 102, 204, 0.5);
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.member-item:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 
    0 4px 16px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.member-avatar {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 50%;
  font-size: 1.2rem;
  color: var(--primary-blue);
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.member-name {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.9rem;
  line-height: 1.2;
}

.member-email {
  color: var(--dark-gray);
  font-size: 0.8rem;
  line-height: 1.2;
}

.member-role {
  display: flex;
  align-items: center;
}

.no-members {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  color: var(--dark-gray);
}

.no-members i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }
  
  .dashboard-illustration {
    width: 300px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .create-org-btn, .join-org-btn {
    width: 100%;
  }
  
  .organizations-section {
    padding: 0 1rem;
  }
  
  .organizations-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .organization-card {
    padding: 1.25rem;
  }
  
  .organization-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .card-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .organization-actions {
    align-self: flex-end;
  }
  
  .no-org-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .no-org-actions .btn {
    width: 100%;
  }
  
  .modal-content {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .tooltip-content {
    max-width: 95vw;
    max-height: 80vh;
  }
  
  .tooltip-header {
    padding: 0.75rem 1rem;
  }
  
  .tooltip-body {
    padding: 0.75rem 1rem;
    max-height: 60vh;
  }
  
  .member-item {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
    padding: 0.5rem;
  }

  /* Responsive pour les onglets */
  .tabs-container {
    margin: 0 1rem 2rem 1rem;
  }
  
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .tab-content {
    padding: 1rem;
  }
  
  /* Responsive pour la barre de recherche */
  .search-container {
    margin: 0 1rem;
  }
  
  .search-input {
    padding: 0.75rem 0.75rem 0.75rem 2.5rem;
    font-size: 0.9rem;
  }
  
  .search-icon {
    left: 0.75rem;
    font-size: 1rem;
  }
  
  .clear-search-btn {
    right: 0.75rem;
    width: 25px;
    height: 25px;
    font-size: 1rem;
  }
  
  /* Responsive pour les messages d'état */
  .no-results, .search-welcome, .loading-indicator {
    min-height: 250px;
    padding: 1rem;
  }
  
  .no-results-icon, .search-welcome-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .no-results-title, .search-welcome-title {
    font-size: 1.25rem;
  }
  
  .no-results-description, .search-welcome-description {
    font-size: 0.9rem;
  }
}

/* POP-UP DE CONFIRMATION POUR REJOINDRE UNE ORGANISATION */
.join-confirmation-popup {
  position: absolute;
  z-index: 10000;
  animation: popupBounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.popup-arrow {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid rgba(255, 255, 255, 0.3);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  opacity: 0.8;
}

.popup-content {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  min-width: 300px;
  max-width: 350px;
  overflow: hidden;
}

.popup-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
}

.popup-icon {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  color: var(--primary-blue);
  flex-shrink: 0;
}

.popup-title {
  flex: 1;
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.2;
}

.popup-close {
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.popup-close:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.popup-body {
  padding: 1rem;
}

.popup-message {
  margin: 0;
  font-size: 0.85rem;
  color: #333333;
  line-height: 1.4;
}

.popup-actions {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
}

.popup-actions .btn {
  flex: 1;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.popup-actions .btn-outline-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--dark-gray);
}

.popup-actions .btn-outline-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: var(--text-dark);
}

.popup-actions .btn-primary {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  border: none;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
}

.popup-actions .btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4);
}

/* NOTIFICATION TOAST */
.notification-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10001;
  min-width: 300px;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.notification-content {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  gap: 0.75rem;
}

.notification-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.notification-text {
  flex: 1;
  min-width: 0;
}

.notification-title {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text-dark);
}

.notification-message {
  margin: 0;
  font-size: 0.8rem;
  color: var(--dark-gray);
  line-height: 1.4;
}

.notification-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.notification-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-dark);
}

/* Types de notifications */
.notification-success {
  border-left: 4px solid #28a745;
}

.notification-success .notification-icon {
  color: #28a745;
}

.notification-error {
  border-left: 4px solid #dc3545;
}

.notification-error .notification-icon {
  color: #dc3545;
}

.notification-warning {
  border-left: 4px solid #ffc107;
}

.notification-warning .notification-icon {
  color: #ffc107;
}

.notification-info {
  border-left: 4px solid #17a2b8;
}

.notification-info .notification-icon {
  color: #17a2b8;
}

/* Animations */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes popupBounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3) translateY(-50px);
  }
  50% {
    opacity: 1;
    transform: scale(1.05) translateY(0);
  }
  70% {
    transform: scale(0.95) translateY(0);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive pour le pop-up */
@media (max-width: 768px) {
  .popup-content {
    min-width: 280px;
    max-width: 320px;
  }
  
  .popup-header,
  .popup-body,
  .popup-actions {
    padding: 0.75rem;
  }
  
  .popup-actions {
    flex-direction: column;
  }
  
  .popup-actions .btn {
    width: 100%;
  }
  
  .notification-toast {
    right: 10px;
    left: 10px;
    min-width: auto;
    max-width: none;
  }
}

/* Bulle d'informations de l'organisation */
.organization-info-tooltip {
  position: absolute;
  z-index: 10000;
  max-width: 450px;
  max-height: 300px;
  animation: tooltipFadeIn 0.3s ease-out;
}

.organization-info-tooltip .tooltip-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  max-width: 450px;
  width: 90vw;
  max-height: 300px;
  overflow: hidden;
}

.organization-info-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 220px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.organization-info-list::-webkit-scrollbar {
  width: 4px;
}

.organization-info-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.organization-info-list::-webkit-scrollbar-thumb {
  background: rgba(0, 102, 204, 0.3);
  border-radius: 2px;
}

.organization-info-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 102, 204, 0.5);
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.info-item i {
  color: var(--primary-blue);
  font-size: 0.9rem;
  width: 16px;
  text-align: center;
}

.info-label {
  font-weight: 600;
  color: var(--text-dark);
  margin-right: 0.5rem;
  min-width: 80px;
}

.info-value {
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.text-success {
  color: #28a745 !important;
}

.text-danger {
  color: #dc3545 !important;
}

@media (max-width: 768px) {
  .member-info {
    align-items: center;
  }
  
  .member-avatar {
    width: 30px;
    height: 30px;
    font-size: 1rem;
  }
  
  .member-name {
    font-size: 0.85rem;
  }
  
  .member-email {
    font-size: 0.75rem;
  }
}
</style>
