<template>
  <div class="dashboard-page">
    <!-- Header avec message de bienvenue -->
    <div class="dashboard-header">
      <div class="welcome-container">
        <div class="welcome-content">
          <h1 class="welcome-title">
            <span class="text-dark">{{ welcomePrefix }}</span>
            <span class="text-primary-blue">{{ userName }}</span>
          </h1>
          <p class="welcome-subtitle">{{ welcomeSubtitle }}</p>
        </div>
        <div class="welcome-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/dashboard.svg" alt="Dashboard" class="dashboard-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques rapides -->
    <div class="stats-section">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">12</h4>
              <p class="stat-label">Documents signés</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">3</h4>
              <p class="stat-label">En attente</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-shield-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">100%</h4>
              <p class="stat-label">Sécurisé</p>
            </div>
          </div>
        </div>
      </div>
    </div>

              <!-- Actions rapides en deux colonnes -->
          <div class="quick-actions">
            <!-- En-tête de section -->
            <div class="row mb-5">
              <div class="col-12">
                <div class="actions-header text-center">
                  <h2 class="display-4 fw-bold mb-3 text-dark actions-title">
                    <span class="text-dark">Actions</span> 
                    <span class="text-primary-blue"> Rapides</span>
                  </h2>
                  <p class="lead mb-0 text-dark actions-subtitle">
                    Accédez rapidement aux fonctionnalités essentielles de votre espace de signature électronique.
                  </p>
                </div>
              </div>
            </div>

            <div class="row align-items-center">
        <!-- Colonne gauche - Image SVG -->
        <div class="col-lg-6 mb-5 mb-lg-0">
          <div class="actions-image text-center position-relative">
            <!-- Bulles décoratives -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
            <div class="bubble bubble-4"></div>
            <img src="/service.svg" alt="Actions rapides" class="img-fluid actions-svg">
          </div>
        </div>
        
        <!-- Colonne droite - Actions rapides -->
        <div class="col-lg-6">
          <div class="actions-content">
            <!-- Actions rapides -->
            <div class="actions-cards">
              <!-- Action 1 - Nouveau document -->
              <div class="action-item mb-4">
                <div class="card border-0 shadow-sm action-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="action-icon me-4">
                        <i class="bi bi-file-earmark-plus text-primary-blue fs-1"></i>
                      </div>
                      <div class="action-content">
                        <h4 class="fw-bold text-dark mb-2">Nouveau Document</h4>
                        <p class="text-muted mb-0">Créez et signez un nouveau document en quelques clics</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Créer ou intégrer une organisation -->
              <div class="action-item mb-4">
                <div class="card border-0 shadow-sm action-card-inner" @click="toggleOrganizationModal" style="cursor: pointer;" ref="organizationBtn">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="action-icon me-4">
                        <i class="bi bi-building-add text-primary-blue fs-1"></i>
                      </div>
                      <div class="action-content">
                        <h4 class="fw-bold text-dark mb-2">Créer ou intégrer une organisation</h4>
                        <p class="text-muted mb-0">Créez une nouvelle organisation ou rejoignez une organisation existante</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Mes Signatures -->
              <div class="action-item mb-4">
                <div class="card border-0 shadow-sm action-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="action-icon me-4">
                        <i class="bi bi-pen text-primary-blue fs-1"></i>
                      </div>
                      <div class="action-content">
                        <h4 class="fw-bold text-dark mb-2">Mes Signatures</h4>
                        <p class="text-muted mb-0">Gérez vos signatures électroniques et modèles</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Historique -->
              <div class="action-item">
                <div class="card border-0 shadow-sm action-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="action-icon me-4">
                        <i class="bi bi-clock-history text-primary-blue fs-1"></i>
                      </div>
                      <div class="action-content">
                        <h4 class="fw-bold text-dark mb-2">Historique</h4>
                        <p class="text-muted mb-0">Consultez l'historique de vos documents signés</p>
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
    
    <!-- Modale contextuelle des organisations -->
    <div v-if="isOrganizationModalOpen" class="organization-modal-overlay" @click="closeOrganizationModal">
      <div class="organization-modal" @click.stop ref="organizationModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-building"></i>
            Options d'Organisation
          </h5>
          <button class="close-btn" @click="closeOrganizationModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-modal-content">
          <div class="organization-option" @click="selectOrganizationOption('create')">
            <div class="option-icon">
              <i class="bi bi-building-add"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Créer une organisation</span>
              <span class="option-desc">Créez une nouvelle organisation et devenez son administrateur</span>
            </div>
          </div>
          
          <div class="organization-option" @click="selectOrganizationOption('join')">
            <div class="option-icon">
              <i class="bi bi-person-plus"></i>
            </div>
            <div class="option-content">
              <span class="option-title">Rejoindre une organisation</span>
              <span class="option-desc">Rejoignez une organisation existante avec un code d'invitation</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale de création d'organisation -->
    <div v-if="isCreateOrganizationModalOpen" class="organization-modal-overlay" @click="closeCreateOrganizationModal">
      <div class="organization-form-modal" @click.stop ref="createOrganizationModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-building-add"></i>
            Créer une Organisation
          </h5>
          <button class="close-btn" @click="closeCreateOrganizationModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-form-content">
          <form @submit.prevent="createOrganization" class="organization-form">
            <div class="form-group">
              <label for="orgName">
                <i class="bi bi-building"></i>
                Nom de l'organisation
              </label>
              <input 
                type="text" 
                id="orgName" 
                v-model="newOrganization.name" 
                placeholder="Entrez le nom de votre organisation"
                required
              >
            </div>

            <div class="form-group">
              <label for="orgDescription">
                <i class="bi bi-file-text"></i>
                Description
              </label>
              <textarea 
                id="orgDescription" 
                v-model="newOrganization.description" 
                placeholder="Décrivez votre organisation..."
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="orgEmail">
                <i class="bi bi-envelope"></i>
                Email de contact
              </label>
              <input 
                type="email" 
                id="orgEmail" 
                v-model="newOrganization.email" 
                placeholder="contact@organisation.com"
                required
              >
            </div>

            <div class="form-group">
              <label for="orgPhone">
                <i class="bi bi-telephone"></i>
                Téléphone
              </label>
              <input 
                type="tel" 
                id="orgPhone" 
                v-model="newOrganization.phone" 
                placeholder="+237 xx xx xx xx"
              >
            </div>

            <div class="form-group">
              <label for="orgAddress">
                <i class="bi bi-geo-alt"></i>
                Adresse
              </label>
              <textarea 
                id="orgAddress" 
                v-model="newOrganization.address" 
                placeholder="Adresse complète de l'organisation..."
                rows="2"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="orgWebsite">
                <i class="bi bi-globe"></i>
                Site web
              </label>
              <input 
                type="url" 
                id="orgWebsite" 
                v-model="newOrganization.website" 
                placeholder="https://www.organisation.com"
              >
            </div>

            <div class="form-group">
              <label for="orgType">
                <i class="bi bi-tags"></i>
                Type d'organisation
              </label>
              <select id="orgType" v-model="newOrganization.organization_type" required>
                <option value="">Sélectionnez un type</option>
                <option value="entreprise">Entreprise</option>
                <option value="association">Association</option>
                <option value="administration">Administration</option>
                <option value="collectivite">Collectivité</option>
                <option value="autre">Autre</option>
              </select>
            </div>

            <div class="form-group">
              <label for="orgSector">
                <i class="bi bi-briefcase"></i>
                Secteur d'activité
              </label>
              <input 
                type="text" 
                id="orgSector" 
                v-model="newOrganization.sector" 
                placeholder="Ex: Technologies, Santé, Éducation..."
              >
            </div>

            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="closeCreateOrganizationModal">
                <i class="bi bi-x-circle"></i>
                Annuler
              </button>
              <button type="submit" class="btn-create" :disabled="isCreatingOrganization">
                <i class="bi bi-check-circle" v-if="!isCreatingOrganization"></i>
                <i class="bi bi-hourglass-split" v-else></i>
                {{ isCreatingOrganization ? 'Création...' : 'Créer l\'organisation' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../../stores/auth'
import OrganizationApiService from '../../services/OrganizationApiService'

// Définir le middleware et le layout
definePageMeta({
  middleware: 'auth',
  layout: 'dashboard'
})

// Store d'authentification (côté client seulement)
const authStore = process.client ? useAuthStore() : null

// Données utilisateur
const route = useRoute()
const userName = computed(() => authStore?.user?.full_name || 'Utilisateur')
const userEmail = computed(() => authStore?.user?.email || '')
const isFromRegistration = ref(false)

// État pour la modale des organisations
const isOrganizationModalOpen = ref(false)
const organizationModal = ref(null)
const organizationBtn = ref(null)

// Variables pour la modale de création d'organisation
const isCreateOrganizationModalOpen = ref(false)
const createOrganizationModal = ref(null)
const isCreatingOrganization = ref(false)
const newOrganization = ref({
  name: '',
  description: '',
  email: '',
  phone: '',
  address: '',
  website: '',
  organization_type: '',
  sector: ''
})

// Initialiser les données utilisateur
onMounted(async () => {
  // Initialiser l'authentification
  if (authStore) {
    await authStore.initAuth()
  }
  
  // Détecter si l'utilisateur vient de l'inscription ou de la connexion
  isFromRegistration.value = route.query.from === 'registration'
})

// Messages de bienvenue personnalisés
const welcomePrefix = computed(() => {
  return isFromRegistration.value ? 'Bienvenue ' : 'Bon retour '
})

const welcomeSubtitle = computed(() => {
  if (isFromRegistration.value) {
    return 'Votre compte a été créé avec succès. Découvrez toutes les fonctionnalités de GVB Sign.'
  }
  return 'Heureux de vous revoir ! Accédez rapidement à vos documents et signatures.'
})

// Meta tags
useHead({
  title: `Dashboard - ${userName.value || 'Utilisateur'} | GVB Sign`,
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

// Fonctions pour la modale des organisations
const toggleOrganizationModal = () => {
  isOrganizationModalOpen.value = !isOrganizationModalOpen.value
  
  if (isOrganizationModalOpen.value) {
    nextTick(() => {
      if (organizationBtn.value && organizationModal.value && window.innerWidth > 768) {
        const buttonRect = organizationBtn.value.getBoundingClientRect()
        const modal = organizationModal.value
        
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
    // Restaurer le scroll
    document.body.style.overflow = 'auto'
  }
}

const closeOrganizationModal = () => {
  isOrganizationModalOpen.value = false
  // Restaurer le scroll
  document.body.style.overflow = 'auto'
}

const selectOrganizationOption = (option) => {
  console.log('Option d\'organisation sélectionnée:', option)
  closeOrganizationModal()
  
  switch (option) {
    case 'create':
      // Ouvrir la modale de création d'organisation
      console.log('Ouverture de la modale de création d\'organisation')
      openCreateOrganizationModal()
      break
    case 'join':
      // Rediriger vers la page des organisations pour rejoindre
      console.log('Redirection vers la jointure d\'organisation')
      // Ici on pourrait naviguer vers la page des organisations
      break
  }
}

// Fonctions pour la modale de création d'organisation
const openCreateOrganizationModal = () => {
  console.log('Ouverture de la modale de création d\'organisation')
  isCreateOrganizationModalOpen.value = true
  
  // Désactiver le scroll du body
  document.body.style.overflow = 'hidden'
  
  // Positionner la modale contextuellement
  nextTick(() => {
    positionCreateOrganizationModal()
  })
}

const closeCreateOrganizationModal = () => {
  console.log('Fermeture de la modale de création d\'organisation')
  isCreateOrganizationModalOpen.value = false
  
  // Réactiver le scroll du body
  document.body.style.overflow = 'auto'
  
  // Réinitialiser le formulaire
  resetOrganizationForm()
}

const positionCreateOrganizationModal = () => {
  if (!createOrganizationModal.value) return
  
  const modal = createOrganizationModal.value
  const rect = modal.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  
  // Calculer la position optimale (centré horizontalement, plus haut verticalement)
  const left = Math.max(20, (viewportWidth - rect.width) / 2)
  const top = Math.max(20, (viewportHeight - rect.height) / 2 - 50) // Décalage de 100px vers le haut
  
  modal.style.left = `${left}px`
  modal.style.top = `${top}px`
  modal.style.transform = 'none'
}

const resetOrganizationForm = () => {
  newOrganization.value = {
    name: '',
    description: '',
    email: '',
    phone: '',
    address: '',
    website: '',
    organization_type: '',
    sector: ''
  }
  isCreatingOrganization.value = false
}

const createOrganization = async () => {
  try {
    isCreatingOrganization.value = true
    console.log('Création de l\'organisation:', newOrganization.value)
    
    // Récupérer l'utilisateur connecté depuis le store
    const authStore = useAuthStore()
    const currentUser = authStore.user
    
    console.log('Utilisateur connecté:', currentUser)
    console.log('ID utilisateur connecté:', currentUser?.id)
    
    if (!currentUser || !currentUser.id) {
      throw new Error('Aucun utilisateur connecté trouvé')
    }
    
    // Ajouter l'ID de l'utilisateur connecté aux données
    const organizationData = {
      ...newOrganization.value,
      user_id: currentUser.id
    }
    
    console.log('Données d\'organisation avec user_id:', organizationData)
    
    // Appel à l'API pour créer l'organisation
    const response = await OrganizationApiService.createOrganization(organizationData)
    
    console.log('Organisation créée avec succès!', response)
    
    // Marquer que l'utilisateur a maintenant une organisation
    localStorage.setItem('user_has_organization', 'true')
    
    // Fermer la modale
    closeCreateOrganizationModal()
    
    // Afficher un message de succès
    alert('Organisation créée avec succès ! Vous êtes maintenant administrateur de cette organisation.')
    
    // Recharger la page pour mettre à jour le menu
    window.location.reload()
    
  } catch (error) {
    console.error('Erreur lors de la création de l\'organisation:', error)
    alert('Erreur lors de la création de l\'organisation: ' + error.message)
  } finally {
    isCreatingOrganization.value = false
  }
}
</script>

<style scoped>
.dashboard-page {
  padding: 0;
  background: #f8f9fa;
  min-height: 100vh;
}

/* HEADER */
.dashboard-header {
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.welcome-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 2rem;
}

.welcome-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.welcome-image {
  flex-shrink: 0;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
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
  background: rgba(0, 102, 204, 0.1);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 100px;
  height: 100px;
  top: -5%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 120px;
  height: 120px;
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
  width: 90px;
  height: 90px;
  top: 40%;
  left: 10%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

.welcome-title {
  font-size: 3rem;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 0;
  font-weight: 400;
}

/* SECTION STATISTIQUES */
.stats-section {
  margin-bottom: 3rem;
}

/* ACTIONS RAPIDES */
.quick-actions {
  margin-bottom: 3rem;
}

/* En-tête de section */
.actions-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.actions-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.5s forwards;
}

.actions-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.6s forwards;
}

.actions-image {
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.9s forwards;
}

.actions-svg {
  max-width: 80%;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
}

.actions-svg:hover {
  transform: translateY(-4px);
  filter: drop-shadow(0 8px 20px rgba(0, 102, 204, 0.15));
}

.actions-content {
  opacity: 0;
  animation: slideInRight 1s ease-out 1.0s forwards;
}

.actions-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.action-item:nth-child(1) { animation-delay: 1.1s; }
.action-item:nth-child(2) { animation-delay: 1.2s; }
.action-item:nth-child(3) { animation-delay: 1.3s; }
.action-item:nth-child(4) { animation-delay: 1.4s; }

.action-card-inner {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  position: relative;
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.action-card-inner .card-body {
  padding: 1rem !important;
}

.action-card-inner:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 25px 50px rgba(0, 102, 204, 0.15),
    0 15px 30px rgba(0, 102, 204, 0.1),
    0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.3);
  background: rgba(255, 255, 255, 0.98);
}

.action-icon {
  flex-shrink: 0;
  width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  border-radius: 14px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(0, 102, 204, 0.1);
  position: relative;
  overflow: hidden;
  color: var(--primary-blue);
  font-size: 1.3rem;
}

.action-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.action-card-inner:hover .action-icon {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.2) 100%);
  transform: scale(1.1) rotate(5deg);
  border-color: rgba(0, 102, 204, 0.3);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.2);
}

.action-card-inner:hover .action-icon::before {
  left: 100%;
}

.action-content h4 {
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.6rem;
  transition: all 0.3s ease;
  position: relative;
}

.action-card-inner:hover .action-content h4 {
  color: var(--primary-blue);
  transform: translateX(5px);
}

.action-content p {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--dark-gray);
  margin: 0;
  transition: all 0.3s ease;
  opacity: 0.85;
}

.action-card-inner:hover .action-content p {
  opacity: 1;
  color: var(--text-dark);
}

/* ANIMATIONS DES CARTES */
.action-card:nth-child(1) { animation-delay: 0.5s; }
.action-card:nth-child(2) { animation-delay: 0.6s; }
.action-card:nth-child(3) { animation-delay: 0.7s; }
.action-card:nth-child(4) { animation-delay: 0.8s; }

/* SECTION STATISTIQUES */
.stats-section {
  margin-bottom: 2rem;
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
    transform: translateY(-25px);
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

/* MODALE DES ORGANISATIONS */
.organization-modal-overlay {
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

/* MODALE DE FORMULAIRE D'ORGANISATION */
.organization-form-modal {
  position: fixed;
  width: 600px;
  max-width: 90vw;
  max-height: 90vh;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  z-index: 10000;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.organization-modal {
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

.organization-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  background: rgba(0, 102, 204, 0.02);
  border-radius: 16px 16px 0 0;
}

.organization-modal-header h5 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Titre plus grand pour la modale de formulaire */
.organization-form-modal .organization-modal-header h5 {
  font-size: 1.2rem;
  font-weight: 700;
}

.organization-modal-header h5 i {
  color: var(--primary-blue);
  font-size: 1rem;
}

/* Icône plus grande pour la modale de formulaire */
.organization-form-modal .organization-modal-header h5 i {
  font-size: 1.3rem;
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
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.organization-modal-content {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* CONTENU DU FORMULAIRE D'ORGANISATION */
.organization-form-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.organization-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.form-group label i {
  color: var(--primary-blue);
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem 1rem;
  border: 2px solid rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  font-size: 0.9rem;
  color: var(--text-dark);
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-blue);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
  transform: translateY(-1px);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(108, 117, 125, 0.7);
  font-style: italic;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-group select {
  cursor: pointer;
}

.form-group select option {
  padding: 0.5rem;
  background: white;
  color: var(--text-dark);
}

/* ACTIONS DU FORMULAIRE */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.btn-cancel,
.btn-create {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: inherit;
}

.btn-cancel {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  border: 2px solid rgba(108, 117, 125, 0.2);
}

.btn-cancel:hover {
  background: rgba(108, 117, 125, 0.15);
  border-color: rgba(108, 117, 125, 0.3);
  transform: translateY(-1px);
}

.btn-create {
  background: linear-gradient(135deg, var(--primary-blue), #0056b3);
  color: white;
  border: 2px solid var(--primary-blue);
}

.btn-create:hover:not(:disabled) {
  background: linear-gradient(135deg, #0056b3, var(--primary-blue));
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

.btn-create:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-create:disabled:hover {
  transform: none;
  box-shadow: none;
}

.organization-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.organization-option:hover {
  background: rgba(0, 102, 204, 0.05);
  border-color: rgba(0, 102, 204, 0.1);
  transform: translateX(2px);
}

.option-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(0, 102, 204, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1rem;
  flex-shrink: 0;
}

.option-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.option-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0;
}

.option-desc {
  font-size: 0.75rem;
  color: #6c757d;
  margin: 0;
  line-height: 1.3;
}

/* Animations pour la modale */
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
    transform: translate(-50%, -50%) translateY(30px) scale(0.8) rotateX(-10deg);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) translateY(-5px) scale(1.05) rotateX(2deg);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) translateY(0) scale(1) rotateX(0deg);
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .dashboard-header {
    padding: 1.5rem 0;
  }
  
  .welcome-container {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  
  .welcome-content {
    text-align: center;
  }
  
  .dashboard-illustration {
    width: 300px;
  }
  
  .welcome-title {
    font-size: 2.5rem;
  }
  
  .welcome-subtitle {
    font-size: 1.25rem;
  }
  
  .actions-image {
    margin-bottom: 2rem;
  }
  
  .actions-svg {
    max-width: 70%;
  }
  
  .actions-title {
    font-size: 2rem;
  }
  
  .actions-subtitle {
    font-size: 1.1rem;
  }
  
  .action-card {
    padding: 1.5rem 1.25rem;
  }
  
  .card-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .card-title {
    font-size: 1.125rem;
  }
  
  .stat-card {
    padding: 1.25rem;
  }
}

@media (max-width: 576px) {
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .action-card {
    text-align: center;
  }
  
  /* Modale des organisations sur mobile */
  .organization-modal {
    width: 90%;
    max-width: 350px;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    animation: modalSlideUpMobile 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    transform-origin: center center;
  }
  
  /* Modale de formulaire d'organisation sur mobile */
  .organization-form-modal {
    width: 98%;
    max-width: none;
    max-height: 95vh;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    animation: modalSlideUpMobile 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    transform-origin: center center;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: none;
  }
  
  .organization-form-content {
    padding: 1rem;
  }
  
  .organization-form {
    gap: 1rem;
  }
  
  .form-group {
    gap: 0.4rem;
  }
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: none;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
    padding-top: 1rem;
  }
  
  .btn-cancel,
  .btn-create {
    width: 100%;
    justify-content: center;
    padding: 0.8rem 1rem;
  }
  
  .organization-modal-content {
    padding: 1rem;
  }
  
  /* Overlay moins flou sur mobile */
  .organization-modal-overlay {
    backdrop-filter: none;
  }
  
  .organization-option {
    padding: 1rem;
  }
  
  .option-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .option-title {
    font-size: 0.9rem;
  }
  
  .option-desc {
    font-size: 0.8rem;
  }
}

</style>