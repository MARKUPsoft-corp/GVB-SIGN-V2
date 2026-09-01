<template>
  <section id="fonctionnalites" class="features-section bg-white position-relative py-5">
    <!-- Point d'ancrage pour le scroll -->
    <div id="features-anchor" class="features-anchor"></div>
    
    <div class="container">
      <!-- En-tête de section - Sur toute la largeur -->
      <div class="row">
        <div class="col-12">
          <div class="features-header text-center mb-5">
            <h2 class="display-3 fw-bold mb-4 text-dark features-title">
              Des <span class="text-primary-blue">Fonctionnalités</span> 
              <span class="text-primary-blue"> Innovantes</span>
            </h2>
            <p class="lead mb-0 text-dark features-subtitle">
              Découvrez tous les avantages de notre solution de signature électronique nouvelle génération.
            </p>
          </div>
        </div>
      </div>

      <!-- Contenu en deux colonnes -->
      <div class="row align-items-center min-vh-75">
        <!-- Colonne gauche - Image SVG -->
        <div class="col-lg-6 mb-5 mb-lg-0">
          <div class="features-image text-center position-relative">
            <!-- Bulles décoratives -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
            <div class="bubble bubble-4"></div>
            <img src="/service.svg" alt="Fonctionnalités GVB Sign" class="img-fluid features-svg features-image-svg">
          </div>
        </div>
        
        <!-- Colonne droite - Cartes de fonctionnalités -->
        <div class="col-lg-6">
          <div class="features-content">
            <!-- Cartes de fonctionnalités -->
            <div class="features-cards">
              <!-- Carte 1 - QR Code -->
              <div class="feature-card mb-4">
                <div class="card border-0 shadow-sm feature-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="feature-icon me-4">
                        <i class="bi bi-qr-code text-primary-blue fs-1"></i>
                      </div>
                      <div class="feature-content">
                        <h4 class="fw-bold text-dark mb-2">Technologie QR Code</h4>
                        <p class="text-muted mb-0">Authentification instantanée via QR Code sécurisé. Plus besoin de mots de passe complexes.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Carte 2 - Sécurité -->
              <div class="feature-card mb-4">
                <div class="card border-0 shadow-sm feature-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="feature-icon me-4">
                        <i class="bi bi-shield-check text-primary-blue fs-1"></i>
                      </div>
                      <div class="feature-content">
                        <h4 class="fw-bold text-dark mb-2">Sécurité Maximale</h4>
                        <p class="text-muted mb-0">Cryptage de bout en bout et conformité aux standards internationaux de sécurité.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Carte 3 - Rapidité -->
              <div class="feature-card mb-4">
                <div class="card border-0 shadow-sm feature-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="feature-icon me-4">
                        <i class="bi bi-lightning text-primary-blue fs-1"></i>
                      </div>
                      <div class="feature-content">
                        <h4 class="fw-bold text-dark mb-2">Signature Instantanée</h4>
                        <p class="text-muted mb-0">Signez vos documents en quelques secondes depuis n'importe quel appareil mobile.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Carte 4 - Multi-plateforme -->
              <div class="feature-card">
                <div class="card border-0 shadow-sm feature-card-inner">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="feature-icon me-4">
                        <i class="bi bi-device-hdd text-primary-blue fs-1"></i>
                      </div>
                      <div class="feature-content">
                        <h4 class="fw-bold text-dark mb-2">Multi-Plateforme</h4>
                        <p class="text-muted mb-0">Compatible avec tous vos appareils : web, mobile iOS et Android.</p>
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
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Animation au montage du composant
onMounted(() => {
  // Les animations sont gérées en CSS
})
</script>

<style scoped>
/* Variables et base */
.features-section {
  padding: 120px 0;
  padding-top: 140px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

/* Classe personnalisée pour une hauteur réduite */
.min-vh-75 {
  min-height: 75vh;
}

/* Point d'ancrage pour le scroll */
.features-anchor {
  position: absolute;
  top: -100px;
  left: 0;
  width: 1px;
  height: 1px;
  visibility: hidden;
}

/* Image et bulles - Style hero section */
.features-image {
  padding: 2.5rem;
  text-align: center;
  position: relative;
  opacity: 0;
  animation: fadeInLeft 0.8s ease-out 0.4s forwards;
}

.features-svg {
  max-width: 110%;
  height: auto;
  filter: drop-shadow(0 10px 30px rgba(0, 102, 204, 0.15));
  position: relative;
  z-index: 2;
  opacity: 0;
  animation: slideInLeft 0.8s ease-out 0.6s forwards;
}

/* Bulles décoratives identiques à la hero section */
.bubble {
  position: absolute;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 50%;
  opacity: 0;
  z-index: 1;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.bubble-1 {
  width: 120px;
  height: 120px;
  top: 15%;
  left: 10%;
  animation: fadeInScale 1s ease-out 0.8s forwards, float 6s ease-in-out infinite 0.8s;
}

.bubble-2 {
  width: 80px;
  height: 80px;
  top: 50%;
  left: 5%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 0.9s forwards, float 6s ease-in-out infinite 0.9s;
}

.bubble-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 15%;
  animation: fadeInScale 1s ease-out 1.0s forwards, float 6s ease-in-out infinite 1.0s;
}

.bubble-4 {
  width: 60px;
  height: 60px;
  top: 25%;
  right: 20%;
  animation: fadeInScale 1s ease-out 1.1s forwards, float 6s ease-in-out infinite 1.1s;
}

/* En-tête de section */
.features-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

/* Contenu des fonctionnalités */
.features-content {
  opacity: 0;
  animation: fadeInRight 0.8s ease-out 0.5s forwards;
}

.features-title {
  font-family: 'Raleway', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.7s forwards;
}

.features-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.8s forwards;
}

/* Cartes de fonctionnalités */
.features-cards {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.9s forwards;
}

.feature-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.feature-card:hover {
  transform: translateY(-2px);
}

.feature-card:nth-child(1) { animation: slideInRight 0.6s ease-out 1.0s forwards; }
.feature-card:nth-child(2) { animation: slideInRight 0.6s ease-out 1.1s forwards; }
.feature-card:nth-child(3) { animation: slideInRight 0.6s ease-out 1.2s forwards; }
.feature-card:nth-child(4) { animation: slideInRight 0.6s ease-out 1.3s forwards; }

.feature-card-inner {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  position: relative;
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
}



.feature-card-inner:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 25px 50px rgba(0, 102, 204, 0.15),
    0 15px 30px rgba(0, 102, 204, 0.1),
    0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.3);
  background: rgba(255, 255, 255, 0.98);
}



.feature-icon {
  flex-shrink: 0;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  border-radius: 16px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(0, 102, 204, 0.1);
  position: relative;
  overflow: hidden;
}

.feature-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.feature-card-inner:hover .feature-icon {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.2) 100%);
  transform: scale(1.1) rotate(5deg);
  border-color: rgba(0, 102, 204, 0.3);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.2);
}

.feature-card-inner:hover .feature-icon::before {
  left: 100%;
}

.feature-content h4 {
  font-family: 'Raleway', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.8rem;
  transition: all 0.3s ease;
  position: relative;
}

.feature-card-inner:hover .feature-content h4 {
  color: var(--primary-blue);
  transform: translateX(5px);
}

.feature-content p {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--dark-gray);
  margin: 0;
  transition: all 0.3s ease;
  opacity: 0.85;
}

.feature-card-inner:hover .feature-content p {
  opacity: 1;
  color: var(--text-dark);
}

/* Animations */
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
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
    opacity: 0.6;
    transform: scale(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .features-section {
    padding: 80px 0;
    padding-top: 100px;
  }
  
  .features-title {
    font-size: 2.2rem;
  }
  
  .features-subtitle {
    font-size: 1rem;
  }
  
  .features-svg {
    max-width: 95%;
  }
  
  .feature-card-inner {
    margin-bottom: 1rem;
  }
  
  .bubble-1, .bubble-2, .bubble-3, .bubble-4 {
    display: none;
  }
}

/* Performance */
.features-section * {
  will-change: transform, opacity;
}
</style>