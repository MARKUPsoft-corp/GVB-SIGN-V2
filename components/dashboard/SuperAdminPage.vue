<template>
  <div class="documents-page super-admin-page">
    <div class="documents-header mb-4">
      <div class="header-container d-flex justify-content-between align-items-center">
        <div class="header-content">
          <h1 class="display-5 fw-bold text-dark mb-2">
            Super <span class="text-primary-blue">Administration</span>
          </h1>
          <p class="lead text-muted">
            Supervisez l'intégralité de la plateforme.
          </p>
        </div>
        <div class="header-actions">
          <div class="pulse-indicator bg-light text-primary-blue px-3 py-2 rounded-pill shadow-sm d-flex align-items-center border">
            <span class="spinner-grow spinner-grow-sm me-2 text-primary-blue" role="status" aria-hidden="true" style="width: 1rem; height: 1rem;"></span>
            Système en ligne
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation par onglets (Standard GVB Sign) -->
    <ul class="nav nav-pills custom-tabs mb-5 d-flex gap-2">
      <li class="nav-item">
        <button class="nav-link px-4 py-2" :class="{ active: activeSection === 'overview' }" @click="activeSection = 'overview'">
          <i class="bi bi-grid-1x2 me-2"></i> Vue d'ensemble
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link px-4 py-2" :class="{ active: activeSection === 'organizations' }" @click="activeSection = 'organizations'">
          <i class="bi bi-building me-2"></i> Organisations
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link px-4 py-2" :class="{ active: activeSection === 'users' }" @click="activeSection = 'users'">
          <i class="bi bi-people me-2"></i> Utilisateurs
        </button>
      </li>
      <li class="nav-item">
        <button class="nav-link px-4 py-2" :class="{ active: activeSection === 'signatures' }" @click="activeSection = 'signatures'">
          <i class="bi bi-journal-text me-2"></i> Registre
        </button>
      </li>
    </ul>

    <!-- Contenu principal -->
    <div class="admin-main-content">
      
      <!-- Chargement global -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary-blue" role="status">
          <span class="visually-hidden">Chargement...</span>
        </div>
        <p class="mt-3 text-muted">Synchronisation du système...</p>
      </div>

      <div v-else class="fade-in-up">
        
        <!-- ==================== VUE D'ENSEMBLE ==================== -->
        <div v-if="activeSection === 'overview'" class="section-content">
          <div class="row g-4 mb-5">
            <div class="col-md-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-people"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ users.length }}</h4>
                  <p class="stat-label">Utilisateurs inscrits</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-building"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ organizations.length }}</h4>
                  <p class="stat-label">Organisations créées</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-pen"></i>
                </div>
                <div class="stat-content">
                  <h4 class="stat-number">{{ signatures.length }}</h4>
                  <p class="stat-label">Signatures générées</p>
                </div>
              </div>
            </div>
          </div>
        </div>

          <!-- ==================== ORGANISATIONS ==================== -->
          <div v-if="activeSection === 'organizations'" class="section-content">
            
            <ul class="nav nav-pills custom-tabs mb-5 d-flex gap-2">
              <li class="nav-item">
                <button class="nav-link px-4 py-2" :class="{ active: currentOrgTab === 'pending' }" @click="currentOrgTab = 'pending'">
                  <i class="bi bi-hourglass-split me-2"></i> En attente
                  <span class="badge ms-2" :class="currentOrgTab === 'pending' ? 'bg-white text-primary' : 'bg-warning text-dark'">{{ pendingOrgs.length }}</span>
                </button>
              </li>
              <li class="nav-item">
                <button class="nav-link px-4 py-2" :class="{ active: currentOrgTab === 'approved' }" @click="currentOrgTab = 'approved'">
                  <i class="bi bi-check-circle-fill me-2"></i> Approuvées
                  <span class="badge ms-2" :class="currentOrgTab === 'approved' ? 'bg-white text-primary' : 'bg-success text-white'">{{ approvedOrgs.length }}</span>
                </button>
              </li>
              <li class="nav-item">
                <button class="nav-link px-4 py-2" :class="{ active: currentOrgTab === 'rejected' }" @click="currentOrgTab = 'rejected'">
                  <i class="bi bi-x-circle-fill me-2"></i> Rejetées
                  <span class="badge ms-2" :class="currentOrgTab === 'rejected' ? 'bg-white text-primary' : 'bg-danger text-white'">{{ rejectedOrgs.length }}</span>
                </button>
              </li>
            </ul>

            <div class="row g-4">
              <div v-if="displayedOrgs.length === 0" class="col-12 text-center py-5">
                <div class="empty-state">
                  <i class="bi bi-building-dash display-1 text-muted mb-3 d-block"></i>
                  <h4>Aucune organisation</h4>
                  <p class="text-muted">La liste est vide pour cette catégorie.</p>
                </div>
              </div>

              <div v-for="org in displayedOrgs" :key="org.id" class="col-lg-6 mb-4">
                <div class="organization-card">
                  <div class="card-header">
                    <div class="organization-icon">
                      <i class="bi bi-building"></i>
                    </div>
                    <div class="organization-header-content">
                      <h3 class="organization-name">{{ org.name }}</h3>
                      <p class="organization-subtitle">{{ org.organization_type || 'Organisation' }}</p>
                    </div>
                    <div class="organization-status-badges">
                      <div class="approval-status-badge" :class="org.approval_status">
                        <span>{{ getStatusText(org.approval_status) }}</span>
                      </div>
                      <div class="organization-status" :class="org.approval_status === 'approved' ? 'active' : (org.approval_status === 'rejected' ? 'rejected' : 'pending')">
                        <i class="bi bi-circle-fill"></i>
                      </div>
                    </div>
                  </div>

                  <div class="card-content">
                    <p class="organization-description">{{ org.description || 'Aucune description renseignée' }}</p>
                    
                    <div class="organization-meta">
                      <div class="meta-item">
                        <i class="bi bi-envelope"></i>
                        <span>{{ org.email || 'Non renseigné' }}</span>
                      </div>
                      <div class="meta-item">
                        <i class="bi bi-telephone"></i>
                        <span>{{ org.phone || 'Non renseigné' }}</span>
                      </div>
                      <div class="meta-item">
                        <i class="bi bi-geo-alt"></i>
                        <span>{{ org.address || 'Non renseignée' }}</span>
                      </div>
                      <div class="meta-item">
                        <i class="bi bi-globe"></i>
                        <span>{{ org.website || 'Non renseigné' }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="card-footer" v-if="org.approval_status === 'pending'">
                    <div class="organization-actions w-100 d-flex gap-2">
                      <button class="btn btn-outline-danger flex-grow-1" @click="handleRejectOrg(org.id)">
                        <i class="bi bi-x-circle me-2"></i> Rejeter
                      </button>
                      <button class="btn btn-primary-blue flex-grow-1" style="background: linear-gradient(135deg, #0066cc 0%, #0056b3 100%); color: white; border: none;" @click="handleApproveOrg(org.id)">
                        <i class="bi bi-check-circle me-2"></i> Valider
                      </button>
                    </div>
                  </div>
                  <div class="card-footer" v-else-if="org.approval_status === 'approved'">
                    <div class="organization-actions w-100 d-flex justify-content-end gap-2">
                      <button class="btn btn-outline-secondary btn-sm" @click="handleRevokeOrg(org.id)">
                        <i class="bi bi-shield-lock me-2"></i> Révoquer l'accès
                      </button>
                    </div>
                  </div>
                  <div class="card-footer" v-else-if="org.approval_status === 'rejected'">
                    <div class="organization-actions w-100 d-flex gap-2">
                      <button class="btn btn-outline-success flex-grow-1" @click="handleRehabilitateOrg(org.id)">
                        <i class="bi bi-arrow-counterclockwise me-2"></i> Réhabiliter
                      </button>
                      <button class="btn btn-outline-danger flex-grow-1" @click="handleRejectOrg(org.id, true)">
                        <i class="bi bi-trash me-2"></i> Supprimer définitivement
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ==================== UTILISATEURS ==================== -->
          <div v-if="activeSection === 'users'" class="section-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div class="search-box position-relative" style="max-width: 400px; width: 100%;">
                <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                <input type="text" class="form-control border-0 shadow-sm ps-5 py-2 rounded-pill" placeholder="Rechercher (nom, email)..." v-model="userSearchQuery">
              </div>
            </div>
            
            <div class="documents-section-card p-0 overflow-hidden border-0 shadow-sm">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0 custom-table">
                  <thead>
                    <tr>
                      <th class="ps-4 py-3">Utilisateur</th>
                      <th class="py-3">Email</th>
                      <th class="py-3">Inscription</th>
                      <th class="py-3">Rôle actuel</th>
                      <th class="text-end pe-4 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="filteredUsers.length === 0">
                      <td colspan="5" class="text-center py-4 text-muted">Aucun utilisateur trouvé.</td>
                    </tr>
                    <tr v-for="user in filteredUsers" :key="user.id">
                      <td>
                        <div class="d-flex align-items-center gap-2">
                          <img v-if="user.photoURL" :src="user.photoURL" class="rounded-circle" width="32" height="32" alt="Avatar">
                          <div v-else class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width: 32px; height: 32px;">
                            <i class="bi bi-person"></i>
                          </div>
                          <span class="fw-semibold">{{ user.displayName || 'Anonyme' }}</span>
                        </div>
                      </td>
                      <td>{{ user.email }}</td>
                      <td class="text-muted small">{{ formatDate(user.createdAt?.toDate ? user.createdAt.toDate() : user.createdAt) }}</td>
                      <td>
                        <span class="badge" :class="getRoleBadgeClass(user.role)">
                          {{ getRoleText(user.role) }}
                        </span>
                      </td>
                      <td class="text-end">
                        <select class="form-select form-select-sm d-inline-block w-auto" 
                                @change="handleRoleChange(user.id, $event.target.value)" 
                                :value="user.role || 'member'">
                          <option value="member">Membre (Défaut)</option>
                          <option value="chief">Chef d'Organisation</option>
                          <option value="super-admin">Super Admin</option>
                        </select>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- ==================== SIGNATURES ==================== -->
          <div v-if="activeSection === 'signatures'" class="section-content">
            
            <div class="documents-section-card p-0 overflow-hidden border-0 shadow-sm">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0 custom-table">
                  <thead>
                    <tr>
                      <th class="ps-4 py-3">ID Document</th>
                      <th class="py-3">Signataire (UID)</th>
                      <th class="py-3">Type</th>
                      <th class="py-3">Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="signatures.length === 0">
                      <td colspan="4" class="text-center py-4 text-muted">Aucune signature enregistrée.</td>
                    </tr>
                    <tr v-for="sig in signatures" :key="sig.id">
                      <td><code class="text-primary-blue">{{ sig.id.substring(0,8) }}...</code></td>
                      <td>
                        <span class="text-muted small">{{ sig.userId || 'Inconnu' }}</span>
                      </td>
                      <td>
                        <span class="badge bg-light text-dark border">Signature PDF</span>
                      </td>
                      <td class="text-muted small">{{ formatDate(sig.createdAt?.toDate ? sig.createdAt.toDate() : sig.createdAt) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import OrganizationApiService from '../../services/OrganizationApiService'
import AdminApiService from '../../services/AdminApiService'

const loading = ref(true)
const activeSection = ref('overview')

// Données en temps réel
const organizations = ref([])
const users = ref([])
const signatures = ref([])

// Onglet organisation
const currentOrgTab = ref('pending')
const userSearchQuery = ref('')

let unsubOrgs = null
let unsubUsers = null
let unsubSigs = null

onMounted(() => {
  loading.value = true
  
  // 1. Écouter les organisations
  unsubOrgs = OrganizationApiService.listenAllOrganizations((orgs) => {
    organizations.value = orgs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    checkLoading()
  })

  // 2. Écouter les utilisateurs
  unsubUsers = AdminApiService.listenAllUsers((usr) => {
    users.value = usr
    checkLoading()
  })

  // 3. Écouter les signatures
  unsubSigs = AdminApiService.listenAllSignatures((sigs) => {
    signatures.value = sigs.sort((a, b) => {
      const dateA = a.createdAt?.toDate ? a.createdAt.toDate() : new Date(a.createdAt || 0)
      const dateB = b.createdAt?.toDate ? b.createdAt.toDate() : new Date(b.createdAt || 0)
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
  // Simple check pour enlever le loader dès qu'une des listes est chargée (ou après un court délai)
  setTimeout(() => { loading.value = false }, 500)
}

// ==================== COMPUTED PROPERTIES ====================

// Organisations
const pendingOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'pending' || !o.approval_status))
const approvedOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'approved'))
const rejectedOrgs = computed(() => organizations.value.filter(o => o.approval_status === 'rejected'))

const displayedOrgs = computed(() => {
  switch (currentOrgTab.value) {
    case 'pending': return pendingOrgs.value
    case 'approved': return approvedOrgs.value
    case 'rejected': return rejectedOrgs.value
    default: return []
  }
})

// Utilisateurs
const filteredUsers = computed(() => {
  if (!userSearchQuery.value) return users.value
  const query = userSearchQuery.value.toLowerCase()
  return users.value.filter(u => 
    (u.displayName && u.displayName.toLowerCase().includes(query)) || 
    (u.email && u.email.toLowerCase().includes(query))
  )
})

// ==================== ACTIONS ====================

const handleApproveOrg = async (id) => {
  try {
    await OrganizationApiService.validateOrganization(id)
  } catch (error) {
    alert('Erreur lors de la validation')
  }
}

const handleRejectOrg = async (id, permanent = false) => {
  const message = permanent 
    ? 'Supprimer définitivement cette organisation ? Cette action est irréversible.' 
    : 'Rejeter cette organisation ?'
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
      alert('Erreur')
    }
  }
}

const handleRevokeOrg = async (id) => {
  if (confirm('Mettre cette organisation en attente de validation ?')) {
    try {
      const { db } = OrganizationApiService.getFirebase()
      const { doc, updateDoc } = await import('firebase/firestore')
      await updateDoc(doc(db, 'organizations', id), { approval_status: 'pending' })
    } catch (error) {
      alert('Erreur')
    }
  }
}

const handleRehabilitateOrg = async (id) => {
  if (confirm('Réhabiliter cette organisation ? Elle sera réapprouvée et ses membres pourront de nouveau y accéder.')) {
    try {
      const { db } = OrganizationApiService.getFirebase()
      const { doc, updateDoc } = await import('firebase/firestore')
      await updateDoc(doc(db, 'organizations', id), { 
        approval_status: 'approved',
        rehabilitated_at: new Date().toISOString()
      })
    } catch (error) {
      alert('Erreur lors de la réhabilitation')
    }
  }
}

const handleRoleChange = async (userId, newRole) => {
  if (confirm(`Voulez-vous vraiment changer le rôle de cet utilisateur vers "${newRole}" ?`)) {
    try {
      await AdminApiService.updateUserRole(userId, newRole)
    } catch (error) {
      alert('Erreur lors du changement de rôle')
    }
  }
}

// ==================== UTILITAIRES ====================

const formatDate = (dateString) => {
  if (!dateString) return 'Inconnue'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return 'Invalide'
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }).format(date)
}

const getStatusBadgeClass = (status) => {
  if (status === 'approved') return 'bg-success text-white'
  if (status === 'rejected') return 'bg-danger text-white'
  return 'bg-warning text-dark'
}

const getStatusText = (status) => {
  if (status === 'approved') return 'Approuvée'
  if (status === 'rejected') return 'Rejetée'
  return 'En attente'
}

const getRoleBadgeClass = (role) => {
  if (role === 'super-admin') return 'bg-primary-blue text-white'
  if (role === 'chief') return 'bg-light text-primary-blue border border-primary'
  return 'bg-light text-secondary border'
}

const getRoleText = (role) => {
  if (role === 'super-admin') return 'Super Admin'
  if (role === 'chief') return 'Chef Org'
  return 'Membre'
}
</script>

<style scoped>
.documents-page {
  padding: 0;
}

.documents-header {
  opacity: 0;
  animation: slideInRight 0.8s ease-out forwards;
}

/* ==================== STYLES DES CARTES ORGANISATION ==================== */
.organization-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 
    0 8px 25px rgba(0, 102, 204, 0.08),
    0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  height: 100%;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
}

.organization-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 102, 204, 0.12),
    0 10px 25px rgba(0, 102, 204, 0.08);
  border-color: rgba(0, 102, 204, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 102, 204, 0.08);
  background: transparent;
}

.organization-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.organization-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 123, 255, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--primary-blue);
  flex-shrink: 0;
}

.organization-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.organization-subtitle {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
  font-weight: 400;
}

.organization-status-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.approval-status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.approval-status-badge.approved {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.approval-status-badge.pending {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.approval-status-badge.rejected {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.organization-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.organization-status.active { color: #28a745; }
.organization-status.pending { color: #ffc107; }
.organization-status.rejected { color: #dc3545; }

.card-content {
  flex-grow: 1;
  margin-bottom: 1.5rem;
}

.organization-description {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.organization-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #6c757d;
}

.meta-item i {
  color: var(--primary-blue);
  font-size: 0.9rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 102, 204, 0.1);
  background: transparent;
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
}

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

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
  font-family: 'Raleway', sans-serif;
}

.stat-label {
  color: #6c757d;
  font-size: 0.95rem;
  margin-bottom: 0;
  font-weight: 500;
}

/* Style Glassmorphism */
.documents-section-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 18px;
  border: 2px solid rgba(0, 102, 204, 0.08);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.documents-section-card:hover {
  box-shadow: 0 20px 40px rgba(0, 102, 204, 0.12);
}

/* Boutons et Onglets */
.custom-tabs {
  border-bottom: 2px solid rgba(0, 102, 204, 0.05);
  padding-bottom: 0.75rem;
}
.custom-tabs .nav-link {
  color: var(--text-muted);
  font-weight: 600;
  border: none;
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 50rem; /* rounded-pill */
}
.custom-tabs .nav-link:hover {
  background: rgba(0, 102, 204, 0.03);
  color: var(--primary-blue);
}
.custom-tabs .nav-link.active {
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.08);
  box-shadow: 0 2px 10px rgba(0, 102, 204, 0.05);
}

.btn-primary-blue {
  background: linear-gradient(135deg, var(--primary-blue) 0%, #007bff 100%);
  border: none;
  color: white;
}
.btn-primary-blue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
}

/* Search input */
.search-box .form-control:focus {
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.1) !important;
  border-color: rgba(0, 102, 204, 0.2);
}

/* Tables */
.custom-table thead {
  background: rgba(0, 102, 204, 0.02);
}
.custom-table th {
  font-weight: 600;
  color: var(--text-muted);
  border-bottom: 2px solid rgba(0, 102, 204, 0.05);
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}
.custom-table td {
  padding: 1.25rem 0.5rem;
  border-bottom: 1px solid rgba(0, 102, 204, 0.05);
}
.custom-table tbody tr:hover {
  background-color: rgba(0, 102, 204, 0.02);
}

/* Animations */
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
}
</style>
