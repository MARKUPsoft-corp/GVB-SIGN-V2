<template>
  <div class="dashboard-container">
    <div class="dashboard-card">
      <div class="dashboard-header">
        <div class="welcome-icon">
          <i class="bi bi-person-circle"></i>
        </div>
        <h1 class="dashboard-title">Bienvenue {{ userName }} !</h1>
        <p class="dashboard-subtitle">Vous êtes maintenant connecté à votre espace personnel</p>
      </div>
      
      <div class="user-info">
        <div class="info-item">
          <i class="bi bi-envelope"></i>
          <span>{{ userEmail }}</span>
        </div>
        <div class="info-item">
          <i class="bi bi-calendar-check"></i>
          <span>Connecté le {{ currentDate }}</span>
        </div>
      </div>
      
      <div class="dashboard-actions">
        <button @click="logout" class="btn btn-outline-primary-custom">
          <i class="bi bi-box-arrow-left me-2"></i>
          Se déconnecter
        </button>
        <NuxtLink to="/" class="btn btn-primary-custom">
          <i class="bi bi-house me-2"></i>
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, navigateTo } from '#app'

const route = useRoute()
const userName = ref('')
const userEmail = ref('')
const currentDate = ref('')

onMounted(() => {
  // Récupérer les paramètres de l'URL
  userName.value = route.query.name || 'Utilisateur'
  userEmail.value = route.query.email || ''
  currentDate.value = new Date().toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

const logout = async () => {
  try {
    const API_BASE_URL = 'http://127.0.0.1:8000/api'
    await fetch(`${API_BASE_URL}/auth/logout/`, {
      method: 'POST',
      credentials: 'include'
    })
    
    await navigateTo('/')
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
    await navigateTo('/')
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--white) 100%);
  padding: 2rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 60px var(--shadow-light);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 3rem;
  text-align: center;
  max-width: 500px;
  width: 100%;
  animation: fadeInUp 0.8s ease-out;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.welcome-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: 50%;
  color: white;
  font-size: 2.5rem;
  animation: pulse 2s ease-in-out infinite;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  font-size: 1.1rem;
  color: var(--dark-gray);
  margin: 0;
}

.user-info {
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px;
  color: var(--text-dark);
}

.info-item i {
  color: var(--primary-blue);
  font-size: 1.2rem;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(0, 102, 204, 0);
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .dashboard-card {
    padding: 2rem;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .dashboard-actions {
    flex-direction: column;
  }
}
</style>
