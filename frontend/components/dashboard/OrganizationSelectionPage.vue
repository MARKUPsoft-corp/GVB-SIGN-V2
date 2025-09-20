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
          <div class="header-actions">
            <button class="btn btn-primary-custom create-org-btn" @click="toggleCreateOrganizationModal" ref="createOrgBtn">
              <i class="bi bi-plus-circle me-2"></i>
              Créer une organisation
            </button>
            <button class="btn btn-outline-primary join-org-btn" @click="toggleJoinOrganizationModal">
              <i class="bi bi-people me-2"></i>
              Rejoindre une organisation
            </button>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Sélection Organisation" class="organization-illustration">
        </div>
      </div>
    </div>

    <!-- Section des organisations -->
    <div class="organizations-section">
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Vos</span> 
              <span class="text-primary-blue"> Organisations</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Sélectionnez l'organisation pour accéder à votre tableau de bord personnalisé.
            </p>
          </div>
        </div>
      </div>

      <!-- Grille des organisations -->
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
              <button class="btn btn-sm btn-outline-primary" @click.stop="viewOrganizationDetails(org)" title="Détails">
                <i class="bi bi-eye"></i>
              </button>
              <button class="btn btn-sm btn-outline-secondary" @click.stop="openOrganizationSettings(org)" title="Paramètres">
                <i class="bi bi-gear"></i>
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

    <!-- Modale de création d'organisation -->
    <div v-if="showCreateOrganizationModal" class="modal-overlay" @click="closeCreateOrganizationModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Créer une nouvelle organisation</h5>
          <button class="btn-close" @click="closeCreateOrganizationModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createOrganization">
            <div class="mb-3">
              <label for="organizationName" class="form-label">Nom de l'organisation</label>
              <input type="text" class="form-control" id="organizationName" v-model="newOrganization.name" required>
            </div>
            <div class="mb-3">
              <label for="organizationDescription" class="form-label">Description</label>
              <textarea class="form-control" id="organizationDescription" v-model="newOrganization.description" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="organizationType" class="form-label">Type d'organisation</label>
              <select class="form-select" id="organizationType" v-model="newOrganization.type" required>
                <option value="">Sélectionner un type</option>
                <option value="company">Entreprise</option>
                <option value="association">Association</option>
                <option value="ngo">ONG</option>
                <option value="government">Gouvernement</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div class="d-flex justify-content-end gap-2">
              <button type="button" class="btn btn-outline-secondary" @click="closeCreateOrganizationModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isCreatingOrganization">
                <span v-if="isCreatingOrganization" class="spinner-border spinner-border-sm me-2"></span>
                Créer l'organisation
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modale de rejoindre une organisation -->
    <div v-if="showJoinOrganizationModal" class="modal-overlay" @click="closeJoinOrganizationModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Rejoindre une organisation</h5>
          <button class="btn-close" @click="closeJoinOrganizationModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="joinOrganization">
            <div class="mb-3">
              <label for="invitationCode" class="form-label">Code d'invitation</label>
              <input type="text" class="form-control" id="invitationCode" v-model="invitationCode" required placeholder="Entrez le code d'invitation">
              <div class="form-text">Demandez le code d'invitation à l'administrateur de l'organisation.</div>
            </div>
            <div class="d-flex justify-content-end gap-2">
              <button type="button" class="btn btn-outline-secondary" @click="closeJoinOrganizationModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isJoiningOrganization">
                <span v-if="isJoiningOrganization" class="spinner-border spinner-border-sm me-2"></span>
                Rejoindre
              </button>
            </div>
          </form>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

// Store d'authentification et router
const authStore = useAuthStore()
const router = useRouter()

// État des données
const userOrganizations = ref([])
const showCreateOrganizationModal = ref(false)
const showJoinOrganizationModal = ref(false)
const showMembersModal = ref(false)
const isCreatingOrganization = ref(false)
const isJoiningOrganization = ref(false)
const currentOrganizationMembers = ref([])
const currentOrganization = ref(null)
const tooltipPosition = ref({ top: 0, left: 0 })
const tooltipDirection = ref('bottom') // 'top', 'bottom', 'left', 'right'

// Nouvelle organisation
const newOrganization = ref({
  name: '',
  description: '',
  type: ''
})

// Code d'invitation
const invitationCode = ref('')

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
    // Horizontal
    if (left < 10) {
      left = 10
    } else if (left + tooltipWidth > windowWidth - 10) {
      left = windowWidth - tooltipWidth - 10
    }
    
    // Vertical
    if (top < scrollTop + 10) {
      top = scrollTop + 10
    } else if (top + tooltipHeight > windowHeight + scrollTop - 10) {
      top = windowHeight + scrollTop - tooltipHeight - 10
    }
    
    tooltipPosition.value = { top, left }
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
      }
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

const openOrganizationSettings = (organization) => {
  console.log('Ouvrir les paramètres de l\'organisation:', organization)
  // Logique pour ouvrir les paramètres
}

// Modales
const toggleCreateOrganizationModal = () => {
  showCreateOrganizationModal.value = !showCreateOrganizationModal.value
}

const closeCreateOrganizationModal = () => {
  showCreateOrganizationModal.value = false
  newOrganization.value = {
    name: '',
    description: '',
    type: ''
  }
}

const toggleJoinOrganizationModal = () => {
  showJoinOrganizationModal.value = !showJoinOrganizationModal.value
}

const closeJoinOrganizationModal = () => {
  showJoinOrganizationModal.value = false
  invitationCode.value = ''
}

// Créer une organisation
const createOrganization = async () => {
  isCreatingOrganization.value = true
  try {
    console.log('Création de l\'organisation:', newOrganization.value)
    // Ici on peut faire un appel API pour créer l'organisation
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulation
    
    // Ajouter la nouvelle organisation à la liste
    const organization = {
      id: Date.now(),
      name: newOrganization.value.name,
      description: newOrganization.value.description,
      type: newOrganization.value.type,
      status: 'active',
      userRole: 'admin',
      memberCount: 1,
      documentCount: 0
    }
    
    userOrganizations.value.unshift(organization)
    closeCreateOrganizationModal()
    console.log('✅ Organisation créée avec succès')
  } catch (error) {
    console.error('❌ Erreur lors de la création de l\'organisation:', error)
  } finally {
    isCreatingOrganization.value = false
  }
}

// Rejoindre une organisation
const joinOrganization = async () => {
  isJoiningOrganization.value = true
  try {
    console.log('Rejoindre l\'organisation avec le code:', invitationCode.value)
    // Ici on peut faire un appel API pour rejoindre l'organisation
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulation
    
    closeJoinOrganizationModal()
    console.log('✅ Organisation rejointe avec succès')
    
    // Recharger les organisations
    await loadUserOrganizations()
  } catch (error) {
    console.error('❌ Erreur lors de la jonction à l\'organisation:', error)
  } finally {
    isJoiningOrganization.value = false
  }
}

// Initialisation
onMounted(async () => {
  await loadUserOrganizations()
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
  width: 370px;
  height: 270px;
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

.role-badge.admin {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.role-badge.manager {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.role-badge.secretary {
  background: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
}

.role-badge.member {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
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
  
  .header-image {
    width: 280px;
    height: 180px;
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
