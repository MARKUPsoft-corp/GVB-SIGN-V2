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
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'dashboard' }" @click="setActivePage('dashboard')">
                <i class="bi bi-house-door me-2"></i>
                Tableau de bord
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'documents' }" @click="setActivePage('documents')">
                <i class="bi bi-file-earmark-text me-2"></i>
                Mes Documents
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'signatures' }" @click="setActivePage('signatures')">
                <i class="bi bi-pen me-2"></i>
                Signatures
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'qr-codes' }" @click="setActivePage('qr-codes')">
                <i class="bi bi-qr-code me-2"></i>
                QR Codes
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'templates' }" @click="setActivePage('templates')">
                <i class="bi bi-file-earmark-plus me-2"></i>
                Modèles
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'history' }" @click="setActivePage('history')">
                <i class="bi bi-clock-history me-2"></i>
                Historique
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-500 border-0 bg-transparent" :class="{ active: activePage === 'settings' }" @click="setActivePage('settings')">
                <i class="bi bi-gear me-2"></i>
                Paramètres
              </button>
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
      <!-- Header fixe -->
      <div class="sidebar-header">
        <div class="sidebar-brand d-flex align-items-center">
          <img src="/gvb-favicon-1755744029.png" alt="GVB Sign" class="sidebar-logo me-2">
          <span class="brand-text fw-bold text-primary-blue fs-4">GVB Sign</span>
        </div>
        <button class="sidebar-close" @click="closeSidebar">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      
      <!-- Navigation scrollable -->
      <nav class="sidebar-nav">
        <ul class="sidebar-nav">
          <li class="sidebar-nav-item">
            <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: activePage === 'dashboard' }" @click="setActivePage('dashboard')">
              <i class="bi bi-house-door me-3"></i>
              Tableau de bord
            </button>
          </li>
          <li class="sidebar-nav-item">
            <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: activePage === 'documents' }" @click="setActivePage('documents')">
              <i class="bi bi-file-earmark-text me-3"></i>
              Mes Documents
            </button>
          </li>
          <li class="sidebar-nav-item">
            <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: activePage === 'signatures' }" @click="setActivePage('signatures')">
              <i class="bi bi-pen me-3"></i>
              Signatures
            </button>
          </li>
          <li class="sidebar-nav-item" v-if="hasOrganization">
            <button class="sidebar-nav-link border-0 bg-transparent w-100 text-start" :class="{ active: activePage === 'organization' }" @click="setActivePage('organization')">
              <i class="bi bi-building me-3"></i>
              Organisation
            </button>
          </li>
        </ul>
      </nav>

      <!-- Footer fixe -->
      <div class="sidebar-footer">
        <div class="user-section">
          <div class="user-info" @click="openProfileModalFromMobile" role="button">
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

    <!-- Sidebar Desktop -->
    <aside class="dashboard-sidebar d-none d-lg-block" :class="{ 'collapsed': isSidebarCollapsed }">
      <!-- Logo et nom de l'app -->
      <div class="sidebar-header">
        <div class="app-brand">
          <img src="/gvb-favicon-1755744029.png" alt="GVB Sign" class="brand-logo">
          <span class="brand-name" v-show="!isSidebarCollapsed">GVB Sign</span>
        </div>
      </div>

      <!-- Menu de navigation -->
      <nav class="sidebar-nav">
        <ul class="nav-menu">
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activePage === 'dashboard' }" @click="setActivePage('dashboard')">
              <i class="bi bi-house-door"></i>
              <span v-show="!isSidebarCollapsed">Tableau de bord</span>
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activePage === 'documents' }" @click="setActivePage('documents')">
              <i class="bi bi-file-earmark-text"></i>
              <span v-show="!isSidebarCollapsed">Mes Documents</span>
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activePage === 'signatures' }" @click="setActivePage('signatures')">
              <i class="bi bi-pen"></i>
              <span v-show="!isSidebarCollapsed">Signatures</span>
            </button>
          </li>
          <li class="nav-item" v-if="hasOrganization">
            <button class="nav-link" :class="{ active: activePage === 'organization' }" @click="setActivePage('organization')">
              <i class="bi bi-building"></i>
              <span v-show="!isSidebarCollapsed">Organisation</span>
            </button>
          </li>
        </ul>
      </nav>

      <!-- Section utilisateur et déconnexion -->
      <div class="sidebar-footer">
        <div class="user-section">
          <div class="user-info" @click="toggleProfileModal" role="button">
            <div class="user-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <div class="user-details" v-show="!isSidebarCollapsed">
              <span class="user-name">{{ userStore.fullName || 'Utilisateur' }}</span>
              <span class="user-email">{{ userStore.email || 'email@example.com' }}</span>
            </div>
          </div>
          <button @click="handleLogout" class="logout-btn">
            <i class="bi bi-box-arrow-right"></i>
            <span v-show="!isSidebarCollapsed">Déconnexion</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Modale de profil utilisateur -->
    <div v-if="isProfileModalOpen" class="profile-modal-overlay" @click="closeProfileModal">
      <div class="profile-modal" @click.stop>
        <!-- Menu latéral (desktop seulement) -->
        <div class="profile-menu d-none d-lg-block" :data-active-tab="activeProfileTab">
          <div class="profile-menu-header">
            <div class="profile-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <h6>Mon Profil</h6>
          </div>
          <ul class="profile-nav">
            <li class="profile-nav-item" :class="{ active: activeProfileTab === 'profile' }" @click="setActiveProfileTab('profile')">
              <i class="bi bi-person"></i>
              <span>Profil</span>
            </li>
            <li class="profile-nav-item" :class="{ active: activeProfileTab === 'certificate' }" @click="setActiveProfileTab('certificate')">
              <i class="bi bi-shield-fill-check"></i>
              <span>Certificat</span>
            </li>
            <li class="profile-nav-item" :class="{ active: activeProfileTab === 'security' }" @click="setActiveProfileTab('security')">
              <i class="bi bi-shield-lock"></i>
              <span>Sécurité</span>
            </li>
            <li class="profile-nav-item" :class="{ active: activeProfileTab === 'preferences' }" @click="setActiveProfileTab('preferences')">
              <i class="bi bi-gear"></i>
              <span>Préférences</span>
            </li>
            <li class="profile-nav-item" :class="{ active: activeProfileTab === 'billing' }" @click="setActiveProfileTab('billing')">
              <i class="bi bi-credit-card"></i>
              <span>Facturation</span>
            </li>
          </ul>
        </div>
        
        <!-- Contenu principal -->
        <div class="profile-content">
          <div class="profile-content-header">
            <h5>
              <i :class="getProfileTabIcon()"></i>
              {{ getProfileTabTitle() }}
            </h5>
            <button class="close-btn" @click="closeProfileModal">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          
          <div class="profile-content-body">
            <!-- Contenu Profil -->
            <div v-if="activeProfileTab === 'profile'" class="tab-content">
              <div class="form-group">
                <label>Nom complet</label>
                <input type="text" class="form-control" :value="userStore.fullName" readonly>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-control" :value="userStore.email" readonly>
              </div>
              <div class="form-group">
                <label>Statut</label>
                <span class="badge bg-success">Actif</span>
              </div>
            </div>
            
            <!-- Contenu Sécurité -->
            <div v-if="activeProfileTab === 'security'" class="tab-content">
              <div class="security-item">
                <div class="security-info">
                  <h6>Mot de passe</h6>
                  <p class="text-muted">Dernière modification : il y a 2 semaines</p>
                </div>
                <button class="btn btn-outline-primary btn-sm">Modifier</button>
              </div>
              <div class="security-item">
                <div class="security-info">
                  <h6>Authentification à deux facteurs</h6>
                  <p class="text-muted">Non configurée</p>
                </div>
                <button class="btn btn-primary btn-sm">Activer</button>
              </div>
            </div>
            
            <!-- Contenu Préférences -->
            <div v-if="activeProfileTab === 'preferences'" class="tab-content">
              <div class="preference-item">
                <div class="preference-info">
                  <h6>Langue</h6>
                  <p class="text-muted">Français</p>
                </div>
                <select class="form-select form-select-sm">
                  <option selected>Français</option>
                  <option>English</option>
                  <option>Español</option>
                </select>
              </div>
              <div class="preference-item">
                <div class="preference-info">
                  <h6>Notifications email</h6>
                  <p class="text-muted">Recevoir les notifications par email</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" checked>
                </div>
              </div>
            </div>
            
            <!-- Contenu Facturation -->
            <div v-if="activeProfileTab === 'billing'" class="tab-content">
              <div class="billing-info">
                <h6>Plan actuel</h6>
                <div class="plan-card">
                  <div class="plan-details">
                    <h5>Plan Gratuit</h5>
                    <p class="text-muted">5 signatures par mois</p>
                  </div>
                  <button class="btn btn-primary btn-sm">Mettre à niveau</button>
                </div>
              </div>
            </div>
            
            <!-- Contenu Certificat -->
            <div v-if="activeProfileTab === 'certificate'" class="tab-content">
              <!-- Section d'importation - affichée seulement s'il n'y a pas de certificat -->
              <div v-if="!certificateInfo" class="certificate-upload-section">
                <h6>Importer votre certificat</h6>
                <div class="certificate-action-item">
                  <div class="action-info">
                    <h6>Certificat de signature</h6>
                    <p class="text-muted certificate-description">
                      Importez votre certificat PFX ou P12 pour signer vos documents.
                    </p>
                  </div>
                  <div class="action-button">
                    <button class="btn btn-outline-primary btn-sm" @click="openCertificateModal">
                      <i class="bi bi-upload me-2"></i>
                      Importer
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="certificate-info-section" :class="{ 'certificate-info-section-top': certificateInfo }">
                <h6>Informations du certificat</h6>
                <div v-if="certificateInfo" class="certificate-status-card certificate-imported" :class="{ 'certificate-expired': !certificateInfo.validity.isValid }">
                  <div class="certificate-header">
                    <div class="certificate-status-icon">
                      <i :class="certificateInfo.validity.isValid ? 'bi bi-shield-check' : 'bi bi-shield-x'"></i>
                    </div>
                    <div class="certificate-title">
                      <h6 class="mb-0">Certificat importé</h6>
                      <span class="certificate-subtitle" :class="certificateInfo.validity.isValid ? 'text-success' : 'text-danger'">
                        {{ certificateInfo.validity.isValid ? 'Prêt pour la signature' : 'Ne peut pas être utilisé - Certificat expiré' }}
                      </span>
                    </div>
                    <div class="certificate-status-badge">
                      <span :class="certificateInfo.validity.isValid ? 'badge bg-success' : 'badge bg-danger'">
                        {{ certificateInfo.validity.isValid ? 'Valide' : 'Expiré' }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="certificate-content">
                    <div class="certificate-section">
                      <h6 class="section-title">
                        <i class="bi bi-person me-2"></i>
                        Informations du titulaire
                      </h6>
                      <div class="info-grid">
                        <div class="info-item">
                          <span class="info-label">Nom</span>
                          <span class="info-value">{{ certificateInfo.subject.commonName }}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Organisation</span>
                          <span class="info-value">{{ certificateInfo.subject.organization }}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Numéro de série</span>
                          <span class="info-value serial-number">{{ certificateInfo.serialNumber }}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Pays</span>
                          <span class="info-value">{{ certificateInfo.subject.country }}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="certificate-section">
                      <h6 class="section-title">
                        <i class="bi bi-building me-2"></i>
                        Autorité de certification
                      </h6>
                      <div class="info-grid">
                        <div class="info-item">
                          <span class="info-label">Émetteur</span>
                          <span class="info-value">{{ certificateInfo.issuer.commonName }}</span>
                        </div>
                        <div class="info-item">
                          <span class="info-label">Organisation</span>
                          <span class="info-value">{{ certificateInfo.issuer.organization }}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="certificate-section">
                      <h6 class="section-title">
                        <i class="bi bi-calendar-check me-2"></i>
                        Validité
                      </h6>
                      <div class="validity-info">
                        <div class="validity-item">
                          <span class="validity-label">Émis le</span>
                          <span class="validity-date">{{ new Date(certificateInfo.validity.notBefore).toLocaleDateString('fr-FR') }}</span>
                        </div>
                        <div class="validity-item">
                          <span class="validity-label">Expire le</span>
                          <span class="validity-date" :class="certificateInfo.validity.isValid ? 'text-success' : 'text-danger'">
                            {{ new Date(certificateInfo.validity.notAfter).toLocaleDateString('fr-FR') }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="certificate-section">
                      <h6 class="section-title">
                        <i class="bi bi-key me-2"></i>
                        Clés et sécurité
                      </h6>
                      <div class="security-info">
                        <div class="security-item">
                          <i class="bi bi-check-circle-fill text-success me-2"></i>
                          <span>Clé privée disponible</span>
                        </div>
                        <div class="security-item">
                          <i class="bi bi-check-circle-fill text-success me-2"></i>
                          <span>Clé publique disponible</span>
                        </div>
                        <div class="security-item">
                          <i class="bi bi-shield-lock me-2"></i>
                          <span>Algorithme: {{ certificateInfo.signatureAlgorithm }}</span>
                        </div>
                        <div v-if="!certificateInfo.validity.isValid" class="security-item security-warning">
                          <i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>
                          <span class="text-warning fw-bold">Les clés ne peuvent pas être utilisées - Certificat expiré</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="certificate-section">
                      <h6 class="section-title">
                        <i class="bi bi-fingerprint me-2"></i>
                        Empreinte du certificat
                      </h6>
                      <div class="fingerprint-container">
                        <code class="fingerprint-code">{{ certificateInfo.fingerprint }}</code>
                        <button class="btn btn-sm btn-outline-secondary copy-btn" @click="copyFingerprint">
                          <i class="bi bi-clipboard"></i>
                        </button>
                      </div>
                    </div>
                    
                    <div class="certificate-section">
                      <div class="certificate-actions">
                        <button class="btn btn-danger btn-sm remove-certificate-btn" @click="removeCertificate">
                          <i class="bi bi-trash me-2"></i>
                          Supprimer le certificat
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="certificate-status-card certificate-empty">
                  <div class="certificate-empty-content">
                    <div class="certificate-empty-icon">
                      <i class="bi bi-shield-slash text-muted"></i>
                    </div>
                    <div class="certificate-empty-text">
                      <h6 class="mb-2">Aucun certificat importé</h6>
                      <p class="text-muted mb-0">
                        Importez un certificat PFX ou P12 pour pouvoir signer vos documents numériquement.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Barre de navigation mobile -->
          <div class="mobile-nav-bar d-lg-none" :data-active-tab="activeProfileTab">
            <div class="mobile-nav-item" :class="{ active: activeProfileTab === 'profile' }" @click="setActiveProfileTab('profile')">
              <i class="bi bi-person"></i>
              <span>Profil</span>
            </div>
            <div class="mobile-nav-item" :class="{ active: activeProfileTab === 'certificate' }" @click="setActiveProfileTab('certificate')">
              <i class="bi bi-shield-fill-check"></i>
              <span>Certificat</span>
            </div>
            <div class="mobile-nav-item" :class="{ active: activeProfileTab === 'security' }" @click="setActiveProfileTab('security')">
              <i class="bi bi-shield-lock"></i>
              <span>Sécurité</span>
            </div>
            <div class="mobile-nav-item" :class="{ active: activeProfileTab === 'preferences' }" @click="setActiveProfileTab('preferences')">
              <i class="bi bi-gear"></i>
              <span>Préférences</span>
            </div>
            <div class="mobile-nav-item" :class="{ active: activeProfileTab === 'billing' }" @click="setActiveProfileTab('billing')">
              <i class="bi bi-credit-card"></i>
              <span>Facturation</span>
            </div>
          </div>
        </div>
        
        <!-- Modale d'import de certificat (enfant de la modale du profil) -->
        <div v-if="isCertificateModalOpen" class="certificate-modal-overlay" @click="closeCertificateModal">
          <div class="certificate-modal" @click.stop>
            <div class="certificate-modal-header">
              <h6>
                <i class="bi bi-shield-fill-check"></i>
                Importer un certificat
              </h6>
              <button class="close-btn" @click="closeCertificateModal">
                <i class="bi bi-x"></i>
              </button>
            </div>
            
            <div class="certificate-modal-body">
              <!-- Affichage des erreurs -->
              <div v-if="certificateError" class="alert alert-danger mb-3">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ certificateError }}
              </div>
              
              <!-- Zone d'import - masquée si fichier déjà sélectionné -->
              <div v-if="!selectedCertificateFile" class="certificate-upload-zone">
                <div class="drop-zone" 
                     :class="{ 'dragging': isDraggingCertificate }"
                     @dragenter="handleDragEnter"
                     @dragover="handleDragOver"
                     @dragleave="handleDragLeave"
                     @drop="handleDrop">
                  <input 
                    type="file" 
                    id="certificate-file" 
                    accept=".pfx,.p12" 
                    @change="handleCertificateFileSelect" 
                    class="file-input"
                    ref="certificateFileInput"
                  >
                  <div class="drop-zone-content">
                    <i class="bi bi-cloud-upload"></i>
                    <p>Glissez-déposez votre fichier .pfx/.p12</p>
                  </div>
                </div>
              </div>
              
              <!-- Fichier sélectionné avec possibilité de suppression -->
              <div v-if="selectedCertificateFile" class="selected-file-container">
                <div class="selected-file">
                  <div class="selected-file-info">
                    <i class="bi bi-shield-check text-success"></i>
                    <span class="selected-file-name">{{ selectedCertificateFile.name }}</span>
                  </div>
                  <button @click="removeCertificateFile" class="remove-file-btn" title="Supprimer le fichier">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>

              <!-- Section mot de passe - affichée seulement si fichier sélectionné -->
              <div v-if="selectedCertificateFile" class="certificate-password-section">
                <div class="password-input-group">
                  <input 
                    v-model="certificatePassword"
                    :type="showCertificatePassword ? 'text' : 'password'"
                    placeholder="Mot de passe du certificat"
                    class="password-input"
                  >
                  <button @click="toggleCertificatePasswordVisibility" class="password-toggle">
                    <i :class="showCertificatePassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>
              

            </div>
            
            <div class="certificate-modal-footer">
              <button @click="closeCertificateModal" class="btn btn-outline-secondary btn-sm">
                Annuler
              </button>
              <button 
                @click="importCertificate" 
                :disabled="!selectedCertificateFile || !certificatePassword"
                class="btn btn-primary btn-sm"
              >
                Importer
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenu principal -->
    <main class="dashboard-main">
      <!-- Bouton toggle sidebar (desktop seulement) -->
      <div class="sidebar-toggle-container d-none d-lg-block">
        <button class="sidebar-toggle" @click="toggleSidebarCollapse">
          <i class="bi" :class="isSidebarCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
        </button>
      </div>
      
      <div class="dashboard-content">
        <!-- Affichage conditionnel des pages -->
        <div v-if="activePage === 'dashboard'">
          <slot />
        </div>
        <div v-else-if="activePage === 'documents'">
          <DocumentsPage 
            @navigate-to-signature="handleSignatureNavigation" 
            @open-profile-modal="handleOpenProfileModal" 
          />
        </div>
        <div v-else>
          <div class="page-placeholder">
            <div class="text-center py-5">
              <i class="bi bi-gear fs-1 text-muted mb-3"></i>
              <h4 class="text-muted">Page en développement</h4>
              <p class="text-muted">Cette section sera bientôt disponible.</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import DocumentsPage from '../../components/dashboard/DocumentsPage.vue'
import SignImmediatelyPage from '../../components/dashboard/SignImmediatelyPage.vue'
import { CertificateService } from '../../services/CertificateService'

// Store d'authentification (côté client seulement)
const authStore = process.client ? useAuthStore() : null

// Store utilisateur avec les données du store d'authentification
const userStore = computed(() => ({
  fullName: authStore?.user?.full_name || 'Utilisateur',
  email: authStore?.user?.email || 'email@example.com'
}))

// État de la sidebar mobile
const isSidebarOpen = ref(false)
const isScrolled = ref(false)
const isSidebarCollapsed = ref(false)

// État des organisations de l'utilisateur
const hasOrganization = ref(false)

// État de la modale de profil
const isProfileModalOpen = ref(false)
const activeProfileTab = ref('profile')

// Service de certificat
const certificateService = new CertificateService()

// État de la modale de certificat
const isCertificateModalOpen = ref(false)
const selectedCertificateFile = ref(null)
const certificatePassword = ref('')
const showCertificatePassword = ref(false)
const isDraggingCertificate = ref(false)
const certificateFileInput = ref(null)

// État des informations du certificat
const certificateInfo = ref(null)
const certificateError = ref(null)

// État de la navigation du dashboard
const activePage = ref('dashboard')

// Fonctions de navigation
const setActivePage = (page) => {
  activePage.value = page
  closeSidebar()
}

// Fonction pour gérer la navigation vers la signature
const handleSignatureNavigation = (type) => {
  console.log('Navigation vers signature:', type)
  // Pour l'instant, nous allons directement modifier DocumentsPage pour inclure SignImmediatelyPage
  // La logique sera dans DocumentsPage pour afficher SignImmediatelyPage
}

// Fonction pour ouvrir la modale de profil depuis DocumentsPage
const handleOpenProfileModal = (tab = 'profile') => {
  // Ouvrir la modale de profil
  isProfileModalOpen.value = true
  
  // Définir l'onglet actif si spécifié
  if (tab) {
    activeProfileTab.value = tab
  }
  
  // Bloquer le scroll du body
  document.body.style.overflow = 'hidden'
}

// Fonction de déconnexion
const handleLogout = async () => {
  // Nettoyer les données du certificat
  certificateService.clearCertificate()
  certificateInfo.value = null
  
  if (authStore) {
    await authStore.logout()
  }
  // Redirection vers la page de connexion
  await navigateTo('/login')
}

// Fonctions pour la sidebar mobile
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

// Fonction pour replier/déplier la sidebar desktop
const toggleSidebarCollapse = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Fonction pour vérifier si l'utilisateur a une organisation
const checkUserOrganizations = async () => {
  try {
    // Pour l'instant, on simule la vérification
    // Plus tard, on fera un appel API pour vérifier les organisations de l'utilisateur
    const userHasOrganization = localStorage.getItem('user_has_organization') === 'true'
    hasOrganization.value = userHasOrganization
    
    console.log('Vérification des organisations:', hasOrganization.value)
  } catch (error) {
    console.error('Erreur lors de la vérification des organisations:', error)
    hasOrganization.value = false
  }
}

// Fonctions pour la modale de profil
const toggleProfileModal = () => {
  isProfileModalOpen.value = !isProfileModalOpen.value
  
  // Bloquer/débloquer le scroll du body
  if (isProfileModalOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
  
  // Préserver l'état de la sidebar - ne pas changer isSidebarCollapsed
}

// Fonction pour ouvrir la modale depuis la sidebar mobile
const openProfileModalFromMobile = () => {
  closeSidebar()
  // Petit délai pour s'assurer que la sidebar se ferme avant d'ouvrir la modale
  setTimeout(() => {
    toggleProfileModal()
  }, 100)
}

const closeProfileModal = () => {
  isProfileModalOpen.value = false
  document.body.style.overflow = ''
}

// Fonctions pour la modale de certificat
const openCertificateModal = (event) => {
  // La modale sera centrée automatiquement par l'overlay
  isCertificateModalOpen.value = true
}

const closeCertificateModal = () => {
  isCertificateModalOpen.value = false
  selectedCertificateFile.value = null
  certificatePassword.value = ''
  showCertificatePassword.value = false
  document.body.style.overflow = ''
}

const handleCertificateFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && (file.name.endsWith('.pfx') || file.name.endsWith('.p12'))) {
    selectedCertificateFile.value = file
  } else {
    alert('Veuillez sélectionner un fichier certificat valide (.pfx ou .p12).')
  }
}

const removeCertificateFile = () => {
  selectedCertificateFile.value = null
  if (certificateFileInput.value) {
    certificateFileInput.value.value = ''
  }
}

const toggleCertificatePasswordVisibility = () => {
  showCertificatePassword.value = !showCertificatePassword.value
}

const handleDragEnter = (e) => {
  e.preventDefault()
  isDraggingCertificate.value = true
}

const handleDragOver = (e) => {
  e.preventDefault()
}

const handleDragLeave = (e) => {
  e.preventDefault()
  isDraggingCertificate.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDraggingCertificate.value = false
  
  const files = e.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    if (file.name.endsWith('.pfx') || file.name.endsWith('.p12')) {
      selectedCertificateFile.value = file
    } else {
      alert('Veuillez sélectionner un fichier certificat valide (.pfx ou .p12).')
    }
  }
}

const importCertificate = async () => {
  try {
    certificateError.value = null
    
    if (!selectedCertificateFile.value || !certificatePassword.value) {
      throw new Error('Veuillez sélectionner un fichier et entrer le mot de passe')
    }
    
    // Décoder le certificat avec le service
    const info = await certificateService.decodeCertificate(
      selectedCertificateFile.value, 
      certificatePassword.value
    )
    
    // Mettre à jour l'état
    certificateInfo.value = info
    
    // Fermer la modale
    closeCertificateModal()
    
    // Réinitialiser les champs
    selectedCertificateFile.value = null
    certificatePassword.value = ''
    
    console.log('Certificat importé avec succès:', info)
    
  } catch (error) {
    console.error('Erreur lors de l\'import du certificat:', error)
    certificateError.value = error.message
  }
}

const setActiveProfileTab = (tab) => {
  activeProfileTab.value = tab
}

const getProfileTabTitle = () => {
  const titles = {
    profile: 'Informations du profil',
    certificate: 'Certificat de signature',
    security: 'Sécurité du compte',
    preferences: 'Préférences utilisateur',
    billing: 'Facturation et abonnement'
  }
  return titles[activeProfileTab.value] || 'Profil'
}

const getProfileTabIcon = () => {
  const icons = {
    profile: 'bi bi-person',
    certificate: 'bi bi-shield-fill-check',
    security: 'bi bi-shield-lock',
    preferences: 'bi bi-gear',
    billing: 'bi bi-credit-card'
  }
  return icons[activeProfileTab.value] || 'bi bi-person'
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
  // Restaurer le scroll du body au cas où la modale était ouverte
  document.body.style.overflow = ''
})

// Initialiser l'authentification au montage
onMounted(async () => {
  if (authStore) {
    await authStore.initAuth()
  }
  
  // Initialiser le service de certificat
  certificateService.initialize()
  certificateInfo.value = certificateService.getCertificateInfo()
})

// Fonction pour copier l'empreinte du certificat
const copyFingerprint = async () => {
  if (certificateInfo.value?.fingerprint) {
    try {
      await navigator.clipboard.writeText(certificateInfo.value.fingerprint)
      // Optionnel: afficher un message de succès
      console.log('Empreinte copiée dans le presse-papiers')
    } catch (error) {
      console.error('Erreur lors de la copie:', error)
    }
  }
}

// Fonction pour supprimer le certificat
const removeCertificate = () => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce certificat ?\n\nCette action va :\n• Supprimer toutes les informations du certificat\n• Effacer les clés privée et publique\n• Nettoyer la sessionStorage\n\nCette action ne peut pas être annulée.')) {
    try {
      // Supprimer les données du service
      certificateService.clearCertificate()
      
      // Réinitialiser l'état local
      certificateInfo.value = null
      certificateError.value = null
      
      // Réinitialiser les champs de la modale si elle est ouverte
      selectedCertificateFile.value = null
      certificatePassword.value = ''
      
      console.log('Certificat supprimé avec succès')
      
      // Optionnel: afficher un message de succès
      // Vous pouvez ajouter ici une notification toast ou un message
      
    } catch (error) {
      console.error('Erreur lors de la suppression du certificat:', error)
      alert('Erreur lors de la suppression du certificat. Veuillez réessayer.')
    }
  }
}

// Initialisation au montage du composant
onMounted(async () => {
  // Vérifier si l'utilisateur a des organisations
  await checkUserOrganizations()
})

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
  background: #ffffff;
  box-shadow: 4px 0 20px rgba(0, 102, 204, 0.15);
  z-index: 1050;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
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
  color: #495057;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-family: 'Raleway', sans-serif;
  cursor: pointer;
}

.sidebar-nav-link:hover,
.sidebar-nav-link.active {
  color: var(--primary-blue);
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 123, 255, 0.08) 100%);
  text-decoration: none;
}

.sidebar-nav-link i {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
  transition: all 0.3s ease;
}

.mobile-sidebar .sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
  margin-top: auto;
}

/* SIDEBAR */
.dashboard-sidebar {
  width: 280px;
  background: #ffffff;
  box-shadow: 
    4px 0 20px rgba(0, 102, 204, 0.08),
    2px 0 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 1000;
  border-right: 1px solid rgba(0, 102, 204, 0.1);
  transition: width 0.3s ease;
}

.dashboard-sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 1.5rem 1.5rem 1rem;
  background: #ffffff;
  position: relative;
  flex-shrink: 0;
  height: 90px; /* Hauteur fixe pour le header */
  display: flex;
  align-items: center;
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 1.5rem;
  right: 1.5rem;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.3), transparent);
  border-radius: 1px;
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
  color: var(--primary-blue);
  font-family: 'Raleway', sans-serif;
  letter-spacing: -0.02em;
}

.sidebar-toggle-container {
  position: fixed;
  top: 2rem;
  left: 290px;
  z-index: 1001;
  transition: left 0.3s ease;
}

.dashboard-sidebar.collapsed + .dashboard-main .sidebar-toggle-container {
  left: 90px;
}

.sidebar-toggle {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 102, 204, 0.2);
  color: var(--primary-blue);
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
  backdrop-filter: blur(8px);
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
}

/* NAVIGATION */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  position: relative;
  overflow-y: auto;
  min-height: 0;
  max-height: calc(100vh - 220px); /* Hauteur fixe pour laisser de l'espace au header et footer */
}

.sidebar-nav::before {
  content: '';
  position: absolute;
  top: 0;
  left: 1.5rem;
  right: 1.5rem;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.2), transparent);
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
  color: #495057;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-family: 'Raleway', sans-serif;
  position: relative;
  border-radius: 0 12px 12px 0;
  margin-right: 0.5rem;
  justify-content: center;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dashboard-sidebar:not(.collapsed) .nav-link {
  justify-content: flex-start;
}

.dashboard-sidebar.collapsed .nav-link {
  padding: 1rem 0.5rem;
  justify-content: center;
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
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
  transition: all 0.3s ease;
}

.dashboard-sidebar.collapsed .nav-link i {
  width: auto;
  font-size: 1.5rem;
}

.nav-link:hover i,
.nav-link.active i {
  transform: scale(1.1);
}

/* FOOTER SIDEBAR */
.sidebar-footer {
  padding: 0.25rem 1.5rem 0.5rem;
  background: #ffffff;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120px; /* Hauteur fixe pour le footer */
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  z-index: 10;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 1.5rem;
  right: 1.5rem;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.4), transparent);
  z-index: 1;
}

.dashboard-sidebar.collapsed .sidebar-footer {
  padding: 0.75rem 0.5rem 1rem;
  align-items: center;
  justify-content: flex-end;
}



.user-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  margin-bottom: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.4rem;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  justify-content: center;
}

.dashboard-sidebar:not(.collapsed) .user-info {
  justify-content: flex-start;
}

.dashboard-sidebar.collapsed .user-info {
  padding: 0.75rem 0.5rem;
  justify-content: center;
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-sidebar.collapsed .user-avatar {
  font-size: 1.5rem;
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
  padding: 0.4rem 1rem;
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

.dashboard-sidebar:not(.collapsed) .logout-btn {
  justify-content: center;
}

.dashboard-sidebar.collapsed .logout-btn {
  padding: 0.75rem 0.5rem;
  justify-content: center;
  min-width: auto;
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
  transition: margin-left 0.3s ease;
}

.dashboard-sidebar.collapsed ~ .dashboard-main {
  margin-left: 80px;
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

/* Modale de profil utilisateur */
.profile-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 9999;
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
  animation: fadeIn 0.3s ease-out;
}

.profile-modal {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  width: 800px;
  height: 500px;
  margin: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  display: flex;
  overflow: hidden;
  transform: translateY(100px) scale(0.9);
  animation: modalSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

/* Responsive pour la modale sur mobile */
@media (max-width: 991px) {
  .profile-modal-overlay {
    align-items: center;
    justify-content: center;
    padding: 0rem;
  }
  
  .profile-modal {
    width: 100%;
    max-width: 500px;
    height: 85vh;
    max-height: 700px;
    margin: 0;
    border-radius: 16px;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* Cacher complètement le menu sur mobile */
  .profile-menu {
    display: none;
  }
  
  /* Contenu principal en pleine largeur */
  .profile-content {
    flex: 1;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* Header du contenu */
  .profile-content-header {
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  
  .profile-content-header h5 {
    font-size: 0.5rem;
    margin: 0;
    color: var(--text-dark);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .profile-content-header h5 i {
    font-size: 1.5rem;
    color: var(--primary-blue);
  }
  
  /* Body du contenu */
  .profile-content-body {
    flex: 1;
    padding: 1rem;
    padding-bottom: 6rem; /* Plus d'espace pour la barre de navigation */
    overflow-y: auto;
    background: rgba(255, 255, 255, 0.02);
    min-height: 0; /* Important pour que flex fonctionne correctement */
  }
  
  /* Style pour la barre de scroll du contenu */
  .profile-content-body::-webkit-scrollbar {
    width: 6px;
  }
  
  .profile-content-body::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }
  
  .profile-content-body::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    transition: all 0.3s ease;
  }
  
  .profile-content-body::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }
  
  /* Pour Firefox */
  .profile-content-body {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
  }
  
  /* Barre de navigation mobile */
  .mobile-nav-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 75px;
    background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 102, 204, 0.08) 100%);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border-top: 1px solid rgba(0, 102, 204, 0.25);
    border-top-left-radius: 25px;
    border-top-right-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0.75rem 1.5rem;
    z-index: 10;
    box-shadow: 
      0 -8px 32px rgba(0, 102, 204, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    perspective: 1000px;
    transform-style: preserve-3d;
  }
  
  .mobile-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    padding: 0.75rem 0.5rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-radius: 16px;
    margin: 0 0.3rem;
    position: relative;
    min-height: 55px;
    z-index: 1;
  }
  
  .mobile-nav-item i {
    font-size: 1.3rem;
    margin-bottom: 0.35rem;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    color: var(--text-dark);
    z-index: 2;
  }
  
  .mobile-nav-item span {
    font-size: 0.7rem;
    font-weight: 500;
    text-align: center;
    line-height: 1.2;
    color: var(--text-dark);
    transition: all 0.3s ease;
    z-index: 2;
  }
  
  /* Effet de loupe qui glisse */
  .mobile-nav-bar::after {
    content: '';
    position: absolute;
    top: 6px;
    left: 20px;
    width: calc(25% - 12px);
    height: calc(100% - 12px);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.2) 100%);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 
      0 8px 32px rgba(0, 102, 204, 0.4),
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3),
      inset 0 -1px 0 rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    z-index: 0;
    transform-origin: center;
    opacity: 0;
    transform: scale(0.8) translateZ(0);
  }
  
  /* Position de la loupe selon l'onglet actif */
  .mobile-nav-bar[data-active-tab="profile"]::after {
    transform: translateX(0%) scale(1.1) translateZ(10px);
    opacity: 1;
  }
  
  .mobile-nav-bar[data-active-tab="security"]::after {
    transform: translateX(100%) scale(1.1) translateZ(10px);
    opacity: 1;
  }
  
  .mobile-nav-bar[data-active-tab="preferences"]::after {
    transform: translateX(200%) scale(1.1) translateZ(10px);
    opacity: 1;
  }
  
  .mobile-nav-bar[data-active-tab="billing"]::after {
    transform: translateX(300%) scale(1.1) translateZ(10px);
    opacity: 1;
  }
  
  .mobile-nav-item.active i {
    color: var(--primary-blue);
    transform: scale(1.3);
    font-size: 1.5rem;
  }
  
  .mobile-nav-item.active span {
    color: var(--primary-blue);
    font-weight: 600;
    font-size: 0.8rem;
  }
  
  .mobile-nav-item:hover i {
    color: var(--primary-blue);
    transform: scale(1.05);
  }
  
  .mobile-nav-item:hover span {
    color: var(--primary-blue);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalSlideUp {
  to {
    transform: translateY(0) scale(1);
  }
}

/* Menu latéral de la modale - Style glassmorphisme */
.profile-menu {
  width: 220px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
}

.profile-menu::before {
  content: '';
  position: absolute;
  top: 0;
  left: 1.5rem;
  right: 1.5rem;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.2), transparent);
}

.profile-menu-header {
  padding: 1.5rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.profile-avatar {
  font-size: 2.5rem;
  color: var(--primary-blue);
  margin-bottom: 0.5rem;
}

.profile-menu-header h6 {
  color: var(--text-dark);
  margin: 0;
  font-weight: 600;
  font-size: 1rem;
  font-family: 'Raleway', sans-serif;
}

.profile-nav {
  list-style: none;
  margin: 0;
  padding: 1rem 0;
  flex: 1;
  position: relative;
  overflow-y: auto;
  max-height: calc(100% - 120px); /* Hauteur maximale pour permettre le scroll */
}

/* Effet de loupe pour le menu PC */
.profile-nav::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.2) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 6px 25px rgba(0, 102, 204, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 0;
  transform-origin: center;
  opacity: 0;
  transform: scale(0.8);
  margin: 0 0.5rem;
}

.profile-nav-item {
  margin-bottom: 0.25rem;
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  color: #495057;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-family: 'Raleway', sans-serif;
  border-radius: 0 12px 12px 0;
  margin-right: 0.5rem;
  cursor: pointer;
  z-index: 1;
}

.profile-nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 0;
  background: var(--primary-blue);
  transition: width 0.3s ease;
  border-radius: 0 12px 12px 0;
}

.profile-nav-item:hover {
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
  text-decoration: none;
  transform: translateX(4px);
}

.profile-nav-item:hover::before {
  width: 4px;
}

/* Position de la loupe selon l'onglet actif pour PC */
.profile-nav[data-active-tab="profile"]::after {
  transform: translateY(0px) scale(1.1);
  opacity: 1;
}

.profile-nav[data-active-tab="security"]::after {
  transform: translateY(60px) scale(1.1);
  opacity: 1;
}

.profile-nav[data-active-tab="preferences"]::after {
  transform: translateY(120px) scale(1.1);
  opacity: 1;
}

.profile-nav[data-active-tab="billing"]::after {
  transform: translateY(180px) scale(1.1);
  opacity: 1;
}

.profile-nav-item.active {
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.15);
  border-right: none;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.profile-nav-item.active::before {
  width: 4px;
}

.profile-nav-item i {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
  transition: all 0.3s ease;
}

.profile-nav-item:hover i,
.profile-nav-item.active i {
  transform: scale(1.1);
}

/* Style pour la barre de scroll de la navigation */
.profile-nav::-webkit-scrollbar {
  width: 6px;
}

.profile-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.profile-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.profile-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Pour Firefox */
.profile-nav {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

/* Contenu principal de la modale - Style glassmorphisme */
.profile-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  height: 100%;
  overflow: hidden;
}

.profile-content-header {
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  position: relative;
}

.profile-content-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 2rem;
  right: 2rem;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.1), transparent);
}

.profile-content-header h5 {
  margin: 0;
  color: var(--text-dark);
  font-weight: 700;
  font-size: 1.5rem;
  flex: 1;
  font-family: 'Raleway', sans-serif;
}

.close-btn {
  background: var(--primary-blue);
  border: none;
  color: white;
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(52, 144, 220, 0.2);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.close-btn:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(52, 144, 220, 0.3);
}

.close-btn i {
  font-size: 0.9rem;
}

.profile-content-body {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  max-height: calc(100vh - 200px); /* Hauteur maximale pour permettre le scroll */
}

/* Style pour la barre de scroll du contenu principal */
.profile-content-body::-webkit-scrollbar {
  width: 8px;
}

.profile-content-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.profile-content-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.profile-content-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Pour Firefox */
.profile-content-body {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

/* Contenu des onglets */
.tab-content {
  animation: fadeInContent 0.3s ease-out;
}

@keyframes fadeInContent {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Formulaires - Style glassmorphisme */
.form-group {
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.form-group:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.85rem;
  font-family: 'Raleway', sans-serif;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: white;
  font-family: 'Raleway', sans-serif;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 4px rgba(52, 144, 220, 0.1);
  transform: translateY(-1px);
}

/* Éléments de sécurité - Style glassmorphisme */
.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.security-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.security-item:last-child {
  margin-bottom: 0;
}

.security-info h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.security-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  font-family: 'Raleway', sans-serif;
}

/* Éléments de préférences - Style glassmorphisme */
.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.preference-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.preference-item:last-child {
  margin-bottom: 0;
}

.preference-info h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.preference-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  font-family: 'Raleway', sans-serif;
}

.form-select {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.9rem;
  min-width: 120px;
}

/* Facturation - Style glassmorphisme */
.billing-info h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.plan-card {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.plan-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.plan-details h5 {
  margin: 0 0 0.5rem 0;
  color: var(--primary-blue);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.2rem;
}

.plan-details p {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  font-family: 'Raleway', sans-serif;
}

/* Boutons - Style identique à la HeroSection */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  border: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  font-family: 'Raleway', sans-serif;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-primary {
  background: var(--primary-blue);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 144, 220, 0.2);
}

.btn-primary:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 144, 220, 0.3);
}

.btn-outline-primary {
  background: transparent;
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(52, 144, 220, 0.1);
}

.btn-outline-primary:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 144, 220, 0.3);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

/* Badge */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.bg-success {
  background: #28a745 !important;
  color: white;
}

/* Switch */
.form-check-input {
  width: 3rem;
  height: 1.5rem;
  border-radius: 1rem;
  background-color: #dee2e6;
  border: none;
  cursor: pointer;
}

.form-check-input:checked {
  background-color: var(--primary-blue);
}

/* Style pour le profil cliquable */
.user-info {
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
  padding: 8px;
}

.user-info:hover {
  background: rgba(52, 144, 220, 0.05);
  transform: translateY(-1px);
}

/* Certificat - Style glassmorphisme */
.certificate-upload-section h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.certificate-action-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  gap: 20px;
}

.certificate-action-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.action-info h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.action-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  font-family: 'Raleway', sans-serif;
  max-width: 100%;
  word-wrap: break-word;
}

.action-button {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

/* Section informations du certificat */
.certificate-info-section {
  margin-top: 2rem;
}

.certificate-info-section-top {
  margin-top: 0;
}

.certificate-info-section h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.certificate-status-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.certificate-status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* Styles pour le certificat importé */
.certificate-imported {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  flex-direction: column;
  align-items: stretch;
}

.certificate-imported:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 15px 40px rgba(0, 0, 0, 0.15),
    inset 1px 0 0 rgba(255, 255, 255, 0.2);
}

/* Styles pour le certificat expiré */
.certificate-expired {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  box-shadow: 
    0 10px 30px rgba(220, 53, 69, 0.1),
    inset 1px 0 0 rgba(220, 53, 69, 0.1);
}

.certificate-expired:hover {
  box-shadow: 
    0 15px 40px rgba(220, 53, 69, 0.15),
    inset 1px 0 0 rgba(220, 53, 69, 0.2);
}

.certificate-expired .certificate-status-icon {
  background: rgba(220, 53, 69, 0.2);
  border: 1px solid rgba(220, 53, 69, 0.3);
  color: #dc3545;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.2);
}

.certificate-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 1rem;
}

.certificate-status-icon {
  width: 48px;
  height: 48px;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #dc3545;
  flex-shrink: 0;
}

.certificate-imported .certificate-status-icon {
  background: rgba(0, 102, 204, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 102, 204, 0.3);
  color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
}

.certificate-title {
  flex: 1;
}

.certificate-title h6 {
  color: var(--text-dark);
  font-weight: 600;
  margin: 0;
}

.certificate-subtitle {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 400;
}

.certificate-status-badge {
  flex-shrink: 0;
}

.certificate-content {
  width: 100%;
}

.certificate-section {
  margin-bottom: 1.5rem;
}

.certificate-section:last-child {
  margin-bottom: 0;
}

.section-title {
  color: var(--text-dark);
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-title i {
  color: var(--primary-blue);
  margin-right: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-label {
  font-size: 0.8rem;
  color: var(--primary-blue);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.9rem;
  color: var(--text-dark);
  font-weight: 500;
  word-break: break-word;
}

.serial-number {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  background: rgba(0, 0, 0, 0.05);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.validity-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.validity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.validity-item:last-child {
  margin-bottom: 0;
}

.validity-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
}

.validity-label {
  font-size: 0.85rem;
  color: var(--primary-blue);
  font-weight: 600;
}

.validity-date {
  font-size: 0.9rem;
  color: var(--text-dark);
  font-weight: 600;
}

.security-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.security-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  font-size: 0.9rem;
  color: var(--text-dark);
  transition: all 0.3s ease;
}

.security-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
}

.security-warning {
  background: rgba(255, 193, 7, 0.1) !important;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.security-warning:hover {
  background: rgba(255, 193, 7, 0.15) !important;
}

.fingerprint-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.fingerprint-code {
  flex: 1;
  font-size: 0.8rem;
  color: var(--text-dark);
  background: transparent;
  border: none;
  font-family: 'Courier New', monospace;
  word-break: break-all;
  line-height: 1.4;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.copy-btn {
  flex-shrink: 0;
  padding: 0.5rem 0.75rem;
  font-size: 0.8rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--primary-blue);
}

.copy-btn:hover {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

/* Styles pour les actions du certificat */
.certificate-actions {
  display: flex;
  justify-content: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.remove-certificate-btn {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  color: #dc3545;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.remove-certificate-btn:hover {
  background: #dc3545;
  color: white;
  border-color: #dc3545;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

.certificate-status-content h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
}

.certificate-status-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #6c757d;
  font-family: 'Raleway', sans-serif;
  line-height: 1.5;
}

.btn-outline-secondary {
  background: transparent;
  border: 2px solid #6c757d;
  color: #6c757d;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.1);
}

.btn-outline-secondary:hover {
  background: #6c757d;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(108, 117, 125, 0.3);
}

/* Tooltip personnalisé pour la description du certificat */
.certificate-description {
  position: relative;
  cursor: help;
  border-bottom: 1px dotted #6c757d;
  transition: all 0.3s ease;
  flex: 1;
  margin-right: 16px;
}

.certificate-description:hover {
  color: var(--primary-blue) !important;
  border-bottom-color: var(--primary-blue);
}

.certificate-description:hover::after {
  content: "Importez votre certificat PFX ou P12 pour signer vos documents. Ce certificat restera effectif tant que vous êtes connecté. Une fois déconnecté, vous devrez le réimporter à nouveau.";
  position: absolute;
  top: 100%;
  left: -40px;
  right: -40px;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  line-height: 1.4;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-top: 8px;
  white-space: normal;
  text-align: left;
  width: calc(100% + 80px);
  min-width: 500px;
  font-family: 'Raleway', sans-serif;
  font-weight: 400;
  animation: tooltipFadeIn 0.2s ease-out;
}

.certificate-description:hover::before {
  content: '';
  position: absolute;
  top: 100%;
  left: 20px;
  border: 6px solid transparent;
  border-bottom-color: rgba(0, 0, 0, 0.9);
  margin-top: 2px;
  z-index: 9999;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Styles pour l'état vide du certificat */
.certificate-empty {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.05);
}

.certificate-empty-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
}

.certificate-empty-icon {
  font-size: 2.5rem;
  color: #6c757d;
  flex-shrink: 0;
}

.certificate-empty-text h6 {
  color: var(--text-dark);
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.certificate-empty-text p {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

/* Styles pour le message "certificat déjà importé" dans la modale */
.certificate-already-imported {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.05);
}

.certificate-already-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
}

.certificate-already-icon {
  font-size: 2.5rem;
  color: #28a745;
  flex-shrink: 0;
}

.certificate-already-text h6 {
  color: var(--text-dark);
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.certificate-already-text p {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

/* Styles pour le fichier sélectionné */
.selected-file-container {
  margin-bottom: 1rem;
}

.selected-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.selected-file:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.selected-file-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.selected-file-info i {
  font-size: 1.2rem;
  color: #28a745;
}

.selected-file-name {
  font-weight: 500;
  color: var(--text-dark);
  font-size: 0.9rem;
}

.remove-file-btn {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
  color: #dc3545;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.remove-file-btn:hover {
  background: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.3);
  color: #dc3545;
  transform: scale(1.05);
}

@keyframes contextMenuFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Modale de certificat - Style identique à la modale de profil */
.certificate-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-out;
}

.certificate-modal {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  width: 400px;
  max-height: 500px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  overflow: hidden;
  transform: translateY(20px) scale(0.9);
  animation: modalSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.certificate-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.certificate-modal-header h6 {
  margin: 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}

.certificate-modal-header h6 i {
  color: var(--primary-blue);
  font-size: 1.2rem;
}

.certificate-modal-body {
  padding: 1.5rem;
  max-height: 350px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
}

.certificate-upload-zone h6,
.certificate-password-section h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1rem;
}

.drop-zone {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  position: relative;
}

.drop-zone:hover,
.drop-zone.dragging {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.05);
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.drop-zone-content i {
  font-size: 2rem;
  color: var(--primary-blue);
}

.drop-zone-content p {
  margin: 0;
  color: var(--text-dark);
  font-weight: 500;
}

.drop-zone-content .text-muted {
  color: #6c757d;
  font-size: 0.9rem;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.selected-file i {
  color: #28a745;
  font-size: 1.25rem;
}

.selected-file span {
  flex: 1;
  color: var(--text-dark);
  font-weight: 500;
}

.remove-file-btn {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: none;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  background: rgba(220, 53, 69, 0.2);
}

.certificate-password-section {
  margin-top: 2rem;
}

.password-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: white;
  font-family: 'Raleway', sans-serif;
}

.password-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.password-toggle:hover {
  color: var(--text-dark);
  background: #f8f9fa;
}

.certificate-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Responsive */
@media (max-width: 768px) {
  .profile-modal {
    width: calc(100vw - 40px);
    height: calc(100vh - 100px);
    margin: 20px;
  }
  
  .profile-menu {
    width: 180px;
  }
  
  .profile-content-body {
    padding: 20px;
  }
}

/* PAGE PLACEHOLDER */
.page-placeholder {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
  margin: 2rem 0;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
