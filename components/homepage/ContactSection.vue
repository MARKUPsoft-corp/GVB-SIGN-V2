<template>
  <section id="contact" class="contact-section bg-white position-relative py-5">
    <div class="container">
      <!-- En-tête de section - Sur toute la largeur -->
      <div class="row">
        <div class="col-12">
          <div class="contact-header text-center mb-5">
            <h2 class="display-3 fw-bold mb-4 text-dark contact-title">
              Nous <span class="text-primary-blue">Contacter</span>
            </h2>
            <p class="lead mb-0 text-dark contact-subtitle">
              Notre équipe est à votre disposition pour répondre à toutes vos questions.
            </p>
          </div>
        </div>
      </div>

      <!-- Contenu en deux colonnes -->
      <div class="row align-items-center min-vh-75">
        <!-- Colonne gauche - Informations de contact -->
        <div class="col-lg-6 mb-5 mb-lg-0">
          <div class="contact-content">
            <div class="contact-cards">
              <!-- Carte Email -->
              <div class="contact-card mb-3">
                <div class="contact-card-inner">
                  <div class="contact-icon-wrapper">
                    <div class="contact-icon">
                      <i class="bi bi-envelope text-primary-blue fs-2"></i>
                    </div>
                  </div>
                  <div class="contact-info">
                    <h4 class="mb-2">Email</h4>
                    <p class="mb-0">
                      <a href="mailto:contact@gvbsign.cm" class="text-decoration-none">
                        contact@gvbsign.cm
                      </a>
                    </p>
                    <p class="text-muted mb-0">Réponse sous 24h</p>
                  </div>
                </div>
              </div>

              <!-- Carte Téléphone -->
              <div class="contact-card mb-3">
                <div class="contact-card-inner">
                  <div class="contact-icon-wrapper">
                    <div class="contact-icon">
                      <i class="bi bi-telephone text-primary-blue fs-2"></i>
                    </div>
                  </div>
                  <div class="contact-info">
                    <h4 class="mb-2">Téléphone</h4>
                    <p class="mb-0">
                      <a href="tel:+237691234567" class="text-decoration-none">
                        +237 691 234 567
                      </a>
                    </p>
                    <p class="text-muted mb-0">Lun - Ven : 8h - 18h</p>
                  </div>
                </div>
              </div>

              <!-- Carte Adresse -->
              <div class="contact-card mb-3">
                <div class="contact-card-inner">
                  <div class="contact-icon-wrapper">
                    <div class="contact-icon">
                      <i class="bi bi-geo-alt text-primary-blue fs-2"></i>
                    </div>
                  </div>
                  <div class="contact-info">
                    <h4 class="mb-2">Adresse</h4>
                    <p class="mb-0">123 Boulevard de l'Indépendance</p>
                    <p class="mb-0">Douala, Cameroun</p>
                    <p class="text-muted mb-0">Quartier Akwa, Zone 1</p>
                  </div>
                </div>
              </div>

              <!-- Carte Horaires -->
              <div class="contact-card mb-3">
                <div class="contact-card-inner">
                  <div class="contact-icon-wrapper">
                    <div class="contact-icon">
                      <i class="bi bi-clock text-primary-blue fs-2"></i>
                    </div>
                  </div>
                  <div class="contact-info">
                    <h4 class="mb-2">Horaires</h4>
                    <p class="mb-0">Lundi - Vendredi : 8h00 - 18h00</p>
                    <p class="mb-0">Samedi : 9h00 - 15h00</p>
                    <p class="text-muted mb-0">Dimanche : Fermé</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Colonne droite - Image SVG -->
        <div class="col-lg-6">
          <div class="contact-image text-center position-relative">
            <!-- Bulles décoratives -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
            <div class="bubble bubble-4"></div>
            <img src="/contact_us.svg" alt="Nous Contacter - GVB Sign" class="img-fluid contact-svg contact-image-svg">
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

// Animation au montage du composant
onMounted(() => {
  // Les animations sont gérées en CSS
})
</script>

<style scoped>
/* Variables et base */
.contact-section {
  padding: 120px 0;
  padding-top: 140px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

/* Titre de la section */
.contact-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
}

.contact-title {
  font-family: 'Raleway', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -1px;
  text-shadow: 0 2px 10px rgba(0, 102, 204, 0.1);
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.4s forwards;
}

.contact-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.6s forwards;
}

/* Image SVG */
.contact-image {
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.8s forwards;
}

.contact-svg {
  max-width: 115%;
  height: auto;
  filter: drop-shadow(0 15px 40px rgba(0, 102, 204, 0.2));
  position: relative;
  z-index: 2;
}

/* Bulles décoratives */
.bubble {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.08) 100%);
  animation: float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 15%;
  animation-delay: 0s;
}

.bubble-2 {
  width: 80px;
  height: 80px;
  top: 50%;
  right: 5%;
  animation-delay: 2s;
}

.bubble-3 {
  width: 120px;
  height: 120px;
  bottom: 20%;
  right: 20%;
  animation-delay: 4s;
}

.bubble-4 {
  width: 90px;
  height: 90px;
  top: 30%;
  left: 5%;
  animation-delay: 1s;
}

/* Cartes de contact */
.contact-cards {
  opacity: 0;
  animation: slideInLeft 0.8s ease-out 0.7s forwards;
}

.contact-card {
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInUp 0.6s ease-out forwards;
  transition: all 0.3s ease;
}

.contact-card:nth-child(1) { animation-delay: 0.9s; }
.contact-card:nth-child(2) { animation-delay: 1.0s; }
.contact-card:nth-child(3) { animation-delay: 1.1s; }
.contact-card:nth-child(4) { animation-delay: 1.2s; }

.contact-card:hover {
  transform: translateY(-5px);
}

.contact-card-inner {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  padding: 1.5rem;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  position: relative;
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.contact-card-inner:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(0, 102, 204, 0.12),
    0 8px 20px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
  background: rgba(255, 255, 255, 0.98);
}

/* Icônes */
.contact-icon-wrapper {
  flex-shrink: 0;
}

.contact-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(0, 102, 204, 0.1);
  position: relative;
  overflow: hidden;
}

.contact-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.contact-card-inner:hover .contact-icon {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.2) 100%);
  transform: scale(1.1) rotate(5deg);
  border-color: rgba(0, 102, 204, 0.3);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.2);
}

.contact-card-inner:hover .contact-icon::before {
  left: 100%;
}

/* Contenu des cartes */
.contact-info {
  flex: 1;
}

.contact-info h4 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.4rem;
  transition: all 0.3s ease;
}

.contact-card-inner:hover .contact-info h4 {
  color: var(--primary-blue);
  transform: translateX(5px);
}

.contact-info p {
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 0.2rem;
  transition: all 0.3s ease;
}

.contact-info a {
  color: var(--primary-blue);
  font-weight: 600;
  transition: all 0.3s ease;
}

.contact-info a:hover {
  color: var(--primary-blue-dark);
  text-decoration: underline !important;
}

/* Animations */
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
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .contact-section {
    padding-top: 100px;
  }
  
  .contact-title {
    font-size: 2.5rem;
  }
  
  .contact-card-inner {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .contact-info h4 {
    font-size: 1.2rem;
  }
  
  .contact-svg {
    max-width: 90%;
  }
}
</style>
