<template>
  <section id="tarifs" class="pricing-section bg-white position-relative py-5">
    <div class="container">
      <!-- En-tête de section - Sur toute la largeur -->
      <div class="row">
        <div class="col-12">
          <div class="pricing-header text-center mb-5">
            <h2 class="display-3 fw-bold mb-4 text-dark pricing-title">
              Des <span class="text-primary-blue">Tarifs</span> 
              <span class="text-primary-blue">Adaptés</span> à vos Besoins
            </h2>
            <p class="lead mb-0 text-dark pricing-subtitle">
              Choisissez le plan qui correspond parfaitement à votre activité. 
              Tous nos plans incluent la sécurité maximale et le support technique.
            </p>
          </div>
        </div>
      </div>

      <!-- Cartes de tarification -->
      <div class="row justify-content-center">
        <!-- Plan Free -->
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="pricing-card">
            <div class="card border-0 shadow-sm pricing-card-inner">
              <div class="card-body p-4 text-center">
                <div class="pricing-badge mb-3">
                  <i class="bi bi-gift text-success fs-2"></i>
                </div>
                <h3 class="pricing-plan-name mb-2">Free</h3>
                <div class="pricing-price mb-4">
                  <span class="price-amount">0</span>
                  <span class="price-currency">FCFA</span>
                  <span class="price-period">/mois</span>
                </div>
                <ul class="pricing-features list-unstyled mb-4">
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    10 signatures/mois
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Stockage 1 GB
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Support email
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-x-circle text-muted me-2"></i>
                    <span class="text-muted">Branding personnalisé</span>
                  </li>
                </ul>
                <button class="btn btn-outline-primary-custom w-100 pricing-btn">
                  Commencer gratuitement
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Plan Pro -->
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="pricing-card">
            <div class="card border-0 shadow-sm pricing-card-inner pricing-popular">
              <div class="popular-badge">
                <span>Plus populaire</span>
              </div>
              <div class="card-body p-4 text-center">
                <div class="pricing-badge mb-3">
                  <i class="bi bi-star-fill text-warning fs-2"></i>
                </div>
                <h3 class="pricing-plan-name mb-2">Pro</h3>
                <div class="pricing-price mb-4">
                  <span class="price-amount">15,000</span>
                  <span class="price-currency">FCFA</span>
                  <span class="price-period">/mois</span>
                </div>
                <ul class="pricing-features list-unstyled mb-4">
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    100 signatures/mois
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Stockage 10 GB
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Support prioritaire
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    API complète
                  </li>
                </ul>
                <button class="btn btn-primary-custom w-100 pricing-btn">
                  Choisir Pro
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Plan Ultra -->
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="pricing-card">
            <div class="card border-0 shadow-sm pricing-card-inner">
              <div class="card-body p-4 text-center">
                <div class="pricing-badge mb-3">
                  <i class="bi bi-rocket-takeoff text-primary-blue fs-2"></i>
                </div>
                <h3 class="pricing-plan-name mb-2">Ultra</h3>
                <div class="pricing-price mb-4">
                  <span class="price-amount">35,000</span>
                  <span class="price-currency">FCFA</span>
                  <span class="price-period">/mois</span>
                </div>
                <ul class="pricing-features list-unstyled mb-4">
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Signatures illimitées
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Stockage 100 GB
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Gestion d'organisation
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Branding personnalisé
                  </li>
                </ul>
                <button class="btn btn-primary-custom w-100 pricing-btn">
                  Choisir Ultra
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Plan Custom -->
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="pricing-card">
            <div class="card border-0 shadow-sm pricing-card-inner">
              <div class="card-body p-4 text-center">
                <div class="pricing-badge mb-3">
                  <i class="bi bi-gear-fill text-dark fs-2"></i>
                </div>
                <h3 class="pricing-plan-name mb-2">Custom</h3>
                <div class="pricing-price mb-4">
                  <span class="price-amount">Sur</span>
                  <span class="price-currency">devis</span>
                  <span class="price-period"></span>
                </div>
                <ul class="pricing-features list-unstyled mb-4">
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Solutions sur mesure
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Intégration dédiée
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Support 24/7
                  </li>
                  <li class="pricing-feature mb-3">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    Formation incluse
                  </li>
                </ul>
                <button class="btn btn-outline-primary-custom w-100 pricing-btn">
                  Nous contacter
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Note de garantie -->
      <div class="row mt-5">
        <div class="col-12 text-center">
          <div class="pricing-guarantee">
            <p class="text-muted mb-0">
              <i class="bi bi-shield-check text-success me-2"></i>
              Tous nos plans incluent une garantie satisfait ou remboursé de 30 jours
            </p>
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
.pricing-section {
  padding: 120px 0;
  padding-top: 140px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  position: relative;
  overflow: hidden;
}

/* En-tête de section */
.pricing-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.pricing-title {
  font-family: 'Raleway', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.5s forwards;
}

.pricing-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--dark-gray);
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.6s forwards;
}

/* Cartes de tarification */
.pricing-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.pricing-card:nth-child(1) { animation: slideInUp 0.6s ease-out 0.8s forwards; }
.pricing-card:nth-child(2) { animation: slideInUp 0.6s ease-out 0.9s forwards; }
.pricing-card:nth-child(3) { animation: slideInUp 0.6s ease-out 1.0s forwards; }
.pricing-card:nth-child(4) { animation: slideInUp 0.6s ease-out 1.1s forwards; }

.pricing-card:hover {
  transform: translateY(-8px);
}

.pricing-card-inner {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  position: relative;
  height: 100%;
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
}

.pricing-card-inner:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 25px 50px rgba(0, 102, 204, 0.15),
    0 15px 30px rgba(0, 102, 204, 0.1),
    0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.3);
  background: rgba(255, 255, 255, 0.98);
}

/* Plan populaire */
.pricing-popular {
  border-color: var(--primary-blue) !important;
  position: relative;
  transform: scale(1.05);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--gradient-primary);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* Badge des plans */
.pricing-badge {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  border-radius: 50%;
  margin: 0 auto;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 2px solid rgba(0, 102, 204, 0.1);
}

.pricing-card-inner:hover .pricing-badge {
  transform: scale(1.1) rotate(10deg);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.2) 100%);
  border-color: rgba(0, 102, 204, 0.3);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.2);
}

/* Nom du plan */
.pricing-plan-name {
  font-family: 'Raleway', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-dark);
  transition: all 0.3s ease;
}

.pricing-card-inner:hover .pricing-plan-name {
  color: var(--primary-blue);
}

/* Prix */
.pricing-price {
  margin-bottom: 2rem;
}

.price-amount {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary-blue);
  font-family: 'Raleway', sans-serif;
}

.price-currency {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary-blue);
  margin-left: 5px;
}

.price-period {
  font-size: 0.9rem;
  color: var(--dark-gray);
  font-weight: 500;
}

/* Fonctionnalités */
.pricing-features {
  margin-bottom: 2rem;
}

.pricing-feature {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--text-dark);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: left;
}

.pricing-card-inner:hover .pricing-feature {
  transform: translateX(5px);
}

/* Boutons */
.pricing-btn {
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 15px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.pricing-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.3);
}

/* Garantie */
.pricing-guarantee {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 1.2s forwards;
  padding: 20px;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 15px;
  max-width: 500px;
  margin: 0 auto;
}

/* Animations */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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

/* Responsive */
@media (max-width: 768px) {
  .pricing-section {
    padding: 80px 0;
    padding-top: 100px;
  }
  
  .pricing-title {
    font-size: 2.2rem;
  }
  
  .pricing-subtitle {
    font-size: 1rem;
  }
  
  .pricing-popular {
    transform: none;
    margin-bottom: 2rem;
  }
  
  .pricing-card-inner {
    margin-bottom: 1rem;
  }
  
  .price-amount {
    font-size: 2rem;
  }
}

/* Performance */
.pricing-section * {
  will-change: transform, opacity;
}
</style>
