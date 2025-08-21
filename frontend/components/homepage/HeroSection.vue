<template>
  <section class="hero-section bg-white position-relative">
    <div class="container">
      <div class="row align-items-center min-vh-100">
        <!-- Contenu principal -->
        <div class="col-lg-6 mb-5 mb-lg-0">
          <div class="hero-content">
            <h1 class="display-1 fw-bold mb-4 text-dark hero-title">
              Sécurisez vos 
              <span class="text-primary-blue">Documents</span> 
              avec la <span class="text-primary-blue">Signature Électronique</span>
            </h1>
            
            <p class="lead mb-5 text-dark hero-subtitle">
              Révolutionnez votre processus de signature avec notre technologie QR Code avancée. 
              Sécurisé, rapide et conforme aux standards internationaux.
            </p>

            <!-- Bouton d'action rapide -->
            <div class="hero-actions">
              <NuxtLink to="/register" class="btn btn-primary-custom btn-lg hero-action-btn">
                <i class="bi bi-play-circle me-2"></i>
                Commencer maintenant
              </NuxtLink>
            </div>

          </div>
        </div>

        <!-- Image SVG -->
        <div class="col-lg-6">
          <div class="hero-image text-center position-relative">
            <!-- Bulles décoratives -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
            <div class="bubble bubble-4"></div>
            
            <img src="/hero.svg" alt="Signature Électronique" class="img-fluid hero-svg hero-image-svg">
          </div>
        </div>
      </div>
      
      <!-- Bouton de défilement vers les fonctionnalités -->
      <div class="scroll-down-container" :class="{ 'visible': isInHeroSection }">
        <button class="scroll-down-btn" @click="scrollToFeatures" aria-label="Voir les fonctionnalités">
          <i class="bi bi-chevron-down"></i>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isInHeroSection = ref(true)

// Fonction pour faire défiler vers la section des fonctionnalités
const scrollToFeatures = () => {
  const featuresSection = document.getElementById('fonctionnalites')
  if (featuresSection) {
    // Scroll simple vers la section avec un offset
    featuresSection.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    })
    
    // Ajustement après le scroll pour compenser la navbar
    setTimeout(() => {
      window.scrollBy({
        top: -100,
        behavior: 'smooth'
      })
    }, 100)
  }
}

// Fonction pour détecter si on est dans la hero section
const handleScroll = () => {
  const heroSection = document.querySelector('.hero-section')
  if (heroSection) {
    const heroBottom = heroSection.offsetTop + heroSection.offsetHeight
    const scrollPosition = window.scrollY + window.innerHeight
    
    // Le bouton est visible si on est dans la hero section
    isInHeroSection.value = scrollPosition > heroBottom - 100
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Vérification initiale
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.hero-section {
  padding: -1rem 0;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero-content {
  opacity: 0;
  animation: fadeInUp 1.2s ease-out 0.3s forwards;
}

.display-1 {
  font-size: 3.2rem;
  line-height: 1.1;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  letter-spacing: -0.02em;
}

.text-primary-blue {
  color: var(--primary-blue) !important;
}

.text-dark {
  color: var(--text-dark) !important;
}

.lead {
  font-size: 1.3rem;
  font-weight: 400;
  line-height: 1.6;
  font-family: 'Raleway', sans-serif;
  letter-spacing: -0.01em;
}





.hero-image {
  opacity: 0;
  animation: fadeInRight 1.2s ease-out 0.6s forwards;
}

.hero-svg {
  max-width: 80%;
  height: auto;
  filter: drop-shadow(0 10px 30px rgba(0, 102, 204, 0.1));
  position: relative;
  z-index: 2;
}

.hero-title {
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.5s forwards;
}

.hero-subtitle {
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.8s forwards;
}

.hero-actions {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 1.1s forwards;
}

.hero-action-btn {
  background: var(--gradient-primary);
  border: none;
  color: white;
  font-weight: 600;
  padding: 15px 35px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-family: 'Raleway', sans-serif;
  letter-spacing: 0.02em;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
  position: relative;
  overflow: hidden;
}

.hero-action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.hero-action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(0, 102, 204, 0.3);
  background: var(--primary-blue-dark);
}

.hero-action-btn:hover::before {
  left: 100%;
}

.hero-action-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.25);
}

.hero-image-svg {
  opacity: 0;
  animation: slideInRight 1s ease-out 0.9s forwards;
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

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-25px);
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

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

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
    transform: translateX(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
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

@media (max-width: 991px) {
  .display-1 {
    font-size: 2.5rem;
  }
  
  .lead {
    font-size: 1.2rem;
  }
  
  .hero-section {
    padding: 2rem 0;
  }
  
  .hero-image {
    margin-top: 2rem;
  }
  
  .hero-svg {
    max-width: 70%;
  }
}

@media (max-width: 576px) {
  .display-1 {
    font-size: 2rem;
  }
  
  .lead {
    font-size: 1.1rem;
  }
  
  .hero-section {
    padding: 3rem 0;
  }
  
  .hero-content {
    text-align: center;
  }
  
  .hero-image {
    margin-top: -1.5rem;
  }
  
  .hero-svg {
    max-width: 80%;
  }
  
  .hero-action-btn {
    padding: 12px 28px;
    font-size: 1rem;
  }
  
  .scroll-down-container {
    bottom: 1rem;
  }
  
  .scroll-down-btn {
    width: 45px;
    height: 45px;
    font-size: 1rem;
  }
  
  .scroll-down-container {
    bottom: 1rem;
    left: 2rem;
    transform: none;
  }
}

/* Bouton de défilement */
.scroll-down-container {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease-out 1.5s forwards;
}

.scroll-down-container.visible {
  opacity: 1;
  visibility: visible;
}

.scroll-down-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 102, 204, 0.2);
  color: var(--primary-blue);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.1);
}

.scroll-down-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: var(--primary-blue);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
  color: var(--primary-blue);
}

.scroll-down-btn:active {
  transform: translateY(-1px) scale(1.02);
}

.scroll-down-btn i {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-3px);
  }
}
</style>
