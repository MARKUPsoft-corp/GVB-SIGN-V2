<template>
  <div class="dashboard-page">
    <!-- Header avec message de bienvenue -->
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1 class="welcome-title">
          <span class="text-dark">{{ welcomePrefix }} </span>
          <span class="text-primary-blue"> {{ userName }}</span>
        </h1>
        <p class="welcome-subtitle">{{ welcomeSubtitle }}</p>
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

    <!-- Cartes d'actions rapides -->
    <div class="quick-actions">
      <div class="row g-4">
        <!-- Carte 1 - Nouveau document -->
        <div class="col-lg-3 col-md-6">
          <div class="action-card">
            <div class="card-icon">
              <i class="bi bi-file-earmark-plus"></i>
            </div>
            <h3 class="card-title">Nouveau Document</h3>
            <p class="card-description">Créez et signez un nouveau document en quelques clics</p>
            <button class="card-btn">
              <span>Commencer</span>
              <i class="bi bi-arrow-right"></i>
            </button>
          </div>
        </div>

        <!-- Carte 2 - Scanner QR Code -->
        <div class="col-lg-3 col-md-6">
          <div class="action-card">
            <div class="card-icon">
              <i class="bi bi-qr-code-scan"></i>
            </div>
            <h3 class="card-title">Scanner QR Code</h3>
            <p class="card-description">Authentifiez-vous rapidement avec votre QR Code personnel</p>
            <button class="card-btn">
              <span>Scanner</span>
              <i class="bi bi-arrow-right"></i>
            </button>
          </div>
        </div>

        <!-- Carte 3 - Mes Signatures -->
        <div class="col-lg-3 col-md-6">
          <div class="action-card">
            <div class="card-icon">
              <i class="bi bi-pen"></i>
            </div>
            <h3 class="card-title">Mes Signatures</h3>
            <p class="card-description">Gérez vos signatures électroniques et modèles</p>
            <button class="card-btn">
              <span>Gérer</span>
              <i class="bi bi-arrow-right"></i>
            </button>
          </div>
        </div>

        <!-- Carte 4 - Historique -->
        <div class="col-lg-3 col-md-6">
          <div class="action-card">
            <div class="card-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <h3 class="card-title">Historique</h3>
            <p class="card-description">Consultez l'historique de vos documents signés</p>
            <button class="card-btn">
              <span>Voir</span>
              <i class="bi bi-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Définir le layout dashboard
definePageMeta({
  layout: 'dashboard'
})

// Données utilisateur
const route = useRoute()
const userName = ref('')
const userEmail = ref('')
const isFromRegistration = ref(false)

// Initialiser les données utilisateur
onMounted(() => {
  // Récupérer les données de la query ou du localStorage
  if (route.query.name) {
    userName.value = route.query.name
  }
  if (route.query.email) {
    userEmail.value = route.query.email
  }
  
  // Détecter si l'utilisateur vient de l'inscription ou de la connexion
  // Si on vient de welcome.vue, c'est une inscription
  const referrer = document.referrer
  isFromRegistration.value = referrer.includes('/welcome') || route.query.from === 'registration'
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
  text-align: center;
}

.welcome-section {
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: #6c757d;
  margin-bottom: 0;
  font-weight: 400;
}

/* SECTION STATISTIQUES */
.stats-section {
  margin-bottom: 3rem;
}

/* CARTES D'ACTIONS RAPIDES */
.quick-actions {
  margin-bottom: 2rem;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  height: 100%;
  display: flex;
  flex-direction: column;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15);
  border-color: var(--primary-blue);
}

.card-icon {
  width: 60px;
  height: 60px;
  background: var(--gradient-primary);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
  font-size: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.75rem;
  font-family: 'Raleway', sans-serif;
}

.card-description {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
  flex: 1;
}

.card-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: none;
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  padding: 0.75rem 1.25rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  font-family: 'Raleway', sans-serif;
}

.card-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateX(4px);
}

.card-btn i {
  font-size: 0.875rem;
  transition: transform 0.3s ease;
}

.card-btn:hover i {
  transform: translateX(4px);
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
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
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