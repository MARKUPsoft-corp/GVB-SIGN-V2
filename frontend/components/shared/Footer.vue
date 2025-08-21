<template>
  <footer class="footer bg-dark text-light py-5">
    <div class="container">
      <div class="row g-4">
        <!-- Logo et description -->
        <div class="col-lg-4 col-md-6">
          <div class="footer-brand mb-4">
            <NuxtLink to="/" class="d-flex align-items-center text-decoration-none mb-3">
              <div class="logo-container me-3">
                <i class="bi bi-shield-check text-primary fs-2"></i>
              </div>
              <span class="brand-text fw-bold text-light fs-4">GVB Sign</span>
            </NuxtLink>
            <p class="text-light-50 mb-4">
              La solution de signature électronique la plus sécurisée et innovante du marché. 
              Simplifiez vos processus de signature avec notre technologie QR Code avancée.
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

        <!-- Liens produit -->
        <div class="col-lg-2 col-md-6 col-sm-6">
          <h5 class="fw-bold mb-3 text-primary">Produit</h5>
          <ul class="footer-links">
            <li><NuxtLink to="/">Fonctionnalités</NuxtLink></li>
            <li><NuxtLink to="/">Tarifs</NuxtLink></li>
            <li><NuxtLink to="/">Sécurité</NuxtLink></li>
            <li><NuxtLink to="/">Intégrations</NuxtLink></li>
            <li><NuxtLink to="/">API</NuxtLink></li>
          </ul>
        </div>

        <!-- Liens solutions -->
        <div class="col-lg-2 col-md-6 col-sm-6">
          <h5 class="fw-bold mb-3 text-primary">Solutions</h5>
          <ul class="footer-links">
            <li><NuxtLink to="/">Entreprises</NuxtLink></li>
            <li><NuxtLink to="/">PME</NuxtLink></li>
            <li><NuxtLink to="/">Freelances</NuxtLink></li>
            <li><NuxtLink to="/">Juridique</NuxtLink></li>
            <li><NuxtLink to="/">Ressources Humaines</NuxtLink></li>
          </ul>
        </div>

        <!-- Liens support -->
        <div class="col-lg-2 col-md-6 col-sm-6">
          <h5 class="fw-bold mb-3 text-primary">Support</h5>
          <ul class="footer-links">
            <li><NuxtLink to="/">Centre d'aide</NuxtLink></li>
            <li><NuxtLink to="/">Documentation</NuxtLink></li>
            <li><NuxtLink to="/">Contact</NuxtLink></li>
            <li><NuxtLink to="/">Statut des services</NuxtLink></li>
            <li><NuxtLink to="/">Communauté</NuxtLink></li>
          </ul>
        </div>

        <!-- Liens légaux -->
        <div class="col-lg-2 col-md-6 col-sm-6">
          <h5 class="fw-bold mb-3 text-primary">Légal</h5>
          <ul class="footer-links">
            <li><NuxtLink to="/">Confidentialité</NuxtLink></li>
            <li><NuxtLink to="/">Conditions d'utilisation</NuxtLink></li>
            <li><NuxtLink to="/">Cookies</NuxtLink></li>
            <li><NuxtLink to="/">RGPD</NuxtLink></li>
            <li><NuxtLink to="/">Conformité</NuxtLink></li>
          </ul>
        </div>
      </div>

      <!-- Newsletter -->
      <div class="row mt-5 pt-4 border-top border-secondary">
        <div class="col-lg-6">
          <h5 class="fw-bold mb-3 text-primary">Restez informé</h5>
          <p class="text-light-50 mb-3">
            Recevez nos dernières actualités et mises à jour produit directement dans votre boîte mail.
          </p>
          <form class="newsletter-form d-flex gap-2" @submit.prevent="subscribeNewsletter">
            <div class="flex-grow-1">
              <input
                type="email"
                class="form-control form-control-lg"
                placeholder="Votre adresse email"
                v-model="email"
                required
              >
            </div>
            <button type="submit" class="btn btn-primary btn-lg px-4" :disabled="isSubscribing">
              <i class="bi bi-send" v-if="!isSubscribing"></i>
              <div class="spinner-border spinner-border-sm" v-else></div>
            </button>
          </form>
        </div>

        <!-- Contact info -->
        <div class="col-lg-6">
          <h5 class="fw-bold mb-3 text-primary">Contact</h5>
          <div class="contact-info">
            <div class="contact-item d-flex align-items-center mb-2">
              <i class="bi bi-geo-alt me-3 text-primary"></i>
              <span class="text-light-50">123 Avenue de l'Innovation, 75001 Paris, France</span>
            </div>
            <div class="contact-item d-flex align-items-center mb-2">
              <i class="bi bi-telephone me-3 text-primary"></i>
              <span class="text-light-50">+33 1 23 45 67 89</span>
            </div>
            <div class="contact-item d-flex align-items-center">
              <i class="bi bi-envelope me-3 text-primary"></i>
              <span class="text-light-50">contact@gvbsign.com</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Copyright -->
      <div class="row mt-4 pt-4 border-top border-secondary">
        <div class="col-lg-6">
          <p class="text-light-50 mb-0">
            &copy; {{ currentYear }} GVB Sign. Tous droits réservés.
          </p>
        </div>
        <div class="col-lg-6 text-lg-end">
          <p class="text-light-50 mb-0">
            Fait avec <i class="bi bi-heart-fill text-danger"></i> en France
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'

// Newsletter
const email = ref('')
const isSubscribing = ref(false)

const subscribeNewsletter = async () => {
  if (!email.value) return
  
  isSubscribing.value = true
  
  // Simulation d'un appel API
  setTimeout(() => {
    // Ici on ajouterait la logique d'inscription à la newsletter
    console.log('Newsletter subscription:', email.value)
    email.value = ''
    isSubscribing.value = false
  }, 1500)
}

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
