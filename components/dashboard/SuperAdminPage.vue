<template>
  <div class="documents-page super-admin-page fade-in-up">
    <!-- Header Signature GVB avec titre, bulles animées et illustration SVG -->
    <div class="documents-header super-admin-header mb-4">
      <div class="header-container">
        <div class="header-content">
          <div class="badge-superadmin mb-2">
            <i class="bi bi-shield-lock-fill me-1"></i>
            <span>{{ t('superAdmin.badge') }}</span>
          </div>
          <h1 class="section-title">
            <span class="text-dark">{{ activeHeaderInfo.prefix }} </span>
            <span class="text-primary-blue">{{ activeHeaderInfo.accent }}</span>
          </h1>
          <p class="section-subtitle">{{ activeHeaderInfo.subtitle }}</p>

          <!-- Contrôles rapides : statut en direct + rafraîchissement -->
          <div class="header-actions d-flex align-items-center gap-3 flex-wrap mt-3">
            <div class="pulse-indicator bg-white text-success px-3 py-2 rounded-pill shadow-sm d-flex align-items-center border">
              <span class="spinner-grow spinner-grow-sm me-2 text-success" role="status" aria-hidden="true" style="width: 0.75rem; height: 0.75rem;"></span>
              <span class="fw-semibold small">{{ t('superAdmin.systemOnline') }}</span>
            </div>

            <button class="btn btn-outline-primary btn-refresh rounded-pill px-3 py-2 shadow-sm d-flex align-items-center gap-2" @click="handleManualRefresh" :disabled="isRefreshing">
              <i class="bi bi-arrow-clockwise" :class="{ 'spin-animation': isRefreshing }"></i>
              <span class="small fw-semibold">{{ t('superAdmin.refresh') }}</span>
            </button>
          </div>
        </div>

        <div class="header-image">
          <!-- Bulles décoratives avec animation flottante GVB -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img :src="activeHeaderInfo.svg" :alt="activeHeaderInfo.prefix" class="documents-illustration">
        </div>
      </div>
    </div>

    <!-- Bannière d'alerte contextuelle si organisations en attente (cliquable pour basculer vers les demandes) -->
    <div v-if="pendingOrgs.length > 0 && currentSection !== 'organizations'" class="alert-pending-banner mb-4 p-3 rounded-4 shadow-sm d-flex align-items-center justify-content-between flex-wrap gap-3">
      <div class="d-flex align-items-center gap-3">
        <div class="alert-icon-pulse">
          <i class="bi bi-bell-fill text-warning fs-4"></i>
        </div>
        <div>
          <h6 class="fw-bold mb-0 text-dark">
            {{ pendingOrgs.length }} {{ t('superAdmin.pendingAlert') }}
          </h6>
          <small class="text-muted">Des structures attendent votre approbation pour activer leur compte.</small>
        </div>
      </div>
      <button class="btn btn-warning btn-sm rounded-pill px-3 fw-bold shadow-sm" @click="switchSection('organizations', 'pending')">
        <i class="bi bi-arrow-right-circle me-1"></i> Examiner les demandes
      </button>
    </div>

    <!-- État de chargement initial -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary-blue" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Chargement...</span>
      </div>
      <p class="mt-3 text-muted fw-semibold">Synchronisation de la console de supervision...</p>
    </div>

    <!-- Contenu des Vues SuperAdmin -->
    <div v-else>

      <!-- ========================================================== -->
      <!-- SECTION 1 : VUE D'ENSEMBLE (OVERVIEW & ANALYTICS)         -->
      <!-- ========================================================== -->
      <div v-if="currentSection === 'overview'" class="section-content fade-in-up">
        
        <!-- Cartes Statistiques Aérées (Format GVB Standard 3 Colonnes) -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-people"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ users.length }}</h4>
                  <p class="stat-label">{{ t('superAdmin.kpiUsers') }}</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-building"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ organizations.length }}</h4>
                  <p class="stat-label">{{ t('superAdmin.kpiOrgs') }}</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-file-earmark-check"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ signatures.length }}</h4>
                  <p class="stat-label">{{ t('superAdmin.kpiSignatures') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section Graphiques -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">Activité & </span>
            <span class="text-primary-blue">Supervision Globale</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Évolution temporelle des signatures et distribution des structures partenaires
          </p>
        </div>

        <!-- Rangée Graphiques : 1 Courbe Temporelle + 1 Donut -->
        <div class="row g-4 mb-5">
          <!-- GRAPHIQUE 1 : COURBE TEMPORELLE INTERACTIVE -->
          <div class="col-lg-8">
            <div class="chart-card-clean shadow-sm h-100 p-4 p-lg-5">
              <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center gap-2 mb-4">
                <div>
                  <h5 class="fw-bold text-dark mb-1">
                    <i class="bi bi-graph-up text-primary-blue me-2"></i>{{ t('superAdmin.chartActivityTitle') }}
                  </h5>
                  <small class="text-muted">{{ t('superAdmin.chartActivitySubtitle') }}</small>
                </div>
                <div class="d-flex align-items-center gap-2">
                  <div class="btn-group btn-group-sm" role="group">
                    <button type="button" class="btn btn-outline-primary" :class="{ active: chartPeriod === '7d' }" @click="chartPeriod = '7d'">7J</button>
                    <button type="button" class="btn btn-outline-primary" :class="{ active: chartPeriod === '30d' }" @click="chartPeriod = '30d'">30J</button>
                    <button type="button" class="btn btn-outline-primary" :class="{ active: chartPeriod === 'all' }" @click="chartPeriod = 'all'">Tout</button>
                  </div>
                </div>
              </div>

              <!-- Zone SVG Chart -->
              <div class="svg-chart-container position-relative">
                <svg viewBox="0 0 800 260" class="w-100 h-auto svg-chart" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="activityGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#0066cc" stop-opacity="0.35" />
                      <stop offset="100%" stop-color="#0066cc" stop-opacity="0.00" />
                    </linearGradient>
                    <linearGradient id="userGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#10b981" stop-opacity="0.25" />
                      <stop offset="100%" stop-color="#10b981" stop-opacity="0.00" />
                    </linearGradient>
                  </defs>

                  <!-- Grille horizontale discrète -->
                  <line x1="40" y1="40" x2="760" y2="40" stroke="#f1f5f9" stroke-dasharray="4 4" />
                  <line x1="40" y1="90" x2="760" y2="90" stroke="#f1f5f9" stroke-dasharray="4 4" />
                  <line x1="40" y1="140" x2="760" y2="140" stroke="#f1f5f9" stroke-dasharray="4 4" />
                  <line x1="40" y1="190" x2="760" y2="190" stroke="#f1f5f9" stroke-dasharray="4 4" />
                  <line x1="40" y1="220" x2="760" y2="220" stroke="#e2e8f0" stroke-width="1.5" />

                  <!-- Aire sous la courbe des signatures -->
                  <path :d="activityAreaPath" fill="url(#activityGrad)" />
                  <!-- Courbe des signatures -->
                  <path :d="activityLinePath" fill="none" stroke="#0066cc" stroke-width="3" stroke-linecap="round" />

                  <!-- Courbe secondaire utilisateurs -->
                  <path :d="usersLinePath" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="4 4" stroke-linecap="round" />

                  <!-- Points interactifs signatures -->
                  <g v-for="(pt, idx) in activityPoints" :key="'pt-' + idx">
                    <circle 
                      :cx="pt.x" 
                      :cy="pt.y" 
                      r="5" 
                      fill="#ffffff" 
                      stroke="#0066cc" 
                      stroke-width="2.5" 
                      class="chart-point"
                      @mouseenter="hoveredPoint = pt"
                      @mouseleave="hoveredPoint = null"
                    />
                  </g>

                  <!-- Labels de date axe X -->
                  <text 
                    v-for="(label, lIdx) in activityLabels" 
                    :key="'lbl-' + lIdx"
                    :x="label.x" 
                    y="245" 
                    text-anchor="middle" 
                    font-size="11" 
                    fill="#64748b"
                    font-weight="500"
                  >
                    {{ label.text }}
                  </text>
                </svg>

                <!-- Tooltip interactif au survol -->
                <div v-if="hoveredPoint" class="chart-tooltip shadow-sm" :style="{ left: hoveredPoint.x + 'px', top: (hoveredPoint.y - 45) + 'px' }">
                  <div class="tooltip-date small text-muted">{{ hoveredPoint.date }}</div>
                  <div class="tooltip-val text-primary-blue fw-bold">{{ hoveredPoint.value }} signature(s)</div>
                </div>
              </div>

              <!-- Légende du graphique -->
              <div class="d-flex align-items-center justify-content-between pt-3 border-top mt-3 flex-wrap gap-2">
                <div class="d-flex align-items-center gap-3 small">
                  <span class="d-flex align-items-center gap-1 text-dark fw-semibold">
                    <span class="legend-color-dot bg-primary-blue"></span> Signatures scellées
                  </span>
                  <span class="d-flex align-items-center gap-1 text-muted">
                    <span class="legend-color-dot bg-success"></span> Inscriptions utilisateurs
                  </span>
                </div>
                <div class="small text-muted">
                  Pic d'activité : <strong class="text-dark">{{ peakActivityValue }} signatures/jour</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- GRAPHIQUE 2 : DIAGRAMME DONUT STATUT DES ORGANISATIONS -->
          <div class="col-lg-4">
            <div class="chart-card-clean shadow-sm h-100 p-4 d-flex flex-column">
              <div class="mb-3">
                <h5 class="fw-bold text-dark mb-1">
                  <i class="bi bi-pie-chart text-primary-blue me-2"></i>{{ t('superAdmin.chartDonutTitle') }}
                </h5>
                <small class="text-muted">{{ t('superAdmin.chartDonutSubtitle') }}</small>
              </div>

              <!-- Zone Donut SVG -->
              <div class="donut-chart-wrapper my-auto py-3 text-center position-relative">
                <svg viewBox="0 0 200 200" class="donut-svg">
                  <!-- Cercle de fond -->
                  <circle cx="100" cy="100" r="70" fill="transparent" stroke="#f1f5f9" stroke-width="20" />
                  
                  <!-- Segment Approuvées -->
                  <circle 
                    cx="100" 
                    cy="100" 
                    r="70" 
                    fill="transparent" 
                    stroke="#10b981" 
                    stroke-width="20" 
                    :stroke-dasharray="donutCircumference"
                    :stroke-dashoffset="donutApprovedOffset"
                    class="donut-segment"
                    transform="rotate(-90 100 100)"
                  />

                  <!-- Segment En attente -->
                  <circle 
                    cx="100" 
                    cy="100" 
                    r="70" 
                    fill="transparent" 
                    stroke="#f59e0b" 
                    stroke-width="20" 
                    :stroke-dasharray="donutCircumference"
                    :stroke-dashoffset="donutPendingOffset"
                    class="donut-segment"
                    transform="rotate(-90 100 100)"
                  />

                  <!-- Segment Rejetées -->
                  <circle 
                    cx="100" 
                    cy="100" 
                    r="70" 
                    fill="transparent" 
                    stroke="#ef4444" 
                    stroke-width="20" 
                    :stroke-dasharray="donutCircumference"
                    :stroke-dashoffset="donutRejectedOffset"
                    class="donut-segment"
                    transform="rotate(-90 100 100)"
                  />
                </svg>

                <!-- Centre du Donut -->
                <div class="donut-center-info">
                  <div class="donut-percentage display-6 fw-bold text-dark">{{ activeOrgsPercentage }}%</div>
                  <div class="donut-label text-muted small fw-semibold">Actives</div>
                </div>
              </div>

              <!-- Légende interactive Donut -->
              <div class="donut-legend pt-3 border-top mt-auto">
                <div class="legend-row d-flex justify-content-between align-items-center py-2 px-2 cursor-pointer rounded-2" @click="switchSection('organizations', 'approved')">
                  <div class="d-flex align-items-center gap-2 small">
                    <span class="legend-color-dot bg-success"></span>
                    <span class="text-dark fw-medium">Approuvées</span>
                  </div>
                  <span class="badge bg-success-subtle text-success fw-bold">{{ approvedOrgs.length }}</span>
                </div>
                <div class="legend-row d-flex justify-content-between align-items-center py-2 px-2 cursor-pointer rounded-2" @click="switchSection('organizations', 'pending')">
                  <div class="d-flex align-items-center gap-2 small">
                    <span class="legend-color-dot bg-warning"></span>
                    <span class="text-dark fw-medium">En attente</span>
                  </div>
                  <span class="badge bg-warning-subtle text-warning-emphasis fw-bold">{{ pendingOrgs.length }}</span>
                </div>
                <div class="legend-row d-flex justify-content-between align-items-center py-2 px-2 cursor-pointer rounded-2" @click="switchSection('organizations', 'rejected')">
                  <div class="d-flex align-items-center gap-2 small">
                    <span class="legend-color-dot bg-danger"></span>
                    <span class="text-dark fw-medium">Rejetées</span>
                  </div>
                  <span class="badge bg-danger-subtle text-danger fw-bold">{{ rejectedOrgs.length }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section Rôles & Flux d'activité -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">Rôles & </span>
            <span class="text-primary-blue">Journal d'Audit</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Distribution des permissions et dernières opérations en direct
          </p>
        </div>

        <!-- Rangée 2 : Distribution des Rôles + Flux d'Activité Récente -->
        <div class="row g-4 mb-4">
          <!-- DISTRIBUTION DES RÔLES -->
          <div class="col-lg-6">
            <div class="chart-card-clean shadow-sm h-100 p-4 p-lg-5">
              <div class="mb-4">
                <h5 class="fw-bold text-dark mb-1">
                  <i class="bi bi-person-badge text-primary-blue me-2"></i>{{ t('superAdmin.chartRolesTitle') }}
                </h5>
                <small class="text-muted">{{ t('superAdmin.chartRolesSubtitle') }}</small>
              </div>

              <div class="roles-progress-list d-flex flex-column gap-3">
                <!-- Membres -->
                <div class="role-progress-item">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-semibold small text-dark d-flex align-items-center gap-2">
                      <i class="bi bi-person text-secondary"></i> Membres Standards
                    </span>
                    <span class="small text-muted">{{ memberUsersCount }} ({{ memberPercentage }}%)</span>
                  </div>
                  <div class="progress" style="height: 10px;">
                    <div class="progress-bar bg-primary-blue" role="progressbar" :style="{ width: memberPercentage + '%' }"></div>
                  </div>
                </div>

                <!-- Chefs d'Organisation -->
                <div class="role-progress-item">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-semibold small text-dark d-flex align-items-center gap-2">
                      <i class="bi bi-building text-info"></i> Chefs d'Organisation
                    </span>
                    <span class="small text-muted">{{ chiefUsersCount }} ({{ chiefPercentage }}%)</span>
                  </div>
                  <div class="progress" style="height: 10px;">
                    <div class="progress-bar bg-info" role="progressbar" :style="{ width: chiefPercentage + '%' }"></div>
                  </div>
                </div>

                <!-- Super Admins -->
                <div class="role-progress-item">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-semibold small text-dark d-flex align-items-center gap-2">
                      <i class="bi bi-shield-lock-fill text-warning"></i> Super Administrateurs
                    </span>
                    <span class="small text-muted">{{ superAdminUsersCount }} ({{ superAdminPercentage }}%)</span>
                  </div>
                  <div class="progress" style="height: 10px;">
                    <div class="progress-bar bg-warning" role="progressbar" :style="{ width: superAdminPercentage + '%' }"></div>
                  </div>
                </div>
              </div>

              <div class="mt-4 p-3 bg-light rounded-3 d-flex align-items-center justify-content-between">
                <span class="small text-muted">Contrôle d'accès basé sur les rôles (RBAC)</span>
                <button class="btn btn-sm btn-link text-primary-blue fw-semibold p-0 text-decoration-none" @click="switchSection('users')">
                  Gérer les permissions →
                </button>
              </div>
            </div>
          </div>

          <!-- FLUX D'ACTIVITÉ EN DIRECT (LIVE AUDIT) -->
          <div class="col-lg-6">
            <div class="chart-card-clean shadow-sm h-100 p-4 p-lg-5">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h5 class="fw-bold text-dark mb-1">
                    <i class="bi bi-broadcast text-danger me-2"></i>{{ t('superAdmin.liveAuditTitle') }}
                  </h5>
                  <small class="text-muted">{{ t('superAdmin.liveAuditSubtitle') }}</small>
                </div>
                <span class="badge bg-light text-dark border">En temps réel</span>
              </div>

              <div class="activity-timeline-list">
                <div v-if="recentActivities.length === 0" class="text-center py-4 text-muted small">
                  Aucun événement récent enregistré.
                </div>
                <div 
                  v-for="(item, idx) in recentActivities" 
                  :key="'act-' + idx" 
                  class="timeline-item d-flex align-items-start gap-3 py-3 border-bottom"
                >
                  <div class="timeline-icon-badge" :class="item.badgeClass">
                    <i :class="item.icon"></i>
                  </div>
                  <div class="timeline-content flex-grow-1">
                    <div class="d-flex justify-content-between align-items-center">
                      <span class="fw-semibold text-dark small">{{ item.title }}</span>
                      <small class="text-muted">{{ item.timeAgo }}</small>
                    </div>
                    <p class="timeline-desc text-muted mb-0 small">{{ item.desc }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ========================================================== -->
      <!-- SECTION 2 : GESTION DES ORGANISATIONS                      -->
      <!-- ========================================================== -->
      <div v-if="currentSection === 'organizations'" class="section-content fade-in-up">
        
        <!-- Cartes Statistiques Dédiées Organisations -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-building-check"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-success">{{ approvedOrgs.length }}</h4>
                  <p class="stat-label">Organisations Validées</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-hourglass-split"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-warning">{{ pendingOrgs.length }}</h4>
                  <p class="stat-label">En Attente de Validation</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-building-dash"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-danger">{{ rejectedOrgs.length }}</h4>
                  <p class="stat-label">Demandes Rejetées</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">Structures & </span>
            <span class="text-primary-blue">Demandes d'Adhésion</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Examinez, approuvez ou révoquez les organisations partenaires
          </p>
        </div>

        <!-- Sous-onglets de statut et recherche -->
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-stretch align-items-md-center gap-3 mb-4">
          <ul class="nav nav-pills custom-tabs d-flex gap-2">
            <li class="nav-item">
              <button class="nav-link px-3 py-2" :class="{ active: currentOrgTab === 'pending' }" @click="currentOrgTab = 'pending'">
                <i class="bi bi-hourglass-split me-1 text-warning"></i> {{ t('superAdmin.pending') }}
                <span class="badge ms-2" :class="currentOrgTab === 'pending' ? 'bg-white text-dark' : 'bg-warning text-dark'">{{ pendingOrgs.length }}</span>
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link px-3 py-2" :class="{ active: currentOrgTab === 'approved' }" @click="currentOrgTab = 'approved'">
                <i class="bi bi-check-circle-fill me-1 text-success"></i> {{ t('superAdmin.approved') }}
                <span class="badge ms-2" :class="currentOrgTab === 'approved' ? 'bg-white text-dark' : 'bg-success text-white'">{{ approvedOrgs.length }}</span>
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link px-3 py-2" :class="{ active: currentOrgTab === 'rejected' }" @click="currentOrgTab = 'rejected'">
                <i class="bi bi-x-circle-fill me-1 text-danger"></i> {{ t('superAdmin.rejected') }}
                <span class="badge ms-2" :class="currentOrgTab === 'rejected' ? 'bg-white text-dark' : 'bg-danger text-white'">{{ rejectedOrgs.length }}</span>
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link px-3 py-2" :class="{ active: currentOrgTab === 'all' }" @click="currentOrgTab = 'all'">
                <i class="bi bi-collection me-1"></i> Toutes ({{ organizations.length }})
              </button>
            </li>
          </ul>

          <div class="search-box position-relative" style="min-width: 280px;">
            <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
            <input 
              type="text" 
              class="form-control border shadow-sm ps-5 py-2 rounded-pill" 
              :placeholder="t('superAdmin.orgSearchPlaceholder')" 
              v-model="orgSearchQuery"
            >
          </div>
        </div>

        <!-- Grille de cartes d'organisations -->
        <div class="row g-4">
          <div v-if="displayedOrgs.length === 0" class="col-12 text-center py-5">
            <div class="empty-state p-5 bg-white rounded-4 border shadow-sm">
              <i class="bi bi-building-dash display-3 text-muted mb-3 d-block"></i>
              <h5 class="fw-bold text-dark">{{ t('superAdmin.noOrgsFound') }}</h5>
              <p class="text-muted small">Aucune structure ne correspond à ces critères.</p>
            </div>
          </div>

          <div v-for="org in displayedOrgs" :key="org.id" class="col-lg-6 mb-2">
            <div class="organization-card shadow-sm h-100">
              <div class="card-header border-0 pb-0 d-flex align-items-start justify-content-between">
                <div class="d-flex align-items-center gap-3">
                  <div class="organization-icon">
                    <i class="bi bi-building"></i>
                  </div>
                  <div>
                    <h5 class="organization-name fw-bold mb-0 text-dark">{{ org.name }}</h5>
                    <span class="badge bg-light text-secondary border mt-1">{{ org.organization_type || 'Organisation' }}</span>
                  </div>
                </div>
                <div class="approval-status-badge" :class="org.approval_status || 'pending'">
                  <span>{{ getStatusText(org.approval_status) }}</span>
                </div>
              </div>

              <div class="card-body py-3">
                <p class="organization-description text-muted small mb-3">
                  {{ org.description || 'Aucune description renseignée pour cette structure.' }}
                </p>

                <div class="row g-2 organization-meta small text-muted">
                  <div class="col-sm-6 d-flex align-items-center gap-2">
                    <i class="bi bi-envelope text-primary-blue"></i>
                    <span class="text-truncate">{{ org.email || 'Non renseigné' }}</span>
                  </div>
                  <div class="col-sm-6 d-flex align-items-center gap-2">
                    <i class="bi bi-telephone text-primary-blue"></i>
                    <span>{{ org.phone || 'Non renseigné' }}</span>
                  </div>
                  <div class="col-sm-6 d-flex align-items-center gap-2">
                    <i class="bi bi-geo-alt text-primary-blue"></i>
                    <span class="text-truncate">{{ org.address || 'Non renseignée' }}</span>
                  </div>
                  <div class="col-sm-6 d-flex align-items-center gap-2">
                    <i class="bi bi-globe text-primary-blue"></i>
                    <span class="text-truncate">{{ org.website || 'Non renseigné' }}</span>
                  </div>
                </div>
              </div>

              <!-- Actions Administratives -->
              <div class="card-footer bg-light border-top pt-3 d-flex gap-2">
                <!-- En attente -->
                <template v-if="org.approval_status === 'pending' || !org.approval_status">
                  <button class="btn btn-outline-danger btn-sm flex-grow-1" @click="handleRejectOrg(org.id)">
                    <i class="bi bi-x-circle me-1"></i> {{ t('superAdmin.rejectOrg') }}
                  </button>
                  <button class="btn btn-success btn-sm flex-grow-1 fw-bold" @click="handleApproveOrg(org.id)">
                    <i class="bi bi-check-circle me-1"></i> {{ t('superAdmin.validateOrg') }}
                  </button>
                </template>

                <!-- Approuvée -->
                <template v-else-if="org.approval_status === 'approved'">
                  <button class="btn btn-outline-secondary btn-sm ms-auto" @click="handleRevokeOrg(org.id)">
                    <i class="bi bi-shield-x me-1"></i> {{ t('superAdmin.revokeOrg') }}
                  </button>
                </template>

                <!-- Rejetée -->
                <template v-else-if="org.approval_status === 'rejected'">
                  <button class="btn btn-outline-success btn-sm flex-grow-1" @click="handleRehabilitateOrg(org.id)">
                    <i class="bi bi-arrow-counterclockwise me-1"></i> {{ t('superAdmin.rehabilitateOrg') }}
                  </button>
                  <button class="btn btn-outline-danger btn-sm flex-grow-1" @click="handleRejectOrg(org.id, true)">
                    <i class="bi bi-trash3 me-1"></i> {{ t('superAdmin.deletePermanent') }}
                  </button>
                </template>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ========================================================== -->
      <!-- SECTION 3 : UTILISATEURS & GESTION DES RÔLES               -->
      <!-- ========================================================== -->
      <div v-if="currentSection === 'users'" class="section-content fade-in-up">
        
        <!-- Cartes Statistiques Dédiées Utilisateurs -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-person"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ memberUsersCount }}</h4>
                  <p class="stat-label">Membres Standards</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-person-badge"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-info">{{ chiefUsersCount }}</h4>
                  <p class="stat-label">Chefs d'Organisation</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-shield-lock"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-primary-blue">{{ superAdminUsersCount }}</h4>
                  <p class="stat-label">Super Administrateurs</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">Annuaire & </span>
            <span class="text-primary-blue">Contrôle des Accès</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Supervisez les utilisateurs enregistrés et gérez les privilèges administratifs
          </p>
        </div>

        <div class="d-flex flex-column flex-sm-row justify-content-between align-items-stretch align-items-sm-center gap-3 mb-4">
          <div class="search-box position-relative" style="max-width: 400px; width: 100%;">
            <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
            <input 
              type="text" 
              class="form-control border shadow-sm ps-5 py-2 rounded-pill" 
              :placeholder="t('superAdmin.userSearchPlaceholder')" 
              v-model="userSearchQuery"
            >
          </div>

          <div class="d-flex align-items-center gap-2">
            <select class="form-select form-select-sm rounded-pill px-3 shadow-sm" v-model="userRoleFilter">
              <option value="all">Tous les rôles ({{ users.length }})</option>
              <option value="member">Membres ({{ memberUsersCount }})</option>
              <option value="chief">Chefs d'organisation ({{ chiefUsersCount }})</option>
              <option value="super-admin">Super Administrateurs ({{ superAdminUsersCount }})</option>
            </select>
          </div>
        </div>

        <div class="chart-card-clean p-0 overflow-hidden border shadow-sm rounded-4">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 custom-table">
              <thead class="table-light">
                <tr>
                  <th class="ps-4 py-3">Utilisateur</th>
                  <th class="py-3">Email</th>
                  <th class="py-3">Date d'inscription</th>
                  <th class="py-3">Rôle actuel</th>
                  <th class="text-end pe-4 py-3">Modifier les privilèges</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="5" class="text-center py-5 text-muted">
                    {{ t('superAdmin.noUsersFound') }}
                  </td>
                </tr>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td class="ps-4">
                    <div class="d-flex align-items-center gap-3">
                      <img v-if="user.photoURL" :src="user.photoURL" class="rounded-circle shadow-sm" width="36" height="36" alt="Avatar">
                      <div v-else class="avatar-initials rounded-circle bg-primary-blue text-white d-flex align-items-center justify-content-center fw-bold" style="width: 36px; height: 36px;">
                        {{ (user.displayName || user.email || 'U').charAt(0).toUpperCase() }}
                      </div>
                      <div>
                        <span class="fw-bold text-dark d-block">{{ user.displayName || 'Utilisateur Anonyme' }}</span>
                        <small class="text-muted">UID: {{ user.id.substring(0, 8) }}...</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="text-dark">{{ user.email }}</span>
                  </td>
                  <td class="text-muted small">
                    {{ formatDate(user.createdAt?.toDate ? user.createdAt.toDate() : user.createdAt) }}
                  </td>
                  <td>
                    <span class="badge rounded-pill px-3 py-1" :class="getRoleBadgeClass(user.role)">
                      {{ getRoleText(user.role) }}
                    </span>
                  </td>
                  <td class="text-end pe-4">
                    <select 
                      class="form-select form-select-sm d-inline-block w-auto rounded-pill shadow-sm" 
                      @change="handleRoleChange(user.id, $event.target.value)" 
                      :value="user.role || 'member'"
                    >
                      <option value="member">{{ t('superAdmin.roleMember') }}</option>
                      <option value="chief">{{ t('superAdmin.roleChief') }}</option>
                      <option value="super-admin">{{ t('superAdmin.roleSuperAdmin') }}</option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ========================================================== -->
      <!-- SECTION 4 : REGISTRE D'AUDIT DES SIGNATURES                -->
      <!-- ========================================================== -->
      <div v-if="currentSection === 'signatures'" class="section-content fade-in-up">
        
        <!-- Cartes Statistiques Dédiées Signatures -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-file-earmark-pdf"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ signatures.length }}</h4>
                  <p class="stat-label">Documents Signés</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-clock-history"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ signatures.length }}</h4>
                  <p class="stat-label">Horodatages Certifiés</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-patch-check"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-success">100%</h4>
                  <p class="stat-label">Intégrité SHA-256</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">Registre & </span>
            <span class="text-primary-blue">Preuves Cryptographiques</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Traçabilité infalsifiable des signatures électroniques et contrôle d'intégrité
          </p>
        </div>

        <div class="d-flex flex-column flex-sm-row justify-content-between align-items-stretch align-items-sm-center gap-3 mb-4">
          <div class="search-box position-relative" style="max-width: 450px; width: 100%;">
            <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
            <input 
              type="text" 
              class="form-control border shadow-sm ps-5 py-2 rounded-pill" 
              :placeholder="t('superAdmin.sigSearchPlaceholder')" 
              v-model="sigSearchQuery"
            >
          </div>
          <span class="badge bg-white text-muted border px-3 py-2 rounded-pill shadow-sm">
            <i class="bi bi-database-check text-success me-1"></i> {{ filteredSignatures.length }} signature(s) enregistrée(s)
          </span>
        </div>

        <div class="chart-card-clean p-0 overflow-hidden border shadow-sm rounded-4">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 custom-table">
              <thead class="table-light">
                <tr>
                  <th class="ps-4 py-3">{{ t('superAdmin.docId') }}</th>
                  <th class="py-3">{{ t('superAdmin.signer') }}</th>
                  <th class="py-3">{{ t('superAdmin.hashSha256') }}</th>
                  <th class="py-3">{{ t('superAdmin.timestamp') }}</th>
                  <th class="text-end pe-4 py-3">Audit</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="filteredSignatures.length === 0">
                  <td colspan="5" class="text-center py-5 text-muted">
                    {{ t('superAdmin.noSignaturesFound') }}
                  </td>
                </tr>
                <tr v-for="sig in filteredSignatures" :key="sig.id">
                  <td class="ps-4">
                    <div class="d-flex align-items-center gap-2">
                      <i class="bi bi-file-earmark-pdf text-danger fs-5"></i>
                      <div>
                        <code class="text-primary-blue fw-bold">{{ (sig.document_id || sig.id).substring(0, 12) }}...</code>
                        <small class="d-block text-muted">{{ sig.original_filename || sig.fileName || 'document.pdf' }}</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="fw-semibold text-dark d-block">{{ sig.signer_full_name || sig.signer_name || 'Signataire' }}</span>
                    <small class="text-muted">{{ sig.signer_email || sig.userId }}</small>
                  </td>
                  <td>
                    <div class="d-flex align-items-center gap-2">
                      <code class="small text-muted bg-light px-2 py-1 rounded">
                        {{ sig.document_hash ? sig.document_hash.substring(0, 16) + '...' : 'SHA-256 Validé' }}
                      </code>
                    </div>
                  </td>
                  <td class="text-muted small">
                    {{ formatDate(sig.createdAt?.toDate ? sig.createdAt.toDate() : (sig.signature_timestamp || sig.createdAt)) }}
                  </td>
                  <td class="text-end pe-4">
                    <a 
                      :href="'/verify?id=' + (sig.document_id || sig.id)" 
                      target="_blank" 
                      class="btn btn-outline-primary btn-sm rounded-pill px-3"
                    >
                      <i class="bi bi-shield-check me-1"></i> {{ t('superAdmin.verifyDoc') }}
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ========================================================== -->
      <!-- SECTION 5 : SÉCURITÉ & SANTÉ DU SYSTÈME                   -->
      <!-- ========================================================== -->
      <div v-if="currentSection === 'system'" class="section-content fade-in-up">
        
        <!-- Cartes Statistiques Dédiées Système -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-hdd-network"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-success">5/5</h4>
                  <p class="stat-label">Services Opérationnels</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-activity"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-primary-blue">99.9%</h4>
                  <p class="stat-label">Disponibilité Plateforme</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-shield-check"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number text-warning">RSA-2048</h4>
                  <p class="stat-label">Zero-Knowledge Chiffré</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- En-tête de section -->
        <div class="sections-header text-center mb-4">
          <h2 class="display-6 fw-bold mb-3 text-dark sections-title">
            <span class="text-dark">État des Services & </span>
            <span class="text-primary-blue">Architecture</span>
          </h2>
          <p class="lead mb-0 text-muted sections-subtitle">
            Indicateurs opérationnels des micro-services et conformité cryptographique
          </p>
        </div>

        <div class="row g-4 mb-4">
          <!-- Statut des Services Connectés -->
          <div class="col-lg-7">
            <div class="chart-card-clean shadow-sm p-4 p-lg-5 h-100">
              <h5 class="fw-bold text-dark mb-4">
                <i class="bi bi-hdd-network text-primary-blue me-2"></i>{{ t('superAdmin.servicesStatus') }}
              </h5>

              <div class="services-status-list d-flex flex-column gap-3">
                <div class="service-status-row p-3 rounded-3 border d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-3">
                    <div class="service-icon bg-primary-subtle text-primary rounded-circle p-2">
                      <i class="bi bi-shield-lock"></i>
                    </div>
                    <div>
                      <h6 class="fw-bold mb-0 text-dark">{{ t('superAdmin.serviceAuth') }}</h6>
                      <small class="text-muted">Google OAuth 2.0 & Jetons sécurisés Firebase</small>
                    </div>
                  </div>
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> {{ t('superAdmin.statusOperational') }}
                  </span>
                </div>

                <div class="service-status-row p-3 rounded-3 border d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-3">
                    <div class="service-icon bg-info-subtle text-info rounded-circle p-2">
                      <i class="bi bi-database"></i>
                    </div>
                    <div>
                      <h6 class="fw-bold mb-0 text-dark">{{ t('superAdmin.serviceFirestore') }}</h6>
                      <small class="text-muted">Listeners réactifs en direct (onSnapshot)</small>
                    </div>
                  </div>
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> {{ t('superAdmin.statusOperational') }}
                  </span>
                </div>

                <div class="service-status-row p-3 rounded-3 border d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-3">
                    <div class="service-icon bg-purple-subtle text-purple rounded-circle p-2">
                      <i class="bi bi-cloud-arrow-up"></i>
                    </div>
                    <div>
                      <h6 class="fw-bold mb-0 text-dark">{{ t('superAdmin.serviceCloudinary') }}</h6>
                      <small class="text-muted">Stockage CDN chiffré des originaux et signés</small>
                    </div>
                  </div>
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> {{ t('superAdmin.statusOperational') }}
                  </span>
                </div>

                <div class="service-status-row p-3 rounded-3 border d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-3">
                    <div class="service-icon bg-success-subtle text-success rounded-circle p-2">
                      <i class="bi bi-cpu"></i>
                    </div>
                    <div>
                      <h6 class="fw-bold mb-0 text-dark">{{ t('superAdmin.serviceCrypto') }}</h6>
                      <small class="text-muted">Zero-Knowledge (les clés privées ne quittent jamais le navigateur)</small>
                    </div>
                  </div>
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> {{ t('superAdmin.statusOperational') }}
                  </span>
                </div>

                <div class="service-status-row p-3 rounded-3 border d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-3">
                    <div class="service-icon bg-warning-subtle text-warning rounded-circle p-2">
                      <i class="bi bi-qr-code-scan"></i>
                    </div>
                    <div>
                      <h6 class="fw-bold mb-0 text-dark">{{ t('superAdmin.serviceVerify') }}</h6>
                      <small class="text-muted">Résolution QR Code et contrôle d'empreinte public</small>
                    </div>
                  </div>
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-1 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> {{ t('superAdmin.statusOperational') }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Spécifications & Architecture Système -->
          <div class="col-lg-5">
            <div class="chart-card-clean shadow-sm p-4 p-lg-5 h-100">
              <h5 class="fw-bold text-dark mb-4">
                <i class="bi bi-gear-wide-connected text-primary-blue me-2"></i>{{ t('superAdmin.systemSpecs') }}
              </h5>

              <ul class="list-group list-group-flush small">
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Architecture Framework</span>
                  <span class="fw-bold text-dark">Nuxt.js 4 (SSR / Nitro Engine)</span>
                </li>
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Moteur Frontend</span>
                  <span class="fw-bold text-dark">Vue.js 3.5 (Composition API)</span>
                </li>
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Standard Cryptographique</span>
                  <span class="fw-bold text-dark">RSA PKCS#1 v1.5 / SHA-256</span>
                </li>
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Certificats Supportés</span>
                  <span class="fw-bold text-dark">PKCS#12 (.p12 / .pfx) & X.509</span>
                </li>
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Génération PDF & Placement</span>
                  <span class="fw-bold text-dark">pdf-lib / vue-pdf-embed</span>
                </li>
                <li class="list-group-item d-flex justify-content-between px-0 py-2">
                  <span class="text-muted">Domaine de Vérification QR</span>
                  <span class="fw-bold text-primary-blue">gvbsign.cm</span>
                </li>
              </ul>

              <div class="security-banner mt-4 p-3 rounded-3 bg-primary-subtle text-primary border border-primary-subtle">
                <div class="d-flex align-items-center gap-2 mb-1">
                  <i class="bi bi-shield-shaded fs-5"></i>
                  <span class="fw-bold small">Politique de Sécurité Zero-Knowledge</span>
                </div>
                <p class="mb-0 small" style="line-height: 1.4;">
                  Les mots de passe de certificats et clés privées des signataires sont déchiffrés localement dans la mémoire vive de l'utilisateur et ne sont jamais journalisés ni envoyés aux serveurs distants.
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import OrganizationApiService from '../../services/OrganizationApiService'
import AdminApiService from '../../services/AdminApiService'
import { useI18n } from '../../composables/useI18n'

const props = defineProps({
  activeSection: {
    type: String,
    default: 'overview'
  }
})

const emit = defineEmits(['update:section', 'update:pending-count'])

const { t, locale } = useI18n()

const loading = ref(true)
const isRefreshing = ref(false)
const currentSection = ref(props.activeSection || 'overview')

// Synchronisation de la section avec la prop sidebar
watch(() => props.activeSection, (newSec) => {
  if (newSec && newSec !== currentSection.value) {
    currentSection.value = newSec
  }
})

const switchSection = (section, orgTab = null) => {
  currentSection.value = section
  if (orgTab) {
    currentOrgTab.value = orgTab
  }
  emit('update:section', section)
}

// Données en temps réel
const organizations = ref([])
const users = ref([])
const signatures = ref([])

// Onglet et filtres pour la gestion des organisations
const currentOrgTab = ref('pending')
const orgSearchQuery = ref('')

// Filtres utilisateurs
const userSearchQuery = ref('')
const userRoleFilter = ref('all')

// Filtres registre signatures
const sigSearchQuery = ref('')

// Graphique d'activité
const chartPeriod = ref('7d')
const hoveredPoint = ref(null)

let unsubOrgs = null
let unsubUsers = null
let unsubSigs = null

onMounted(() => {
  loading.value = true
  
  // 1. Écouter les organisations en direct
  unsubOrgs = OrganizationApiService.listenAllOrganizations((orgs) => {
    organizations.value = orgs.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    emit('update:pending-count', pendingOrgs.value.length)
    checkLoading()
  })

  // 2. Écouter les utilisateurs en direct
  unsubUsers = AdminApiService.listenAllUsers((usr) => {
    users.value = usr
    checkLoading()
  })

  // 3. Écouter les signatures en direct
  unsubSigs = AdminApiService.listenAllSignatures((sigs) => {
    signatures.value = sigs.sort((a, b) => {
      const dateA = a.createdAt?.toDate ? a.createdAt.toDate() : new Date(a.createdAt || a.signature_timestamp || 0)
      const dateB = b.createdAt?.toDate ? b.createdAt.toDate() : new Date(b.createdAt || b.signature_timestamp || 0)
      return dateB - dateA
    })
    checkLoading()
  })
})

onUnmounted(() => {
  if (unsubOrgs) unsubOrgs()
  if (unsubUsers) unsubUsers()
  if (unsubSigs) unsubSigs()
})

const checkLoading = () => {
  setTimeout(() => { loading.value = false }, 300)
}

const handleManualRefresh = () => {
  isRefreshing.value = true
  setTimeout(() => {
    isRefreshing.value = false
  }, 700)
}

// ==================== HEADER DYNAMIQUE SELON LA SECTION ACTIVE ====================

const activeHeaderInfo = computed(() => {
  switch (currentSection.value) {
    case 'organizations':
      return {
        prefix: locale.value === 'fr' ? 'Gestion des' : 'Manage',
        accent: locale.value === 'fr' ? 'Organisations' : 'Organizations',
        subtitle: locale.value === 'fr' 
          ? 'Validation des nouvelles structures, contrôle des accès et annuaire d\'entreprises' 
          : 'Validation of new structures, access control and business directory',
        svg: '/organisation.svg'
      }
    case 'users':
      return {
        prefix: locale.value === 'fr' ? 'Utilisateurs &' : 'Users &',
        accent: locale.value === 'fr' ? 'Rôles' : 'Roles',
        subtitle: locale.value === 'fr' 
          ? 'Annuaire des comptes enregistrés, attribution des privilèges et matrice RBAC' 
          : 'Directory of registered accounts, permission management and RBAC matrix',
        svg: '/service.svg'
      }
    case 'signatures':
      return {
        prefix: locale.value === 'fr' ? 'Registre des' : 'Registry of',
        accent: locale.value === 'fr' ? 'Signatures' : 'Signatures',
        subtitle: locale.value === 'fr' 
          ? 'Journal d\'audit immuable, empreintes SHA-256 et certificats cryptographiques' 
          : 'Immutable audit log, SHA-256 fingerprints and cryptographic certificates',
        svg: '/My_documents.svg'
      }
    case 'system':
      return {
        prefix: locale.value === 'fr' ? 'Sécurité &' : 'Security &',
        accent: locale.value === 'fr' ? 'Système' : 'System',
        subtitle: locale.value === 'fr' 
          ? 'État opérationnel des micro-services, connecteurs et conformité Zero-Knowledge' 
          : 'Operational health of micro-services, connectors and Zero-Knowledge compliance',
        svg: '/dashboard.svg'
      }
    default: // overview
      return {
        prefix: locale.value === 'fr' ? 'Console de' : 'Supervision',
        accent: locale.value === 'fr' ? 'Supervision' : 'Console',
        subtitle: locale.value === 'fr' 
          ? 'Surveillance globale de la plateforme, flux des signatures et indicateurs de performance' 
          : 'Global platform monitoring, signature flows and performance indicators',
        svg: '/dashboard.svg'
      }
  }
})

// ==================== COMPUTED KPIS ====================

const pendingOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'pending' || !o.approval_status))
const approvedOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'approved'))
const rejectedOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'rejected'))

const activeOrgsPercentage = computed(() => {
  if (organizations.value.length === 0) return 0
  return Math.round((approvedOrgs.value.length / organizations.value.length) * 100)
})

const memberUsersCount = computed(() => users.value.filter(u => !u.role || u.role === 'member').length)
const chiefUsersCount = computed(() => users.value.filter(u => u.role === 'chief').length)
const superAdminUsersCount = computed(() => users.value.filter(u => u.role === 'super-admin').length)

const memberPercentage = computed(() => users.value.length ? Math.round((memberUsersCount.value / users.value.length) * 100) : 0)
const chiefPercentage = computed(() => users.value.length ? Math.round((chiefUsersCount.value / users.value.length) * 100) : 0)
const superAdminPercentage = computed(() => users.value.length ? Math.round((superAdminUsersCount.value / users.value.length) * 100) : 0)

// ==================== COMPUTED DONUT SVG ====================

const donutCircumference = 2 * Math.PI * 70 // ~439.82

const donutApprovedOffset = computed(() => {
  const total = organizations.value.length || 1
  const pct = approvedOrgs.value.length / total
  return donutCircumference * (1 - pct)
})

const donutPendingOffset = computed(() => {
  const total = organizations.value.length || 1
  const pct = pendingOrgs.value.length / total
  const approvedPct = approvedOrgs.value.length / total
  return donutCircumference * (1 - pct) + (donutCircumference * (1 - approvedPct))
})

const donutRejectedOffset = computed(() => {
  const total = organizations.value.length || 1
  const pct = rejectedOrgs.value.length / total
  const prevPct = (approvedOrgs.value.length + pendingOrgs.value.length) / total
  return donutCircumference * (1 - pct) + (donutCircumference * (1 - prevPct))
})

// ==================== COMPUTED ACTIVITY SPLINE CHART ====================

const activityChartData = computed(() => {
  const daysCount = chartPeriod.value === '7d' ? 7 : (chartPeriod.value === '30d' ? 30 : 14)
  const days = []
  const today = new Date()

  for (let i = daysCount - 1; i >= 0; i--) {
    const d = new Date()
    d.setDate(today.getDate() - i)
    const key = d.toISOString().split('T')[0]
    const label = new Intl.DateTimeFormat(locale.value === 'fr' ? 'fr-FR' : 'en-US', { day: 'numeric', month: 'short' }).format(d)
    
    // Compter les signatures du jour
    const sigCount = signatures.value.filter(s => {
      const sDate = s.createdAt?.toDate ? s.createdAt.toDate() : new Date(s.createdAt || s.signature_timestamp || 0)
      return sDate.toISOString().split('T')[0] === key
    }).length

    // Compter les users du jour
    const userCount = users.value.filter(u => {
      const uDate = u.createdAt?.toDate ? u.createdAt.toDate() : new Date(u.createdAt || 0)
      return uDate.toISOString().split('T')[0] === key
    }).length

    days.push({ key, label, signatures: sigCount, users: userCount })
  }

  return days
})

const peakActivityValue = computed(() => {
  const vals = activityChartData.value.map(d => d.signatures)
  return Math.max(...vals, 1)
})

const activityPoints = computed(() => {
  const data = activityChartData.value
  if (!data.length) return []
  const maxVal = Math.max(peakActivityValue.value, 4)
  const width = 800
  const height = 260
  const padX = 50
  const padY = 50
  const stepX = (width - 2 * padX) / (data.length - 1 || 1)

  return data.map((d, idx) => {
    const x = padX + idx * stepX
    const y = height - padY - (d.signatures / maxVal) * (height - 2 * padY)
    return { x, y, value: d.signatures, date: d.label }
  })
})

const activityLinePath = computed(() => {
  const pts = activityPoints.value
  if (!pts.length) return ''
  let path = `M ${pts[0].x} ${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cpX = (prev.x + curr.x) / 2
    path += ` C ${cpX} ${prev.y}, ${cpX} ${curr.y}, ${curr.x} ${curr.y}`
  }
  return path
})

const activityAreaPath = computed(() => {
  const pts = activityPoints.value
  if (!pts.length) return ''
  const bottomY = 220
  let path = `M ${pts[0].x} ${bottomY} L ${pts[0].x} ${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cpX = (prev.x + curr.x) / 2
    path += ` C ${cpX} ${prev.y}, ${cpX} ${curr.y}, ${curr.x} ${curr.y}`
  }
  path += ` L ${pts[pts.length - 1].x} ${bottomY} Z`
  return path
})

const usersLinePath = computed(() => {
  const data = activityChartData.value
  if (!data.length) return ''
  const maxVal = Math.max(peakActivityValue.value, 4)
  const width = 800
  const height = 260
  const padX = 50
  const padY = 50
  const stepX = (width - 2 * padX) / (data.length - 1 || 1)

  const pts = data.map((d, idx) => {
    const x = padX + idx * stepX
    const y = height - padY - (d.users / maxVal) * (height - 2 * padY)
    return { x, y }
  })

  let path = `M ${pts[0].x} ${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cpX = (prev.x + curr.x) / 2
    path += ` C ${cpX} ${prev.y}, ${cpX} ${curr.y}, ${curr.x} ${curr.y}`
  }
  return path
})

const activityLabels = computed(() => {
  const pts = activityPoints.value
  const data = activityChartData.value
  return pts.map((p, idx) => ({ x: p.x, text: data[idx]?.label || '' }))
})

// ==================== COMPUTED LIVE ACTIVITY STREAM ====================

const recentActivities = computed(() => {
  const list = []

  // Signatures récentes
  signatures.value.slice(0, 3).forEach(sig => {
    const date = sig.createdAt?.toDate ? sig.createdAt.toDate() : new Date(sig.createdAt || sig.signature_timestamp || Date.now())
    list.push({
      title: 'Signature scellée',
      desc: (sig.signer_full_name || 'Utilisateur') + ' a signé ' + (sig.original_filename || 'document.pdf'),
      timeAgo: getTimeAgo(date),
      timestamp: date.getTime(),
      icon: 'bi-pen-fill',
      badgeClass: 'badge-emerald'
    })
  })

  // Organisations récentes
  organizations.value.slice(0, 2).forEach(org => {
    const date = new Date(org.created_at || Date.now())
    list.push({
      title: 'Nouvelle organisation',
      desc: org.name + ' (' + (org.approval_status || 'en attente') + ')',
      timeAgo: getTimeAgo(date),
      timestamp: date.getTime(),
      icon: 'bi-building-add',
      badgeClass: 'badge-purple'
    })
  })

  // Utilisateurs récents
  users.value.slice(0, 2).forEach(usr => {
    const date = usr.createdAt?.toDate ? usr.createdAt.toDate() : new Date(usr.createdAt || Date.now())
    list.push({
      title: 'Inscription utilisateur',
      desc: usr.displayName || usr.email || 'Nouveau compte',
      timeAgo: getTimeAgo(date),
      timestamp: date.getTime(),
      icon: 'bi-person-plus-fill',
      badgeClass: 'badge-blue'
    })
  })

  return list.sort((a, b) => b.timestamp - a.timestamp).slice(0, 5)
})

// ==================== FILTER COMPUTEDS ====================

const displayedOrgs = computed(() => {
  let list = []
  switch (currentOrgTab.value) {
    case 'pending': list = pendingOrgs.value; break
    case 'approved': list = approvedOrgs.value; break
    case 'rejected': list = rejectedOrgs.value; break
    default: list = organizations.value; break
  }

  if (!orgSearchQuery.value) return list
  const q = orgSearchQuery.value.toLowerCase()
  return list.filter(o => 
    (o.name && o.name.toLowerCase().includes(q)) ||
    (o.email && o.email.toLowerCase().includes(q)) ||
    (o.address && o.address.toLowerCase().includes(q)) ||
    (o.organization_type && o.organization_type.toLowerCase().includes(q))
  )
})

const filteredUsers = computed(() => {
  let list = users.value

  if (userRoleFilter.value !== 'all') {
    list = list.filter(u => {
      if (userRoleFilter.value === 'member') return !u.role || u.role === 'member'
      return u.role === userRoleFilter.value
    })
  }

  if (!userSearchQuery.value) return list
  const q = userSearchQuery.value.toLowerCase()
  return list.filter(u => 
    (u.displayName && u.displayName.toLowerCase().includes(q)) || 
    (u.email && u.email.toLowerCase().includes(q)) ||
    (u.id && u.id.toLowerCase().includes(q))
  )
})

const filteredSignatures = computed(() => {
  if (!sigSearchQuery.value) return signatures.value
  const q = sigSearchQuery.value.toLowerCase()
  return signatures.value.filter(s => 
    (s.document_id && s.document_id.toLowerCase().includes(q)) ||
    (s.id && s.id.toLowerCase().includes(q)) ||
    (s.signer_full_name && s.signer_full_name.toLowerCase().includes(q)) ||
    (s.signer_email && s.signer_email.toLowerCase().includes(q)) ||
    (s.original_filename && s.original_filename.toLowerCase().includes(q))
  )
})

// ==================== ACTIONS ====================

const handleApproveOrg = async (id) => {
  try {
    await OrganizationApiService.validateOrganization(id)
  } catch (error) {
    alert(locale.value === 'fr' ? 'Erreur lors de la validation' : 'Error during validation')
  }
}

const handleRejectOrg = async (id, permanent = false) => {
  const message = permanent 
    ? (locale.value === 'fr' ? 'Supprimer définitivement cette organisation ? Cette action est irréversible.' : 'Permanently delete this organization? This action is irreversible.')
    : (locale.value === 'fr' ? 'Rejeter cette organisation ?' : 'Reject this organization?')
  if (confirm(message)) {
    try {
      if (permanent) {
        const { db } = OrganizationApiService.getFirebase()
        const { doc, deleteDoc } = await import('firebase/firestore')
        await deleteDoc(doc(db, 'organizations', id))
      } else {
        await OrganizationApiService.rejectOrganization(id)
      }
    } catch (error) {
      alert(locale.value === 'fr' ? 'Erreur lors du traitement' : 'Error during processing')
    }
  }
}

const handleRevokeOrg = async (id) => {
  if (confirm(locale.value === 'fr' ? 'Mettre cette organisation en attente de validation ?' : 'Put this organization on pending validation?')) {
    try {
      const { db } = OrganizationApiService.getFirebase()
      const { doc, updateDoc } = await import('firebase/firestore')
      await updateDoc(doc(db, 'organizations', id), { approval_status: 'pending' })
    } catch (error) {
      alert(locale.value === 'fr' ? 'Erreur' : 'Error')
    }
  }
}

const handleRehabilitateOrg = async (id) => {
  if (confirm(locale.value === 'fr' ? 'Réhabiliter cette organisation ? Elle sera de nouveau active.' : 'Rehabilitate this organization?')) {
    try {
      const { db } = OrganizationApiService.getFirebase()
      const { doc, updateDoc } = await import('firebase/firestore')
      await updateDoc(doc(db, 'organizations', id), { 
        approval_status: 'approved',
        rehabilitated_at: new Date().toISOString()
      })
    } catch (error) {
      alert(locale.value === 'fr' ? 'Erreur lors de la réhabilitation' : 'Error during rehabilitation')
    }
  }
}

const handleRoleChange = async (userId, newRole) => {
  if (confirm(locale.value === 'fr' ? `Attribuer le rôle "${newRole}" à cet utilisateur ?` : `Assign role "${newRole}" to this user?`)) {
    try {
      await AdminApiService.updateUserRole(userId, newRole)
    } catch (error) {
      alert(locale.value === 'fr' ? 'Erreur lors du changement de rôle' : 'Error changing role')
    }
  }
}

// ==================== HELPERS ====================

const formatDate = (dateString) => {
  if (!dateString) return locale.value === 'fr' ? 'Inconnue' : 'Unknown'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return locale.value === 'fr' ? 'Invalide' : 'Invalid'
  return new Intl.DateTimeFormat(locale.value === 'fr' ? 'fr-FR' : 'en-US', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }).format(date)
}

const getTimeAgo = (date) => {
  const diffSec = Math.floor((Date.now() - date.getTime()) / 1000)
  if (diffSec < 60) return "À l'instant"
  if (diffSec < 3600) return `Il y a ${Math.floor(diffSec / 60)} min`
  if (diffSec < 86400) return `Il y a ${Math.floor(diffSec / 3600)} h`
  return `Il y a ${Math.floor(diffSec / 86400)} j`
}

const getStatusText = (status) => {
  if (status === 'approved') return locale.value === 'fr' ? 'Approuvée' : 'Approved'
  if (status === 'rejected') return locale.value === 'fr' ? 'Rejetée' : 'Rejected'
  return locale.value === 'fr' ? 'En attente' : 'Pending'
}

const getRoleBadgeClass = (role) => {
  if (role === 'super-admin') return 'bg-primary-blue text-white'
  if (role === 'chief') return 'bg-info-subtle text-info-emphasis border border-info-subtle'
  return 'bg-light text-secondary border'
}

const getRoleText = (role) => {
  if (role === 'super-admin') return 'Super Admin'
  if (role === 'chief') return locale.value === 'fr' ? 'Chef Org' : 'Org Chief'
  return locale.value === 'fr' ? 'Membre' : 'Member'
}
</script>

<style scoped>
.super-admin-page {
  padding-bottom: 3rem;
}

/* ==========================================================================
   HEADER DE LA PAGE (DESIGN SIGNATURE GVB)
   ========================================================================== */
.documents-header {
  padding: 1.5rem 0 2rem 0;
  margin-bottom: 2rem;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 2rem;
  position: relative;
}

.header-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.section-title {
  font-size: 2.8rem;
  font-weight: 700;
  font-family: 'Raleway', sans-serif;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.15rem;
  color: #6c757d;
  margin-bottom: 0;
  font-weight: 400;
  max-width: 650px;
}

.header-image {
  flex-shrink: 0;
  position: relative;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
}

.documents-illustration {
  width: 380px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.documents-illustration:hover {
  transform: translateY(-4px);
  filter: drop-shadow(0 8px 20px rgba(0, 102, 204, 0.15));
}

/* Bulles décoratives avec animation flottante */
.bubble {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 102, 204, 0.1);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 90px;
  height: 90px;
  top: -8%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 110px;
  height: 110px;
  top: 45%;
  right: 2%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.4s forwards, float 6s ease-in-out infinite 1.4s;
}

.bubble-3 {
  width: 75px;
  height: 75px;
  bottom: 0%;
  right: 25%;
  animation: fadeInScale 1s ease-out 1.6s forwards, float 6s ease-in-out infinite 1.6s;
}

.bubble-4 {
  width: 80px;
  height: 80px;
  top: 30%;
  left: -5%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

/* Badge Super Admin */
.badge-superadmin {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08) 0%, rgba(0, 123, 255, 0.12) 100%);
  color: var(--primary-blue);
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  padding: 0.35rem 0.85rem;
  border-radius: 50px;
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.badge-superadmin i {
  color: #f59e0b;
}

/* Alerte Bannière */
.alert-pending-banner {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid #fde68a;
  animation: pulseGlow 3s infinite alternate;
}

@keyframes pulseGlow {
  0% { box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1); }
  100% { box-shadow: 0 8px 25px rgba(245, 158, 11, 0.25); }
}

.spin-animation {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* ==========================================================================
   STAT CARDS (DESIGN IDENTIQUE A DASHBOARD.VUE / DOCUMENTSPAGE.VUE)
   ========================================================================== */
.stats-section {
  margin-bottom: 2.5rem;
}

.stat-card {
  background: white;
  border-radius: 14px;
  padding: 1.5rem 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 2px 12px rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.08);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 102, 204, 0.12);
  border-color: rgba(0, 102, 204, 0.25);
}

.stat-icon {
  width: 52px;
  height: 52px;
  background: rgba(0, 102, 204, 0.08);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.35rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.85rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
  font-family: 'Raleway', sans-serif;
  line-height: 1.1;
}

.stat-label {
  color: #6c757d;
  font-size: 0.875rem;
  margin-bottom: 0;
  font-weight: 500;
}

/* ==========================================================================
   EN-TÊTE DE SECTION (SECTIONS-HEADER DANS DASHBOARD & DOCUMENTSPAGE)
   ========================================================================== */
.sections-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.sections-title {
  font-family: 'Raleway', sans-serif;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.sections-subtitle {
  font-size: 1.05rem;
  font-weight: 400;
  color: #6c757d;
}

/* ==========================================================================
   CARTES DE GRAPHIQUES ET CONTENEURS BLANCS AIRÉS
   ========================================================================== */
.chart-card-clean {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid rgba(0, 102, 204, 0.08);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.06);
  transition: all 0.3s ease;
}

.chart-card-clean:hover {
  box-shadow: 0 10px 30px rgba(0, 102, 204, 0.1);
  border-color: rgba(0, 102, 204, 0.18);
}

/* SVG Chart */
.svg-chart-container {
  min-height: 220px;
}

.chart-point {
  cursor: pointer;
  transition: all 0.2s ease;
}

.chart-point:hover {
  r: 7;
  stroke-width: 3.5;
  filter: drop-shadow(0 0 6px rgba(0, 102, 204, 0.6));
}

.chart-tooltip {
  position: absolute;
  background: rgba(15, 23, 42, 0.9);
  color: #ffffff;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  pointer-events: none;
  transform: translate(-50%, -100%);
  font-size: 0.75rem;
  white-space: nowrap;
  z-index: 10;
}

.legend-color-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* Donut Chart */
.donut-svg {
  width: 180px;
  height: 180px;
  max-width: 100%;
}

.donut-segment {
  transition: stroke-dashoffset 1s ease-out;
}

.donut-center-info {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.donut-percentage {
  line-height: 1;
}

.cursor-pointer {
  cursor: pointer;
}

.legend-row:hover {
  background: #f8fafc;
}

/* Live Audit Timeline */
.timeline-icon-badge {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.badge-blue { background: rgba(0, 102, 204, 0.1); color: #0066cc; }
.badge-purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
.badge-emerald { background: rgba(16, 185, 129, 0.1); color: #10b981; }

/* Cartes Organisations */
.organization-card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid rgba(0, 102, 204, 0.08);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.organization-card:hover {
  transform: translateY(-3px);
  border-color: rgba(0, 102, 204, 0.25);
  box-shadow: 0 10px 25px rgba(0, 102, 204, 0.08) !important;
}

.organization-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.approval-status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.approval-status-badge.approved {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.approval-status-badge.pending {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.25);
}

.approval-status-badge.rejected {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.25);
}

.avatar-initials {
  flex-shrink: 0;
  font-size: 0.9rem;
}

/* Custom Table */
.custom-table th {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  font-weight: 700;
}

.custom-table td {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

/* ==========================================================================
   ANIMATIONS GVB SIGN
   ========================================================================== */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
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

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.2);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(25px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .header-container {
    flex-direction: column;
    text-align: center;
  }

  .header-content {
    text-align: center;
  }

  .section-subtitle {
    margin: 0 auto;
  }

  .header-actions {
    justify-content: center;
  }

  .documents-illustration {
    width: 280px;
  }
}
</style>
