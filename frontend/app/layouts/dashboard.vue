<template>
  <div class="dashboard-layout">
    <!-- Navbar Mobile -->
    <nav class="dashboard-navbar navbar navbar-expand-lg navbar-light fixed-top d-lg-none" :class="{ 'navbar-scrolled': isScrolled }">
      <div class="container">
        <!-- Logo et nom de l'application -->
        <div class="navbar-brand d-flex align-items-center">
          <img src="/gvb-favicon-1755744029.png" alt="GVB Sign" class="navbar-logo me-2">
          <span class="brand-text fw-bold text-primary-blue fs-4">GVB Sign</span>
        </div>

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
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-5">
            <li class="nav-item">
              <NuxtLink to="/dashboard" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path === '/dashboard' }">
                <i class="bi bi-house-door me-2"></i>
                Tableau de bord
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/documents" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/documents') }">
                <i class="bi bi-file-earmark-text me-2"></i>
                Mes Documents
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/signature" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/signature') }">
                <i class="bi bi-pen me-2"></i>
                Signature
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/qr-codes" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/qr-codes') }">
                <i class="bi bi-qr-code me-2"></i>
                QR Codes
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/templates" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/templates') }">
                <i class="bi bi-file-earmark-plus me-2"></i>
                Modèles
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/history" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/history') }">
                <i class="bi bi-clock-history me-2"></i>
                Historique
              </NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink to="/dashboard/settings" class="nav-link fw-500 border-0 bg-transparent" :class="{ active: $route.path.includes('/settings') }">
                <i class="bi bi-gear me-2"></i>
                Paramètres
              </NuxtLink>
            </li>
          </ul>

          <!-- User info et logout -->
          <div class="d-flex align-items-center gap-3">
            <div class="user-info-navbar">
              <i class="bi bi-person-circle me-2"></i>
              <span class="user-name-navbar">{{ userStore.fullName || 'Utilisateur' }}</span>
            </div>
            <button class="btn btn-outline-danger btn-sm" @click="handleLogout">
              <i class="bi bi-box-arrow-right me-2"></i>
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Sidebar Mobile -->
    <div class="mobile-sidebar-overlay" :class="{ 'active': isSidebarOpen }" @click="closeSidebar"></div>
    
    <div class="mobile-sidebar" :class="{ 'active': isSidebarOpen }">
      <div class="sidebar-header">
        <div class="sidebar-brand d-flex align-items-center">
          <img src="/gvb-favicon-1755744029.png" alt="GVB Sign" class="sidebar-logo me-2">
          <span class="brand-text fw-bold text-primary-blue fs-4">GVB Sign</span>
        </div>
        <button class="sidebar-close" @click="closeSidebar">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      
      <div class="sidebar-content">
        <ul class="sidebar-nav">
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path === '/dashboard' }" @click="closeSidebar">
              <i class="bi bi-house-door me-3"></i>
              Tableau de bord
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/documents" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/documents') }" @click="closeSidebar">
              <i class="bi bi-file-earmark-text me-3"></i>
              Mes Documents
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/signature" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/signature') }" @click="closeSidebar">
              <i class="bi bi-pen me-3"></i>
              Signature
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/qr-codes" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/qr-codes') }" @click="closeSidebar">
              <i class="bi bi-qr-code me-3"></i>
              QR Codes
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/templates" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/templates') }" @click="closeSidebar">
              <i class="bi bi-file-earmark-plus me-3"></i>
              Modèles
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/history" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/history') }" @click="closeSidebar">
              <i class="bi bi-clock-history me-3"></i>
              Historique
            </NuxtLink>
          </li>
          <li class="sidebar-nav-item">
            <NuxtLink to="/dashboard/settings" class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: $route.path.includes('/settings') }" @click="closeSidebar">
              <i class="bi bi-gear me-3"></i>
              Paramètres
            </NuxtLink>
          </li>
        </ul>

        <!-- User info et logout dans sidebar mobile -->
        <div class="sidebar-footer">
          <div class="user-section">
            <div class="user-info">
              <div class="user-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
              <div class="user-details">
                <span class="user-name">{{ userStore.fullName || 'Utilisateur' }}</span>
                <span class="user-email">{{ userStore.email || 'email@example.com' }}</span>
              </div>
            </div>
            <button @click="handleLogout" class="logout-btn">
              <i class="bi bi-box-arrow-right"></i>
              <span>Déconnexion</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sidebar Desktop -->
    <aside class="dashboard-sidebar d-none d-lg-block">
      <!-- Logo et nom de l'app -->
      <div class="sidebar-header">
        <div class="app-brand">
          <img src="/gvb-favicon-1755744029.png" alt="GVB Sign" class="brand-logo">
          <span class="brand-name">GVB Sign</span>
        </div>
      </div>

      <!-- Menu de navigation -->
      <nav class="sidebar-nav">
        <ul class="nav-menu">
          <li class="nav-item">
            <NuxtLink to="/dashboard" class="nav-link" :class="{ active: $route.path === '/dashboard' }">
              <i class="bi bi-house-door"></i>
              <span>Tableau de bord</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/documents" class="nav-link" :class="{ active: $route.path.includes('/documents') }">
              <i class="bi bi-file-earmark-text"></i>
              <span>Mes Documents</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/signature" class="nav-link" :class="{ active: $route.path.includes('/signature') }">
              <i class="bi bi-pen"></i>
              <span>Signature</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/qr-codes" class="nav-link" :class="{ active: $route.path.includes('/qr-codes') }">
              <i class="bi bi-qr-code"></i>
              <span>QR Codes</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/templates" class="nav-link" :class="{ active: $route.path.includes('/templates') }">
              <i class="bi bi-file-earmark-plus"></i>
              <span>Modèles</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/history" class="nav-link" :class="{ active: $route.path.includes('/history') }">
              <i class="bi bi-clock-history"></i>
              <span>Historique</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/dashboard/settings" class="nav-link" :class="{ active: $route.path.includes('/settings') }">
              <i class="bi bi-gear"></i>
              <span>Paramètres</span>
            </NuxtLink>
          </li>
        </ul>
      </nav>

      <!-- Section utilisateur et déconnexion -->
      <div class="sidebar-footer">
        <div class="user-section">
          <div class="user-info">
            <div class="user-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <div class="user-details">
              <span class="user-name">{{ userStore.fullName || 'Utilisateur' }}</span>
              <span class="user-email">{{ userStore.email || 'email@example.com' }}</span>
            </div>
          </div>
          <button @click="handleLogout" class="logout-btn">
            <i class="bi bi-box-arrow-right"></i>
            <span>Déconnexion</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Contenu principal -->
    <main class="dashboard-main">
      <div class="dashboard-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Store utilisateur simulé (à remplacer par un vrai store plus tard)
const userStore = ref({
  fullName: '',
  email: ''
})

// État de la sidebar mobile
const isSidebarOpen = ref(false)
const isScrolled = ref(false)

// Fonction de déconnexion
const handleLogout = async () => {
  try {
    // Appel API de déconnexion
    const response = await fetch('http://127.0.0.1:8000/api/auth/logout/', {
      method: 'POST',
      credentials: 'include'
    })
    
    // Redirection vers la page d'accueil
    await navigateTo('/')
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
    // Redirection même en cas d'erreur
    await navigateTo('/')
  }
}

// Fonctions pour la sidebar mobile
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

// Gestion du scroll pour la navbar
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Vérification initiale
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Récupérer les données utilisateur depuis les query params ou le store
const route = useRoute()
if (route.query.name) {
  userStore.value.fullName = route.query.name
}
if (route.query.email) {
  userStore.value.email = route.query.email
}

// Meta tags pour le dashboard
useHead({
  title: 'Dashboard - GVB Sign',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ],
  link: [
    { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
    { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Raleway:wght@100;200;300;400;500;600;700;800;900&display=swap' }
  ]
})
</script>

<style scoped>
/* Variables CSS intégrées */
:root {
  --primary-blue: #0066cc;
  --primary-blue-dark: #004d99;
  --primary-blue-light: #3385d6;
  --secondary-blue: #f0f8ff;
  --accent-blue: #007bff;
  --white: #ffffff;
  --light-gray: #f8f9fa;
  --dark-gray: #6c757d;
  --text-dark: #2c3e50;
  --gradient-primary: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
  --gradient-hero: linear-gradient(135deg, var(--primary-blue-dark) 0%, var(--primary-blue) 50%, var(--accent-blue) 100%);
  --shadow-light: rgba(0, 102, 204, 0.1);
  --shadow-medium: rgba(0, 102, 204, 0.2);
}

/* Styles de base */
body {
  font-family: 'Raleway', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-dark);
  background-color: var(--white);
}

.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* NAVBAR MOBILE */
.dashboard-navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}

.dashboard-navbar.navbar-scrolled {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.1);
}

.navbar-logo {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.navbar-toggler {
  border: none;
  padding: 0.5rem;
  transition: all 0.3s ease;
}

.navbar-toggler:focus {
  box-shadow: none;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(0, 102, 204, 0.8)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.user-info-navbar {
  display: flex;
  align-items: center;
  color: var(--primary-blue);
  font-weight: 500;
}

.user-name-navbar {
  font-family: 'Raleway', sans-serif;
  font-size: 0.9rem;
}

/* SIDEBAR MOBILE */
.mobile-sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-sidebar-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-sidebar {
  position: fixed;
  top: 0;
  left: -100%;
  width: 300px;
  height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  box-shadow: 4px 0 20px rgba(0, 102, 204, 0.15);
  z-index: 1050;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow-y: auto;
}

.mobile-sidebar.active {
  left: 0;
}

.mobile-sidebar .sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-logo {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.sidebar-close {
  background: none;
  border: none;
  color: var(--primary-blue);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-close:hover {
  background: rgba(0, 102, 204, 0.1);
  transform: scale(1.1);
}

.mobile-sidebar .sidebar-content {
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
}

.mobile-sidebar .sidebar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.sidebar-nav-item {
  margin: 0;
}

.sidebar-nav-link {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: var(--dark-gray);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-family: 'Raleway', sans-serif;
}

.sidebar-nav-link:hover,
.sidebar-nav-link.active {
  color: var(--primary-blue);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 123, 255, 0.08) 100%);
  text-decoration: none;
}

.mobile-sidebar .sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
  margin-top: auto;
}

/* SIDEBAR */
.dashboard-sidebar {
  width: 280px;
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  box-shadow: 
    4px 0 20px rgba(0, 102, 204, 0.08),
    2px 0 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  z-index: 1000;
  border-right: 1px solid rgba(0, 102, 204, 0.1);
}

.sidebar-header {
  padding: 2rem 1.5rem 1.5rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.15);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  position: relative;
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.2), transparent);
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.brand-logo {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
  transition: all 0.3s ease;
}

.brand-logo:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 102, 204, 0.3);
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'Raleway', sans-serif;
  letter-spacing: -0.02em;
}

/* NAVIGATION */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin-bottom: 0.25rem;
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  color: #6c757d;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-family: 'Raleway', sans-serif;
  position: relative;
  border-radius: 0 12px 12px 0;
  margin-right: 0.5rem;
}

.nav-link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 0;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-blue) 100%);
  transition: width 0.3s ease;
  border-radius: 0 12px 12px 0;
}

.nav-link:hover {
  color: var(--primary-blue);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 123, 255, 0.18) 100%);
  text-decoration: none;
  transform: translateX(4px);
}

.nav-link:hover::before {
  width: 4px;
}

.nav-link.active {
  color: var(--primary-blue);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 123, 255, 0.22) 100%);
  border-right: none;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.nav-link.active::before {
  width: 4px;
}

.nav-link i {
  font-size: 1.125rem;
  width: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.nav-link:hover i,
.nav-link.active i {
  transform: scale(1.1);
}

/* FOOTER SIDEBAR */
.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(0, 102, 204, 0.15);
  margin-top: auto;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  position: relative;
}

.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.2), transparent);
}

.user-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.15);
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
}

.user-avatar {
  color: var(--primary-blue);
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0, 102, 204, 0.2));
  transition: all 0.3s ease;
}

.user-info:hover .user-avatar {
  transform: scale(1.05);
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Raleway', sans-serif;
}

.user-email {
  font-size: 0.75rem;
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Raleway', sans-serif;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.05) 0%, rgba(220, 53, 69, 0.1) 100%);
  border: 1px solid rgba(220, 53, 69, 0.3);
  color: #dc3545;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  width: 100%;
  justify-content: center;
  font-family: 'Raleway', sans-serif;
  position: relative;
  overflow: hidden;
}

.logout-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  border-color: #dc3545;
}

.logout-btn:hover::before {
  left: 100%;
}

.logout-btn:active {
  transform: translateY(-1px);
}

/* CONTENU PRINCIPAL */
.dashboard-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
}

.dashboard-content {
  padding: 2rem;
  min-height: 100vh;
}

/* RESPONSIVE */
@media (max-width: 991px) {
  .dashboard-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .dashboard-main {
    margin-left: 0;
    padding-top: 5rem; /* Espace pour la navbar fixe */
  }
  
  .dashboard-content {
    padding: 1rem;
  }
}

/* ANIMATIONS */
.nav-link {
  opacity: 0;
  animation: slideInLeft 0.5s ease-out forwards;
}

.nav-item:nth-child(1) .nav-link { animation-delay: 0.1s; }
.nav-item:nth-child(2) .nav-link { animation-delay: 0.2s; }
.nav-item:nth-child(3) .nav-link { animation-delay: 0.3s; }
.nav-item:nth-child(4) .nav-link { animation-delay: 0.4s; }
.nav-item:nth-child(5) .nav-link { animation-delay: 0.5s; }
.nav-item:nth-child(6) .nav-link { animation-delay: 0.6s; }
.nav-item:nth-child(7) .nav-link { animation-delay: 0.7s; }

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.sidebar-header {
  opacity: 0;
  animation: fadeInDown 0.8s ease-out 0.2s forwards;
}

.sidebar-footer {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
}

@keyframes fadeInDown {
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
</style>
