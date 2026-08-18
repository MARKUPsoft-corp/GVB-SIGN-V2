<template>
  <div class="organization-manager-page">
  <!-- Bouton de fermeture -->
  <button class="close-organization-btn" @click="closeOrganizationDashboard" title="Fermer et retourner à la sélection d'organisation">
    <i class="bi bi-x"></i>
  </button>
  
  <!-- Header avec titre de la section -->
    <div class="organization-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="display-4 fw-bold mb-3 text-dark header-title">
            <span class="text-dark">Espace Direction de l'</span>
            <span class="text-primary-blue">organisation </span>
            <span class="text-primary-blue" v-if="userOrganization && userOrganization.organization"> {{ userOrganization.organization.name }}</span>
          </h1>
          <p class="lead mb-3 text-dark sections-subtitle" v-if="userOrganization && userOrganization.organization">
            Gérez l'organisation {{ userOrganization.organization.name }} et supervisez les équipes.
          </p>
          <p class="lead mb-3 text-dark sections-subtitle" v-else>
            Vous êtes directeur d'une organisation. Gérez et supervisez les équipes.
          </p>
          <div class="role-badge mb-3">
            <i class="bi bi-person-badge me-2"></i>
            <span class="role-text">{{ roleDisplayName }}</span>
            <span v-if="userOrganization && userOrganization.organization" class="organization-context">
              de {{ userOrganization.organization.name }}
            </span>
          </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Organisation Direction" class="organization-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques avancées -->
    <div class="docs-stats-section">
      <div class="row g-4">
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.totalDocuments || 0 }}</h4>
              <p class="stat-label">Total documents</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.totalMembers || 0 }}</h4>
              <p class="stat-label">Membres actifs</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-graph-up"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.productivityScore || 0 }}%</h4>
              <p class="stat-label">Productivité</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ managerStats.pendingTasks || 0 }}</h4>
              <p class="stat-label">Tâches en cours</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sections de gestion en deux colonnes -->
    <div v-if="!showAllDocuments" class="documents-sections">
      <!-- En-tête de section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Gestion</span> 
              <span class="text-primary-blue"> Documentaire</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Signez les documents de l'organisation et supervisez les équipes.
            </p>
          </div>
        </div>
      </div>

      <!-- Système d'onglets pour la gestion documentaire -->
      <div class="tabs-container">
        <div class="tabs-header">
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'prepared-immediate' }"
            @click="setActiveDocumentTab('prepared-immediate')"
          >
            <i class="bi bi-file-earmark-arrow-up me-2"></i>
            Documents préparés
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'signed-documents' }"
            @click="setActiveDocumentTab('signed-documents')"
          >
            <i class="bi bi-file-earmark-pen me-2"></i>
            Documents signés
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeDocumentTab === 'org-management' }"
            @click="setActiveDocumentTab('org-management')"
          >
            <i class="bi bi-gear me-2"></i>
            Gestion de l'organisation
          </button>
              </div>

        <!-- Contenu de l'onglet "Documents préparés immédiatement" -->
        <div v-if="activeDocumentTab === 'prepared-immediate'" class="tab-content">
         <!-- En-tête avec barre de recherche -->
         <div class="d-flex justify-content-between align-items-center mb-4">
           <!-- Barre de recherche -->
           <div class="search-container">
             <div class="search-input-wrapper">
               <i class="bi bi-search search-icon"></i>
               <input 
                 type="text" 
                 class="search-input" 
                 placeholder="Rechercher dans les documents..."
                 v-model="searchQuery"
                 @input="searchDocuments"
               >
               <button 
                 v-if="searchQuery" 
                 class="clear-search-btn"
                 @click="clearSearch"
               >
                 <i class="bi bi-x"></i>
               </button>
              </div>
            </div>
            
           <!-- Bouton Tout signer -->
           <div class="sign-all-btn-container" :class="{ 'has-tooltip': (filteredDocuments.length === 0 || !hasCertificates) }">
             <button 
               class="btn btn-primary-blue sign-all-btn"
               @click="signAllDocuments"
               :disabled="filteredDocuments.length === 0 || !hasCertificates"
             >
               <i class="bi bi-pen me-2"></i>
               Tout signer
             </button>
             
             <!-- Info-bulle pour bouton désactivé -->
             <div v-if="filteredDocuments.length === 0 || !hasCertificates" class="info-tooltip">
               <div class="tooltip-content">
                 <i class="bi bi-info-circle me-2"></i>
                 <div class="tooltip-text">
                   <strong>Bouton désactivé</strong><br>
                   <span v-if="filteredDocuments.length === 0">Aucun document à signer</span>
                   <span v-else-if="!hasCertificates">Aucun certificat de signature disponible</span>
                </div>
               </div>
               <div class="tooltip-arrow"></div>
             </div>
                </div>
              </div>

          <!-- Loading state -->
          <div v-if="isLoadingDocuments" class="text-center py-5">
            <div class="spinner-border text-primary-blue" role="status">
              <span class="visually-hidden">Chargement...</span>
                </div>
            <p class="text-muted mt-3">Chargement des documents...</p>
              </div>

          <!-- Error state -->
          <div v-else-if="documentsError" class="text-center py-5">
            <div class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ documentsError }}
                </div>
              </div>

          <!-- Documents grid -->
          <div v-else-if="filteredDocuments.length > 0" class="documents-grid">
            <div 
              class="document-card" 
              v-for="(document, index) in filteredDocuments" 
              :key="document.id"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <!-- Header de la carte -->
              <div class="card-header">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf"></i>
                </div>
                <div class="document-name">{{ document.document_title || document.original_filename }}</div>
                <div class="document-header-content">
                  <div class="organization-badge">
                    <span>{{ document.organization_name }}</span>
                </div>
              </div>
            </div>

              <!-- Contenu de la carte -->
              <div class="card-content">
                <p class="document-description">{{ document.document_description || 'Aucune description' }}</p>
                
                <!-- Hiérarchie de signature -->
                <div class="signature-hierarchy">
                  <h6 class="hierarchy-title">
                    <i class="bi bi-diagram-3 me-2"></i>
                    Hiérarchie de signature
                  </h6>
                  <div class="signature-steps">
                    <!-- Étapes précédentes (complétées) -->
                    <div class="signature-step completed" v-if="document.current_step > 1">
                      <div class="step-indicator">
                        <i class="bi bi-check-circle-fill"></i>
            </div>
                      <div class="step-content">
                        <span class="step-title">Préparé par</span>
                        <span class="step-person">{{ document.prepared_by_name }}</span>
          </div>
        </div>
        
                    <!-- Étape actuelle -->
                    <div class="signature-step current">
                      <div class="step-indicator">
                        <i class="bi bi-clock"></i>
              </div>
                      <div class="step-content">
                        <span class="step-title">En attente de signature</span>
                        <span class="step-person">{{ document.current_signer_name || 'Non assigné' }}</span>
              </div>
            </div>
            
                    <!-- Étapes restantes -->
                    <div class="signature-step pending" v-if="document.current_step < document.total_steps">
                      <div class="step-indicator">
                        <i class="bi bi-circle"></i>
                  </div>
                      <div class="step-content">
                        <span class="step-title">Étapes restantes</span>
                        <span class="step-person">{{ document.total_steps - document.current_step }} étape(s)</span>
                  </div>
                  </div>
                </div>
              </div>

                  </div>
              
              <!-- Footer de la carte -->
              <div class="card-footer">
                <div class="document-info">
                  <div class="document-meta">
                    <div class="meta-item">
                      <i class="bi bi-calendar"></i>
                      <span>{{ formatDate(document.created_at) }}</span>
                  </div>
                    <div class="meta-item">
                      <i class="bi bi-bar-chart"></i>
                      <span>{{ document.progress_percentage || 0 }}% complété</span>
                  </div>
                </div>
                  <span class="document-step">Étape {{ document.current_step || 1 }}/{{ document.total_steps || 1 }}</span>
              </div>
               <div class="document-actions">
                 <button 
                   class="btn btn-sm btn-outline-primary" 
                   title="Aperçu du document"
                   @click="showDocumentPreview(document, 'current', $event)"
                 >
                   <i class="bi bi-eye"></i>
                 </button>
                 <button 
                   class="btn btn-sm btn-outline-info" 
                   title="Aperçu final (PDF généré)" 
                   v-if="document.generated_pdf"
                   @click="showDocumentPreview(document, 'generated', $event)"
                 >
                   <i class="bi bi-file-earmark-pdf"></i>
                 </button>
                 <div class="sign-btn-container" :class="{ 'has-tooltip': !hasCertificates }">
                   <button 
                     class="btn btn-sm btn-primary-blue sign-btn" 
                     :class="{ 'disabled': !hasCertificates }"
                     :disabled="!hasCertificates"
                     @click="signDocument(document)"
                   >
                     <i class="bi bi-pen me-1"></i>
                     Signer
                   </button>
                   
                   <!-- Info-bulle pour bouton désactivé -->
                   <div v-if="!hasCertificates" class="info-tooltip">
                     <div class="tooltip-content">
                       <i class="bi bi-info-circle me-2"></i>
                       <div class="tooltip-text">
                         <strong>Bouton désactivé</strong><br>
                         Aucun certificat de signature disponible
                  </div>
                  </div>
                     <div class="tooltip-arrow"></div>
                   </div>
                 </div>
                 <button 
                   class="btn btn-sm btn-outline-success" 
                   title="Télécharger"
                   @click="downloadDocument(document)"
                 >
                   <i class="bi bi-download"></i>
                 </button>
                  </div>
                  </div>
                </div>
              </div>

          <!-- Empty state -->
          <div v-else-if="preparedDocuments.length === 0" class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-arrow-up fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Aucun document préparé</h4>
              <p class="text-muted mb-4">Aucun document n'est en attente de signature pour cette organisation</p>
                  </div>
                  </div>

          <!-- No search results state -->
          <div v-else-if="searchQuery && filteredDocuments.length === 0" class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-search fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Aucun résultat trouvé</h4>
              <p class="text-muted mb-4">Aucun document ne correspond à votre recherche</p>
              <button class="btn btn-primary-blue" @click="clearSearch">
                <i class="bi bi-arrow-left me-2"></i>
                Effacer la recherche
              </button>
                  </div>
                </div>
              </div>

        <!-- Contenu de l'onglet "Documents préparés avec modèle" -->
        <div v-if="activeDocumentTab === 'prepared-with-model'" class="tab-content">
          <div class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-check fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Documents Préparés avec Modèle</h4>
              <p class="text-muted mb-4">Documents créés à partir de modèles en attente de signature</p>
              <button class="btn btn-primary-blue">
                <i class="bi bi-eye me-2"></i>
                Voir les documents avec modèle
              </button>
            </div>
              </div>
            </div>

        <!-- Contenu de l'onglet "Documents signés" -->
        <div v-if="activeDocumentTab === 'signed-documents'" class="tab-content">
          
          <!-- Loading state -->
          <div v-if="isLoadingSignedDocuments" class="text-center py-5">
            <div class="spinner-border text-primary-blue" role="status">
              <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="text-muted mt-3">Chargement des documents signés...</p>
          </div>

          <!-- Error state -->
          <div v-else-if="signedDocumentsError" class="text-center py-5">
            <div class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle me-2"></i>
              {{ signedDocumentsError }}
            </div>
          </div>

          <!-- Empty state -->
          <div v-else-if="signedDocuments.length === 0" class="text-center py-5">
            <div class="tab-placeholder">
              <i class="bi bi-file-earmark-pen fs-1 text-primary-blue mb-3"></i>
              <h4 class="text-dark mb-3">Aucun Document Signé</h4>
              <p class="text-muted mb-4">Aucun document n'a encore été signé dans cette organisation</p>
            </div>
          </div>

          <!-- Documents list -->
          <div v-else class="signed-documents-list">
            <!-- Header avec barre de recherche -->
            <div class="signed-docs-header mb-4">
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="mb-0">
                  <i class="bi bi-file-earmark-pen me-2"></i>
                  Documents Signés ({{ filteredSignedDocuments.length }})
                </h4>
                
                <!-- Barre de recherche -->
                <div class="search-container">
                  <div class="search-input-wrapper">
                    <i class="bi bi-search search-icon"></i>
                    <input 
                      type="text" 
                      class="search-input" 
                      placeholder="Rechercher dans les documents signés..."
                      v-model="signedDocumentsSearchQuery"
                      @input="searchSignedDocuments"
                    >
                    <button 
                      v-if="signedDocumentsSearchQuery" 
                      class="clear-search-btn"
                      @click="clearSignedDocumentsSearch"
                    >
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="signed-document-item" v-for="document in filteredSignedDocuments" :key="document.id">
              <!-- En-tête du document -->
              <div class="signed-doc-header">
                <div class="doc-icon">
                  <i class="bi bi-file-earmark-pdf-fill"></i>
                </div>
                <div class="doc-info">
                  <h5 class="doc-title">{{ document.original_filename }}</h5>
                  <div class="doc-meta">
                    <span class="meta-item">
                      <i class="bi bi-person-check me-1"></i>
                      {{ document.signer_name }}
                    </span>
                    <span class="meta-item">
                      <i class="bi bi-calendar-check me-1"></i>
                      {{ formatDate(document.signature_timestamp) }}
                    </span>
                    <span class="meta-item">
                      <i class="bi bi-building me-1"></i>
                      {{ document.organization_name }}
                    </span>
                  </div>
                </div>
                <div class="doc-status">
                  <span class="status-badge status-signed">
                    <i class="bi bi-check-circle-fill me-1"></i>
                    Signé
                  </span>
                </div>
              </div>

              <!-- Détails du document -->
              <div class="signed-doc-details">
                <div class="detail-row">
                  <div class="detail-item">
                    <span class="detail-label">
                      <i class="bi bi-fingerprint me-1"></i>
                      Hash SHA-256
                    </span>
                    <span class="detail-value hash-value" :title="document.document_hash">
                      {{ document.document_hash.substring(0, 16) }}...
                    </span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">
                      <i class="bi bi-file-earmark-arrow-down me-1"></i>
                      Taille originale
                    </span>
                    <span class="detail-value">
                      {{ formatFileSize(document.file_size_original) }}
                    </span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">
                      <i class="bi bi-file-earmark-check me-1"></i>
                      Taille signée
                    </span>
                    <span class="detail-value">
                      {{ formatFileSize(document.file_size_signed) }}
                    </span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">
                      <i class="bi bi-clock-history me-1"></i>
                      Temps d'exécution
                    </span>
                    <span class="detail-value">
                      {{ document.execution_time.toFixed(3) }}s
                    </span>
                  </div>
                </div>

                <!-- Workflow history si disponible -->
                <div v-if="document.is_workflow_document && document.workflow_history.length > 0" class="workflow-info">
                  <h6 class="workflow-title">
                    <i class="bi bi-diagram-3 me-2"></i>
                    Historique du workflow
                  </h6>
                  <div class="workflow-steps">
                    <div 
                      class="workflow-step-mini" 
                      v-for="(step, index) in document.workflow_history" 
                      :key="index"
                    >
                      <div class="step-number">{{ step.step }}</div>
                      <div class="step-info-mini">
                        <span class="step-name">{{ step.user_name }}</span>
                        <span class="step-role">{{ step.role }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div class="signed-doc-actions">
                <button 
                  @click="downloadDocument(document)"
                  class="action-btn btn-download"
                >
                  <i class="bi bi-download me-2"></i>
                  Télécharger le document signé
                </button>
                <button 
                  @click="showDocumentPreview(document, 'original', $event)"
                  class="action-btn btn-view-original"
                >
                  <i class="bi bi-eye me-2"></i>
                  Voir l'original
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Vue complète du tableau de bord -->
    <div v-else class="all-documents-view">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">Tableau de bord de direction</h3>
            <div class="d-flex gap-2">
              <button class="btn btn-primary" @click="toggleAnalyticsModal">
                <i class="bi bi-graph-up me-2"></i>
                Analyses avancées
              </button>
              <button class="btn btn-outline-primary" @click="toggleAllDocuments">
                <i class="bi bi-arrow-left me-2"></i>
                Retour aux sections
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tableau de bord complet -->
      <div class="dashboard-grid">
        <!-- Graphique de performance -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Performance de l'organisation</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="refreshPerformance">
                <i class="bi bi-arrow-clockwise"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="performance-chart">
              <div class="chart-placeholder">
                <i class="bi bi-graph-up fs-1 text-primary-blue"></i>
                <p class="text-muted">Graphique de performance</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Membres de l'équipe -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Membres de l'équipe</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="toggleTeamManagement">
                <i class="bi bi-people"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="team-members">
              <div class="team-member" v-for="member in teamMembers" :key="member.id">
                <div class="member-avatar">
                  <i class="bi bi-person-circle"></i>
                </div>
                <div class="member-info">
                  <h6 class="member-name">{{ member.name }}</h6>
                  <p class="member-role">{{ member.role }}</p>
                </div>
                <div class="member-status" :class="member.status">
                  <i class="bi bi-circle-fill"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Documents récents -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Documents récents</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="viewAllDocuments">
                <i class="bi bi-eye"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="recent-documents">
              <div class="document-item" v-for="(document, index) in recentDocuments" :key="index">
                <div class="document-icon">
                  <i class="bi bi-file-earmark-pdf text-danger"></i>
                </div>
                <div class="document-info">
                  <h6 class="document-name">{{ document.name }}</h6>
                  <p class="document-meta">{{ document.author }} • {{ document.date }}</p>
                </div>
                <div class="document-status" :class="document.status">
                  <span class="status-badge" :class="document.status">{{ document.statusText }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Activité récente -->
        <div class="dashboard-card">
          <div class="card-header">
            <h5 class="card-title">Activité récente</h5>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline-primary" @click="viewActivityLog">
                <i class="bi bi-clock-history"></i>
              </button>
            </div>
          </div>
          <div class="card-content">
            <div class="activity-feed">
              <div class="activity-item" v-for="(activity, index) in recentActivity" :key="index">
                <div class="activity-icon" :class="activity.type">
                  <i :class="activity.icon"></i>
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.description }}</p>
                  <span class="activity-time">{{ activity.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale d'analyses avancées -->
    <div v-if="showAnalyticsModal" class="modal-overlay" @click="closeAnalyticsModal">
      <div class="modal-content analytics-modal" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Analyses avancées</h5>
          <button class="btn-close" @click="closeAnalyticsModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="analytics-tabs">
            <button class="tab-btn" :class="{ active: activeTab === 'performance' }" @click="activeTab = 'performance'">
              Performance
            </button>
            <button class="tab-btn" :class="{ active: activeTab === 'team' }" @click="activeTab = 'team'">
              Équipe
            </button>
            <button class="tab-btn" :class="{ active: activeTab === 'documents' }" @click="activeTab = 'documents'">
              Documents
            </button>
          </div>
          
          <div class="analytics-content">
            <div v-if="activeTab === 'performance'" class="analytics-panel">
              <h6>Analyse de performance</h6>
              <p class="text-muted">Graphiques et métriques de performance de l'organisation.</p>
            </div>
            <div v-if="activeTab === 'team'" class="analytics-panel">
              <h6>Analyse d'équipe</h6>
              <p class="text-muted">Statistiques et performances des membres de l'équipe.</p>
            </div>
            <div v-if="activeTab === 'documents'" class="analytics-panel">
              <h6>Analyse de documents</h6>
              <p class="text-muted">Métriques et tendances des documents de l'organisation.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Tooltip de prévisualisation de document -->
    <div 
      v-if="showPreviewTooltip" 
      class="document-preview-tooltip" 
      :style="{ top: tooltipPosition.top + 'px', left: tooltipPosition.left + 'px' }" 
      @click.stop 
      @mouseenter="cancelCloseTooltip" 
      @mouseleave="closePreviewTooltip"
    >
      <div class="tooltip-arrow" :class="'arrow-' + tooltipDirection"></div>
      <div class="tooltip-content">
        <div class="tooltip-header">
           <h4 class="tooltip-title">
             <i class="bi bi-file-earmark-pdf me-2"></i>
             {{ previewType === 'current' ? 'Document actuel (workflow)' : 'PDF généré (avec éléments)' }} - {{ currentPreviewDocument?.document_title || currentPreviewDocument?.original_filename }}
           </h4>
          <button class="tooltip-close" @click="closePreviewTooltip">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="tooltip-body">
          
            <!-- Aperçu PDF exactement comme dans DocumentPreparationPage -->
            <div class="pdf-preview-content">
              <div v-if="previewPdfSource && !pdfLoadError" class="pdf-container">
                <!-- Solution simple avec iframe native -->
                <iframe
                  :src="previewPdfSource"
                  class="pdf-iframe"
                  frameborder="0"
                  @load="onPreviewPdfLoaded"
                  @error="onPreviewPdfLoadError"
                ></iframe>
              </div>
              
              <!-- Fallback si iframe ne fonctionne pas -->
              <div v-else-if="previewPdfSource && pdfLoadError" class="pdf-fallback">
                <div class="fallback-content">
                  <i class="bi bi-file-earmark-pdf-fill"></i>
                  <h3>{{ currentPreviewDocument?.document_title || currentPreviewDocument?.original_filename || 'Document PDF' }}</h3>
                  <p class="fallback-description">
                    <i class="bi bi-info-circle me-2"></i>
                    Aperçu non disponible dans cette vue
                  </p>
                  <p class="fallback-subtitle">
                    Cliquez sur "Ouvrir dans un nouvel onglet" pour voir le contenu complet
                  </p>
                  <div class="fallback-actions">
                    <button 
                      class="btn btn-primary me-2" 
                      @click="openDocumentDirectly"
                    >
                      <i class="bi bi-box-arrow-up-right me-2"></i>
                      Ouvrir le PDF
                    </button>
                    <a 
                      :href="previewPdfSource" 
                      :download="currentPreviewDocument?.original_filename || 'document.pdf'"
                      class="btn btn-outline-primary"
                    >
                      <i class="bi bi-download me-2"></i>
                      Télécharger
                    </a>
                  </div>
                </div>
              </div>
              
              <!-- État de chargement -->
              <div v-else-if="!previewPdfSource && !pdfLoadError" class="pdf-loading-state">
                <i class="bi bi-file-earmark-pdf-fill fs-1 text-primary mb-3"></i>
                <p>Chargement du document...</p>
              </div>
              
              <!-- État d'erreur -->
              <div v-else-if="pdfLoadError" class="pdf-error-state">
                <i class="bi bi-exclamation-triangle fs-1 text-warning mb-3"></i>
                <p>Impossible de charger le PDF</p>
                <button class="btn btn-sm btn-outline-primary mt-2" @click="retryPdfLoad">
                  <i class="bi bi-arrow-clockwise me-1"></i>
                  Réessayer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { DocumentSigningService } from '../../services/DocumentSigningService'
import OrganizationApiService from '../../services/OrganizationApiService'
import { SignatureApiService } from '../../services/SignatureApiService'

// Store d'authentification
const authStore = useAuthStore()

// Service de signature de documents
const documentSigningService = new DocumentSigningService()

// Gestion des onglets de gestion documentaire
const activeDocumentTab = ref('prepared-immediate')

// Données pour les documents préparés
const preparedDocuments = ref([])
const filteredDocuments = ref([])
const isLoadingDocuments = ref(false)
const documentsError = ref(null)
const searchQuery = ref('')

// Données pour les documents signés
const signedDocuments = ref([])
const filteredSignedDocuments = ref([])
const isLoadingSignedDocuments = ref(false)
const signedDocumentsError = ref(null)
const signedDocumentsSearchQuery = ref('')

// Variables pour les tooltips de prévisualisation
const showPreviewTooltip = ref(false)
const previewType = ref('')
const tooltipPosition = ref({ top: 0, left: 0 })
const tooltipDirection = ref('right')
const currentPreviewDocument = ref(null)
const closeTooltipTimeout = ref(null)
const previewPdfSource = ref(null)
const pdfLoadError = ref(false)

// Variables pour les certificats
const hasCertificates = ref(false)
const isLoadingCertificates = ref(false)

// État des données
const userOrganization = ref(null)
const selectedOrganization = ref(null)
const userRole = ref(null)
const showAllDocuments = ref(false)
const showAnalyticsModal = ref(false)

// Computed pour l'organisation
const organizationName = computed(() => {
  return userOrganization.value?.organization?.name || userOrganization.value?.name || ''
})

// Computed pour le rôle
const roleDisplayName = computed(() => {
  if (!userRole.value) return 'Membre'
  
  const roleMap = {
    'admin': 'Administrateur',
    'chief': 'Chef (Directeur)',
    'secretaire': 'Secrétaire', 
    'chef': 'Chef',
    'chef+1': 'Chef +1',
    'chef+2': 'Chef +2',
    'chef+n': 'Chef +n',
    'member': 'Membre'
  }
  
  return roleMap[userRole.value] || 'Membre'
})
const activeTab = ref('performance')

// Statistiques du manager
const managerStats = ref({
  totalDocuments: 0,
  totalMembers: 0,
  productivityScore: 0,
  pendingTasks: 0,
  overallPerformance: 0,
  documentsInProgress: 0,
  activeTeamMembers: 0
})

// Membres de l'équipe
const teamMembers = ref([
  { id: 1, name: 'Jean Dupont', role: 'Secrétaire', status: 'active' },
  { id: 2, name: 'Marie Martin', role: 'Membre', status: 'active' },
  { id: 3, name: 'Pierre Durand', role: 'Chef d\'équipe', status: 'active' },
  { id: 4, name: 'Sophie Bernard', role: 'Membre', status: 'inactive' }
])

// Documents récents
const recentDocuments = ref([
  {
    name: 'Rapport mensuel Q1',
    author: 'Jean Dupont',
    date: '15 Jan 2024',
    status: 'signed',
    statusText: 'Signé'
  },
  {
    name: 'Contrat de service',
    author: 'Marie Martin',
    date: '12 Jan 2024',
    status: 'pending',
    statusText: 'En attente'
  },
  {
    name: 'Accord de confidentialité',
    author: 'Pierre Durand',
    date: '10 Jan 2024',
    status: 'draft',
    statusText: 'Brouillon'
  }
])

// Activité récente
const recentActivity = ref([
  {
    type: 'success',
    icon: 'bi bi-check-circle',
    description: 'Document "Rapport mensuel" signé par Jean Dupont',
    time: 'Il y a 2 heures'
  },
  {
    type: 'info',
    icon: 'bi bi-person-plus',
    description: 'Nouveau membre ajouté à l\'équipe',
    time: 'Il y a 4 heures'
  },
  {
    type: 'warning',
    icon: 'bi bi-exclamation-triangle',
    description: 'Document "Contrat de service" en attente depuis 3 jours',
    time: 'Il y a 1 jour'
  },
  {
    type: 'primary',
    icon: 'bi bi-file-earmark-plus',
    description: 'Nouveau document créé par Marie Martin',
    time: 'Il y a 2 jours'
  }
])

// Fonctions de navigation
const closeOrganizationDashboard = () => {
  // Émettre un événement pour retourner à la page de sélection d'organisation
  window.dispatchEvent(new CustomEvent('navigateToOrganizationSelection'))
}

const toggleAllDocuments = () => {
  showAllDocuments.value = !showAllDocuments.value
}

const toggleAnalyticsModal = () => {
  showAnalyticsModal.value = !showAnalyticsModal.value
}

const closeAnalyticsModal = () => {
  showAnalyticsModal.value = false
}

// Actions de direction
const toggleTeamManagement = () => {
  console.log('Gestion d\'équipe')
  // Logique pour gérer l'équipe
}

const generateReports = () => {
  console.log('Génération de rapports')
  // Logique pour générer des rapports
}

const openOrganizationSettings = () => {
  console.log('Paramètres de l\'organisation')
  // Émettre un événement pour ouvrir les paramètres
  emit('open-organization-settings')
}

const openAdvancedSettings = () => {
  console.log('Paramètres avancés')
  // Logique pour les paramètres avancés
}

// Gestion des onglets de gestion documentaire
const setActiveDocumentTab = (tab) => {
  activeDocumentTab.value = tab
  console.log('Onglet actif changé:', tab)
  
  // Charger les documents selon l'onglet sélectionné
  if (tab === 'prepared-immediate') {
    fetchPreparedDocuments()
  } else if (tab === 'signed-documents') {
    fetchSignedDocuments()
  }
}

// Récupérer les documents préparés depuis l'API
const fetchPreparedDocuments = async () => {
  console.log('🔄 Début de fetchPreparedDocuments')
  
  isLoadingDocuments.value = true
  documentsError.value = null
  
  try {
    const organizationId = userOrganization.value?.organization?.id || userOrganization.value?.id
    
    if (!organizationId) {
      throw new Error('Organisation non trouvée')
    }
    
    const signatureApiService = new SignatureApiService()
    const data = await signatureApiService.getDocumentPreparations(organizationId)
    
    if (data.success) {
      preparedDocuments.value = data.preparations || []
      filteredDocuments.value = data.preparations || []
      console.log('✅ Documents préparés récupérés:', preparedDocuments.value.length, 'documents')
    } else {
      throw new Error('Erreur lors de la récupération des documents')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des documents préparés:', error)
    documentsError.value = error.message
  } finally {
    isLoadingDocuments.value = false
  }
}

// Récupérer les documents signés depuis l'API
const fetchSignedDocuments = async () => {
  console.log('📄 Début de fetchSignedDocuments')
  
  isLoadingSignedDocuments.value = true
  signedDocumentsError.value = null
  
  try {
    const organizationId = userOrganization.value?.organization?.id || userOrganization.value?.id
    
    if (!organizationId) {
      throw new Error('Organisation non trouvée')
    }
    
    const signatureApiService = new SignatureApiService()
    const data = await signatureApiService.getSignedDocuments(organizationId)
    
    if (data.success) {
      signedDocuments.value = data.documents || []
      filteredSignedDocuments.value = data.documents || []
      console.log('✅ Documents signés récupérés:', signedDocuments.value.length, 'documents')
    } else {
      throw new Error('Erreur lors de la récupération des documents signés')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des documents signés:', error)
    signedDocumentsError.value = error.message
  } finally {
    isLoadingSignedDocuments.value = false
  }
}

// Fonctions de recherche
const searchDocuments = () => {
  if (!searchQuery.value.trim()) {
    filteredDocuments.value = preparedDocuments.value
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  filteredDocuments.value = preparedDocuments.value.filter(doc => 
    doc.document_title?.toLowerCase().includes(query) ||
    doc.original_filename?.toLowerCase().includes(query) ||
    doc.document_description?.toLowerCase().includes(query) ||
    doc.organization_name?.toLowerCase().includes(query)
  )
}

const clearSearch = () => {
  searchQuery.value = ''
  filteredDocuments.value = preparedDocuments.value
}

// Fonctions de recherche pour les documents signés
const searchSignedDocuments = () => {
  if (!signedDocumentsSearchQuery.value.trim()) {
    filteredSignedDocuments.value = signedDocuments.value
    return
  }
  
  const query = signedDocumentsSearchQuery.value.toLowerCase()
  filteredSignedDocuments.value = signedDocuments.value.filter(doc => 
    doc.original_filename?.toLowerCase().includes(query) ||
    doc.signer_name?.toLowerCase().includes(query) ||
    doc.signer_email?.toLowerCase().includes(query) ||
    doc.organization_name?.toLowerCase().includes(query) ||
    doc.document_hash?.toLowerCase().includes(query)
  )
}

const clearSignedDocumentsSearch = () => {
  signedDocumentsSearchQuery.value = ''
  filteredSignedDocuments.value = signedDocuments.value
}

// Fonction pour signer tous les documents
const signAllDocuments = async () => {
  if (filteredDocuments.value.length === 0) return
  
  try {
    // Vérifier d'abord si l'organisation a des certificats
    if (!hasCertificates.value) {
      // Afficher une notification d'erreur
      showNotification('error', 'Impossible de signer', 'Cette organisation n\'a pas importé de certificats de signature. Veuillez contacter l\'administrateur pour importer un certificat.')
      return
    }
    
    // Confirmation avant de signer tous les documents
    const confirmMessage = `Êtes-vous sûr de vouloir signer tous les ${filteredDocuments.value.length} document(s) affiché(s) ?`
    
    if (confirm(confirmMessage)) {
      console.log('🖊️ Signature de tous les documents:', filteredDocuments.value.length)
      
      // TODO: Implémenter la logique de signature en lot
      // Pour l'instant, on affiche juste un message
      alert(`Signature en cours de ${filteredDocuments.value.length} document(s)...`)
    }
  } catch (error) {
    console.error('❌ Erreur lors de la signature en lot:', error)
    showNotification('error', 'Erreur', 'Impossible de procéder à la signature en lot.')
  }
}

// Fonctions pour les tooltips de prévisualisation
const showDocumentPreview = (document, type, event) => {
  // Vérifier que nous sommes dans un environnement client
  if (typeof window === 'undefined') return
  
  // Annuler le délai de fermeture si la souris revient
  if (closeTooltipTimeout.value) {
    clearTimeout(closeTooltipTimeout.value)
    closeTooltipTimeout.value = null
  }
  
  // Calculer la position du tooltip par rapport au bouton cliqué
  if (event && event.target) {
    const button = event.target.closest('button')
    const rect = button ? button.getBoundingClientRect() : event.target.getBoundingClientRect()
    const scrollTop = window.pageYOffset || (document.documentElement ? document.documentElement.scrollTop : 0)
    const scrollLeft = window.pageXOffset || (document.documentElement ? document.documentElement.scrollLeft : 0)
    
    const tooltipWidth = 550 // Largeur du tooltip de prévisualisation
    const tooltipHeight = 750 // Hauteur du tooltip de prévisualisation
    const windowWidth = window.innerWidth
    const windowHeight = window.innerHeight
    
    // Calculer l'espace disponible de chaque côté
    const spaceLeft = rect.left
    const spaceRight = windowWidth - rect.right
    const spaceTop = rect.top
    const spaceBottom = windowHeight - rect.bottom
    
    let top, left, direction
    
    // Déterminer la meilleure position en fonction de l'espace disponible
    const horizontalSpace = Math.max(spaceLeft, spaceRight)
    const verticalSpace = Math.max(spaceTop, spaceBottom)
    
    if (horizontalSpace > verticalSpace) {
      // Position horizontale (droite ou gauche)
      if (spaceRight >= tooltipWidth + 20) {
        // À droite
        left = rect.right + 10
        top = rect.top + (rect.height / 2) - (tooltipHeight / 2)
        direction = 'right'
      } else if (spaceLeft >= tooltipWidth + 20) {
        // À gauche
        left = rect.left - tooltipWidth - 10
        top = rect.top + (rect.height / 2) - (tooltipHeight / 2)
        direction = 'left'
      } else {
        // Par défaut à droite
        left = rect.right + 10
        top = rect.top + (rect.height / 2) - (tooltipHeight / 2)
        direction = 'right'
      }
    } else {
      // Position verticale (haut ou bas)
      if (spaceBottom >= tooltipHeight + 20) {
        // En bas
        top = rect.bottom + 10
        left = rect.left + (rect.width / 2) - (tooltipWidth / 2)
        direction = 'bottom'
      } else if (spaceTop >= tooltipHeight + 20) {
        // En haut
        top = rect.top - tooltipHeight - 10
        left = rect.left + (rect.width / 2) - (tooltipWidth / 2)
        direction = 'top'
      } else {
        // Par défaut en bas
        top = rect.bottom + 10
        left = rect.left + (rect.width / 2) - (tooltipWidth / 2)
        direction = 'bottom'
      }
    }
    
    // Ajuster la position pour rester dans la fenêtre
    const margin = 20
    const finalLeft = Math.max(margin, Math.min(left, windowWidth - tooltipWidth - margin))
    const finalTop = Math.max(scrollTop + margin, Math.min(top, windowHeight + scrollTop - tooltipHeight - margin))
    
    tooltipPosition.value = { top: finalTop, left: finalLeft }
  } else {
    // Position de fallback si pas d'event
    tooltipPosition.value = { top: 100, left: 100 }
  }
  
  currentPreviewDocument.value = document
  previewType.value = type
  pdfLoadError.value = false // Réinitialiser l'erreur PDF
  
  // Utiliser les données du document Firestore au lieu de l'endpoint
  let pdfUrl = null
  
  if (type === 'current' && document.current_document_url) {
    pdfUrl = document.current_document_url;
    console.log('📄 Aperçu du document actuel (état du workflow)')
  } else if (type === 'generated' && document.final_document_url) {
    pdfUrl = document.final_document_url;
    console.log('📄 Aperçu du PDF généré (avec éléments)')
  } else {
    // Fallback
    pdfUrl = document.original_document_url || document.current_document_url || document.final_document_url;
  }
  
  // Rétrocompatibilité Base64
  if (!pdfUrl) {
    const base64Data = document.current_document_data || document.final_document_data || document.original_document_data || document.original_document_base64 || document.signed_document_base64;
    if (base64Data) {
      pdfUrl = base64Data.startsWith('data:') ? base64Data : `data:application/pdf;base64,${base64Data}`;
    }
  }
  
  previewPdfSource.value = pdfUrl
  showPreviewTooltip.value = true
  
  console.log('🔄 Affichage du PDF via URL Cloudinary')
}

const closePreviewTooltip = () => {
  console.log('🔄 closePreviewTooltip appelé')
  closeTooltipTimeout.value = setTimeout(() => {
    console.log('⏰ Fermeture du tooltip après délai')
    showPreviewTooltip.value = false
    currentPreviewDocument.value = null
    previewType.value = ''
    previewPdfSource.value = null
  }, 300) // Délai plus long pour éviter les fermetures accidentelles
}

const cancelCloseTooltip = () => {
  console.log('🔄 cancelCloseTooltip appelé')
  if (closeTooltipTimeout.value) {
    clearTimeout(closeTooltipTimeout.value)
    closeTooltipTimeout.value = null
  }
}

// Fonctions de gestion du PDF
const onPreviewPdfLoaded = () => {
  pdfLoadError.value = false
  console.log('PDF chargé avec succès')
}

const onPreviewPdfLoadError = () => {
  pdfLoadError.value = true
  console.log('Erreur lors du chargement du PDF (X-Frame-Options probable)')
}

const retryPdfLoad = () => {
  if (currentPreviewDocument.value && previewType.value) {
    showDocumentPreview(currentPreviewDocument.value, previewType.value, null)
  }
}

const openDocumentDirectly = () => {
  if (previewPdfSource.value) {
    window.open(previewPdfSource.value, '_blank')
  }
}

// Fonction pour télécharger le document depuis le tooltip
const downloadCurrentPreviewDocument = () => {
  if (currentPreviewDocument.value) {
    downloadDocument(currentPreviewDocument.value)
  }
}

// Fonction pour télécharger le document
const downloadDocument = (document) => {
  if (typeof window === 'undefined') return
  
  try {
    const filename = document.original_filename || document.document_title || 'document.pdf'
    
    // Essayer les URLs Cloudinary d'abord
    let downloadUrl = document.current_document_url || document.final_document_url || document.original_document_url;
    
    // Fallback sur le Base64
    if (!downloadUrl) {
      const base64Data = document.current_document_data || document.final_document_data || document.original_document_data || document.original_document_base64 || document.signed_document_base64;
      if (base64Data) {
        downloadUrl = base64Data.startsWith('data:') ? base64Data : `data:application/pdf;base64,${base64Data}`;
      }
    }
    
    if (!downloadUrl) {
      showNotification('error', 'Erreur', 'Données du document introuvables');
      return;
    }
    
    const link = window.document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    
    window.document.body.appendChild(link)
    link.click()
    window.document.body.removeChild(link)
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error)
  }
}

// Fonction pour signer un document
const signDocument = async (document) => {
  console.log('🖊️ === DÉBUT DE LA SIGNATURE DU DOCUMENT ===')
  console.log('🖊️ Document:', document.document_title || document.original_filename)
  console.log('🖊️ Document ID:', document.id)
  
  try {
    // ÉTAPE 1: Initialiser le service
    documentSigningService.initialize()
    
    // ÉTAPE 2: Récupérer l'ID de l'organisation
    const organizationId = userOrganization.value?.organization?.id || userOrganization.value?.id
    
    if (!organizationId) {
      showNotification('error', 'Erreur', 'Organisation non trouvée')
      return
    }
    
    // ÉTAPE 3: Vérifier que l'organisation a un certificat valide dans la BDD
    console.log('🔐 Vérification du certificat de l\'organisation...')
    const hasCert = await documentSigningService.hasOrganizationCertificate(organizationId)
    
    if (!hasCert) {
      showNotification('error', 'Certificat requis', 
        'Cette organisation n\'a pas de certificat de signature actif. Veuillez d\'abord importer un certificat dans les paramètres de l\'organisation.')
      return
    }
    
    console.log('✅ Certificat de l\'organisation trouvé')
    
    // ÉTAPE 4: Récupérer les détails complets du document pour vérifier les permissions
    console.log('📄 Récupération des détails du document pour vérification des permissions...')
    const documentDetails = await documentSigningService.fetchDocumentPreparation(document.id)
    
    // ÉTAPE 5: Vérifier que l'utilisateur peut signer ce document
    const canSign = documentSigningService.canUserSignDocument(documentDetails, authStore.user.id)
    
    if (!canSign) {
      console.log('❌ Vérification des permissions échouée')
      console.log('❌ Document current_signer:', documentDetails.current_signer)
      console.log('❌ Utilisateur actuel:', authStore.user.id)
      showNotification('error', 'Non autorisé', 
        'Vous n\'êtes pas autorisé à signer ce document ou le document n\'est pas dans un état signable.')
      return
    }
    
    console.log('✅ Permissions vérifiées - utilisateur autorisé à signer')
    
    // ÉTAPE 6: Demander confirmation
    const confirmMessage = `Êtes-vous sûr de vouloir signer le document "${document.document_title || document.original_filename}" ?
    
Cette action est irréversible et le document sera signé avec le certificat de l'organisation.`
    
    if (!confirm(confirmMessage)) {
      console.log('❌ Signature annulée par l\'utilisateur')
      return
    }
    
    console.log('✅ Signature confirmée, début du processus...')
    
    // ÉTAPE 7: Afficher un indicateur de chargement
    const loadingNotification = showLoadingNotification('Signature en cours', 
      'Récupération des données et signature du document...')
    
    try {
      // ÉTAPE 8: Préparer les informations de l'utilisateur
      const userInfo = {
        id: authStore.user.id,
        full_name: authStore.user.full_name,
        email: authStore.user.email,
        role: userRole.value
      }
      
      console.log('👤 Utilisateur:', userInfo)
      
      // ÉTAPE 9: SIGNER LE DOCUMENT avec le DocumentSigningService
      console.log('✍️ Appel du service de signature...')
      const signatureResult = await documentSigningService.signDocument(
        document.id,
        organizationId,
        userInfo
      )
      
      console.log('✅ === SIGNATURE RÉUSSIE ===')
      console.log('✅ Résultat:', signatureResult)
      
      // Fermer la notification de chargement
      closeLoadingNotification(loadingNotification)
      
      // ÉTAPE 8: Afficher un message de succès
      showNotification('success', 'Document signé avec succès !', 
        `Le document "${document.document_title || document.original_filename}" a été signé.
        
Document ID: ${signatureResult.signatureResult.documentId}
Hash: ${signatureResult.signatureResult.originalHash.substring(0, 20)}...
Temps: ${signatureResult.signatureResult.executionTime.toFixed(2)}s`)
      
      // ÉTAPE 9: Rafraîchir la liste des documents
      console.log('🔄 Rafraîchissement de la liste des documents...')
      await fetchPreparedDocuments()
      
      // ÉTAPE 10: Afficher les détails du workflow et de l'enregistrement
      if (signatureResult.saveResult.is_complete) {
        console.log('🎉 Workflow terminé - Document complètement signé!')
        showNotification('success', 'Workflow terminé', 
          'Ce document a été signé par tous les signataires requis et est maintenant finalisé.')
      } else if (signatureResult.saveResult.next_signer) {
        console.log('⏭️ Prochain signataire:', signatureResult.saveResult.next_signer)
        showNotification('info', 'Prochaine étape', 
          `Le document va maintenant être envoyé à ${signatureResult.saveResult.next_signer.name} (${signatureResult.saveResult.next_signer.role})`)
      }
      
      // Afficher les détails de l'enregistrement
      console.log('💾 Signature enregistrée avec ID:', signatureResult.saveResult.signature_id)
      console.log('💾 Workflow avancé:', signatureResult.saveResult.workflow_advanced)
      
    } catch (signError) {
      // Fermer la notification de chargement en cas d'erreur
      closeLoadingNotification(loadingNotification)
      throw signError
    }
    
  } catch (error) {
    console.error('❌ === ERREUR LORS DE LA SIGNATURE ===')
    console.error('❌ Message:', error.message)
    console.error('❌ Stack:', error.stack)
    
    // Afficher l'erreur à l'utilisateur
    showNotification('error', 'Erreur de signature', 
      `Impossible de signer le document: ${error.message}`)
  }
}

// Fonction pour vérifier si l'organisation a des certificats
const checkOrganizationCertificates = async () => {
  try {
    isLoadingCertificates.value = true
    
    const organizationId = userOrganization.value?.organization?.id || userOrganization.value?.id
    
    if (!organizationId) {
      throw new Error('Organisation non trouvée')
    }
    
    const certificates = await OrganizationApiService.getOrganizationCertificates(organizationId)
    
    // Vérifier s'il y a des certificats actifs (on ignore temporairement is_valid pour les tests avec certificats expirés)
    const activeCertificates = certificates?.filter(cert => cert.is_active) || []
    
    console.log('🔐 Certificats trouvés:', activeCertificates.length)
    
    // Mettre à jour l'état réactif
    hasCertificates.value = activeCertificates.length > 0
    
    return activeCertificates.length > 0
    
  } catch (error) {
    console.error('❌ Erreur lors de la vérification des certificats:', error)
    hasCertificates.value = false
    return false
  } finally {
    isLoadingCertificates.value = false
  }
}

// Fonction pour afficher des notifications
const showNotification = (type, title, message) => {
  // Créer une notification toast
  const notification = document.createElement('div')
  const alertType = type === 'error' ? 'danger' : (type === 'info' ? 'info' : 'success')
  notification.className = `alert alert-${alertType} alert-dismissible fade show position-fixed`
  notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 500px;'
  
  notification.innerHTML = `
    <strong>${title}</strong><br>
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `
  
  document.body.appendChild(notification)
  
  // Auto-supprimer après 5 secondes
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification)
    }
  }, 5000)
}

// Fonction pour afficher une notification de chargement
const showLoadingNotification = (title, message) => {
  const notification = document.createElement('div')
  notification.className = 'alert alert-primary alert-dismissible fade show position-fixed'
  notification.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px; max-width: 500px;'
  notification.id = `loading-notification-${Date.now()}`
  
  notification.innerHTML = `
    <div class="d-flex align-items-center">
      <div class="spinner-border spinner-border-sm me-2" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      <div>
        <strong>${title}</strong><br>
        <small>${message}</small>
      </div>
    </div>
  `
  
  document.body.appendChild(notification)
  
  return notification
}

// Fonction pour fermer une notification de chargement
const closeLoadingNotification = (notification) => {
  if (notification && notification.parentNode) {
    notification.remove()
  }
}

// Formater la date pour l'affichage
const formatDate = (dateString) => {
  if (!dateString) return 'Date inconnue'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Formater la taille des fichiers
const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

// Actions du tableau de bord
const refreshPerformance = () => {
  console.log('Actualisation des performances')
  // Logique pour actualiser les performances
}

const viewAllDocuments = () => {
  console.log('Voir tous les documents')
  // Logique pour voir tous les documents
}

const viewActivityLog = () => {
  console.log('Voir le journal d\'activité')
  // Logique pour voir le journal d'activité
}


// Charger les statistiques du manager
const loadManagerStats = async () => {
  try {
    // Ici on peut faire un appel API pour récupérer les vraies statistiques
    // Pour l'instant, on utilise des données simulées
    managerStats.value = {
      totalDocuments: 45,
      totalMembers: teamMembers.value.length,
      productivityScore: 87,
      pendingTasks: 12,
      overallPerformance: 92,
      documentsInProgress: 8,
      activeTeamMembers: teamMembers.value.filter(m => m.status === 'active').length
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des statistiques:', error)
  }
}

// Initialisation
// Charger les données de l'organisation (temps réel)
let unsubOrg = null
const loadOrganizationData = () => {
  if (unsubOrg) unsubOrg()
  unsubOrg = OrganizationApiService.listenUserOrganization((org) => {
    if (org) {
      userOrganization.value = {
        organization: org,
        role: org.role || 'chef'
      }
      userRole.value = org.role || 'chef'
      selectedOrganization.value = org
      console.log('✅ Organisation chargée en temps réel:', org.name)
    } else {
      userOrganization.value = null
    }
  }, (error) => {
    console.error('❌ Erreur lors du chargement de l\'organisation:', error)
  })
}

// Event listeners pour fermer le tooltip
const handleDocumentClick = (event) => {
  // Fermer le tooltip si on clique en dehors
  if (showPreviewTooltip.value && !event.target.closest('.document-preview-tooltip') && !event.target.closest('.document-actions button')) {
    closePreviewTooltip()
  }
}

const handleKeyDown = (event) => {
  if (event.key === 'Escape' && showPreviewTooltip.value) {
    closePreviewTooltip()
  }
}

onMounted(() => {
  loadOrganizationData()
  
  // Attendre que l'organisation soit chargée pour charger les documents
  const waitAndLoad = setInterval(async () => {
    if (userOrganization.value?.organization?.id) {
      clearInterval(waitAndLoad)
      console.log('📊 userOrganization après chargement:', userOrganization.value)
      await loadManagerStats()
      await fetchPreparedDocuments()
      await checkOrganizationCertificates()
    }
  }, 300)
  
  // Sécurité : arrêter après 10 secondes
  setTimeout(() => clearInterval(waitAndLoad), 10000)
  
  // Ajouter les event listeners
  document.addEventListener('click', handleDocumentClick)
  document.addEventListener('keydown', handleKeyDown)
})

// Nettoyage
onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleKeyDown)
  if (unsubOrg) unsubOrg()
})

// Émettre les événements
const emit = defineEmits(['open-organization-settings'])
</script>

<style scoped>
/* Variables CSS intégrées */
:root {
  --primary-blue: #0066cc;
  --primary-blue-dark: #0056b3;
  --text-dark: #2c3e50;
  --dark-gray: #6c757d;
  --light-gray: #f8f9fa;
  --success: #28a745;
  --warning: #ffc107;
  --danger: #dc3545;
  --info: #17a2b8;
}

/* STYLES GÉNÉRAUX */
.organization-manager-page {
  min-height: 100vh;
  background: transparent;
  padding: 2rem 0;
  position: relative;
}

/* BOUTON DE FERMETURE */
.close-organization-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #666;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.close-organization-btn:hover {
  background: rgba(255, 255, 255, 1);
  color: #333;
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.close-organization-btn:active {
  transform: scale(0.95);
}

/* Responsive pour mobile */
@media (max-width: 768px) {
  .close-organization-btn {
    position: fixed;
    top: 70px;
    right: 20px;
    width: 40px;
    height: 40px;
    font-size: 18px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    color: #666;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .close-organization-btn:hover {
    background: rgba(255, 255, 255, 1);
    color: #333;
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  }
}

/* CODES COULEURS POUR LES RÔLES */
.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-badge.admin {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.role-badge.secretaire {
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
  border: 1px solid rgba(0, 123, 255, 0.2);
}

.role-badge.chef,
.role-badge.manager,
.role-badge[class*="chef+"] {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.role-badge.member {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

/* HEADER */
.organization-header {
  margin-bottom: 3rem;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  gap: 3rem;
}

.header-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-title {
  font-family: 'Raleway', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.sections-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.5;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-image {
  flex-shrink: 0;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
  position: relative;
  width: 320px;
  height: 240px;
}

.organization-illustration {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.organization-illustration:hover {
  transform: translateY(-4px);
  filter: drop-shadow(0 8px 20px rgba(0, 102, 204, 0.15));
}

/* Bulles décoratives */
.bubble {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 60px;
  height: 60px;
  top: -5%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 40px;
  height: 40px;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.4s forwards, float 6s ease-in-out infinite 1.4s;
}

.bubble-3 {
  width: 80px;
  height: 80px;
  bottom: 5%;
  right: 20%;
  animation: fadeInScale 1s ease-out 1.6s forwards, float 6s ease-in-out infinite 1.6s;
}

.bubble-4 {
  width: 50px;
  height: 50px;
  top: 40%;
  left: 10%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

/* BOUTONS PRINCIPAUX */
.analytics-btn {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  font-size: 1rem;
}

.analytics-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0056b3 100%);
}

.team-btn, .settings-btn {
  border: 2px solid var(--primary-blue);
  color: var(--primary-blue);
  background: transparent;
  transition: all 0.3s ease;
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  font-size: 1rem;
}

.team-btn:hover, .settings-btn:hover {
  background: var(--primary-blue);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

/* STATISTIQUES */
.docs-stats-section {
  margin-top: 6rem;
  margin-bottom: 4rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.08);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.stat-card:nth-child(1) { animation-delay: 0.9s; }
.stat-card:nth-child(2) { animation-delay: 1s; }
.stat-card:nth-child(3) { animation-delay: 1.1s; }
.stat-card:nth-child(4) { animation-delay: 1.2s; }

.stat-icon {
  width: 50px;
  height: 50px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: var(--primary-blue);
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--dark-gray);
  margin: 0;
}

/* SECTIONS DES DOCUMENTS */
.documents-sections {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.sections-header {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
  max-width: 800px;
  margin: 0 auto;
}

.sections-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.5s forwards;
}

.sections-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--dark-gray);
  margin-bottom: 2rem;
  line-height: 1.5;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.6s forwards;
}

/* BADGE DE RÔLE */
.role-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(0, 102, 204, 0.08);
  color: var(--primary-blue);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
  border: 1px solid rgba(0, 102, 204, 0.15);
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.4s forwards;
  transition: all 0.3s ease;
}

.role-badge:hover {
  background: rgba(0, 102, 204, 0.12);
  border-color: rgba(0, 102, 204, 0.25);
}

.role-badge i {
  font-size: 0.9rem;
  opacity: 0.8;
}

.role-text {
  font-weight: 600;
  margin-right: 0.4rem;
}

.organization-context {
  font-weight: 400;
  opacity: 0.7;
  font-size: 0.85rem;
}

.documents-section-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  height: 100%;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.05);
}

.documents-section-card:nth-child(1) { animation-delay: 1.3s; }
.documents-section-card:nth-child(2) { animation-delay: 1.4s; }

.documents-section-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 8px 16px rgba(0, 102, 204, 0.08);
}

.section-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.section-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.section-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
  font-family: 'Raleway', sans-serif;
}

.section-card-subtitle {
  color: var(--dark-gray);
  margin: 0;
  font-size: 0.9rem;
}

/* VUE D'ENSEMBLE */
.overview-list {
  margin-bottom: 1.5rem;
}

.overview-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  background: rgba(248, 249, 250, 0.5);
}

.overview-item:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.overview-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.overview-info {
  flex: 1;
}

.overview-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.overview-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-size: 0.85rem;
  color: var(--dark-gray);
}

.overview-value {
  font-weight: 700;
  color: var(--primary-blue);
  font-size: 1.1rem;
}

.overview-trend {
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.overview-trend.positive {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.overview-trend.neutral {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
}

/* ACTIONS RAPIDES */
.documents-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item-doc {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.action-item-doc:nth-child(1) { animation-delay: 1.5s; }
.action-item-doc:nth-child(2) { animation-delay: 1.6s; }
.action-item-doc:nth-child(3) { animation-delay: 1.7s; }
.action-item-doc:nth-child(4) { animation-delay: 1.8s; }

.action-card-doc {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(248, 249, 250, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-card-doc:hover {
  background: rgba(0, 102, 204, 0.03);
  border-color: rgba(0, 102, 204, 0.15);
  transform: translateX(5px);
}

.action-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.1rem;
  color: var(--primary-blue);
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.action-description {
  font-size: 0.85rem;
  color: var(--dark-gray);
  margin: 0;
}

.action-arrow {
  color: var(--primary-blue);
  opacity: 0.6;
  transition: all 0.3s ease;
}

.action-card-doc:hover .action-arrow {
  opacity: 1;
  transform: translateX(3px);
}

/* BOUTONS */
.btn-primary-blue {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  color: white;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary-blue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* TABLEAU DE BORD */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.05);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.card-content {
  padding: 0.5rem 0;
}

/* PERFORMANCE CHART */
.performance-chart {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px;
}

.chart-placeholder {
  text-align: center;
  color: var(--dark-gray);
}

/* TEAM MEMBERS */
.team-members {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.team-member {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.team-member:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.member-avatar {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 1.5rem;
  color: var(--primary-blue);
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.member-role {
  font-size: 0.8rem;
  color: var(--dark-gray);
  margin: 0;
}

.member-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 0.6rem;
}

.member-status.active {
  color: var(--success);
}

.member-status.inactive {
  color: var(--dark-gray);
}

/* RECENT DOCUMENTS */
.recent-documents {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.document-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.document-item:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.document-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 1rem;
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
}

.document-meta {
  font-size: 0.8rem;
  color: var(--dark-gray);
  margin: 0;
}

.document-status {
  display: flex;
  align-items: center;
}

.status-badge {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  text-transform: uppercase;
}

.status-badge.signed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.status-badge.draft {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
}

/* ACTIVITY FEED */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(248, 249, 250, 0.5);
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(0, 102, 204, 0.03);
  transform: translateX(3px);
}

.activity-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  font-size: 0.9rem;
  border-radius: 50%;
}

.activity-icon.success {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.activity-icon.info {
  background: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
}

.activity-icon.warning {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.activity-icon.primary {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 0.85rem;
  color: var(--text-dark);
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.activity-time {
  font-size: 0.75rem;
  color: var(--dark-gray);
}

/* MODALE D'ANALYSES */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(1px);
  animation: fadeInOverlay 0.3s ease-out;
}

.analytics-modal {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  z-index: 10000;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--dark-gray);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  transform: scale(1.1);
}

/* ONGLETS D'ANALYSES */
.analytics-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px 8px 0 0;
  font-weight: 600;
  color: var(--dark-gray);
  transition: all 0.3s ease;
  cursor: pointer;
}

.tab-btn:hover {
  background: rgba(0, 102, 204, 0.05);
  color: var(--primary-blue);
}

.tab-btn.active {
  background: var(--primary-blue);
  color: white;
}

.analytics-content {
  min-height: 300px;
}

.analytics-panel {
  padding: 1rem 0;
}

.analytics-panel h6 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

/* ANIMATIONS */
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
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modalSlideUp {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.8) rotateX(-10deg);
  }
  50% {
    opacity: 0.8;
    transform: translateY(-5px) scale(1.05) rotateX(2deg);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1) rotateX(0deg);
  }
}

/* ===== STYLES POUR LE SYSTÈME D'ONGLETS ===== */
/* ONGLETS */
.tabs-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(0, 102, 204, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(0, 102, 204, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

.tabs-header {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
}

.tab-button {
  flex: 1;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.tab-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--primary-blue);
}

.tab-button.active {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border-bottom: 2px solid var(--primary-blue);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-blue);
}

.tab-content {
  padding: 2rem;
  min-height: 400px;
}

.tab-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.tab-placeholder i {
  opacity: 0.8;
  transition: all 0.3s ease;
}

.tab-placeholder:hover i {
  opacity: 1;
  transform: scale(1.1);
}

.tab-placeholder h4 {
  font-weight: 700;
  margin-bottom: 1rem;
}

.tab-placeholder p {
  color: var(--dark-gray);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.tab-placeholder .btn {
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.tab-placeholder .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

/* ===== STYLES POUR LES CARTES DE DOCUMENTS ===== */
/* GRILLE DE DOCUMENTS */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.document-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.08);
  position: relative;
  overflow: hidden;
}

.document-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 10px 25px rgba(0, 102, 204, 0.08),
    0 5px 15px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
}

/* HEADER DE LA CARTE DE DOCUMENT */
.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  position: relative;
}

.document-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--dark-gray);
  margin: 0;
  line-height: 1.3;
  max-width: calc(100% - 120px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-icon {
  width: 40px;
  height: 40px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.organization-badge {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
}

/* CONTENU DE LA CARTE */
.card-content {
  margin-bottom: 1rem;
}

.document-description {
  color: var(--dark-gray);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* HIÉRARCHIE DE SIGNATURE */
.signature-hierarchy {
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.hierarchy-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary-blue);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
}

.signature-steps {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.signature-step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.signature-step.completed {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.signature-step.current {
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.signature-step.pending {
  background: rgba(108, 117, 125, 0.1);
  border: 1px solid rgba(108, 117, 125, 0.2);
}

.step-indicator {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-indicator i {
  font-size: 1rem;
}

.signature-step.completed .step-indicator i {
  color: #28a745;
}

.signature-step.current .step-indicator i {
  color: #ffc107;
}

.signature-step.pending .step-indicator i {
  color: #6c757d;
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.step-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--dark-gray);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.step-person {
  font-size: 0.9rem;
  color: var(--text-dark);
  font-weight: 500;
}

/* FOOTER DE LA CARTE */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.document-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--dark-gray);
}

.meta-item i {
  color: var(--primary-blue);
  font-size: 0.9rem;
}

.document-step {
  font-size: 0.8rem;
  color: var(--primary-blue);
  font-weight: 600;
  background: rgba(0, 102, 204, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  align-self: flex-start;
}

.document-actions {
  display: flex;
  gap: 0.5rem;
}

.document-actions .btn {
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  border: 1px solid;
}

.document-actions .btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
}

.sign-btn {
  background: var(--primary-blue);
  color: white;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 0.5rem 0.75rem;
}

.sign-btn:hover:not(:disabled) {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.sign-btn:disabled {
  background: #ccc;
  color: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
}

/* BARRE DE RECHERCHE */
.search-container {
  flex: 1;
  max-width: 400px;
}

/* Style pour le bouton "Tout signer" */
.sign-all-btn {
  background: var(--primary-blue);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 140px;
}

.sign-all-btn:hover:not(:disabled) {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.sign-all-btn:disabled {
  background: #ccc;
  color: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
}

/* Conteneurs pour les info-bulles */
.sign-all-btn-container,
.sign-btn-container {
  position: relative;
  display: inline-block;
}

/* Info-bulles */
.info-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  pointer-events: none;
}

.has-tooltip:hover .info-tooltip {
  opacity: 1;
  visibility: visible;
}

.info-tooltip .tooltip-content {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 50%, 
    rgba(0, 0, 0, 0.1) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  padding: 12px 16px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  min-width: 200px;
  max-width: 300px;
  font-size: 0.875rem;
  line-height: 1.4;
  color: var(--text-dark);
}

/* Effet de verre incurvé */
.info-tooltip .tooltip-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.2) 0%, 
    rgba(255, 255, 255, 0.1) 50%, 
    transparent 100%);
  border-radius: 20px 20px 0 0;
  pointer-events: none;
}

.info-tooltip .tooltip-content::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30%;
  background: linear-gradient(180deg, 
    transparent 0%, 
    rgba(0, 0, 0, 0.05) 100%);
  border-radius: 0 0 20px 20px;
  pointer-events: none;
}

.info-tooltip .tooltip-content i {
  color: var(--primary-blue);
  font-size: 1rem;
  margin-top: 2px;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.info-tooltip .tooltip-text {
  flex: 1;
  position: relative;
  z-index: 1;
}

.info-tooltip .tooltip-text strong {
  color: var(--text-dark);
  font-weight: 600;
}

.info-tooltip .tooltip-arrow {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid rgba(0, 0, 0, 0.15);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

/* Animation d'apparition */
.info-tooltip {
  animation: tooltipFadeIn 0.3s ease-out;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) scale(1);
  }
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  color: var(--dark-gray);
  font-size: 1rem;
  z-index: 1;
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: var(--dark-gray);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }
  
  .header-image {
    width: 280px;
    height: 210px;
  }
  
  .header-title {
    font-size: 2rem;
  }
  
  .sections-title {
    font-size: 2.5rem;
  }
  
  .role-badge {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .role-badge i {
    font-size: 0.8rem;
  }
  
  .organization-context {
    font-size: 0.75rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .analytics-btn, .team-btn, .settings-btn {
    width: 100%;
  }
  
  .documents-sections {
    padding: 0 1rem;
  }
  
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .tab-content {
    padding: 1.5rem 1rem;
    min-height: 300px;
  }
  
  .tab-placeholder {
    padding: 2rem 1rem;
  }
  
  .tab-placeholder h4 {
    font-size: 1.25rem;
  }
  
  .tab-placeholder p {
    font-size: 0.9rem;
  }
  
  .documents-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .document-card {
    padding: 1rem;
  }
  
  .card-header {
    flex-direction: row;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .document-name {
    font-size: 1rem;
    max-width: calc(100% - 100px);
  }
  
  .document-header-content {
    gap: 0.25rem;
  }
  
  .organization-badge {
    position: absolute;
    top: 0;
    right: 0;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
  }
  
  .signature-hierarchy {
    padding: 0.75rem;
  }
  
  .hierarchy-title {
    font-size: 0.85rem;
  }
  
  .signature-step {
    padding: 0.4rem;
  }
  
  .step-indicator {
    width: 20px;
    height: 20px;
  }
  
  .step-title {
    font-size: 0.75rem;
  }
  
  .step-person {
    font-size: 0.8rem;
  }
  
  .document-meta {
    gap: 0.5rem;
  }
  
  .meta-item {
    font-size: 0.75rem;
  }
  
  .document-actions {
    gap: 0.25rem;
  }
  
  .document-actions .btn {
    padding: 0.4rem;
  }
  
  .sign-btn {
    background: var(--primary-blue);
    color: white;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
  }
  
  .sign-btn:hover {
    background: #0056b3;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
  }
  
  .search-container {
    max-width: 100%;
  }
  
  .sign-all-btn {
    padding: 0.6rem 1rem;
    font-size: 0.8rem;
    min-width: 120px;
  }
  
  .info-tooltip .tooltip-content {
    min-width: 180px;
    max-width: 250px;
    font-size: 0.8rem;
    padding: 10px 12px;
    border-radius: 16px;
  }
}

/* TOOLTIP DE PRÉVISUALISATION DES DOCUMENTS */
.document-preview-tooltip {
  position: absolute;
  z-index: 1000;
  animation: tooltipFadeIn 0.3s ease-out;
}

/* Transform selon la direction */
.document-preview-tooltip[class*="arrow-top"],
.document-preview-tooltip[class*="arrow-bottom"] {
  transform: translateX(-50%);
}

.document-preview-tooltip[class*="arrow-left"],
.document-preview-tooltip[class*="arrow-right"] {
  transform: translateY(-50%);
}

.tooltip-arrow {
  position: absolute;
  width: 0;
  height: 0;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Flèche vers le haut (bulle en bas) */
.arrow-top {
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid white;
}

/* Flèche vers le bas (bulle en haut) */
.arrow-bottom {
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid white;
}

/* Flèche vers la gauche (bulle à droite) */
.arrow-left {
  left: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid white;
}

/* Flèche vers la droite (bulle à gauche) */
.arrow-right {
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-left: 8px solid white;
}

.tooltip-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 102, 204, 0.1);
  max-width: 550px;
  max-height: 750px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.tooltip-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0;
  display: flex;
  align-items: center;
  flex: 1;
}

.tooltip-close {
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tooltip-close:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.tooltip-body {
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.preview-container {
  flex: 1;
  border-radius: 0;
  overflow: hidden;
  background: #f8f9fa;
  border: none;
  display: flex;
  flex-direction: column;
  max-height: 450px;
}

.pdf-preview-content {
  flex: 1;
  display: flex;
  align-items: stretch;
  justify-content: center;
  min-height: 400px;
  position: relative;
}

/* Styles exactement comme dans DocumentPreparationPage */
.pdf-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: stretch;
  background: white;
  border-radius: 0;
  box-shadow: none;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-height: 400px;
  max-height: 450px;
}

.pdf-fallback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: var(--text-muted);
}

.fallback-content {
  text-align: center;
  padding: 2rem;
  max-width: 400px;
  margin: 0 auto;
}

.fallback-content i {
  font-size: 3rem;
  color: var(--primary-blue);
  margin-bottom: 1rem;
}

.fallback-content h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.fallback-description {
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fallback-subtitle {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  font-size: 0.85rem;
  line-height: 1.4;
}

.fallback-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--primary-blue);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.download-btn:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-1px);
}

.pdf-loading-state,
.pdf-error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  height: 100%;
}

.pdf-loading-state i,
.pdf-error-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.pdf-loading-state p,
.pdf-error-state p {
  font-size: 1rem;
  color: var(--dark-gray);
  margin-bottom: 1rem;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-5px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Animation d'entrée contextuelle selon la direction */
.document-preview-tooltip[class*="arrow-left"] {
  animation: tooltipSlideInRight 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-right"] {
  animation: tooltipSlideInLeft 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-top"] {
  animation: tooltipSlideInUp 0.3s ease-out;
}

.document-preview-tooltip[class*="arrow-bottom"] {
  animation: tooltipSlideInDown 0.3s ease-out;
}

@keyframes tooltipSlideInRight {
  from {
    opacity: 0;
    transform: translateX(20px) translateY(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0) translateY(-50%);
  }
}

@keyframes tooltipSlideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px) translateY(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0) translateY(-50%);
  }
}

@keyframes tooltipSlideInUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

@keyframes tooltipSlideInDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Responsive pour les tooltips */
@media (max-width: 768px) {
  .document-preview-tooltip {
    max-width: 90vw;
    max-height: 80vh;
  }
  
  .pdf-iframe {
    min-height: 400px;
  }
  
  .search-input {
    padding: 0.6rem 0.8rem 0.6rem 2rem;
    font-size: 0.85rem;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .analytics-modal {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .analytics-tabs {
    flex-direction: column;
  }
  
  .tab-btn {
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }
}

/* ===== STYLES POUR LES DOCUMENTS SIGNÉS ===== */
.signed-documents-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.signed-docs-header {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.signed-docs-header h4 {
  color: var(--dark-gray);
  font-weight: 700;
  display: flex;
  align-items: center;
  margin: 0;
}

.list-header h4 {
  color: var(--dark-gray);
  font-weight: 700;
  display: flex;
  align-items: center;
}

.signed-document-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.signed-document-item:hover {
  border-color: var(--primary-blue);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.15);
  transform: translateY(-2px);
}

.signed-doc-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.signed-doc-header .doc-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-blue) 0%, #0056b3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.signed-doc-header .doc-icon i {
  font-size: 1.5rem;
  color: white;
}

.doc-info {
  flex: 1;
}

.doc-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--dark-gray);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.doc-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.meta-item i {
  color: var(--primary-blue);
}

.doc-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.status-signed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.3);
}

.signed-doc-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.85rem;
  color: var(--dark-gray);
  opacity: 0.8;
  font-weight: 600;
}

.detail-label i {
  color: var(--primary-blue);
}

.detail-value {
  font-size: 0.95rem;
  color: var(--dark-gray);
  font-weight: 600;
}

.hash-value {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: var(--primary-blue);
  cursor: pointer;
}

.hash-value:hover {
  opacity: 0.8;
}

.workflow-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.workflow-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--dark-gray);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.workflow-steps {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.workflow-step-mini {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.step-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--primary-blue);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.step-info-mini {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.step-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--dark-gray);
}

.step-role {
  font-size: 0.75rem;
  color: var(--dark-gray);
  opacity: 0.7;
  text-transform: capitalize;
}

.signed-doc-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  border: 1px solid;
}

.btn-download {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #0056b3 100%);
  color: white;
  border-color: var(--primary-blue);
}

.btn-download:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 102, 204, 0.3);
  color: white;
}

.btn-view-original {
  background: rgba(108, 117, 125, 0.1);
  color: var(--dark-gray);
  border-color: rgba(108, 117, 125, 0.3);
}

.btn-view-original:hover {
  background: rgba(108, 117, 125, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(108, 117, 125, 0.2);
  color: var(--dark-gray);
}

/* Responsive pour les documents signés */
@media (max-width: 768px) {
  .signed-docs-header {
    padding: 1rem;
  }
  
  .signed-docs-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .signed-docs-header .search-container {
    max-width: 100%;
  }
  
  .signed-doc-header {
    flex-direction: column;
  }
  
  .doc-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
  }
  
  .workflow-steps {
    flex-direction: column;
  }
  
  .signed-doc-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
