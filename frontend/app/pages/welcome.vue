<template>
  <div class="welcome-page">
    <div class="welcome-container">
      <div class="welcome-card">
        <!-- Animation de succès -->
        <div class="success-animation">
          <div class="success-icon">
            <i class="bi bi-check-circle-fill"></i>
          </div>
        </div>

        <!-- Message de bienvenue -->
        <div class="welcome-content">
          <h1 class="welcome-title">
            Bienvenue {{ userName }} !
          </h1>
          
          <div class="welcome-subtitle">
            Votre compte GVB Sign a été créé avec succès
          </div>
          
          <div class="welcome-details">
            <div class="detail-item">
              <i class="bi bi-envelope-check"></i>
              <span>Email : {{ userEmail }}</span>
            </div>
            <div class="detail-item">
              <i class="bi bi-calendar-check"></i>
              <span>Compte créé le {{ currentDate }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="welcome-actions">
            <NuxtLink to="/" class="btn btn-primary-custom">
              <i class="bi bi-house me-2"></i>
              Retourner à l'accueil
            </NuxtLink>
            <NuxtLink to="/login" class="btn btn-outline-primary-custom ms-3">
              <i class="bi bi-box-arrow-in-right me-2"></i>
              Se connecter
            </NuxtLink>
          </div>
        </div>

        <!-- Bulles décoratives -->
        <div class="welcome-bubble bubble-1"></div>
        <div class="welcome-bubble bubble-2"></div>
        <div class="welcome-bubble bubble-3"></div>
        <div class="welcome-bubble bubble-4"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Métadonnées de la page
definePageMeta({
  layout: 'auth',
  title: 'Bienvenue - GVB Sign'
})

// Récupération des paramètres de query
const route = useRoute()
const userName = computed(() => route.query.name || 'Nouvel utilisateur')
const userEmail = computed(() => route.query.email || '')

// Date actuelle formatée
const currentDate = computed(() => {
  return new Date().toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// Configuration SEO
useHead({
  title: `Bienvenue ${userName.value} - GVB Sign`,
  meta: [
    {
      name: 'description',
      content: 'Bienvenue sur GVB Sign ! Votre compte a été créé avec succès.'
    }
  ]
})
</script>

<style scoped>
.welcome-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.welcome-container {
  width: 100%;
  max-width: 600px;
  padding: 2rem;
}

.welcome-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(0, 102, 204, 0.15),
    0 8px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  opacity: 0;
  animation: welcomeAppear 1s ease-out forwards;
}

.success-animation {
  margin-bottom: 2rem;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: 50%;
  color: white;
  font-size: 2.5rem;
  animation: successPulse 2s ease-out infinite;
}

.welcome-content {
  margin-bottom: 2rem;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleSlide 1s ease-out 0.5s both;
}

.welcome-subtitle {
  font-size: 1.25rem;
  color: #6c757d;
  margin-bottom: 2rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.8s both;
}

.welcome-details {
  margin-bottom: 2rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out 1s both;
}

.detail-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #495057;
}

.detail-item i {
  margin-right: 0.75rem;
  font-size: 1.25rem;
  color: #667eea;
}

.welcome-actions {
  opacity: 0;
  animation: fadeInUp 1s ease-out 1.3s both;
}

.btn {
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.btn-primary-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  color: white;
}

.btn-outline-primary-custom {
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  backdrop-filter: blur(10px);
}

.btn-outline-primary-custom:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
  transform: translateY(-2px);
  color: #667eea;
}

/* Bulles décoratives */
.welcome-bubble {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
  animation: float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 60px;
  height: 60px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.bubble-2 {
  width: 40px;
  height: 40px;
  top: 20%;
  right: 15%;
  animation-delay: 1s;
}

.bubble-3 {
  width: 80px;
  height: 80px;
  bottom: 15%;
  left: 15%;
  animation-delay: 2s;
}

.bubble-4 {
  width: 50px;
  height: 50px;
  bottom: 10%;
  right: 10%;
  animation-delay: 3s;
}

/* Animations */
@keyframes welcomeAppear {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes successPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
}

@keyframes titleSlide {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  33% {
    transform: translateY(-10px) rotate(120deg);
  }
  66% {
    transform: translateY(10px) rotate(240deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .welcome-card {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1.1rem;
  }
  
  .btn {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .welcome-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .ms-3 {
    margin-left: 0 !important;
  }
}
</style>
