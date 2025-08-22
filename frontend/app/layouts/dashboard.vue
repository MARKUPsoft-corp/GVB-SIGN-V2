<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="dashboard-sidebar">
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
import { ref, computed } from 'vue'

// Store utilisateur simulé (à remplacer par un vrai store plus tard)
const userStore = ref({
  fullName: '',
  email: ''
})

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
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.02) 0%, rgba(0, 123, 255, 0.05) 100%);
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
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 123, 255, 0.08) 100%);
  text-decoration: none;
  transform: translateX(4px);
}

.nav-link:hover::before {
  width: 4px;
}

.nav-link.active {
  color: var(--primary-blue);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-right: none;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.1);
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
  border-top: 1px solid rgba(0, 102, 204, 0.1);
  margin-top: auto;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.02) 0%, rgba(0, 123, 255, 0.05) 100%);
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
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.1);
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
@media (max-width: 992px) {
  .dashboard-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .dashboard-main {
    margin-left: 0;
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
