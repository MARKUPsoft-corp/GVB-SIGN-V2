<template>
  <div class="organizations-page">
    <!-- Bouton de fermeture -->
    <button class="close-organization-btn" @click="closeOrganizationDashboard" title="Fermer et retourner à la sélection d'organisation">
      <i class="bi bi-x"></i>
    </button>
    
    <!-- Header avec titre de la section -->
    <div class="organizations-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="section-title">
            <span class="text-dark">Espace d'administration de l'</span>
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
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'invitations' }" @click="setActiveOrganizationTab('invitations')">
              <i class="bi bi-envelope"></i>
              <span>Invitations</span>
            </li>
            <li class="organization-settings-nav-item" :class="{ active: activeOrganizationTab === 'certificates' }" @click="setActiveOrganizationTab('certificates')">
              <i class="bi bi-shield-fill-check"></i>
              <span>Certificats</span>
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
              
              <!-- Onglets pour les membres -->
              <div class="members-tabs">
                <div class="members-tab-nav">
                  <button 
                    class="members-tab-btn" 
                    :class="{ active: activeMembersTab === 'active' }"
                    @click="setActiveMembersTab('active')"
                  >
                    <i class="bi bi-people-fill me-2"></i>
                    Actifs
                    <span class="tab-badge">{{ organizationMembers.length }}</span>
                  </button>
                  <button 
                    class="members-tab-btn" 
                    :class="{ active: activeMembersTab === 'pending' }"
                    @click="setActiveMembersTab('pending')"
                  >
                    <i class="bi bi-clock-fill me-2"></i>
                    En attente
                    <span class="tab-badge">{{ pendingMembers.length }}</span>
                  </button>
                  <button 
                    class="members-tab-btn" 
                    :class="{ active: activeMembersTab === 'rejected' }"
                    @click="setActiveMembersTab('rejected')"
                  >
                    <i class="bi bi-x-circle-fill me-2"></i>
                    Rejeté
                    <span class="tab-badge">{{ rejectedMembers.length }}</span>
                  </button>
                </div>
                
                <!-- Contenu des onglets -->
                <div class="members-tab-content">
                  <!-- Onglet Membres actifs -->
                  <div v-if="activeMembersTab === 'active'" class="members-tab-pane">
              <!-- Loading state -->
              <div v-if="isLoadingMembers" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Chargement...</span>
                </div>
                <p class="text-muted mt-2">Chargement des membres...</p>
              </div>
              
                    <!-- Liste des membres actifs -->
              <div v-else-if="organizationMembers.length > 0" class="members-list">
                <div v-for="member in organizationMembers" :key="member.id" class="member-item">
                  <div class="member-info">
                    <div class="member-avatar">
                      <i class="bi bi-person-circle"></i>
                    </div>
                    <div class="member-details">
                      <h6>{{ member.user_name || member.user_email }}</h6>
                      <p class="text-muted">{{ member.user_email }}</p>
                      <small class="text-muted">
                        Rejoint le {{ formatDate(member.joined_at) }}
                      </small>
                    </div>
                  </div>
                  <div class="member-actions">
                    <span class="badge" :class="getRoleBadgeClass(member.role)">
                      {{ getRoleDisplayName(member.role) }}
                    </span>
                  </div>
                </div>
              </div>
              
                    <!-- Aucun membre actif -->
              <div v-else class="text-center py-4">
                      <i class="bi bi-people text-muted" style="font-size: 2rem;"></i>
                      <p class="text-muted mt-2">Aucun membre actif dans cette organisation</p>
                    </div>
                  </div>
                  
                  <!-- Onglet Membres en attente -->
                  <div v-if="activeMembersTab === 'pending'" class="members-tab-pane">
                    <!-- Loading state -->
                    <div v-if="isLoadingPendingMembers" class="text-center py-4">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Chargement...</span>
                      </div>
                      <p class="text-muted mt-2">Chargement des demandes...</p>
                    </div>
                    
                    <!-- Liste des membres en attente -->
                    <div v-else-if="pendingMembers.length > 0" class="members-list">
                      <div v-for="request in pendingMembers" :key="request.id" class="member-item pending-member">
                        <div class="member-info">
                          <div class="member-avatar pending">
                            <i class="bi bi-person-plus"></i>
                          </div>
                          <div class="member-details">
                            <h6>{{ request.user_name || request.user_email }}</h6>
                            <p class="text-muted">{{ request.user_email }}</p>
                            <small class="text-muted">
                              Demande du {{ formatDate(request.created_at) }}
                            </small>
                            <div class="request-role">
                              <span class="badge bg-info">
                                Rôle demandé: {{ getRoleDisplayName(request.requested_role) }}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div class="member-actions">
                          <button class="btn btn-success btn-sm me-2" @click="approveMembershipRequest(request)">
                            <i class="bi bi-check"></i>
                            Approuver
                          </button>
                          <button class="btn btn-danger btn-sm" @click="rejectMembershipRequest(request)">
                            <i class="bi bi-x"></i>
                            Rejeter
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Aucune demande en attente -->
                    <div v-else class="text-center py-4">
                      <i class="bi bi-clock text-muted" style="font-size: 2rem;"></i>
                      <p class="text-muted mt-2">Aucune demande d'adhésion en attente</p>
                    </div>
                  </div>
                  
                  <!-- Onglet Membres rejetés -->
                  <div v-if="activeMembersTab === 'rejected'" class="members-tab-pane">
                    <!-- Loading state -->
                    <div v-if="isLoadingRejectedMembers" class="text-center py-4">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Chargement...</span>
                      </div>
                      <p class="text-muted mt-2">Chargement des membres rejetés...</p>
                    </div>
                    
                    <!-- Liste des membres rejetés -->
                    <div v-else-if="rejectedMembers.length > 0" class="members-list">
                      <div v-for="request in rejectedMembers" :key="request.id" class="member-item rejected-member">
                        <div class="member-info">
                          <div class="member-avatar rejected">
                            <i class="bi bi-person-x"></i>
                          </div>
                          <div class="member-details">
                            <h6>{{ request.user_name || request.user_email }}</h6>
                            <p class="text-muted">{{ request.user_email }}</p>
                            <small class="text-muted">
                              Rejeté le {{ formatDate(request.processed_at) }}
                            </small>
                            <div class="request-role">
                              <span class="badge bg-secondary">{{ getRoleDisplayName(request.requested_role) }}</span>
                            </div>
                            <div v-if="request.response_message" class="rejection-reason mt-2">
                              <small class="text-muted">
                                <strong>Raison :</strong> {{ request.response_message }}
                              </small>
                            </div>
                          </div>
                        </div>
                        <div class="member-actions">
                          <button 
                            class="btn btn-success btn-sm me-2" 
                            @click="reapproveMembershipRequest(request.id)"
                            :disabled="isProcessingRequest"
                          >
                            <i class="bi bi-check-circle me-1"></i>
                            Réapprouver
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Aucun membre rejeté -->
                    <div v-else class="text-center py-4">
                      <i class="bi bi-x-circle text-muted" style="font-size: 2rem;"></i>
                      <p class="text-muted mt-2">Aucun membre rejeté</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Contenu Invitations -->
            <div v-if="activeOrganizationTab === 'invitations'" class="tab-content">
              
              <!-- Loading state -->
              <div v-if="isLoadingInvitations" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Chargement...</span>
                </div>
                <p class="text-muted mt-2">Chargement des codes d'invitation...</p>
              </div>
              
              <!-- Liste des codes d'invitation -->
              <div v-else-if="invitationCodes.length > 0" class="invitations-list">
                <div v-for="code in invitationCodes" :key="code.id" class="member-item">
                  <div class="member-info">
                    <div class="member-avatar">
                      <i class="bi bi-envelope"></i>
                    </div>
                    <div class="member-details">
                      <h6>{{ code.code }}</h6>
                      <p class="text-muted">Rôle: {{ getRoleDisplayName(code.role) }}</p>
                      <small class="text-muted">
                        Créé le {{ formatDate(code.created_at) }}
                        <span v-if="code.used_at"> • Utilisé le {{ formatDate(code.used_at) }}</span>
                        <span v-if="code.used_by_name"> par {{ code.used_by_name }}</span>
                      </small>
                    </div>
                  </div>
                  <div class="member-actions">
                    <span class="badge" :class="getInvitationStatusClass(code)">
                      {{ getInvitationStatusText(code) }}
                    </span>
                    <div class="invitation-buttons mt-2">
                      <button 
                        class="btn btn-outline-primary btn-sm me-1" 
                        @click="copyInvitationCode(code.code)"
                        title="Copier le code"
                      >
                        <i class="bi bi-copy"></i>
                      </button>
                      <button 
                        v-if="!code.is_used && code.is_active !== false" 
                        class="btn btn-outline-warning btn-sm me-1" 
                        @click="deactivateInvitationCode(code.id)"
                        title="Désactiver le code"
                      >
                        <i class="bi bi-pause-circle"></i>
                      </button>
                      <button 
                        v-if="!code.is_used && code.is_active === false" 
                        class="btn btn-outline-success btn-sm me-1" 
                        @click="reactivateInvitationCode(code.id)"
                        title="Réactiver le code"
                      >
                        <i class="bi bi-play-circle"></i>
                      </button>
                      <button 
                        class="btn btn-outline-danger btn-sm" 
                        @click="deleteInvitationCode(code.id)"
                        title="Supprimer définitivement le code"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Aucun code d'invitation -->
              <div v-else class="text-center py-4">
                <i class="bi bi-envelope text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-2">Aucun code d'invitation trouvé</p>
                <small class="text-muted">Les codes d'invitation apparaîtront ici une fois créés</small>
              </div>
            </div>
            
            <!-- Contenu Certificats -->
            <div v-if="activeOrganizationTab === 'certificates'" class="tab-content">
              
              <!-- Loading state -->
              <div v-if="isLoadingCertificates" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Chargement...</span>
                </div>
                <p class="text-muted mt-2">Chargement des certificats...</p>
              </div>
              
              <!-- Liste des certificats -->
              <div v-else-if="organizationCertificates.length > 0" class="certificates-list">
                <div v-for="certificate in organizationCertificates" :key="certificate.id" class="member-item">
                  <div class="member-info">
                    <div class="member-avatar">
                      <i class="bi bi-shield-fill-check"></i>
                    </div>
                    <div class="member-details">
                      <h6>{{ certificate.name }}</h6>
                      <p class="text-muted">{{ certificate.subject_common_name || 'Certificat de signature' }}</p>
                      <small class="text-muted">
                        Importé le {{ formatDate(certificate.imported_at) }}
                        <span v-if="certificate.imported_by_name"> par {{ certificate.imported_by_name }}</span>
                      </small>
                    </div>
                  </div>
                  <div class="member-actions">
                    <span class="badge" :class="getCertificateStatusClass(certificate)">
                      {{ getCertificateStatusText(certificate) }}
                    </span>
                    <div class="certificate-buttons mt-2">
                      <button 
                        class="btn btn-outline-info btn-sm me-1" 
                        @click="viewCertificateDetails(certificate, $event)"
                        @mouseenter="viewCertificateDetails(certificate, $event)"
                        @mouseleave="closeCertificateDetails"
                        title="Voir les détails"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                      <button 
                        class="btn btn-outline-danger btn-sm" 
                        @click="deleteCertificate(certificate.id)"
                        title="Supprimer le certificat"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Aucun certificat -->
              <div v-else class="text-center py-4">
                <i class="bi bi-shield-fill-check text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-2">Aucun certificat trouvé</p>
                <button class="btn btn-primary btn-sm" @click="openCertificateImportModal">
                  <i class="bi bi-upload me-1"></i>
                  Importer un certificat
                </button>
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

      <!-- Modale d'import de certificat (enfant de la modale des paramètres) -->
      <div v-if="isCertificateImportModalOpen" class="certificate-modal-overlay" @click="closeCertificateImportModal">
        <div class="certificate-modal" @click.stop>
          <div class="certificate-modal-header">
            <h6>
              <i class="bi bi-shield-fill-check"></i>
              Importer un certificat d'organisation
            </h6>
            <button class="close-btn" @click="closeCertificateImportModal">
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
            <button @click="closeCertificateImportModal" class="btn btn-outline-secondary btn-sm">
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

    <!-- Bulle de détails du certificat (à l'intérieur de la modale) -->
    <div v-if="showCertificateDetailsModal" class="certificate-details-tooltip" :style="{ top: certificateDetailsPosition.top + 'px', left: certificateDetailsPosition.left + 'px' }" @click.stop @mouseenter="cancelCloseCertificateDetails" @mouseleave="closeCertificateDetails">
      <div class="tooltip-arrow" :class="'arrow-' + certificateDetailsDirection"></div>
      <div class="tooltip-content">
        <div class="tooltip-header">
          <h4 class="tooltip-title">
            <i class="bi bi-shield-fill-check me-2"></i>
            {{ currentCertificateDetails?.name }}
          </h4>
          <button class="tooltip-close" @click="closeCertificateDetails">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="tooltip-body">
          <div class="certificate-info-list">
            <!-- Informations générales -->
            <div class="info-section">
              <h6 class="info-section-title">
                <i class="bi bi-info-circle me-2"></i>
                Informations générales
              </h6>
              <div class="info-item">
                <i class="bi bi-tag me-2"></i>
                <span class="info-label">Nom:</span>
                <span class="info-value">{{ currentCertificateDetails?.name || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-calendar me-2"></i>
                <span class="info-label">Importé le:</span>
                <span class="info-value">{{ formatDate(currentCertificateDetails?.imported_at) || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-person me-2"></i>
                <span class="info-label">Importé par:</span>
                <span class="info-value">{{ currentCertificateDetails?.imported_by_name || 'Non renseigné' }}</span>
              </div>
            </div>

            <!-- Sujet du certificat -->
            <div class="info-section">
              <h6 class="info-section-title">
                <i class="bi bi-person-badge me-2"></i>
                Sujet du certificat
              </h6>
              <div class="info-item">
                <i class="bi bi-person me-2"></i>
                <span class="info-label">Nom commun:</span>
                <span class="info-value">{{ currentCertificateDetails?.subject_common_name || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-building me-2"></i>
                <span class="info-label">Organisation:</span>
                <span class="info-value">{{ currentCertificateDetails?.subject_organization || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-geo-alt me-2"></i>
                <span class="info-label">Pays:</span>
                <span class="info-value">{{ currentCertificateDetails?.subject_country || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-envelope me-2"></i>
                <span class="info-label">Email:</span>
                <span class="info-value">{{ currentCertificateDetails?.subject_email || 'Non renseigné' }}</span>
              </div>
            </div>

            <!-- Émetteur du certificat -->
            <div class="info-section">
              <h6 class="info-section-title">
                <i class="bi bi-shield me-2"></i>
                Émetteur du certificat
              </h6>
              <div class="info-item">
                <i class="bi bi-person me-2"></i>
                <span class="info-label">Nom commun:</span>
                <span class="info-value">{{ currentCertificateDetails?.issuer_common_name || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-building me-2"></i>
                <span class="info-label">Organisation:</span>
                <span class="info-value">{{ currentCertificateDetails?.issuer_organization || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-geo-alt me-2"></i>
                <span class="info-label">Pays:</span>
                <span class="info-value">{{ currentCertificateDetails?.issuer_country || 'Non renseigné' }}</span>
              </div>
            </div>

            <!-- Validité -->
            <div class="info-section">
              <h6 class="info-section-title">
                <i class="bi bi-clock me-2"></i>
                Validité
              </h6>
              <div class="info-item">
                <i class="bi bi-calendar-check me-2"></i>
                <span class="info-label">Valide du:</span>
                <span class="info-value">{{ formatDate(currentCertificateDetails?.not_before) || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-calendar-x me-2"></i>
                <span class="info-label">Valide jusqu'au:</span>
                <span class="info-value">{{ formatDate(currentCertificateDetails?.not_after) || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-shield-check me-2"></i>
                <span class="info-label">Statut:</span>
                <span class="info-value" :class="getCertificateStatusClass(currentCertificateDetails)">
                  {{ getCertificateStatusText(currentCertificateDetails) }}
                </span>
              </div>
            </div>

            <!-- Détails techniques -->
            <div class="info-section">
              <h6 class="info-section-title">
                <i class="bi bi-gear me-2"></i>
                Détails techniques
              </h6>
              <div class="info-item">
                <i class="bi bi-hash me-2"></i>
                <span class="info-label">Numéro de série:</span>
                <span class="info-value">{{ currentCertificateDetails?.serial_number || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-fingerprint me-2"></i>
                <span class="info-label">Empreinte:</span>
                <span class="info-value">{{ currentCertificateDetails?.fingerprint || 'Non renseigné' }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-shield-lock me-2"></i>
                <span class="info-label">Algorithme:</span>
                <span class="info-value">{{ currentCertificateDetails?.signature_algorithm || 'Non renseigné' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, defineEmits } from 'vue'
import { useAuthStore } from '../../stores/auth'
import OrganizationApiService from '../../services/OrganizationApiService'
import { CertificateService } from '../../services/CertificateService'

// Store d'authentification
const authStore = useAuthStore()

// Service de certificat
const certificateService = new CertificateService()

// Émissions
const emit = defineEmits(['navigate-to-organization', 'open-profile-modal'])

// État pour l'organisation de l'utilisateur
const userOrganization = ref(null)
const selectedOrganization = ref(null)
const isLoadingOrganization = ref(false)

// État pour les membres de l'organisation
const organizationMembers = ref([])
const isLoadingMembers = ref(false)

// État pour les codes d'invitation
const invitationCodes = ref([])
const isLoadingInvitations = ref(false)

// État pour les certificats d'organisation
const organizationCertificates = ref([])
const isLoadingCertificates = ref(false)

// État de la modale d'import de certificat
const isCertificateImportModalOpen = ref(false)
const selectedCertificateFile = ref(null)
const certificatePassword = ref('')
const showCertificatePassword = ref(false)

// État des onglets membres
const activeMembersTab = ref('active')
const pendingMembers = ref([])
const rejectedMembers = ref([])
const isLoadingPendingMembers = ref(false)
const isLoadingRejectedMembers = ref(false)
const isDraggingCertificate = ref(false)
const certificateFileInput = ref(null)
const certificateError = ref(null)

// État pour la modale de paramètres d'organisation
const isOrganizationSettingsModalOpen = ref(false)
const activeOrganizationTab = ref('edit')
const isSavingOrganization = ref(false)

// Variables pour la bulle de détails du certificat
const showCertificateDetailsModal = ref(false)
const currentCertificateDetails = ref(null)
const certificateDetailsPosition = ref({ top: 0, left: 0 })
const certificateDetailsDirection = ref('left')
const closeCertificateDetailsTimeout = ref(null)
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

// Fonctions de navigation
const closeOrganizationDashboard = () => {
  // Émettre un événement pour retourner à la page de sélection d'organisation
  window.dispatchEvent(new CustomEvent('navigateToOrganizationSelection'))
}

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
    
    // Vérifier d'abord le localStorage pour une organisation sélectionnée
    const savedOrganization = localStorage.getItem('selectedOrganization')
    if (savedOrganization) {
      const organization = JSON.parse(savedOrganization)
      console.log('✅ Utilisation de l\'organisation sélectionnée depuis localStorage:', organization.name)
      console.log('🔍 Détails de l\'organisation sélectionnée:', organization)
      
      // Récupérer les données complètes de l'organisation sélectionnée
      try {
        const fullOrganization = await OrganizationApiService.getOrganization(organization.id)
        console.log('✅ Données complètes de l\'organisation récupérées:', fullOrganization)
        userOrganization.value = {
          organization: fullOrganization.organization,
          role: organization.role || 'admin'
        }
      } catch (error) {
        console.error('❌ Erreur lors de la récupération des données complètes:', error)
        // Fallback sur les données du localStorage
        userOrganization.value = {
          organization: organization,
          role: organization.role || 'admin'
        }
      }
      console.log('✅ Organisation mise à jour avec les données complètes:', userOrganization.value)
      return // Sortir de la fonction sans faire d'appel API
    }
    
    // Si une organisation est déjà sélectionnée en mémoire, l'utiliser
    if (selectedOrganization.value) {
      console.log('✅ Utilisation de l\'organisation sélectionnée:', selectedOrganization.value.name)
      userOrganization.value = {
        organization: selectedOrganization.value,
        role: selectedOrganization.value.role || 'admin'
      }
      console.log('✅ Organisation mise à jour avec les données sélectionnées:', userOrganization.value)
      return // Sortir de la fonction sans faire d'appel API
    }
    
    // Sinon, récupérer l'organisation par défaut
    const organization = await OrganizationApiService.getUserOrganization()
    userOrganization.value = organization
    console.log('Organisation de l\'utilisateur (API):', organization)
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
  
  // Charger les membres de l'organisation
  loadOrganizationMembers()
  
  // Charger les codes d'invitation
  loadInvitationCodes()
  
  // Charger les certificats
  loadOrganizationCertificates()
  
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

// Fonction pour charger les membres de l'organisation
const loadOrganizationMembers = async () => {
  if (!userOrganization.value?.organization?.id) {
    console.log('❌ Aucune organisation disponible pour charger les membres')
    return
  }
  
  try {
    isLoadingMembers.value = true
    console.log('🔄 Chargement des membres de l\'organisation...')
    
    const members = await OrganizationApiService.getOrganizationMembers(userOrganization.value.organization.id)
    organizationMembers.value = members.members || []
    
    console.log('✅ Membres chargés:', organizationMembers.value)
  } catch (error) {
    console.error('❌ Erreur lors du chargement des membres:', error)
    organizationMembers.value = []
  } finally {
    isLoadingMembers.value = false
  }
}

// Fonction pour charger les codes d'invitation
const loadInvitationCodes = async () => {
  if (!userOrganization.value?.organization?.id) {
    console.log('❌ Aucune organisation disponible pour charger les codes d\'invitation')
    return
  }
  
  try {
    isLoadingInvitations.value = true
    console.log('🔄 Chargement des codes d\'invitation...')
    
    const codes = await OrganizationApiService.getInvitationCodes(userOrganization.value.organization.id)
    invitationCodes.value = codes.invitation_codes || []
    
    console.log('✅ Codes d\'invitation chargés:', invitationCodes.value)
  } catch (error) {
    console.error('❌ Erreur lors du chargement des codes d\'invitation:', error)
    invitationCodes.value = []
  } finally {
    isLoadingInvitations.value = false
  }
}

const closeOrganizationSettingsModal = () => {
  isOrganizationSettingsModalOpen.value = false
  document.body.style.overflow = 'auto'
}

const setActiveOrganizationTab = (tab) => {
  activeOrganizationTab.value = tab
  
  // Charger toutes les données des membres dès qu'on clique sur l'onglet "Membres"
  if (tab === 'members') {
    loadAllMembersData()
  }
}

// Fonction pour changer l'onglet des membres
const setActiveMembersTab = (tab) => {
  activeMembersTab.value = tab
  if (tab === 'pending') {
    loadPendingMembers()
  } else if (tab === 'rejected') {
    loadRejectedMembers()
  }
}

// Fonction pour charger toutes les données des membres (pour l'onglet principal "Membres")
const loadAllMembersData = async () => {
  // Charger les membres actifs (déjà chargés)
  await loadOrganizationMembers()
  
  // Charger en parallèle les membres en attente et rejetés pour un effet temps réel
  await Promise.all([
    loadPendingMembers(),
    loadRejectedMembers()
  ])
}

// Charger les demandes d'adhésion en attente
const loadPendingMembers = async () => {
  if (!userOrganization.value?.organization?.id) return
  
  // Éviter de recharger si déjà en cours de chargement
  if (isLoadingPendingMembers.value) return
  
  isLoadingPendingMembers.value = true
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/${userOrganization.value.organization.id}/pending-membership-requests/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        pendingMembers.value = data.requests || []
        console.log('✅ Demandes d\'adhésion en attente chargées:', pendingMembers.value)
      } else {
        console.error('❌ Erreur lors du chargement des demandes:', data.message)
        pendingMembers.value = []
      }
    } else {
      console.error('❌ Erreur HTTP lors du chargement des demandes')
      pendingMembers.value = []
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des demandes:', error)
    pendingMembers.value = []
  } finally {
    isLoadingPendingMembers.value = false
  }
}

// Approuver une demande d'adhésion
const approveMembershipRequest = async (request) => {
  try {
    // Récupérer le token CSRF
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    };
    
    const csrfToken = getCookie('csrftoken');
    
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/membership-requests/${request.id}/approve/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        console.log('✅ Demande d\'adhésion approuvée')
        // Recharger les listes
        await loadPendingMembers()
        await loadOrganizationMembers()
        // Notification de succès
        alert('Demande d\'adhésion approuvée avec succès !')
      } else {
        console.error('❌ Erreur lors de l\'approbation:', data.message)
        alert('Erreur lors de l\'approbation: ' + data.message)
      }
    } else {
      console.error('❌ Erreur HTTP lors de l\'approbation')
      alert('Erreur lors de l\'approbation')
    }
  } catch (error) {
    console.error('❌ Erreur lors de l\'approbation:', error)
    alert('Erreur lors de l\'approbation')
  }
}

// Rejeter une demande d'adhésion
const rejectMembershipRequest = async (request) => {
  if (!confirm('Êtes-vous sûr de vouloir rejeter cette demande d\'adhésion ?')) {
    return
  }
  
  try {
    // Récupérer le token CSRF
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    };
    
    const csrfToken = getCookie('csrftoken');
    
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/membership-requests/${request.id}/reject/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        console.log('✅ Demande d\'adhésion rejetée')
        // Recharger la liste
        await loadPendingMembers()
        // Notification de succès
        alert('Demande d\'adhésion rejetée')
      } else {
        console.error('❌ Erreur lors du rejet:', data.message)
        alert('Erreur lors du rejet: ' + data.message)
      }
    } else {
      console.error('❌ Erreur HTTP lors du rejet')
      alert('Erreur lors du rejet')
    }
  } catch (error) {
    console.error('❌ Erreur lors du rejet:', error)
    alert('Erreur lors du rejet')
  }
}

// Charger les membres rejetés
const loadRejectedMembers = async () => {
  if (!userOrganization.value?.organization?.id) return
  
  // Éviter de recharger si déjà en cours de chargement
  if (isLoadingRejectedMembers.value) return
  
  isLoadingRejectedMembers.value = true
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/${userOrganization.value.organization.id}/rejected-membership-requests/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        rejectedMembers.value = data.requests || []
        console.log('✅ Membres rejetés chargés:', rejectedMembers.value)
      } else {
        console.error('❌ Erreur lors du chargement des membres rejetés:', data.message)
        rejectedMembers.value = []
      }
    } else {
      console.error('❌ Erreur HTTP lors du chargement des membres rejetés')
      rejectedMembers.value = []
    }
  } catch (error) {
    console.error('❌ Erreur lors du chargement des membres rejetés:', error)
    rejectedMembers.value = []
  } finally {
    isLoadingRejectedMembers.value = false
  }
}

// Réapprouver une demande d'adhésion rejetée
const reapproveMembershipRequest = async (requestId) => {
  if (!confirm('Êtes-vous sûr de vouloir réapprouver cette demande d\'adhésion ?')) {
    return
  }
  
  try {
    // Récupérer le token CSRF
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    };
    
    const csrfToken = getCookie('csrftoken');
    
    const response = await fetch(`http://127.0.0.1:8000/api/organizations/membership-requests/${requestId}/reapprove/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        // Recharger les listes
        await loadRejectedMembers()
        await loadPendingMembers()
        await loadOrganizationMembers()
        // Notification de succès
        alert('Demande d\'adhésion réapprouvée avec succès')
      } else {
        console.error('❌ Erreur lors de la réapprobation:', data.message)
        alert('Erreur lors de la réapprobation: ' + data.message)
      }
    } else {
      const errorData = await response.json().catch(() => ({ message: 'Erreur inconnue' }))
      console.error('❌ Erreur HTTP lors de la réapprobation:', response.status, errorData)
      alert(`Erreur ${response.status}: ${errorData.message || 'Erreur lors de la réapprobation'}`)
    }
  } catch (error) {
    console.error('❌ Erreur lors de la réapprobation:', error)
    alert('Erreur lors de la réapprobation')
  }
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
    invitations: 'Codes d\'invitation',
    certificates: 'Certificats d\'organisation',
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
    'admin': 'Administrateur',
    'secretaire': 'Secrétaire',
    'member': 'Membre',
    'chef': 'Chef',
    'chef+1': 'Chef+1',
    'chef+2': 'Chef+2',
    'chef+n': 'Chef+n'
  }
  return roleNames[role] || role
}

// Fonction pour obtenir la classe CSS du badge selon le rôle
const getRoleBadgeClass = (role) => {
  const roleClasses = {
    'admin': 'bg-danger',
    'secretaire': 'bg-primary',
    'member': 'bg-warning',
    'chef': 'bg-success',
    'chef+1': 'bg-success',
    'chef+2': 'bg-success',
    'chef+n': 'bg-success'
  }
  return roleClasses[role] || 'bg-secondary'
}

// Fonctions pour l'affichage du statut des codes d'invitation
const getInvitationStatusClass = (code) => {
  if (code.is_used) {
    return 'bg-success'
  } else if (code.is_active === false) {
    return 'bg-secondary'
  } else {
    return 'bg-warning'
  }
}

const getInvitationStatusText = (code) => {
  if (code.is_used) {
    return 'Utilisé'
  } else if (code.is_active === false) {
    return 'Inactif'
  } else {
    return 'Actif'
  }
}

// Fonctions pour gérer les codes d'invitation
const deactivateInvitationCode = async (codeId) => {
  if (!confirm('Êtes-vous sûr de vouloir désactiver ce code d\'invitation ?')) {
    return
  }
  
  try {
    console.log('🔄 Désactivation du code d\'invitation:', codeId)
    
    const response = await OrganizationApiService.deactivateInvitationCode(codeId)
    
    if (response.success) {
      console.log('✅ Code d\'invitation désactivé')
      // Recharger la liste des codes
      await loadInvitationCodes()
      showNotification('success', 'Succès', 'Code d\'invitation désactivé avec succès !')
    } else {
      throw new Error(response.message || 'Erreur lors de la désactivation du code')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la désactivation du code:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la désactivation du code d\'invitation: ' + error.message)
  }
}

const reactivateInvitationCode = async (codeId) => {
  if (!confirm('Êtes-vous sûr de vouloir réactiver ce code d\'invitation ?')) {
    return
  }
  
  try {
    console.log('🔄 Réactivation du code d\'invitation:', codeId)
    
    const response = await OrganizationApiService.reactivateInvitationCode(codeId)
    
    if (response.success) {
      console.log('✅ Code d\'invitation réactivé')
      // Recharger la liste des codes
      await loadInvitationCodes()
      showNotification('success', 'Succès', 'Code d\'invitation réactivé avec succès !')
    } else {
      throw new Error(response.message || 'Erreur lors de la réactivation du code')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la réactivation du code:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la réactivation du code d\'invitation: ' + error.message)
  }
}

const copyInvitationCode = async (code) => {
  try {
    await navigator.clipboard.writeText(code)
    showNotification('success', 'Succès', 'Code copié dans le presse-papiers !')
  } catch (error) {
    console.error('❌ Erreur lors de la copie:', error)
    showNotification('error', 'Erreur', 'Impossible de copier le code d\'invitation')
  }
}

const deleteInvitationCode = async (codeId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce code d\'invitation ?')) {
    return
  }
  
  try {
    console.log('🔄 Suppression du code d\'invitation:', codeId)
    
    const response = await OrganizationApiService.deleteInvitationCode(codeId)
    
    if (response.success) {
      console.log('✅ Code d\'invitation supprimé')
      // Recharger la liste des codes
      await loadInvitationCodes()
      showNotification('success', 'Succès', 'Code d\'invitation supprimé avec succès !')
    } else {
      throw new Error(response.message || 'Erreur lors de la suppression du code')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la suppression du code:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la suppression du code d\'invitation: ' + error.message)
  }
}

// Fonction pour charger les certificats d'organisation
const loadOrganizationCertificates = async () => {
  if (!userOrganization.value?.organization?.id) {
    console.log('❌ Aucune organisation disponible pour charger les certificats')
    return
  }
  
  try {
    isLoadingCertificates.value = true
    console.log('🔄 Chargement des certificats...')
    
    const certificates = await OrganizationApiService.getOrganizationCertificates(userOrganization.value.organization.id)
    organizationCertificates.value = certificates.certificates || []
    
    console.log('✅ Certificats chargés:', organizationCertificates.value)
  } catch (error) {
    console.error('❌ Erreur lors du chargement des certificats:', error)
    organizationCertificates.value = []
  } finally {
    isLoadingCertificates.value = false
  }
}

// Fonctions pour l'affichage du statut des certificats
const getCertificateStatusClass = (certificate) => {
  if (certificate.is_expired) {
    return 'bg-danger'
  } else if (certificate.validity_info?.daysUntilExpiry <= 30) {
    return 'bg-warning'
  } else {
    return 'bg-success'
  }
}

const getCertificateStatusText = (certificate) => {
  if (certificate.is_expired) {
    return 'Expiré'
  } else if (certificate.validity_info?.daysUntilExpiry <= 30) {
    return 'Expire bientôt'
  } else {
    return 'Valide'
  }
}

// Fonctions pour gérer les certificats
const openCertificateImportModal = () => {
  isCertificateImportModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeCertificateImportModal = () => {
  isCertificateImportModalOpen.value = false
  selectedCertificateFile.value = null
  certificatePassword.value = ''
  showCertificatePassword.value = false
  certificateError.value = null
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
    const certificateInfo = await certificateService.decodeCertificate(
      selectedCertificateFile.value, 
      certificatePassword.value
    )
    
    // Sauvegarder en base de données pour l'organisation
    const certificateData = {
      name: certificateInfo.subject.commonName || 'Certificat d\'organisation',
      subject_common_name: certificateInfo.subject.commonName,
      subject_organization: certificateInfo.subject.organization,
      subject_organizational_unit: certificateInfo.subject.organizationalUnit,
      subject_country: certificateInfo.subject.country,
      subject_email: certificateInfo.subject.email,
      issuer_common_name: certificateInfo.issuer.commonName,
      issuer_organization: certificateInfo.issuer.organization,
      issuer_country: certificateInfo.issuer.country,
      serial_number: certificateInfo.serialNumber,
      fingerprint: certificateInfo.fingerprint,
      signature_algorithm: certificateInfo.signatureAlgorithm,
      not_before: certificateInfo.validity.notBefore,
      not_after: certificateInfo.validity.notAfter,
      is_valid: certificateInfo.validity.isValid,
      key_usage: certificateInfo.keyUsage,
      private_key_pem: certificateService.getPrivateKeyPem(),
      public_key_pem: certificateService.getPublicKeyPem(),
      certificate_pem: certificateService.getCertificatePem()
    }
    
    // Envoyer à l'API
    const response = await OrganizationApiService.createOrganizationCertificate(
      userOrganization.value.organization.id,
      certificateData
    )
    
    if (response.success) {
      console.log('✅ Certificat importé avec succès:', response.certificate)
      
      // Fermer la modale
      closeCertificateImportModal()
      
      // Recharger la liste des certificats
      await loadOrganizationCertificates()
      
      showNotification('success', 'Succès', 'Certificat importé avec succès !')
    } else {
      throw new Error(response.message || 'Erreur lors de l\'import du certificat')
    }
    
  } catch (error) {
    console.error('❌ Erreur lors de l\'import du certificat:', error)
    certificateError.value = error.message
  }
}

const viewCertificateDetails = (certificate, event) => {
  console.log('🔄 Affichage des détails du certificat:', certificate.name)
  
  // Annuler le délai de fermeture si la souris revient
  if (closeCertificateDetailsTimeout.value) {
    clearTimeout(closeCertificateDetailsTimeout.value)
    closeCertificateDetailsTimeout.value = null
  }
  
  if (event && event.target) {
    const rect = event.target.getBoundingClientRect()
    
    // Trouver la modale parente
    const modal = event.target.closest('.organization-settings-modal')
    if (!modal) return
    
    const modalRect = modal.getBoundingClientRect()
    
    const tooltipWidth = 500 // Largeur approximative de la bulle
    const tooltipHeight = 400 // Hauteur approximative de la bulle
    
    // Position relative à la modale
    let top, left, direction
    
    // Positionner à droite du bouton, à l'intérieur de la modale
    left = rect.right - modalRect.left + 15
    top = rect.top - modalRect.top - 50
    direction = 'left'
    
    certificateDetailsDirection.value = direction
    
    // Ajustements pour rester dans la modale
    const margin = 20
    
    // Ajustement horizontal - s'assurer que la bulle reste dans la modale
    if (left < margin) {
      left = margin
    } else if (left + tooltipWidth > modalRect.width - margin) {
      left = modalRect.width - tooltipWidth - margin
    }
    
    // Ajustement vertical - s'assurer que la bulle reste dans la modale
    if (top < margin) {
      top = margin
    } else if (top + tooltipHeight > modalRect.height - margin) {
      top = modalRect.height - tooltipHeight - margin
      
      // Si même en haut elle ne rentre pas, la centrer verticalement dans la modale
      if (top < margin) {
        top = (modalRect.height - tooltipHeight) / 2
      }
    }
    
    // Position finale relative à la modale
    certificateDetailsPosition.value = { top: top, left: left }
  }
  
  currentCertificateDetails.value = certificate
  showCertificateDetailsModal.value = true
}

const closeCertificateDetails = () => {
  closeCertificateDetailsTimeout.value = setTimeout(() => {
    showCertificateDetailsModal.value = false
    currentCertificateDetails.value = null
  }, 150)
}

const cancelCloseCertificateDetails = () => {
  if (closeCertificateDetailsTimeout.value) {
    clearTimeout(closeCertificateDetailsTimeout.value)
    closeCertificateDetailsTimeout.value = null
  }
}

const deleteCertificate = async (certificateId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce certificat ?')) {
    return
  }
  
  try {
    console.log('🔄 Suppression du certificat:', certificateId)
    
    const response = await OrganizationApiService.deleteOrganizationCertificate(
      userOrganization.value.organization.id, 
      certificateId
    )
    
    if (response.success) {
      console.log('✅ Certificat supprimé')
      // Recharger la liste des certificats
      await loadOrganizationCertificates()
      showNotification('success', 'Succès', 'Certificat supprimé avec succès !')
    } else {
      throw new Error(response.message || 'Erreur lors de la suppression du certificat')
    }
  } catch (error) {
    console.error('❌ Erreur lors de la suppression du certificat:', error)
    showNotification('error', 'Erreur', 'Erreur lors de la suppression du certificat: ' + error.message)
  }
}

// Gestionnaire pour l'organisation sélectionnée
const handleOrganizationSelected = (event) => {
  const { organization, role } = event.detail
  console.log('🏢 Organisation sélectionnée dans OrganizationsPage:', organization.name, 'Rôle:', role)
  
  // Mettre à jour l'organisation sélectionnée
  selectedOrganization.value = organization
  
  // Mettre à jour userOrganization avec l'organisation sélectionnée
  userOrganization.value = {
    organization: organization,
    role: role
  }
  
  console.log('✅ Organisation mise à jour dans OrganizationsPage:', userOrganization.value)
  
  // Nettoyer le localStorage après utilisation
  localStorage.removeItem('selectedOrganization')
  
  // Recharger les données avec la nouvelle organisation
  fetchUserOrganization()
}

onMounted(() => {
  console.log('Organizations page loaded')
  
  // Écouter les événements de sélection d'organisation AVANT de charger les données
  window.addEventListener('organizationSelected', handleOrganizationSelected)
  
  // Attendre un peu pour que l'événement organizationSelected soit traité
  setTimeout(() => {
    // Récupérer l'organisation de l'utilisateur
    fetchUserOrganization()
  }, 100)
  
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

onUnmounted(() => {
  // Nettoyer les écouteurs d'événements
  window.removeEventListener('organizationSelected', handleOrganizationSelected)
})
</script>

<style scoped>
.organizations-page {
  padding: 0;
  background: #f8f9fa;
  min-height: 100vh;
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
  font-family: 'Raleway', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
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
  background: rgba(0, 0, 0, 0.3);
  z-index: 10000;
  backdrop-filter: blur(1px);
  -webkit-backdrop-filter: blur(1px);
  animation: fadeInOverlay 0.3s ease-out;
}

.organization-settings-modal {
  position: fixed;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  width: 800px;
  height: 500px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  display: flex;
  overflow: hidden;
  z-index: 10001;
  animation: modalSlideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center bottom;
  position: relative; /* Ajouté pour le positionnement de la notification */
}

.organization-settings-menu {
  width: 250px;
  background: rgba(255, 255, 255, 0.7);
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
  background: rgba(255, 255, 255, 0.6);
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

/* STYLES POUR LES ONGLETS DES MEMBRES */
.members-tabs {
  margin-top: 1rem;
}

.members-tab-nav {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.members-tab-btn {
  background: transparent;
  border: none;
  color: #2c3e50;
  padding: 0.75rem 1rem;
  border-radius: 8px 8px 0 0;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.members-tab-btn:hover {
  color: #1a252f;
  background: rgba(255, 255, 255, 0.1);
}

.members-tab-btn.active {
  color: var(--primary-blue);
  background: rgba(13, 110, 253, 0.1);
  border-bottom: 2px solid var(--primary-blue);
}

.tab-badge {
  background: rgba(44, 62, 80, 0.1);
  color: #2c3e50;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

.members-tab-btn.active .tab-badge {
  background: var(--primary-blue);
  color: white;
}

.members-tab-content {
  min-height: 200px;
}

.members-tab-pane {
  animation: fadeIn 0.3s ease;
}

.member-item.pending-member {
  border-color: rgba(255, 193, 7, 0.3);
  background: rgba(255, 193, 7, 0.05);
}

.member-item.pending-member:hover {
  border-color: rgba(255, 193, 7, 0.5);
  background: rgba(255, 193, 7, 0.1);
}

.member-avatar.pending {
  background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
  color: white;
}

.member-item.rejected-member {
  border-color: rgba(220, 53, 69, 0.3);
  background: rgba(220, 53, 69, 0.05);
}

.member-item.rejected-member:hover {
  border-color: rgba(220, 53, 69, 0.5);
  background: rgba(220, 53, 69, 0.1);
}

.member-avatar.rejected {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
}

.rejection-reason {
  background: rgba(220, 53, 69, 0.1);
  padding: 0.5rem;
  border-radius: 6px;
  border-left: 3px solid #dc3545;
}

.request-role {
  margin-top: 0.5rem;
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
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
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

/* Styles pour les invitations */
.invitations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.invitations-list {
  max-height: 400px;
  overflow-y: auto;
}

.invitation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  background: #fff;
}

.invitation-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.invitation-code {
  min-width: 200px;
}

.invitation-code h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'Courier New', monospace;
  color: #0066cc;
}

.invitation-code p {
  margin: 0;
  font-size: 0.875rem;
}

.invitation-details {
  flex: 1;
}

.invitation-status {
  margin-bottom: 0.5rem;
}

.invitation-meta {
  font-size: 0.75rem;
}

.invitation-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.invitation-buttons {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.invitation-buttons .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

/* Styles pour les certificats */
.certificates-list {
  max-height: 400px;
  overflow-y: auto;
}

.certificate-buttons {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.certificate-buttons .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
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
    font-weight: 800;
  }
  
  .sections-title {
    font-size: 2rem;
    font-weight: 800;
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

/* STYLES POUR LA MODALE D'IMPORT DE CERTIFICAT */
.certificate-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  z-index: 10001;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-out;
}

/* Ajustement pour centrer par rapport au contenu principal */
.organization-settings-content .certificate-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  z-index: 10001;
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

.close-btn {
  background: none;
  border: none;
  color: #6c757d;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.certificate-modal-body {
  padding: 1.5rem;
  max-height: 350px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
}

.certificate-upload-zone {
  margin-bottom: 1rem;
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
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
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

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.selected-file-container {
  margin-top: 1rem;
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.selected-file i {
  color: #28a745;
  font-size: 1.25rem;
}

.selected-file-name {
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

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
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
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .certificate-modal {
    width: calc(100% - 40px);
    max-width: calc(100% - 40px);
    max-height: calc(100% - 40px);
    margin: 20px;
  }
  
  .certificate-modal-body {
    padding: 1rem;
  }
  
  .drop-zone {
    padding: 1rem;
  }
}

/* BULLE DE DÉTAILS DU CERTIFICAT */
.certificate-details-tooltip {
  position: absolute;
  z-index: 10001; /* Au-dessus de la modale */
  max-width: 500px;
  max-height: 400px;
  animation: tooltipFadeIn 0.3s ease-out;
}

.certificate-details-tooltip .tooltip-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  max-width: 500px;
  width: 90vw;
  max-height: 400px;
  overflow: hidden;
}

.certificate-details-tooltip .tooltip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px 20px 0 0;
}

.certificate-details-tooltip .tooltip-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
  display: flex;
  align-items: center;
}

.certificate-details-tooltip .tooltip-close {
  background: none;
  border: none;
  color: var(--dark-gray);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.certificate-details-tooltip .tooltip-close:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
}

.certificate-details-tooltip .tooltip-body {
  padding: 1rem 1.5rem;
  max-height: 300px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 102, 204, 0.3) transparent;
}

.certificate-details-tooltip .tooltip-body::-webkit-scrollbar {
  width: 6px;
}

.certificate-details-tooltip .tooltip-body::-webkit-scrollbar-track {
  background: transparent;
}

.certificate-details-tooltip .tooltip-body::-webkit-scrollbar-thumb {
  background: rgba(0, 102, 204, 0.3);
  border-radius: 3px;
}

.certificate-details-tooltip .tooltip-body::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 102, 204, 0.5);
}

.certificate-info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-section {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem;
  transition: all 0.3s ease;
}

.info-section:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 
    0 4px 16px rgba(0, 102, 204, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.info-section-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary-blue);
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(0, 102, 204, 0.2);
  padding-bottom: 0.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: var(--dark-gray);
  min-width: 120px;
  font-size: 0.85rem;
}

.info-value {
  color: var(--text-dark);
  font-size: 0.85rem;
  word-break: break-word;
}

.info-value.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

/* Animation pour la bulle */
@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive pour la bulle de certificat */
@media (max-width: 768px) {
  .certificate-details-tooltip {
    max-width: 95vw;
    max-height: 80vh;
  }
  
  .certificate-details-tooltip .tooltip-content {
    max-width: 95vw;
    max-height: 80vh;
  }
  
  .certificate-details-tooltip .tooltip-header {
    padding: 0.75rem 1rem;
  }
  
  .certificate-details-tooltip .tooltip-body {
    padding: 0.75rem 1rem;
    max-height: 60vh;
  }
  
  .info-section {
    padding: 0.75rem;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .info-label {
    min-width: auto;
    font-size: 0.8rem;
  }
  
  .info-value {
    font-size: 0.8rem;
  }
}
</style>

