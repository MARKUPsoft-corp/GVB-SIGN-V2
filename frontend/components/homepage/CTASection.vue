<template>
  <section class="cta-section bg-gradient-primary text-white py-5 position-relative overflow-hidden">
    <!-- Background decorative elements -->
    <div class="cta-bg-elements">
      <div class="floating-circle circle-1"></div>
      <div class="floating-circle circle-2"></div>
      <div class="floating-circle circle-3"></div>
    </div>

    <div class="container position-relative">
      <div class="row justify-content-center">
        <div class="col-lg-8 text-center">
          <div class="cta-content">
            <h2 class="display-4 fw-bold mb-4">
              Prêt à Révolutionner Vos Signatures ?
            </h2>
            <p class="lead mb-5">
              Rejoignez plus de <strong class="text-warning">10,000+</strong> entreprises qui font déjà confiance 
              à GVB Sign pour sécuriser leurs documents importants.
            </p>
            
            <!-- Statistiques -->
            <div class="row g-4 mb-5">
              <div class="col-md-4">
                <div class="stat-item">
                  <div class="stat-number">10K+</div>
                  <div class="stat-label">Entreprises Actives</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="stat-item">
                  <div class="stat-number">1M+</div>
                  <div class="stat-label">Documents Signés</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="stat-item">
                  <div class="stat-number">99.9%</div>
                  <div class="stat-label">Temps de Disponibilité</div>
                </div>
              </div>
            </div>

            <!-- Boutons d'action -->
            <div class="cta-buttons d-flex flex-column flex-md-row justify-content-center gap-3">
              <NuxtLink to="/register" class="btn btn-light btn-lg px-5 py-3 fw-bold">
                <i class="bi bi-rocket-takeoff me-2"></i>
                Commencer Gratuitement
                <small class="d-block text-muted mt-1">Aucune carte de crédit requise</small>
              </NuxtLink>
              <NuxtLink to="/contact" class="btn btn-outline-light btn-lg px-5 py-3 fw-bold">
                <i class="bi bi-headset me-2"></i>
                Parler à un Expert
                <small class="d-block mt-1">Consultation gratuite</small>
              </NuxtLink>
            </div>

            <!-- Garantie -->
            <div class="guarantee-section mt-5 pt-4 border-top border-light border-opacity-25">
              <div class="d-flex align-items-center justify-content-center flex-wrap gap-4">
                <div class="guarantee-item d-flex align-items-center">
                  <i class="bi bi-shield-check me-2 fs-5"></i>
                  <span>Essai gratuit 30 jours</span>
                </div>
                <div class="guarantee-item d-flex align-items-center">
                  <i class="bi bi-arrow-clockwise me-2 fs-5"></i>
                  <span>Annulation à tout moment</span>
                </div>
                <div class="guarantee-item d-flex align-items-center">
                  <i class="bi bi-chat-dots me-2 fs-5"></i>
                  <span>Support 24/7</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-section {
  min-height: 600px;
  display: flex;
  align-items: center;
  position: relative;
}

/* Background Elements */
.cta-bg-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.floating-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 8s ease-in-out infinite;
}

.circle-1 {
  width: 200px;
  height: 200px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 150px;
  height: 150px;
  bottom: -75px;
  right: -75px;
  animation-delay: 3s;
}

.circle-3 {
  width: 100px;
  height: 100px;
  top: 50%;
  right: 10%;
  animation-delay: 6s;
}

/* Content */
.cta-content {
  position: relative;
  z-index: 2;
}

/* Statistics */
.stat-item {
  text-align: center;
  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

.stat-item:nth-child(1) { animation-delay: 0.2s; }
.stat-item:nth-child(2) { animation-delay: 0.4s; }
.stat-item:nth-child(3) { animation-delay: 0.6s; }

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Buttons */
.btn-light {
  background: white;
  color: var(--primary-blue);
  border: none;
  border-radius: 50px;
  font-weight: 700;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-light::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: all 0.5s;
}

.btn-light:hover::before {
  left: 100%;
}

.btn-light:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  color: var(--primary-blue-dark);
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: white;
  background: transparent;
  border-radius: 50px;
  font-weight: 700;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

/* Guarantee Section */
.guarantee-section {
  opacity: 0.9;
}

.guarantee-item {
  font-size: 0.95rem;
  font-weight: 500;
  white-space: nowrap;
}

.guarantee-item i {
  opacity: 0.8;
}

/* Responsive */
@media (max-width: 768px) {
  .stat-number {
    font-size: 2rem;
  }
  
  .stat-label {
    font-size: 0.85rem;
  }
  
  .btn-lg {
    padding: 1rem 2rem !important;
    font-size: 1rem !important;
  }
  
  .guarantee-item {
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
  }
  
  .circle-1,
  .circle-2 {
    display: none;
  }
  
  .circle-3 {
    width: 80px;
    height: 80px;
  }
}

@media (max-width: 576px) {
  .cta-buttons {
    gap: 1rem !important;
  }
  
  .guarantee-section .d-flex {
    flex-direction: column !important;
    align-items: center !important;
  }
}
</style>
