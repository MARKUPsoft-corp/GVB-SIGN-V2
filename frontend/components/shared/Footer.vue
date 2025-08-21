<template>
  <footer class="footer bg-dark text-light py-5">
    <div class="container">
      <div class="row g-4">
        <!-- Logo et description -->
        <div class="col-lg-4 col-md-6">
          <div class="footer-brand mb-4 footer-brand-mobile">
            <NuxtLink to="/" class="d-flex align-items-center text-decoration-none mb-3 footer-logo-link">
              <div class="logo-container me-3">
                <i class="bi bi-qr-code text-primary fs-2"></i>
              </div>
              <span class="brand-text fw-bold text-light fs-4">GVB Sign</span>
            </NuxtLink>
            <p class="text-light-50 mb-4">
              La solution de signature électronique la plus sécurisée et innovante du marché. 
              Simplifiez vos processus de signature avec notre technologie QR Code avancée et authentification mobile.
            </p>
            <!-- Réseaux sociaux -->
            <div class="social-links d-flex gap-3">
              <NuxtLink to="/" class="social-link" aria-label="Facebook">
                <i class="bi bi-facebook"></i>
              </NuxtLink>
              <NuxtLink to="/" class="social-link" aria-label="Twitter">
                <i class="bi bi-twitter"></i>
              </NuxtLink>
              <NuxtLink to="/" class="social-link" aria-label="LinkedIn">
                <i class="bi bi-linkedin"></i>
              </NuxtLink>
              <NuxtLink to="/" class="social-link" aria-label="Instagram">
                <i class="bi bi-instagram"></i>
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Menu et Tarification (Desktop) -->
        <div class="col-lg-4 d-none d-lg-block">
          <div class="row">
            <!-- Menu -->
            <div class="col-6">
              <h5 class="fw-bold mb-3 text-primary footer-section-title">Menu</h5>
              <ul class="footer-links">
                <li><NuxtLink to="/">Accueil</NuxtLink></li>
                <li><NuxtLink to="/">Fonctionnalités</NuxtLink></li>
                <li><NuxtLink to="/">Tarifs</NuxtLink></li>
                <li><NuxtLink to="/">Contact</NuxtLink></li>
              </ul>
            </div>

            <!-- Tarification -->
            <div class="col-6">
              <h5 class="fw-bold mb-3 text-primary footer-section-title">Tarification</h5>
              <ul class="footer-links">
                <li><NuxtLink to="/">Plan Free</NuxtLink></li>
                <li><NuxtLink to="/">Plan Pro</NuxtLink></li>
                <li><NuxtLink to="/">Plan Ultra</NuxtLink></li>
                <li><NuxtLink to="/">Plan Custom</NuxtLink></li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Contact (Desktop) -->
        <div class="col-lg-4 d-none d-lg-block">
          <h5 class="fw-bold mb-3 text-primary footer-section-title">Contact</h5>
          <div class="contact-info">
            <div class="contact-item d-flex align-items-center mb-2">
              <div class="contact-icon-wrapper me-3">
                <i class="bi bi-geo-alt text-primary"></i>
              </div>
              <span class="text-light-50">123 Boulevard de l'Indépendance, Douala, Cameroun</span>
            </div>
            <div class="contact-item d-flex align-items-center mb-2">
              <div class="contact-icon-wrapper me-3">
                <i class="bi bi-telephone text-primary"></i>
              </div>
              <span class="text-light-50">+237 691 234 567</span>
            </div>
            <div class="contact-item d-flex align-items-center">
              <div class="contact-icon-wrapper me-3">
                <i class="bi bi-envelope text-primary"></i>
              </div>
              <span class="text-light-50">contact@gvbsign.cm</span>
            </div>
          </div>
        </div>

        <!-- Layout Mobile -->
        <div class="col-12 d-lg-none text-center">
          <!-- Menu et Tarification en deux colonnes -->
          <div class="row mb-4 justify-content-center">
            <!-- Tarification (Gauche) -->
            <div class="col-6 text-center">
              <h5 class="fw-bold mb-3 text-primary footer-section-title">Tarification</h5>
              <ul class="footer-links">
                <li><NuxtLink to="/">Plan Free</NuxtLink></li>
                <li><NuxtLink to="/">Plan Pro</NuxtLink></li>
                <li><NuxtLink to="/">Plan Ultra</NuxtLink></li>
                <li><NuxtLink to="/">Plan Custom</NuxtLink></li>
              </ul>
            </div>

            <!-- Menu (Droite) -->
            <div class="col-6 text-center">
              <h5 class="fw-bold mb-3 text-primary footer-section-title">Menu</h5>
              <ul class="footer-links">
                <li><NuxtLink to="/">Accueil</NuxtLink></li>
                <li><NuxtLink to="/">Fonctionnalités</NuxtLink></li>
                <li><NuxtLink to="/">Tarifs</NuxtLink></li>
                <li><NuxtLink to="/">Contact</NuxtLink></li>
              </ul>
            </div>
          </div>

          <!-- Contact en bas -->
          <div class="row justify-content-center">
            <div class="col-12 text-center">
              <h5 class="fw-bold mb-3 text-primary footer-section-title">Contact</h5>
              <div class="contact-info">
                <div class="contact-item d-flex align-items-center justify-content-center mb-2">
                  <div class="contact-icon-wrapper me-3">
                    <i class="bi bi-geo-alt text-primary"></i>
                  </div>
                  <span class="text-light-50">123 Boulevard de l'Indépendance, Douala, Cameroun</span>
                </div>
                <div class="contact-item d-flex align-items-center justify-content-center mb-2">
                  <div class="contact-icon-wrapper me-3">
                    <i class="bi bi-telephone text-primary"></i>
                  </div>
                  <span class="text-light-50">+237 691 234 567</span>
                </div>
                <div class="contact-item d-flex align-items-center justify-content-center">
                  <div class="contact-icon-wrapper me-3">
                    <i class="bi bi-envelope text-primary"></i>
                  </div>
                  <span class="text-light-50">contact@gvbsign.cm</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Copyright -->
      <div class="row mt-4 pt-4 border-top border-secondary">
        <div class="col-12 text-center">
          <p class="text-light-50 mb-0">
            &copy; {{ currentYear }} GVB Sign. Tous droits réservés.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

// Année courante
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
}

.text-light-50 {
  color: rgba(255, 255, 255, 0.7) !important;
}

.logo-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-container i {
  color: white !important;
}

.brand-text {
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.5px;
}

.footer-section-title {
  position: relative;
  padding-bottom: 8px;
}

.footer-section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-blue);
  border-radius: 2px;
}

/* Centrage sur mobile */
@media (max-width: 991px) {
  .footer-brand-mobile {
    text-align: center;
  }
  
  .footer-brand-mobile .social-links {
    justify-content: center;
  }
  
  .footer-logo-link {
    justify-content: center;
  }
  
  .footer-section-title::after {
    left: 50%;
    transform: translateX(-50%);
  }
}

/* Suppression de l'arrière-plan du logo */
.logo-container {
  background: none !important;
  border: none !important;
  box-shadow: none !important;
}

/* Styles pour les icônes de contact */
.contact-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.05) 100%);
  border: 2px solid rgba(0, 102, 204, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.contact-icon-wrapper:hover {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.1) 100%);
  border-color: rgba(0, 102, 204, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.15);
}

.contact-icon-wrapper i {
  font-size: 1.2rem;
  color: var(--primary-blue);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 400;
}

.footer-links a:hover {
  color: var(--primary-blue);
  transform: translateX(5px);
}

.social-links {
  margin-top: 1rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 1.1rem;
}

.social-link:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 102, 204, 0.3);
}

.newsletter-form .form-control {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.newsletter-form .form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.newsletter-form .form-control:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--primary-blue);
  color: white;
  box-shadow: 0 0 0 0.2rem rgba(0, 102, 204, 0.25);
}

.contact-item {
  font-size: 0.95rem;
}

.contact-item i {
  font-size: 1.1rem;
}

/* Animation pour l'apparition */
.footer {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  animation-delay: 0.2s;
}

@media (max-width: 768px) {
  .newsletter-form {
    flex-direction: column;
  }
  
  .newsletter-form .btn {
    margin-top: 0.5rem;
  }
  
  .contact-item {
    font-size: 0.9rem;
  }
  
  .social-links {
    justify-content: center;
  }
}
</style>
