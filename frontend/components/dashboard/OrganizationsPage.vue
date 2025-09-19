<template>
  <div class="organizations-page">
    <!-- Header avec titre de la section -->
    <div class="organizations-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Espace de gestion de l'</span>
            <span class="text-primary-blue">organisation </span>
            <span class="text-primary-blue" v-if="userOrganization && userOrganization.organization"> {{ userOrganization.organization.name }}</span>
          </h1>
          <p class="section-subtitle" v-if="userOrganization && userOrganization.organization">Gérez votre organisation {{ userOrganization.organization.name }} et ses membres</p>
          <p class="section-subtitle" v-else>Créez et gérez vos organisations pour collaborer efficacement</p>
          <div class="header-actions" v-if="!userOrganization || !userOrganization.organization">
            <button class="btn btn-primary-custom create-org-btn" @click="toggleCreateModal" ref="createBtn">
              <i class="bi bi-building-add me-2"></i>
              Créer une organisation
            </button>
          </div>
            <div class="header-actions" v-else>
              <button class="btn btn-primary-custom settings-btn" @click="openSettings" ref="settingsBtn">
                <i class="bi bi-gear me-2"></i>
                Paramètres de l'organisation
              </button>
            </div>
        </div>
        <div class="header-image">
          <!-- Bulles décoratives -->
          <div class="bubble bubble-1"></div>
          <div class="bubble bubble-2"></div>
          <div class="bubble bubble-3"></div>
          <div class="bubble bubble-4"></div>
          
          <img src="/organisation.svg" alt="Organisations" class="organizations-illustration">
        </div>
      </div>
    </div>

    <!-- Section statistiques des organisations -->
    <div class="orgs-stats-section" v-if="userOrganization && userOrganization.organization">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ userOrganization.organization.member_count || 0 }}</h4>
              <p class="stat-label">Membres</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-shield-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ userOrganization.organization.admin_count || 0 }}</h4>
              <p class="stat-label">Administrateurs</p>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="bi bi-calendar-check"></i>
            </div>
            <div class="stat-content">
              <h4 class="stat-number">{{ formatDate(userOrganization.organization.created_at) }}</h4>
              <p class="stat-label">Créée le</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Message pour utilisateur sans organisation -->
    <div class="no-organization-message" v-else>
      <div class="no-org-content">
        <div class="no-org-icon">
          <i class="bi bi-building"></i>
        </div>
        <h3>Vous n'avez pas encore d'organisation</h3>
        <p>Créez votre première organisation pour commencer à collaborer avec votre équipe.</p>
        <button class="btn btn-primary-custom" @click="toggleCreateModal">
          <i class="bi bi-building-add me-2"></i>
          Créer ma première organisation
        </button>
      </div>
    </div>

    <!-- Sections des organisations en deux colonnes -->
    <div v-if="!showAllOrganizations" class="organizations-sections">
      <!-- En-tête de section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="sections-header text-center">
            <h2 class="display-4 fw-bold mb-3 text-dark sections-title">
              <span class="text-dark">Gestion</span> 
              <span class="text-primary-blue"> Organisationnelle</span>
            </h2>
            <p class="lead mb-0 text-dark sections-subtitle">
              Gérez vos organisations et collaborez avec votre équipe.
            </p>
          </div>
        </div>
      </div>

      <div class="row align-items-center">
        <!-- Colonne gauche - Mes Organisations Récentes -->
        <div class="col-lg-6 mb-4">
          <div class="organizations-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-building text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Organisations Récentes</h3>
                <p class="section-card-subtitle">Vos dernières organisations créées</p>
              </div>
            </div>
            
            <div class="organizations-list">
              <!-- Organisation 1 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-primary-blue"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">TechCorp Solutions</h5>
                  <p class="organization-details">
                    <span class="organization-date">15 Jan 2024</span>
                    <span class="organization-status active">Active</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(1)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>

              <!-- Organisation 2 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-warning"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">Startup Innovante</h5>
                  <p class="organization-details">
                    <span class="organization-date">12 Jan 2024</span>
                    <span class="organization-status pending">En attente</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(2)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>

              <!-- Organisation 3 -->
              <div class="organization-item">
                <div class="organization-icon">
                  <i class="bi bi-building text-success"></i>
                </div>
                <div class="organization-info">
                  <h5 class="organization-name">Digital Agency</h5>
                  <p class="organization-details">
                    <span class="organization-date">10 Jan 2024</span>
                    <span class="organization-status active">Active</span>
                  </p>
                </div>
                <div class="organization-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(3)" title="Voir">
                    <i class="bi bi-eye"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="section-footer">
              <button class="btn btn-primary-blue btn-sm" @click="toggleAllOrganizations">
                Voir toutes les organisations
                <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Colonne droite - Actions sur les Organisations -->
        <div class="col-lg-6 mb-4">
          <div class="organizations-section-card">
            <div class="section-card-header">
              <div class="section-icon">
                <i class="bi bi-plus-circle text-primary-blue"></i>
              </div>
              <div class="section-header-content">
                <h3 class="section-card-title">Actions Rapides</h3>
                <p class="section-card-subtitle">Créez et gérez vos organisations</p>
              </div>
            </div>
            
            <div class="organizations-actions">
              <!-- Action 1 - Nouvelle organisation -->
              <div class="action-item-org">
                <div class="action-card-org" @click="toggleCreateModal()">
                  <div class="action-icon-org">
                    <i class="bi bi-building-add text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Nouvelle Organisation</h5>
                    <p class="action-description">Créer une nouvelle organisation</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 2 - Rejoindre -->
              <div class="action-item-org">
                <div class="action-card-org" @click="toggleJoinModal()">
                  <div class="action-icon-org">
                    <i class="bi bi-person-plus text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Rejoindre</h5>
                    <p class="action-description">Rejoindre une organisation existante</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 3 - Invitations -->
              <div class="action-item-org">
                <div class="action-card-org">
                  <div class="action-icon-org">
                    <i class="bi bi-envelope text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Invitations</h5>
                    <p class="action-description">Gérer vos invitations</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>

              <!-- Action 4 - Paramètres -->
              <div class="action-item-org">
                <div class="action-card-org">
                  <div class="action-icon-org">
                    <i class="bi bi-gear text-primary-blue"></i>
                  </div>
                  <div class="action-content-org">
                    <h5 class="action-title">Paramètres</h5>
                    <p class="action-description">Configurer vos organisations</p>
                  </div>
                  <div class="action-arrow">
                    <i class="bi bi-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vue de toutes les organisations -->
    <div v-if="showAllOrganizations" class="all-organizations-view">
      <!-- Header de la vue complète -->
      <div class="all-organizations-header">
        <div class="row mb-4">
          <div class="col-12">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <h2 class="display-6 fw-bold mb-2 text-dark">
                  <span class="text-dark">Mes</span>
                  <span class="text-primary-blue"> Organisations</span>
                </h2>
                <p class="lead mb-0 text-muted">
                  Toutes vos organisations et invitations
                </p>
              </div>
              <button class="btn btn-outline-primary" @click="backToMainView">
                <i class="bi bi-arrow-left me-2"></i>
                Retour
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Liste complète des organisations -->
      <div class="all-organizations-list">
        <div class="row">
          <div class="col-12">
            <div class="organizations-table-container">
              <div class="organizations-table">
                <div class="table-header">
                  <div class="table-row">
                    <div class="table-cell">Organisation</div>
                    <div class="table-cell">Statut</div>
                    <div class="table-cell">Rôle</div>
                    <div class="table-cell">Date de création</div>
                    <div class="table-cell">Actions</div>
                  </div>
                </div>
                <div class="table-body">
                  <div v-for="org in organizations" :key="org.id" class="table-row">
                    <div class="table-cell">
                      <div class="organization-cell">
                        <div class="organization-icon">
                          <i class="bi bi-building"></i>
                        </div>
                        <div class="organization-details">
                          <h6 class="organization-name">{{ org.name }}</h6>
                          <p class="organization-description">{{ org.description }}</p>
                        </div>
                      </div>
                    </div>
                    <div class="table-cell">
                      <span :class="`status-badge ${org.status}`">
                        {{ getStatusText(org.status) }}
                      </span>
                    </div>
                    <div class="table-cell">
                      <span class="role-badge">{{ org.role }}</span>
                    </div>
                    <div class="table-cell">
                      <span class="date-text">{{ org.createdAt }}</span>
                    </div>
                    <div class="table-cell">
                      <div class="action-buttons">
                        <button class="btn btn-sm btn-outline-primary" @click="viewOrganization(org.id)" title="Voir">
                          <i class="bi bi-eye"></i>
                        </button>
                        <button v-if="org.status === 'active'" class="btn btn-sm btn-outline-success" @click="manageOrganization(org.id)" title="Gérer">
                          <i class="bi bi-gear"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modale de création d'organisation -->
    <div v-if="isCreateModalOpen" class="organization-modal-overlay" @click="closeCreateModal">
      <div class="organization-modal" @click.stop ref="createModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-building-add"></i>
            Créer une Organisation
          </h5>
          <button class="close-btn" @click="closeCreateModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-modal-content">
          <form @submit.prevent="createOrganization">
            <div class="form-group">
              <label for="orgName">Nom de l'organisation</label>
              <input 
                type="text" 
                id="orgName" 
                v-model="newOrganization.name" 
                class="form-control" 
                placeholder="Ex: TechCorp Solutions"
                required
              >
            </div>
            <div class="form-group">
              <label for="orgDescription">Description</label>
              <textarea 
                id="orgDescription" 
                v-model="newOrganization.description" 
                class="form-control" 
                rows="3"
                placeholder="Décrivez votre organisation..."
              ></textarea>
            </div>
            <div class="form-group">
              <label for="orgType">Type d'organisation</label>
              <select id="orgType" v-model="newOrganization.type" class="form-control">
                <option value="company">Entreprise</option>
                <option value="association">Association</option>
                <option value="ngo">ONG</option>
                <option value="government">Gouvernement</option>
                <option value="other">Autre</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-outline-secondary" @click="closeCreateModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isCreating">
                <span v-if="isCreating" class="spinner-border spinner-border-sm me-2"></span>
                Créer l'organisation
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Modale de rejoindre une organisation -->
    <div v-if="isJoinModalOpen" class="organization-modal-overlay" @click="closeJoinModal">
      <div class="organization-modal" @click.stop ref="joinModal">
        <div class="organization-modal-header">
          <h5>
            <i class="bi bi-person-plus"></i>
            Rejoindre une Organisation
          </h5>
          <button class="close-btn" @click="closeJoinModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="organization-modal-content">
          <form @submit.prevent="joinOrganization">
            <div class="form-group">
              <label for="inviteCode">Code d'invitation</label>
              <input 
                type="text" 
                id="inviteCode" 
                v-model="inviteCode" 
                class="form-control" 
                placeholder="Entrez le code d'invitation"
                required
              >
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-outline-secondary" @click="closeJoinModal">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isJoining">
                <span v-if="isJoining" class="spinner-border spinner-border-sm me-2"></span>
                Rejoindre
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modale de paramètres d'organisation -->
    <div v-if="isOrganizationSettingsModalOpen" class="organization-settings-modal-overlay" @click="closeOrganizationSettingsModal">
      <div class="organization-settings-modal" @click.stop ref="organizationSettingsModal">
        <!-- Menu latéral (desktop seulement) -->
        <div class="organization-settings-menu d-none d-lg-block" :data-active-tab="activeOrganizationTab">
          <div class="organization-settings-menu-header">
            <div class="organization-avatar">
              <i class="bi bi-building"></i>
            </div>
            <h6>{{ userOrganization?.organization?.name || 'Organisation' }}</h6>
          </div>
          <ul class="organization-settings-nav">
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'edit' }" @click="setActiveOrganizationTab('edit')">
              <i class="bi bi-pencil-square"></i>
              <span>Éditer</span>
            </li>
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'members' }" @click="setActiveOrganizationTab('members')">
              <i class="bi bi-people"></i>
              <span>Membres</span>
            </li>
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'permissions' }" @click="setActiveOrganizationTab('permissions')">
              <i class="bi bi-shield-check"></i>
              <span>Permissions</span>
            </li>
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'billing' }" @click="setActiveOrganizationTab('billing')">
              <i class="bi bi-credit-card"></i>
              <span>Facturation</span>
            </li>
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'delete' }" @click="setActiveOrganizationTab('delete')">
              <i class="bi bi-trash3"></i>
              <span>Supprimer</span>
            </li>
          </ul>
        </div>
        
        <!-- Contenu principal -->
        <div class="organization-settings-content">
          <div class="organization-settings-content-header">
            <h5>
              <i :class="getOrganizationTabIcon()"></i>
              {{ getOrganizationTabTitle() }}
            </h5>
            <button class="close-btn" @click="closeOrganizationSettingsModal">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
          
          <div class="organization-settings-content-body">
            <!-- Contenu Éditer -->
            <div v-if="activeOrganizationTab === 'edit'" class="tab-content">
              <div class="form-group">
                <label>Nom de l'organisation</label>
                <input type="text" class="form-control" v-model="editOrganizationForm.name">
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea class="form-control" v-model="editOrganizationForm.description" rows="3"></textarea>
              </div>
              <div class="form-group">
                <label>Email de contact</label>
                <input type="email" class="form-control" v-model="editOrganizationForm.email">
              </div>
              <div class="form-group">
                <label>Téléphone</label>
                <input type="tel" class="form-control" v-model="editOrganizationForm.phone">
              </div>
              <div class="form-group">
                <label>Adresse</label>
                <textarea class="form-control" v-model="editOrganizationForm.address" rows="2"></textarea>
              </div>
              <div class="form-group">
                <label>Site web</label>
                <input type="url" class="form-control" v-model="editOrganizationForm.website">
              </div>
              <div class="form-group">
                <label>Type d'organisation</label>
                <select class="form-control" v-model="editOrganizationForm.organization_type">
                  <option value="entreprise">Entreprise</option>
                  <option value="association">Association</option>
                  <option value="administration">Administration</option>
                  <option value="collectivite">Collectivité</option>
                  <option value="autre">Autre</option>
                </select>
              </div>
              <div class="form-group">
                <label>Secteur d'activité</label>
                <input type="text" class="form-control" v-model="editOrganizationForm.sector">
              </div>
              <div class="form-actions">
                <button class="btn btn-outline-secondary" @click="closeOrganizationSettingsModal">Annuler</button>
                <button class="btn btn-primary" @click="saveOrganizationChanges" :disabled="isSavingOrganization">
                  <span v-if="isSavingOrganization" class="spinner-border spinner-border-sm me-2"></span>
                  Sauvegarder
                </button>
              </div>
            </div>
            
            <!-- Contenu Membres -->
            <div v-if="activeOrganizationTab === 'members'" class="tab-content">
              <div class="members-header">
                <h6>Membres de l'organisation</h6>
                <button class="btn btn-primary btn-sm" @click="openInviteModal">
                  <i class="bi bi-person-plus me-1"></i>
                  Inviter un membre
                </button>
              </div>
              <div class="members-list">
                <div class="member-item">
                  <div class="member-info">
                    <div class="member-avatar">
                      <i class="bi bi-person-circle"></i>
                    </div>
                    <div class="member-details">
                      <h6>{{ userOrganization?.organization?.created_by_name || 'Administrateur' }}</h6>
                      <p class="text-muted">Administrateur</p>
                    </div>
                  </div>
                  <span class="badge bg-primary">Admin</span>
                </div>
              </div>
            </div>
            
            <!-- Contenu Permissions -->
            <div v-if="activeOrganizationTab === 'permissions'" class="tab-content">
              <div class="permission-item">
                <div class="permission-info">
                  <h6>Gestion des documents</h6>
                  <p class="text-muted">Autoriser les membres à créer et gérer des documents</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" checked>
                </div>
              </div>
              <div class="permission-item">
                <div class="permission-info">
                  <h6>Invitation de membres</h6>
                  <p class="text-muted">Autoriser les membres à inviter d'autres personnes</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox">
                </div>
              </div>
            </div>
            
            <!-- Contenu Facturation -->
            <div v-if="activeOrganizationTab === 'billing'" class="tab-content">
              <div class="billing-info">
                <h6>Plan actuel</h6>
                <p class="text-muted">Plan Gratuit - Jusqu'à 5 membres</p>
                <button class="btn btn-primary btn-sm">Mettre à niveau</button>
              </div>
            </div>
            
            <!-- Contenu Supprimer -->
            <div v-if="activeOrganizationTab === 'delete'" class="tab-content">
              <div v-if="!showDeleteConfirmation" class="delete-warning">
                <div class="warning-icon">
                  <i class="bi bi-exclamation-triangle"></i>
                </div>
                <h6>Supprimer l'organisation</h6>
                <p class="text-muted">Cette action est irréversible. Tous les documents et données de l'organisation seront supprimés.</p>
                <div class="form-group">
                  <label>Confirmer en tapant votre mot de passe</label>
                  <input type="password" class="form-control" v-model="deleteConfirmation" placeholder="Votre mot de passe">
                </div>
                <div class="delete-actions">
                  <button class="btn btn-outline-secondary" @click="cancelDelete">
                    Annuler
                  </button>
                  <button class="btn btn-danger" @click="confirmDelete" :disabled="!deleteConfirmation">
                    <i class="bi bi-trash3 me-1"></i>
                    Supprimer l'organisation
                  </button>
                </div>
              </div>
              
              <!-- Confirmation de suppression -->
              <div v-else class="delete-confirmation">
                <div class="confirmation-icon">
                  <i class="bi bi-shield-exclamation"></i>
                </div>
                <h6>Confirmation de suppression</h6>
                <p class="text-muted">Êtes-vous absolument sûr de vouloir supprimer l'organisation <strong>{{ userOrganization?.organization?.name }}</strong> ?</p>
                <p class="text-danger small">Cette action supprimera définitivement :</p>
                <ul class="text-danger small">
                  <li>Tous les documents de l'organisation</li>
                  <li>Toutes les signatures associées</li>
                  <li>Tous les membres de l'organisation</li>
                  <li>Toutes les données de l'organisation</li>
                </ul>
                <div class="confirmation-actions">
                  <button class="btn btn-outline-secondary" @click="cancelDelete">
                    <i class="bi bi-x me-1"></i>
                    Annuler
                  </button>
                  <button class="btn btn-danger" @click="executeDelete">
                    <i class="bi bi-trash3 me-1"></i>
                    Oui, supprimer définitivement
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Modale d'invitation de membre (enfant de la modale des paramètres) -->
        <div v-if="isInviteModalOpen" class="invite-modal-overlay" @click="closeInviteModal">
          <div class="invite-modal" @click.stop>
            <div class="invite-modal-header">
              <h6>
                <i class="bi bi-person-plus"></i>
                Inviter un membre
              </h6>
              <button class="close-btn" @click="closeInviteModal">
                <i class="bi bi-x"></i>
              </button>
            </div>
            
            <div class="invite-modal-body">
              <div class="invite-form">
                <div class="form-group">
                  <label class="form-label">Rôle du membre</label>
                  <select v-model="inviteForm.role" class="form-control">
                    <option value="">Sélectionner un rôle</option>
                    <option value="secretaire">Secrétaire</option>
                    <option value="chef">Chef</option>
                    <option value="chef+1">Chef+1</option>
                    <option value="chef+2">Chef+2</option>
                    <option value="chef+n">Chef+n</option>
                  </select>
                </div>
              </div>
              
              <!-- Affichage du code d'invitation généré -->
              <div v-if="generatedInviteCode" class="invite-code-section">
                <div class="invite-code-header">
                  <h6>Code d'invitation généré</h6>
                  <p class="text-muted">Partagez ce code avec le membre que vous souhaitez inviter</p>
                </div>
                
                <div class="invite-code-display">
                  <div class="code-container">
                    <code class="invite-code">{{ generatedInviteCode }}</code>
                    <button class="btn btn-outline-primary btn-sm" @click="copyInviteCode">
                      <i class="bi bi-clipboard me-1"></i>
                      Copier
                    </button>
                  </div>
                </div>
                
                <div class="invite-code-info">
                  <div class="info-item">
                    <i class="bi bi-building me-2"></i>
                    <span>Organisation : {{ userOrganization?.organization?.name }}</span>
                  </div>
                  <div class="info-item">
                    <i class="bi bi-person-badge me-2"></i>
                    <span>Rôle : {{ getRoleDisplayName(inviteForm.role) }}</span>
                  </div>
                  <div class="info-item">
                    <i class="bi bi-clock me-2"></i>
                    <span>Expire dans 7 jours</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="invite-modal-footer">
              <button @click="closeInviteModal" class="btn btn-outline-secondary btn-sm">
                Annuler
              </button>
              <button 
                @click="generateInviteCode" 
                :disabled="!inviteForm.role"
                class="btn btn-primary btn-sm"
              >
                <i class="bi bi-link-45deg me-1"></i>
                Générer le code d'invitation
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Notification Toast dans la modale -->
      <div v-if="notification.show" class="notification-toast" :class="`notification-${notification.type}`">
        <div class="notification-content">
          <div class="notification-icon">
            <i v-if="notification.type === 'success'" class="bi bi-check-circle-fill"></i>
            <i v-else-if="notification.type === 'error'" class="bi bi-exclamation-circle-fill"></i>
            <i v-else-if="notification.type === 'warning'" class="bi bi-exclamation-triangle-fill"></i>
          </div>
          <div class="notification-text">
            <h6 class="notification-title">{{ notification.title }}</h6>
            <p class="notification-message">{{ notification.message }}</p>
          </div>
          <button class="notification-close" @click="hideNotification">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, defineEmits } from 'vue'
import { useAuthStore } from '../../stores/auth'
import OrganizationApiService from '../../services/OrganizationApiService'

// Store d'authentification
const authStore = useAuthStore()

// Émissions
const emit = defineEmits(['navigate-to-organization', 'open-profile-modal'])

// État pour l'organisation de l'utilisateur
const userOrganization = ref(null)
const isLoadingOrganization = ref(false)

// État pour la modale de paramètres d'organisation
const isOrganizationSettingsModalOpen = ref(false)
const activeOrganizationTab = ref('edit')
const isSavingOrganization = ref(false)
const deleteConfirmation = ref('')

// État pour les notifications
const notification = ref({
  show: false,
  type: 'success', // 'success', 'error', 'warning'
  title: '',
  message: ''
})

// État pour la confirmation de suppression
const showDeleteConfirmation = ref(false)

// État pour la modale d'invitation
const isInviteModalOpen = ref(false)
const inviteForm = ref({
  role: ''
})
const generatedInviteCode = ref('')

// Refs pour le positionnement contextuel
const settingsBtn = ref(null)
const organizationSettingsModal = ref(null)

// Formulaire d'édition d'organisation
const editOrganizationForm = ref({
  name: '',
  description: '',
  email: '',
  phone: '',
  address: '',
  website: '',
  organization_type: 'entreprise',
  sector: ''
})

// État pour afficher la liste complète des organisations
const showAllOrganizations = ref(false)

// État pour les modales
const isCreateModalOpen = ref(false)
const isJoinModalOpen = ref(false)
const createBtn = ref(null)
const createModal = ref(null)
const joinModal = ref(null)

// État pour les formulaires
const isCreating = ref(false)
const isJoining = ref(false)

// Données des organisations (simulées)
const organizations = ref([
  {
    id: 1,
    name: 'TechCorp Solutions',
    description: 'Entreprise de solutions technologiques',
    type: 'company',
    status: 'active',
    role: 'Administrateur',
    createdAt: '15 Jan 2024'
  },
  {
    id: 2,
    name: 'Startup Innovante',
    description: 'Startup dans le domaine de l\'innovation',
    type: 'company',
    status: 'pending',
    role: 'Créateur',
    createdAt: '12 Jan 2024'
  },
  {
    id: 3,
    name: 'Digital Agency',
    description: 'Agence digitale spécialisée',
    type: 'company',
    status: 'active',
    role: 'Membre',
    createdAt: '10 Jan 2024'
  },
  {
    id: 4,
    name: 'Association Tech',
    description: 'Association des professionnels du tech',
    type: 'association',
    status: 'active',
    role: 'Modérateur',
    createdAt: '08 Jan 2024'
  },
  {
    id: 5,
    name: 'ONG Humanitaire',
    description: 'Organisation non gouvernementale',
    type: 'ngo',
    status: 'pending',
    role: 'Créateur',
    createdAt: '05 Jan 2024'
  }
])

// Nouvelle organisation
const newOrganization = ref({
  name: '',
  description: '',
  type: 'company'
})

// Code d'invitation
const inviteCode = ref('')

// Computed properties
const totalOrganizations = computed(() => organizations.value.length)
const activeOrganizations = computed(() => 
  organizations.value.filter(org => org.status === 'active').length
)
const pendingOrganizations = computed(() => 
  organizations.value.filter(org => org.status === 'pending').length
)

// Fonctions pour les modales
const toggleCreateModal = () => {
  isCreateModalOpen.value = !isCreateModalOpen.value
  if (isCreateModalOpen.value) {
    nextTick(() => {
      positionModal(createModal.value, createBtn.value)
    })
  }
}

const closeCreateModal = () => {
  isCreateModalOpen.value = false
  // Réinitialiser le formulaire
  newOrganization.value = {
    name: '',
    description: '',
    type: 'company'
  }
}

const toggleJoinModal = () => {
  isJoinModalOpen.value = !isJoinModalOpen.value
  if (isJoinModalOpen.value) {
    nextTick(() => {
      positionModal(joinModal.value, createBtn.value)
    })
  }
}

const closeJoinModal = () => {
  isJoinModalOpen.value = false
  inviteCode.value = ''
}

// Fonctions pour les organisations
const toggleAllOrganizations = () => {
  showAllOrganizations.value = true
}

const backToMainView = () => {
  showAllOrganizations.value = false
}

const viewOrganization = (orgId) => {
  console.log('Voir organisation:', orgId)
  // Émettre un événement pour naviguer vers l'organisation
  emit('navigate-to-organization', orgId)
}

const manageOrganization = (orgId) => {
  console.log('Gérer organisation:', orgId)
  // Émettre un événement pour gérer l'organisation
  emit('navigate-to-organization', orgId, 'manage')
}

const createOrganization = async () => {
  if (!newOrganization.value.name.trim()) {
    return
  }
  
  isCreating.value = true
  
  try {
    // Simuler la création d'organisation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newOrg = {
      id: organizations.value.length + 1,
      name: newOrganization.value.name,
      description: newOrganization.value.description,
      type: newOrganization.value.type,
      status: 'pending',
      role: 'Créateur',
      createdAt: new Date().toLocaleDateString('fr-FR', { 
        day: '2-digit', 
        month: 'short', 
        year: 'numeric' 
      })
    }
    
    organizations.value.unshift(newOrg)
    closeCreateModal()
    
    console.log('Organisation créée:', newOrg)
  } catch (error) {
    console.error('Erreur lors de la création:', error)
  } finally {
    isCreating.value = false
  }
}

const joinOrganization = async () => {
  if (!inviteCode.value.trim()) {
    return
  }
  
  isJoining.value = true
  
  try {
    // Simuler la jointure d'organisation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('Code d\'invitation:', inviteCode.value)
    closeJoinModal()
    
    // Ici on pourrait ajouter l'organisation à la liste
  } catch (error) {
    console.error('Erreur lors de la jointure:', error)
  } finally {
    isJoining.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'active': 'Active',
    'pending': 'En attente',
    'inactive': 'Inactive'
  }
  return statusMap[status] || status
}

// Fonction pour récupérer le token CSRF
const getCsrfToken = async () => {
  try {
    // D'abord, faire une requête GET pour obtenir le cookie CSRF
    await $fetch('http://127.0.0.1:8000/api/auth/csrf/', {
      method: 'GET',
      credentials: 'include'
    })
    
    // Ensuite, récupérer le token depuis les cookies
    const cookies = document.cookie.split(';')
    const csrfCookie = cookies.find(cookie => cookie.trim().startsWith('csrftoken='))
    
    if (csrfCookie) {
      const token = csrfCookie.split('=')[1]
      console.log('Token CSRF récupéré depuis les cookies:', token)
      return token
    }
    
    // Fallback: utiliser l'endpoint API
    const response = await $fetch('http://127.0.0.1:8000/api/auth/csrf/', {
      credentials: 'include'
    })
    return response.csrfToken
  } catch (error) {
    console.error('Erreur lors de la récupération du token CSRF:', error)
    return null
  }
}

// Fonction pour positionner les modales
const positionModal = (modal, button) => {
  if (!modal || !button) return
  
  const buttonRect = button.getBoundingClientRect()
  const modalWidth = 400
  const modalHeight = 500
  const margin = 20
  
  // Calculer l'espace disponible
  const spaceRight = window.innerWidth - buttonRect.right
  const spaceLeft = buttonRect.left
  const spaceBelow = window.innerHeight - buttonRect.bottom
  const spaceAbove = buttonRect.top
  
  let leftPosition, topPosition
  
  // Positionner horizontalement selon l'espace disponible
  if (spaceRight >= modalWidth + margin) {
    // Plus d'espace à droite
    leftPosition = buttonRect.right + 10
  } else if (spaceLeft >= modalWidth + margin) {
    // Plus d'espace à gauche
    leftPosition = buttonRect.left - modalWidth - 10
  } else {
    // Pas assez d'espace, centrer horizontalement
    leftPosition = (window.innerWidth - modalWidth) / 2
  }
  
  // Positionner verticalement selon l'espace disponible
  if (spaceBelow >= modalHeight + margin) {
    // Plus d'espace en bas
    topPosition = buttonRect.bottom + 10
  } else if (spaceAbove >= modalHeight + margin) {
    // Plus d'espace en haut
    topPosition = buttonRect.top - modalHeight - 10
  } else {
    // Pas assez d'espace, centrer verticalement
    topPosition = (window.innerHeight - modalHeight) / 2
  }
  
  // GARANTIR que la modale reste entièrement dans les limites de l'écran
  // Vérification horizontale
  if (leftPosition < margin) {
    leftPosition = margin
  } else if (leftPosition + modalWidth > window.innerWidth - margin) {
    leftPosition = window.innerWidth - modalWidth - margin
  }
  
  // Vérification verticale
  if (topPosition < margin) {
    topPosition = margin
  } else if (topPosition + modalHeight > window.innerHeight - margin) {
    topPosition = window.innerHeight - modalHeight - margin
  }
  
  // Vérification finale - si la modale est encore trop grande pour l'écran
  if (modalWidth > window.innerWidth - 2 * margin) {
    // Modale trop large, centrer et réduire la largeur
    leftPosition = margin
    modal.style.width = (window.innerWidth - 2 * margin) + 'px'
  } else {
    modal.style.width = modalWidth + 'px'
  }
  
  if (modalHeight > window.innerHeight - 2 * margin) {
    // Modale trop haute, centrer et réduire la hauteur
    topPosition = margin
    modal.style.height = (window.innerHeight - 2 * margin) + 'px'
    modal.style.overflowY = 'auto'
  } else {
    modal.style.height = 'auto'
    modal.style.overflowY = 'visible'
  }
  
  modal.style.left = leftPosition + 'px'
  modal.style.top = topPosition + 'px'
}

// Fonction pour récupérer l'organisation de l'utilisateur
const fetchUserOrganization = async () => {
  try {
    isLoadingOrganization.value = true
    console.log('Récupération de l\'organisation de l\'utilisateur...')
    
    const organization = await OrganizationApiService.getUserOrganization()
    userOrganization.value = organization
    
    console.log('Organisation de l\'utilisateur:', organization)
  } catch (error) {
    console.error('Erreur lors de la récupération de l\'organisation:', error)
    userOrganization.value = null
  } finally {
    isLoadingOrganization.value = false
  }
}

const openSettings = () => {
  console.log('Ouverture des paramètres de l\'organisation')
  // Remplir le formulaire avec les données actuelles
  if (userOrganization.value?.organization) {
    editOrganizationForm.value = {
      name: userOrganization.value.organization.name,
      description: userOrganization.value.organization.description,
      email: userOrganization.value.organization.email,
      phone: userOrganization.value.organization.phone,
      address: userOrganization.value.organization.address,
      website: userOrganization.value.organization.website,
      organization_type: userOrganization.value.organization.organization_type,
      sector: userOrganization.value.organization.sector
    }
  }
  
  isOrganizationSettingsModalOpen.value = true
  document.body.style.overflow = 'hidden'
  
  // Positionnement contextuel
  nextTick(() => {
    if (settingsBtn.value && organizationSettingsModal.value && window.innerWidth > 768) {
      const buttonRect = settingsBtn.value.getBoundingClientRect()
      const modal = organizationSettingsModal.value
      
      // Dimensions de la modale
      const modalWidth = 800
      const modalHeight = 500
      
      // Calculer la position optimale
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight
      
      // Espace disponible à droite et à gauche du bouton
      const spaceRight = viewportWidth - buttonRect.right
      const spaceLeft = buttonRect.left
      
      // Espace disponible en haut et en bas du bouton
      const spaceTop = buttonRect.top
      const spaceBottom = viewportHeight - buttonRect.bottom
      
      let left, top
      
      // Position horizontale : privilégier le côté avec le plus d'espace
      if (spaceRight >= spaceLeft && spaceRight >= modalWidth) {
        // Placer à droite du bouton avec un décalage supplémentaire
        left = buttonRect.right + 20
      } else if (spaceLeft >= modalWidth) {
        // Placer à gauche du bouton
        left = buttonRect.left - modalWidth - 10
      } else {
        // Centrer horizontalement avec un décalage vers la droite
        left = (viewportWidth - modalWidth) / 2 + 50
      }
      
      // Position verticale : privilégier le côté avec le plus d'espace
      if (spaceBottom >= spaceTop && spaceBottom >= modalHeight) {
        // Placer en bas du bouton
        top = buttonRect.bottom + 10
      } else if (spaceTop >= modalHeight) {
        // Placer au-dessus du bouton
        top = buttonRect.top - modalHeight - 10
      } else {
        // Centrer verticalement
        top = (viewportHeight - modalHeight) / 2
      }
      
      // S'assurer que la modale reste dans la viewport
      left = Math.max(10, Math.min(left, viewportWidth - modalWidth - 10))
      top = Math.max(10, Math.min(top, viewportHeight - modalHeight - 10))
      
      // Appliquer la position
      modal.style.position = 'fixed'
      modal.style.left = `${left}px`
      modal.style.top = `${top}px`
      modal.style.transform = 'none'
      modal.style.margin = '0'
    }
  })
}

const closeOrganizationSettingsModal = () => {
  isOrganizationSettingsModalOpen.value = false
  document.body.style.overflow = 'auto'
}

const setActiveOrganizationTab = (tab) => {
  activeOrganizationTab.value = tab
}

const getOrganizationTabIcon = () => {
  const icons = {
    edit: 'bi-pencil-square',
    members: 'bi-people',
    permissions: 'bi-shield-check',
    billing: 'bi-credit-card',
    delete: 'bi-trash3'
  }
  return icons[activeOrganizationTab.value] || 'bi-gear'
}

const getOrganizationTabTitle = () => {
  const titles = {
    edit: 'Éditer l\'organisation',
    members: 'Gestion des membres',
    permissions: 'Permissions',
    billing: 'Facturation',
    delete: 'Supprimer l\'organisation'
  }
  return titles[activeOrganizationTab.value] || 'Paramètres'
}

const saveOrganizationChanges = async () => {
  try {
    isSavingOrganization.value = true
    console.log('Sauvegarde des modifications:', editOrganizationForm.value)
    
    // Vérifier que l'organisation existe
    if (!userOrganization.value?.organization?.id) {
      throw new Error('Aucune organisation trouvée')
    }
    
    // Appel à l'API pour mettre à jour l'organisation
    const response = await OrganizationApiService.updateOrganization(
      userOrganization.value.organization.id, 
      editOrganizationForm.value
    )
    
    console.log('Organisation mise à jour avec succès:', response)
    
    // Mettre à jour les données locales
    if (response.organization) {
      userOrganization.value.organization = {
        ...userOrganization.value.organization,
        ...response.organization
      }
    }
    
    // Afficher le message de succès
    showNotification('success', 'Succès', 'Organisation mise à jour avec succès !')
    
    // Fermer la modale après un délai
    setTimeout(() => {
      closeOrganizationSettingsModal()
    }, 2000)
    
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la mise à jour de l\'organisation: ' + error.message)
  } finally {
    isSavingOrganization.value = false
  }
}

// Fonctions pour les notifications
const showNotification = (type, title, message) => {
  notification.value = {
    show: true,
    type,
    title,
    message
  }
  
  // Auto-masquer après 5 secondes
  setTimeout(() => {
    hideNotification()
  }, 5000)
}

const hideNotification = () => {
  notification.value.show = false
}

// Fonction pour formater la date
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const confirmDelete = () => {
  // Vérifier que le mot de passe est fourni
  if (!deleteConfirmation.value) {
    showNotification('error', 'Erreur', 'Veuillez entrer votre mot de passe pour confirmer la suppression')
    return
  }
  
  // Afficher la confirmation
  showDeleteConfirmation.value = true
}

const cancelDelete = () => {
  // Réinitialiser l'état
  showDeleteConfirmation.value = false
  deleteConfirmation.value = ''
}

const executeDelete = async () => {
  try {
    console.log('Suppression de l\'organisation')
    
    // Vérifier que l'organisation existe
    if (!userOrganization.value?.organization?.id) {
      throw new Error('Aucune organisation trouvée')
    }
    
    // Appel à l'API pour supprimer l'organisation avec le mot de passe
    await OrganizationApiService.deleteOrganization(userOrganization.value.organization.id, deleteConfirmation.value)
    
    console.log('Organisation supprimée avec succès')
    
    // Afficher le message de succès
    showNotification('success', 'Succès', 'Organisation supprimée avec succès !')
    
    // Fermer la modale après un délai
    setTimeout(() => {
      closeOrganizationSettingsModal()
      
      // Réinitialiser les données locales
      userOrganization.value = null
      
      // Marquer que l'utilisateur n'a plus d'organisation
      localStorage.removeItem('user_has_organization')
      
      // Recharger la page pour mettre à jour l'interface
      window.location.reload()
    }, 2000)
    
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la suppression de l\'organisation: ' + error.message)
    
    // Revenir à l'état initial en cas d'erreur
    showDeleteConfirmation.value = false
  }
}

// Fonctions pour la modale d'invitation
const openInviteModal = () => {
  console.log('Ouverture de la modale d\'invitation')
  isInviteModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeInviteModal = () => {
  console.log('Fermeture de la modale d\'invitation')
  isInviteModalOpen.value = false
  document.body.style.overflow = 'auto'
  
  // Réinitialiser le formulaire
  inviteForm.value.role = ''
  generatedInviteCode.value = ''
}

const generateInviteCode = async () => {
  console.log('Génération du code d\'invitation pour le rôle:', inviteForm.value.role)
  
  try {
    // Récupérer le token CSRF
    const csrfToken = await getCsrfToken()
    console.log('Token CSRF récupéré:', csrfToken)
    
    if (!csrfToken) {
      showNotification('error', 'Erreur', 'Impossible de récupérer le token CSRF')
      return
    }
    
    const requestData = {
      organization: userOrganization.value?.organization?.id,
      role: inviteForm.value.role
    }
    console.log('Données à envoyer:', requestData)
    
    // Appeler l'API pour créer le code d'invitation en base de données
    const response = await $fetch('http://127.0.0.1:8000/api/organizations/invitations/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Csrftoken': csrfToken  // Note: Django attend 'X-Csrftoken' (minuscule 's')
      },
      credentials: 'include', // Inclure les cookies de session
      body: requestData
    })
    
    console.log('Réponse du serveur:', response)
    
    if (response.success) {
      // Récupérer le code généré par le backend
      generatedInviteCode.value = response.data.code
      console.log('Code d\'invitation généré et sauvegardé:', generatedInviteCode.value)
      showNotification('success', 'Succès', 'Code d\'invitation généré et sauvegardé !')
    } else {
      console.error('Erreur lors de la génération:', response.message)
      showNotification('error', 'Erreur', response.message || 'Erreur lors de la génération du code')
    }
  } catch (error) {
    console.error('Erreur lors de la génération du code d\'invitation:', error)
    console.error('Détails de l\'erreur:', error.data)
    showNotification('error', 'Erreur', 'Impossible de générer le code d\'invitation')
  }
}

const copyInviteCode = async () => {
  try {
    await navigator.clipboard.writeText(generatedInviteCode.value)
    showNotification('success', 'Succès', 'Code d\'invitation copié dans le presse-papiers !')
  } catch (error) {
    console.error('Erreur lors de la copie:', error)
    showNotification('error', 'Erreur', 'Impossible de copier le code d\'invitation')
  }
}

const getRoleDisplayName = (role) => {
  const roleNames = {
    'secretaire': 'Secrétaire',
    'chef': 'Chef',
    'chef+1': 'Chef+1',
    'chef+2': 'Chef+2',
    'chef+n': 'Chef+n'
  }
  return roleNames[role] || role
}

onMounted(() => {
  // Récupérer l'organisation de l'utilisateur
  fetchUserOrganization()
  console.log('Organizations page loaded')
  
  // Vérifier si l'utilisateur vient de créer une organisation
  const urlParams = new URLSearchParams(window.location.search)
  if (urlParams.get('created') === 'true') {
    // Afficher un message de bienvenue
    console.log('Organisation créée avec succès, affichage de la page d\'organisation')
    
    // Nettoyer l'URL en retirant le paramètre
    const newUrl = window.location.pathname + '?page=organization'
    window.history.replaceState({}, document.title, newUrl)
  }
})
</script>

<style scoped>
.organizations-page {
  padding: 0;
  background: #f8f9fa;
  min-height: 100vh;
}

/* HEADER */
.organizations-header {
  padding: 1rem 0;
  margin-bottom: 1.5rem;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 2rem;
}

.header-content {
  flex: 1;
  text-align: left;
  opacity: 0;
  animation: slideInLeft 1s ease-out 0.3s forwards;
}

.header-image {
  flex-shrink: 0;
  opacity: 0;
  animation: slideInRight 1s ease-out 0.5s forwards;
}

.organizations-illustration {
  width: 340px;
  height: auto;
  filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.1));
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.organizations-illustration:hover {
  transform: translateY(-4px);
  filter: drop-shadow(0 8px 20px rgba(0, 102, 204, 0.15));
}

/* Bulles décoratives */
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
  top: -5%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

.bubble-2 {
  width: 110px;
  height: 110px;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.4s forwards, float 6s ease-in-out infinite 1.4s;
}

.bubble-3 {
  width: 70px;
  height: 70px;
  bottom: 5%;
  right: 20%;
  animation: fadeInScale 1s ease-out 1.6s forwards, float 6s ease-in-out infinite 1.6s;
}

.bubble-4 {
  width: 80px;
  height: 80px;
  top: 40%;
  left: 10%;
  animation: fadeInScale 1s ease-out 1.8s forwards, float 6s ease-in-out infinite 1.8s;
}

/* Titres et sous-titres */
.section-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* Boutons */
.btn-primary-custom {
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0052a3 0%, #003366 100%);
}

.create-org-btn {
  font-size: 1.1rem;
  padding: 14px 28px;
}

/* STATISTIQUES */
.orgs-stats-section {
  margin-bottom: 3rem;
}

/* BOUTON PARAMÈTRES */
.settings-btn {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.settings-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
  background: linear-gradient(135deg, #0056b3 0%, #0066cc 100%);
}

/* MODALE PARAMÈTRES D'ORGANISATION */
.organization-settings-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  z-index: 10000;
  backdrop-filter: blur(1px);
  animation: fadeInOverlay 0.3s ease-out;
}

.organization-settings-modal {
  position: fixed;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  width: 800px;
  height: 500px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  display: flex;
  overflow: hidden;
  z-index: 10001;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
  position: relative; /* Ajouté pour le positionnement de la notification */
}

.organization-settings-menu {
  width: 250px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  position: relative;
}

.organization-settings-menu::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 60% 30%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 90% 70%, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px, 30px 30px, 40px 40px, 35px 35px, 45px 45px;
  background-position: 0 0, 10px 10px, 20px 20px, 30px 30px, 40px 40px;
  opacity: 0.3;
  pointer-events: none;
  z-index: 1;
}

.organization-settings-menu-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-top-left-radius: 16px;
}

.organization-avatar {
  width: 50px;
  height: 50px;
  background: rgba(0, 102, 204, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
  color: var(--primary-blue);
  font-size: 1.5rem;
}

.organization-settings-menu-header h6 {
  color: var(--text-dark);
  font-weight: 600;
  margin: 0;
  font-size: 0.9rem;
}

.organization-settings-nav {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  position: relative;
  z-index: 2;
}

.organization-settings-nav-item {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
  border-left: 3px solid transparent;
  background: rgba(255, 255, 255, 0.1);
  margin: 0.25rem 0.5rem;
  border-radius: 8px;
}

.organization-settings-nav-item:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.organization-settings-nav-item.active {
  background: rgba(0, 102, 204, 0.15);
  color: var(--primary-blue);
  border-left-color: var(--primary-blue);
}

.organization-settings-nav-item i {
  font-size: 1rem;
  width: 16px;
}

.organization-settings-nav-item span {
  font-size: 0.9rem;
  font-weight: 500;
}

.organization-settings-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  position: relative;
}

.organization-settings-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 15% 25%, rgba(0, 102, 204, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 75% 15%, rgba(0, 102, 204, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 35% 75%, rgba(0, 102, 204, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 85% 45%, rgba(0, 102, 204, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 55% 85%, rgba(0, 102, 204, 0.05) 1px, transparent 1px);
  background-size: 60px 60px, 25px 25px, 45px 45px, 30px 30px, 50px 50px;
  background-position: 0 0, 15px 15px, 25px 25px, 35px 35px, 45px 45px;
  opacity: 0.4;
  pointer-events: none;
  z-index: 1;
}

.organization-settings-content-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}

.organization-settings-content-header h5 {
  margin: 0;
  color: var(--text-dark);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-dark);
}

.organization-settings-content-body {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  position: relative;
  z-index: 2;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-dark);
  font-weight: 500;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.members-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.member-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 8px;
  margin-bottom: 0.75rem;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.member-avatar {
  width: 40px;
  height: 40px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.25rem;
}

.member-details h6 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
}

.member-details p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}

.permission-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 8px;
  margin-bottom: 0.75rem;
}

.permission-info h6 {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-dark);
}

.permission-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}

.billing-info {
  padding: 1.5rem;
  background: rgba(0, 102, 204, 0.05);
  border-radius: 8px;
  text-align: center;
}

.billing-info h6 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.billing-info p {
  margin: 0 0 1rem 0;
  color: #666;
}

.delete-warning {
  text-align: center;
  padding: 2rem;
}

.warning-icon {
  width: 60px;
  height: 60px;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: #dc3545;
  font-size: 1.5rem;
}

.delete-warning h6 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.delete-warning p {
  margin: 0 0 1.5rem 0;
  color: #666;
  line-height: 1.5;
}

.delete-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.delete-confirmation {
  text-align: center;
  padding: 2rem;
  background: rgba(220, 53, 69, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.confirmation-icon {
  width: 60px;
  height: 60px;
  background: rgba(220, 53, 69, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: #dc3545;
  font-size: 1.5rem;
}

.delete-confirmation h6 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.delete-confirmation p {
  margin: 0 0 1rem 0;
  color: #666;
  line-height: 1.5;
}

.delete-confirmation ul {
  text-align: left;
  margin: 0.5rem 0 1.5rem 0;
  padding-left: 1.5rem;
}

.delete-confirmation li {
  margin-bottom: 0.25rem;
}

.confirmation-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

/* Message pour utilisateur sans organisation */
.no-organization-message {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin: 2rem 0;
}

.no-org-content {
  max-width: 500px;
  margin: 0 auto;
}

.no-org-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
  font-size: 2rem;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.no-org-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.no-org-content p {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.no-org-content .btn {
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Modale d'invitation - Style identique à la modale de certificat */
.invite-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(0.5px);
  -webkit-backdrop-filter: blur(0.5px);
  z-index: 10002;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-out;
}

.invite-modal {
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

.invite-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.invite-modal-header h6 {
  margin: 0;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}

.invite-modal-header h6 i {
  color: var(--primary-blue);
  font-size: 1.2rem;
}

.invite-modal-body {
  padding: 1.5rem;
  max-height: 350px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.6);
}

.invite-form h6 {
  margin-bottom: 1rem;
  color: var(--text-dark);
  font-weight: 600;
  font-family: 'Raleway', sans-serif;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-dark);
  font-family: 'Raleway', sans-serif;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: var(--text-dark);
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: 'Raleway', sans-serif;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
  background: rgba(255, 255, 255, 0.9);
}

.invite-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.invite-code-section {
  background: rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1.5rem;
}

.invite-code-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.invite-code-header h6 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.invite-code-display {
  margin-bottom: 1.5rem;
}

.code-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 102, 204, 0.3);
  border-radius: 8px;
  padding: 1rem;
}

.invite-code {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(0, 102, 204, 0.2);
  word-break: break-all;
}

.invite-code-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.info-item i {
  color: var(--primary-blue);
  font-size: 1rem;
}

/* Responsive pour la modale d'invitation */
@media (max-width: 768px) {
  .invite-modal {
    width: 95%;
    margin: 1rem;
  }
  
  .invite-modal-content {
    padding: 1rem;
  }
  
  .code-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .invite-code {
    text-align: center;
  }
}

/* Responsive pour la modale sur mobile */
@media (max-width: 768px) {
  .organization-settings-modal {
    width: 90%;
    max-width: 500px;
    height: 85vh;
    max-height: 700px;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    animation: modalSlideUpMobile 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    transform-origin: center center;
  }
  
  .organization-settings-menu {
    display: none;
  }
  
  .organization-settings-content {
    flex: 1;
    width: 100%;
    height: 100%;
  }
}

/* Animations pour la modale */
@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(100px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes modalSlideUpMobile {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.9) rotateX(10deg);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotateX(0deg);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* NOTIFICATIONS TOAST */
.notification-toast {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10001;
  min-width: 300px;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInRight 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.notification-content {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  gap: 0.75rem;
}

.notification-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.notification-text {
  flex: 1;
  min-width: 0;
}

.notification-title {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.2;
}

.notification-message {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
}

.notification-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #999;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.notification-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

/* Types de notifications */
.notification-success {
  border-left: 4px solid #28a745;
}

.notification-success .notification-icon {
  color: #28a745;
}

.notification-error {
  border-left: 4px solid #dc3545;
}

.notification-error .notification-icon {
  color: #dc3545;
}

.notification-warning {
  border-left: 4px solid #ffc107;
}

.notification-warning .notification-icon {
  color: #ffc107;
}

/* Animation */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .notification-toast {
    top: 10px;
    right: 10px;
    left: 10px;
    min-width: auto;
    max-width: none;
  }
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

.stat-icon {
  width: 50px;
  height: 50px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  font-size: 1.25rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0066cc;
  margin: 0;
  line-height: 1;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
  font-weight: 500;
}

/* SECTIONS */
.organizations-sections {
  padding: 2rem 0;
}

.sections-header {
  margin-bottom: 3rem;
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.4s forwards;
}

.sections-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.sections-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  line-height: 1.5;
}

/* CARTES DE SECTION */
.organizations-section-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  opacity: 0;
  animation: slideInUp 0.8s ease-out forwards;
}

.organizations-section-card:nth-child(1) { animation-delay: 0.5s; }
.organizations-section-card:nth-child(2) { animation-delay: 0.6s; }

.organizations-section-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 102, 204, 0.15);
}

.section-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.section-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.3rem;
}

.section-header-content {
  flex: 1;
}

.section-card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.section-card-subtitle {
  color: #6c757d;
  margin: 0;
  font-size: 1rem;
}

/* LISTE DES ORGANISATIONS */
.organizations-list {
  margin-bottom: 2rem;
}

.organization-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.organization-item:hover {
  background: rgba(0, 102, 204, 0.05);
  transform: translateX(4px);
}

.organization-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(0, 102, 204, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0066cc;
  font-size: 1.2rem;
}

.organization-info {
  flex: 1;
}

.organization-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.organization-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-size: 0.9rem;
}

.organization-date {
  color: #6c757d;
}

.organization-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.organization-status.active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.organization-status.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.organization-actions {
  display: flex;
  gap: 0.5rem;
}

/* ACTIONS RAPIDES */
.organizations-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-item-org {
  transition: all 0.3s ease;
}

.action-card-org {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: rgba(0, 102, 204, 0.05);
  border: 1px solid rgba(0, 102, 204, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card-org:hover {
  background: rgba(0, 102, 204, 0.1);
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
}

.action-icon-org {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.action-content-org {
  flex: 1;
}

.action-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.action-description {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

.action-arrow {
  color: #0066cc;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.action-card-org:hover .action-arrow {
  transform: translateX(4px);
}

/* FOOTER DE SECTION */
.section-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

.btn-primary-blue {
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary-blue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* VUE COMPLÈTE */
.all-organizations-view {
  padding: 2rem 0;
}

.all-organizations-header {
  margin-bottom: 2rem;
}

.all-organizations-list {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.organizations-table-container {
  overflow-x: auto;
}

.organizations-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  background: rgba(0, 102, 204, 0.05);
  border-radius: 12px 12px 0 0;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  align-items: center;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.table-body .table-row:hover {
  background: rgba(0, 102, 204, 0.05);
}

.table-cell {
  font-size: 0.9rem;
  color: #2c3e50;
}

.organization-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.organization-cell .organization-icon {
  width: 35px;
  height: 35px;
  font-size: 1rem;
}

.organization-cell .organization-name {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.organization-cell .organization-description {
  font-size: 0.85rem;
  color: #6c757d;
  margin: 0;
}

.status-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
}

.status-badge.active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.role-badge {
  background: rgba(0, 102, 204, 0.1);
  color: #0066cc;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.date-text {
  color: #6c757d;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* MODALES */
.organization-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.organization-modal {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: modalSlideIn 0.3s ease-out;
}

.organization-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
}

.organization-modal-header h5 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #6c757d;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: #0066cc;
}

.organization-modal-content {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
}

/* ANIMATIONS */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
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

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    text-align: center;
  }
  
  .organizations-illustration {
    width: 200px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .sections-title {
    font-size: 2rem;
  }
  
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .table-cell {
    text-align: left;
  }
  
  .organization-modal {
    width: 95%;
    margin: 1rem;
  }
}
</style>

