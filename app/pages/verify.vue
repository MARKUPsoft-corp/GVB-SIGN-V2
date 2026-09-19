<template>
  <div class="verify-page py-5">
    <div class="container">
      <!-- En-tête -->
      <div class="text-center mb-5">
        <div class="badge-brand mb-2">
          <i class="bi bi-shield-check me-1"></i> GVB Sign Verification
        </div>
        <h1 class="page-title fw-bold">
          {{ isFrench ? 'Vérification d\'Authenticité de Document' : 'Document Authenticity Verification' }}
        </h1>
        <p class="page-subtitle text-muted mx-auto" style="max-width: 600px;">
          {{ isFrench 
            ? 'Vérifiez la validité, l\'intégrité cryptographique et l\'historique de signature de tout document certifié par GVB Sign.' 
            : 'Verify the validity, cryptographic integrity, and signature history of any GVB Sign certified document.' 
          }}
        </p>
      </div>

      <!-- Barre de recherche manuelle si aucun ID ou pour chercher un autre document -->
      <div class="search-card card shadow-sm border-0 mb-5 mx-auto" style="max-width: 700px;">
        <div class="card-body p-4">
          <form @submit.prevent="handleSearch" class="d-flex flex-column flex-sm-row gap-2">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0">
                <i class="bi bi-qr-code-scan text-primary"></i>
              </span>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control border-start-0"
                :placeholder="isFrench ? 'Collez un ID de document ou une URL...' : 'Paste document ID or URL...'"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary px-4 fw-semibold d-flex align-items-center justify-content-center" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-search me-2"></i>
              {{ isFrench ? 'Vérifier' : 'Verify' }}
            </button>
          </form>
        </div>
      </div>

      <!-- État de chargement -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-grow text-primary" role="status" style="width: 3rem; height: 3rem;"></div>
        <p class="mt-3 text-muted fw-medium">
          {{ isFrench ? 'Vérification cryptographique en cours...' : 'Cryptographic verification in progress...' }}
        </p>
      </div>

      <!-- Résultat de vérification : Succès -->
      <div v-else-if="verificationData && verificationData.success" class="result-container mx-auto" style="max-width: 850px;">
        <!-- Carte de statut principal -->
        <div class="card status-card border-0 shadow-lg text-white mb-4" :class="isValid ? 'bg-success-gradient' : 'bg-danger-gradient'">
          <div class="card-body p-4 p-md-5 text-center">
            <div class="status-icon-wrapper mb-3">
              <i class="bi" :class="isValid ? 'bi-patch-check-fill' : 'bi-exclamation-triangle-fill'"></i>
            </div>
            <h2 class="status-title fw-bold mb-2">
              {{ isValid 
                ? (isFrench ? 'Document Authentique & Conforme' : 'Authentic & Compliant Document') 
                : (isFrench ? 'Document Non Certifié' : 'Uncertified Document') 
              }}
            </h2>
            <p class="status-desc mb-3">
              {{ verificationData.verification?.message || (isFrench ? 'Le document est authentique et n\'a subi aucune modification.' : 'The document is authentic and unmodified.') }}
            </p>
            <div class="d-inline-flex align-items-center gap-2 px-3 py-1 bg-white bg-opacity-25 rounded-pill text-white fw-medium small">
              <i class="bi bi-person-check"></i>
              <span>{{ isFrench ? 'Signé par' : 'Signed by' }} : <strong>{{ verificationData.document_info?.signer_name }}</strong></span>
            </div>
          </div>
        </div>

        <!-- Détails du document et de la signature -->
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4">
          <div class="card-header bg-white border-bottom p-4">
            <h5 class="fw-bold mb-0 text-dark d-flex align-items-center">
              <i class="bi bi-file-earmark-text text-primary me-2"></i>
              {{ isFrench ? 'Informations du Document' : 'Document Information' }}
            </h5>
          </div>
          <div class="card-body p-4">
            <div class="row g-3">
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Nom du fichier' : 'Filename' }}</span>
                <span class="fw-semibold text-dark">{{ verificationData.document_info?.filename }}</span>
              </div>
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Identifiant Unique' : 'Document ID' }}</span>
                <code class="text-primary small">{{ verificationData.document_info?.document_id }}</code>
              </div>
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Signataire' : 'Signer' }}</span>
                <span class="fw-semibold text-dark">{{ verificationData.document_info?.signer_name }}</span>
                <span v-if="verificationData.document_info?.signer_email" class="text-muted small d-block">
                  ({{ verificationData.document_info?.signer_email }})
                </span>
              </div>
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Date et heure de signature' : 'Signature Date & Time' }}</span>
                <span class="fw-semibold text-dark">{{ formatDate(verificationData.document_info?.signature_timestamp) }}</span>
              </div>
              <div class="col-sm-6" v-if="verificationData.organization_info?.name">
                <span class="text-muted small d-block">{{ isFrench ? 'Organisation' : 'Organization' }}</span>
                <span class="badge bg-primary-subtle text-primary fw-medium px-3 py-2">
                  <i class="bi bi-building me-1"></i> {{ verificationData.organization_info?.name }}
                </span>
              </div>
              <div class="col-sm-6" v-if="verificationData.document_info?.file_size_signed">
                <span class="text-muted small d-block">{{ isFrench ? 'Taille du document signé' : 'Signed File Size' }}</span>
                <span class="text-dark">{{ formatBytes(verificationData.document_info?.file_size_signed) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Détails Cryptographiques -->
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4">
          <div class="card-header bg-white border-bottom p-4">
            <h5 class="fw-bold mb-0 text-dark d-flex align-items-center">
              <i class="bi bi-shield-lock text-primary me-2"></i>
              {{ isFrench ? 'Preuve Cryptographique' : 'Cryptographic Proof' }}
            </h5>
          </div>
          <div class="card-body p-4">
            <div class="mb-3">
              <span class="text-muted small d-block mb-1">{{ isFrench ? 'Empreinte Numérique du Document (SHA-256)' : 'Document Hash (SHA-256)' }}</span>
              <div class="p-3 bg-light rounded-3 font-monospace small text-break border">
                {{ verificationData.verification?.document_hash || 'N/A' }}
              </div>
            </div>
            <div class="row g-3">
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Méthode de vérification' : 'Verification Method' }}</span>
                <span class="fw-semibold">{{ verificationData.verification?.verification_method || 'RSA-SHA256' }}</span>
              </div>
              <div class="col-sm-6">
                <span class="text-muted small d-block">{{ isFrench ? 'Algorithme de signature' : 'Signature Algorithm' }}</span>
                <span class="fw-semibold">{{ verificationData.verification?.signature_algorithm || 'RSA (2048-bit)' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions de téléchargement -->
        <div v-if="verificationData.document_urls?.signed_document_url" class="card border-0 shadow-sm rounded-4 p-4 text-center bg-light">
          <h6 class="fw-bold mb-2">{{ isFrench ? 'Consulter le Document Signé' : 'View Signed Document' }}</h6>
          <p class="text-muted small mb-3">
            {{ isFrench 
              ? 'Vous pouvez télécharger et consulter le document original certifié avec ses signatures apposées.' 
              : 'You can download and view the certified document with its embedded signatures.' 
            }}
          </p>
          <div class="d-flex justify-content-center gap-3">
            <a
              :href="verificationData.document_urls.signed_document_url"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary px-4 py-2 fw-semibold rounded-pill d-inline-flex align-items-center"
            >
              <i class="bi bi-download me-2"></i>
              {{ isFrench ? 'Télécharger le Document Certifié (PDF)' : 'Download Certified Document (PDF)' }}
            </a>
          </div>
        </div>
      </div>

      <!-- Erreur : Document non trouvé -->
      <div v-else-if="errorMessage" class="error-container mx-auto" style="max-width: 650px;">
        <div class="card border-0 shadow-sm rounded-4 text-center p-5">
          <div class="text-danger mb-3">
            <i class="bi bi-x-circle-fill" style="font-size: 3.5rem;"></i>
          </div>
          <h3 class="fw-bold text-dark mb-2">
            {{ isFrench ? 'Document Introuvable' : 'Document Not Found' }}
          </h3>
          <p class="text-muted mb-4">
            {{ errorMessage }}
          </p>
          <div class="p-3 bg-light rounded-3 text-start small text-muted mb-4">
            <strong>{{ isFrench ? 'Conseils :' : 'Tips:' }}</strong>
            <ul class="mb-0 mt-1 ps-3">
              <li>{{ isFrench ? 'Assurez-vous que l\'ID scanné correspond exactement à un document signé sur GVB Sign.' : 'Ensure the scanned ID matches a document signed on GVB Sign.' }}</li>
              <li>{{ isFrench ? 'Si la signature vient d\'être effectuée, patientez quelques secondes et réessayez.' : 'If just signed, wait a few moments and try again.' }}</li>
            </ul>
          </div>
          <button @click="resetSearch" class="btn btn-outline-secondary px-4 rounded-pill">
            <i class="bi bi-arrow-counterclockwise me-1"></i> {{ isFrench ? 'Nouvelle recherche' : 'New search' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from '../../composables/useI18n'

definePageMeta({
  layout: 'default'
})

const route = useRoute()
const { isFrench } = useI18n()

const searchQuery = ref('')
const loading = ref(false)
const verificationData = ref(null)
const errorMessage = ref(null)

const isValid = computed(() => verificationData.value?.verification?.valid === true)

// Formater la date
function formatDate(dateStr) {
  if (!dateStr) return 'N/A'
  try {
    const d = new Date(dateStr)
    return d.toLocaleString(isFrench.value ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (_) {
    return dateStr
  }
}

// Formater la taille en octets
function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Extraire l'ID du document à partir d'une URL ou d'une chaîne
function extractDocumentId(input) {
  if (!input) return null
  const text = input.trim()

  if (text.startsWith('http://') || text.startsWith('https://')) {
    try {
      const url = new URL(text)
      if (url.searchParams.has('id')) return url.searchParams.get('id')
      if (url.searchParams.has('document_id')) return url.searchParams.get('document_id')
      const segments = url.pathname.split('/').filter(Boolean)
      if (segments.length > 0) return segments[segments.length - 1]
    } catch (_) {}
  }

  const uuidMatch = text.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/)
  if (uuidMatch) return uuidMatch[0]

  return text
}

// Lancer la vérification
async function verifyDocument(rawId) {
  const documentId = extractDocumentId(rawId)
  if (!documentId) return

  loading.value = true
  errorMessage.value = null
  verificationData.value = null

  try {
    const response = await $fetch(`/api/signatures/verify-signature/${encodeURIComponent(documentId)}`)
    if (response && response.success) {
      verificationData.value = response
    } else {
      errorMessage.value = response?.error || (isFrench.value ? 'Document non trouvé sur GVB Sign.' : 'Document not found on GVB Sign.')
    }
  } catch (err) {
    if (err.statusCode === 404) {
      errorMessage.value = isFrench.value 
        ? `Le document avec l'identifiant "${documentId}" n'a pas été trouvé. Il n'a peut-être pas encore été signé ou le QR code est invalide.`
        : `Document with ID "${documentId}" was not found. It may not have been signed yet or the QR code is invalid.`
    } else {
      errorMessage.value = isFrench.value 
        ? `Erreur lors de la vérification : ${err.data?.error || err.message}`
        : `Verification error: ${err.data?.error || err.message}`
    }
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    verifyDocument(searchQuery.value)
  }
}

function resetSearch() {
  searchQuery.value = ''
  errorMessage.value = null
  verificationData.value = null
}

onMounted(() => {
  const queryId = route.query.id || route.query.document_id
  if (queryId) {
    searchQuery.value = String(queryId)
    verifyDocument(String(queryId))
  }
})

useHead(() => ({
  title: isFrench.value ? 'Vérification de Signature - GVB Sign' : 'Signature Verification - GVB Sign',
  meta: [
    {
      name: 'description',
      content: isFrench.value 
        ? 'Vérifiez en direct l\'authenticité et la validité des documents signés électroniquement avec GVB Sign.'
        : 'Verify the authenticity and validity of digitally signed documents with GVB Sign.'
    }
  ]
}))
</script>

<style scoped>
.verify-page {
  min-height: 80vh;
  background-color: #f8fafc;
}

.badge-brand {
  display: inline-block;
  padding: 6px 16px;
  background-color: rgba(0, 102, 204, 0.1);
  color: #0066cc;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
}

.page-title {
  color: #1e293b;
  font-size: 2.2rem;
}

.bg-success-gradient {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.bg-danger-gradient {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.status-icon-wrapper {
  font-size: 3.5rem;
  line-height: 1;
}

.status-title {
  font-size: 1.8rem;
}

.status-desc {
  font-size: 1.1rem;
  opacity: 0.95;
}

.font-monospace {
  font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
</style>
