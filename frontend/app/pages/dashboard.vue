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

              <!-- Action 2 - Scanner QR Code -->
              <div class="action-item mb-4">
                <div class="card border-0 shadow-sm action-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="action-icon me-4">
                        <i class="bi bi-qr-code-scan text-primary-blue fs-1"></i>
                      </div>
                      <div class="action-content">
                        <h4 class="fw-bold text-dark mb-2">Scanner QR Code</h4>
                        <p class="text-muted mb-0">Authentifiez-vous rapidement avec votre QR Code personnel</p>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

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
}
</style>