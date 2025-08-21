<template>
  <nav class="navbar navbar-expand-lg navbar-light fixed-top navbar-animated" :class="{ 'navbar-scrolled': isScrolled }">
    <div class="container">
      <!-- Logo et nom de l'application -->
      <NuxtLink to="/" class="navbar-brand d-flex align-items-center navbar-brand-animated">
        <i class="bi bi-qr-code text-primary-blue fs-2 me-2 navbar-logo"></i>
        <span class="brand-text fw-bold text-primary-blue fs-4 navbar-brand-text">GVB Sign</span>
      </NuxtLink>

      <!-- Bouton mobile -->
      <button
        class="navbar-toggler border-0 d-lg-none"
        type="button"
        @click="toggleSidebar"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Menu de navigation desktop -->
      <div class="collapse navbar-collapse d-none d-lg-block" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-5 navbar-nav-animated">
                      <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ 'active': $route.path === '/' && !isInFeaturesSection }" @click="scrollToTop">
                Accueil
              </button>
            </li>
                      <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ 'active': isInFeaturesSection }" @click="scrollToFeatures">
                Fonctionnalités
              </button>
            </li>
          <li class="nav-item">
            <NuxtLink to="/" class="nav-link fw-500">
              Tarifs
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/" class="nav-link fw-500">
              Contact
            </NuxtLink>
          </li>
        </ul>

        <!-- Boutons d'authentification -->
        <div class="d-flex align-items-center gap-3 navbar-buttons-animated">
          <NuxtLink to="/login" class="btn btn-outline-primary-custom btn-sm">
            <i class="bi bi-box-arrow-in-right me-2"></i>
            Connexion
          </NuxtLink>
          <NuxtLink to="/" class="btn btn-primary-custom btn-sm">
            <i class="bi bi-person-plus me-2"></i>
            Inscription
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>

  <!-- Sidebar Mobile -->
  <div class="mobile-sidebar-overlay" :class="{ 'active': isSidebarOpen }" @click="closeSidebar"></div>
  
  <div class="mobile-sidebar" :class="{ 'active': isSidebarOpen }">
    <div class="sidebar-header">
      <div class="sidebar-brand d-flex align-items-center">
        <i class="bi bi-qr-code text-primary-blue fs-2 me-2"></i>
        <span class="brand-text fw-bold text-primary-blue fs-4">GVB Sign</span>
      </div>
      <button class="sidebar-close" @click="closeSidebar">
        <i class="bi bi-x-lg"></i>
      </button>
    </div>
    
    <div class="sidebar-content">
      <ul class="sidebar-nav">
        <li class="sidebar-nav-item">
          <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ 'active': $route.path === '/' && !isInFeaturesSection }" @click="scrollToTopAndClose">
            <i class="bi bi-house me-3"></i>
            Accueil
          </button>
        </li>
        <li class="sidebar-nav-item">
          <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ 'active': isInFeaturesSection }" @click="scrollToFeaturesAndClose">
            <i class="bi bi-gear me-3"></i>
            Fonctionnalités
          </button>
        </li>
        <li class="sidebar-nav-item">
          <NuxtLink to="/" class="sidebar-nav-link" @click="closeSidebar">
            <i class="bi bi-tag me-3"></i>
            Tarifs
          </NuxtLink>
        </li>
        <li class="sidebar-nav-item">
          <NuxtLink to="/" class="sidebar-nav-link" @click="closeSidebar">
            <i class="bi bi-envelope me-3"></i>
            Contact
          </NuxtLink>
        </li>
      </ul>
      
      <div class="sidebar-actions">
        <NuxtLink to="/login" class="btn btn-outline-primary-custom w-100 mb-3" @click="closeSidebar">
          <i class="bi bi-box-arrow-in-right me-2"></i>
          Connexion
        </NuxtLink>
        <NuxtLink to="/" class="btn btn-primary-custom w-100" @click="closeSidebar">
          <i class="bi bi-person-plus me-2"></i>
          Inscription
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const isSidebarOpen = ref(false)
const isInFeaturesSection = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 80
  
  // Détecter si on est dans la section fonctionnalités
  const featuresSection = document.getElementById('fonctionnalites')
  if (featuresSection) {
    const rect = featuresSection.getBoundingClientRect()
    const windowHeight = window.innerHeight
    
    // On est dans la section fonctionnalités si elle est visible à l'écran
    isInFeaturesSection.value = rect.top < windowHeight * 0.3 && rect.bottom > windowHeight * 0.3
  }
}

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
  // Empêcher le scroll du body quand la sidebar est ouverte
  if (isSidebarOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeSidebar = () => {
  isSidebarOpen.value = false
  document.body.style.overflow = ''
}

// Fonction pour faire défiler vers les fonctionnalités
const scrollToFeatures = () => {
  const featuresSection = document.getElementById('fonctionnalites')
  if (featuresSection) {
    // Calculer la position exacte
    const navbarHeight = 80
    const elementPosition = featuresSection.offsetTop - navbarHeight - 50
    
    // Scroll vers la position calculée
    window.scrollTo({
      top: elementPosition,
      behavior: 'smooth'
    })
  }
}

// Fonction pour faire défiler vers le haut
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// Fonction pour faire défiler vers le haut et fermer la sidebar
const scrollToTopAndClose = () => {
  scrollToTop()
  closeSidebar()
}

// Fonction pour faire défiler et fermer la sidebar
const scrollToFeaturesAndClose = () => {
  scrollToFeatures()
  closeSidebar()
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.navbar {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.6) !important;
  transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transform: translateY(0);
  will-change: transform, background-color, box-shadow;
}

.navbar-animated {
  opacity: 0;
  transform: translateY(-20px);
  animation: slideDownNavbar 0.8s ease-out 0.2s forwards;
}

.navbar-brand-animated {
  opacity: 0;
  animation: fadeInLeft 0.6s ease-out 0.4s forwards;
}

.navbar-logo {
  opacity: 0;
  animation: fadeInScale 0.5s ease-out 0.5s forwards;
}

.navbar-brand-text {
  opacity: 0;
  animation: fadeInLeft 0.6s ease-out 0.6s forwards;
}

.navbar-nav-animated {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out 0.8s forwards;
}

.navbar-nav-animated .nav-item {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

.navbar-nav-animated .nav-item:nth-child(1) { animation-delay: 0.9s; }
.navbar-nav-animated .nav-item:nth-child(2) { animation-delay: 1.0s; }
.navbar-nav-animated .nav-item:nth-child(3) { animation-delay: 1.1s; }
.navbar-nav-animated .nav-item:nth-child(4) { animation-delay: 1.2s; }

.navbar-buttons-animated {
  opacity: 0;
  animation: fadeInRight 0.6s ease-out 1.0s forwards;
}

.navbar-buttons-animated .btn {
  opacity: 0;
  animation: fadeInScale 0.5s ease-out forwards;
}

.navbar-buttons-animated .btn:nth-child(1) { animation-delay: 1.1s; }
.navbar-buttons-animated .btn:nth-child(2) { animation-delay: 1.2s; }

.navbar-scrolled {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(25px) saturate(150%);
  -webkit-backdrop-filter: blur(25px) saturate(150%);
  box-shadow: 
    0 8px 30px rgba(0, 0, 0, 0.12),
    0 2px 15px rgba(0, 102, 204, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  transform: translateY(-2px) scale(0.98);
  animation: slideDown 0.3s ease-out forwards;
}

@keyframes slideDown {
  0% {
    transform: translateY(-10px) scale(0.95);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-2px) scale(0.98);
    opacity: 1;
  }
}

@keyframes slideDownNavbar {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
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

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}



.brand-text {
  font-family: 'Raleway', sans-serif;
  letter-spacing: -0.5px;
  transition: all 0.3s ease;
}

.navbar-scrolled .brand-text {
  transform: scale(0.95);
  color: var(--primary-blue) !important;
}

.nav-link {
  color: var(--text-dark) !important;
  font-weight: 500;
  padding: 0.75rem 1rem !important;
  margin: 0 0.25rem;
  border-radius: 25px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  transform: translateY(0);
  border: 2px solid transparent;
}

.navbar-scrolled .nav-link {
  transform: translateY(-1px);
  font-size: 0.95em;
}

.nav-link:hover,
.nav-link.active {
  color: var(--primary-blue) !important;
  background: rgba(0, 102, 204, 0.15);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(0, 102, 204, 0.3);
  transform: translateY(-2px);
  box-shadow: 
    0 4px 20px rgba(0, 102, 204, 0.2),
    0 2px 8px rgba(0, 102, 204, 0.1);
  font-weight: 600;
}

.nav-link.active {
  background: rgba(0, 102, 204, 0.2);
  border-color: var(--primary-blue);
  box-shadow: 
    0 6px 25px rgba(0, 102, 204, 0.25),
    0 3px 12px rgba(0, 102, 204, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 4px;
  background: var(--gradient-primary);
  border-radius: 3px;
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
}

.navbar-toggler {
  padding: 0.25rem 0.5rem;
}

.navbar-toggler:focus {
  box-shadow: none;
}

.btn-sm {
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  transform: translateY(0) scale(1);
}

.navbar-scrolled .btn-sm {
  transform: translateY(-1px) scale(0.95);
  padding: 0.4rem 0.8rem;
}

.btn-outline-primary-custom {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.btn-outline-primary-custom:hover {
  background: rgba(0, 102, 204, 0.8);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
}

.btn-primary-custom {
  background: rgba(0, 102, 204, 0.8);
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.btn-primary-custom:hover {
  background: rgba(0, 102, 204, 0.9);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* Animation pour le menu mobile */
.navbar-collapse {
  transition: all 0.3s ease;
}

/* Sidebar Mobile */
.mobile-sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 1040;
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-sidebar-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-sidebar-overlay:not(.active) {
  opacity: 0;
  visibility: hidden;
  transition-delay: 0.2s;
}

.mobile-sidebar {
  position: fixed;
  top: 0;
  right: -100%;
  width: 320px;
  height: 100vh;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(25px) saturate(150%);
  -webkit-backdrop-filter: blur(25px) saturate(150%);
  border-left: 1px solid rgba(255, 255, 255, 0.3);
  z-index: 1050;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    -10px 0 30px rgba(0, 0, 0, 0.15),
    inset 1px 0 0 rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
}

.mobile-sidebar.active {
  right: 0;
  transform: translateX(0);
}

.mobile-sidebar:not(.active) {
  right: -100%;
  transform: translateX(100%);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.5s ease;
}

.mobile-sidebar.active .sidebar-header {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.2s;
}

.mobile-sidebar:not(.active) .sidebar-header {
  opacity: 0;
  transform: translateY(-20px);
  transition-delay: 0s;
}

.sidebar-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-dark);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8) rotate(-90deg);
}

.mobile-sidebar.active .sidebar-close {
  opacity: 1;
  transform: scale(1) rotate(0deg);
  transition-delay: 0.3s;
}

.mobile-sidebar:not(.active) .sidebar-close {
  opacity: 0;
  transform: scale(0.8) rotate(-90deg);
  transition-delay: 0s;
}

.mobile-sidebar.active .sidebar-close:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.1) rotate(90deg);
}

.sidebar-content {
  flex: 1;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.mobile-sidebar.active .sidebar-content {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.4s;
}

.mobile-sidebar:not(.active) .sidebar-content {
  opacity: 0;
  transform: translateY(30px);
  transition-delay: 0s;
}

.sidebar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav-item {
  margin-bottom: 0.5rem;
  opacity: 0;
  transform: translateX(-30px);
  transition: all 0.5s ease;
}

.mobile-sidebar.active .sidebar-nav-item {
  opacity: 1;
  transform: translateX(0);
}

.mobile-sidebar.active .sidebar-nav-item:nth-child(1) { transition-delay: 0.5s; }
.mobile-sidebar.active .sidebar-nav-item:nth-child(2) { transition-delay: 0.6s; }
.mobile-sidebar.active .sidebar-nav-item:nth-child(3) { transition-delay: 0.7s; }
.mobile-sidebar.active .sidebar-nav-item:nth-child(4) { transition-delay: 0.8s; }

.mobile-sidebar:not(.active) .sidebar-nav-item {
  opacity: 0;
  transform: translateX(-30px);
  transition-delay: 0s;
}

.sidebar-nav-link {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: var(--text-dark);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
  font-size: 1.1rem;
  border: 2px solid transparent;
  position: relative;
}

.sidebar-nav-link:hover {
  background: rgba(0, 102, 204, 0.15);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(0, 102, 204, 0.3);
  color: var(--primary-blue);
  transform: translateX(15px);
  box-shadow: 
    0 6px 20px rgba(0, 102, 204, 0.2),
    0 3px 10px rgba(0, 102, 204, 0.1);
  font-weight: 600;
}

.sidebar-nav-link.active {
  background: rgba(0, 102, 204, 0.2);
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  transform: translateX(15px);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.25),
    0 4px 15px rgba(0, 102, 204, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  font-weight: 700;
}

.sidebar-nav-link.active::before {
  content: '';
  position: absolute;
  left: -2px;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background: var(--gradient-primary);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.4);
}

.sidebar-nav-link i {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.sidebar-actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.mobile-sidebar.active .sidebar-actions {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.9s;
}

.mobile-sidebar:not(.active) .sidebar-actions {
  opacity: 0;
  transform: translateY(20px);
  transition-delay: 0s;
}

.sidebar-actions .btn {
  opacity: 0;
  transform: scale(0.9);
  transition: all 0.4s ease;
}

.mobile-sidebar.active .sidebar-actions .btn:nth-child(1) {
  opacity: 1;
  transform: scale(1);
  transition-delay: 1.0s;
}

.mobile-sidebar.active .sidebar-actions .btn:nth-child(2) {
  opacity: 1;
  transform: scale(1);
  transition-delay: 1.1s;
}

.mobile-sidebar:not(.active) .sidebar-actions .btn {
  opacity: 0;
  transform: scale(0.9);
  transition-delay: 0s;
}

@media (max-width: 991px) {
  .navbar-nav {
    margin-top: 1rem;
    text-align: center;
  }
  
  .d-flex.gap-3 {
    margin-top: 1rem;
    justify-content: center;
  }
  
  .nav-link.active::after {
    display: none;
  }
}

@media (max-width: 576px) {
  .mobile-sidebar {
    width: 100%;
    right: -100%;
  }
}
</style>
