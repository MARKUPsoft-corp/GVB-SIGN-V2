<template>
  <div class="sign-base-container">

    <!-- Section d'upload de signature -->
    <div class="signature-upload-section">
      
      <div v-if="!signatureImage" class="upload-dropzone">
        <input 
          type="file" 
          id="signature-upload" 
          accept="image/png,image/jpeg,image/jpg,image/gif,image/bmp,image/webp,image/svg+xml" 
          @change="handleSignatureUpload" 
          class="file-input"
        >
        <label for="signature-upload" class="upload-label">
          <div class="upload-icon">
            <i class="bi bi-pen-fill"></i>
          </div>
          <div class="upload-text">
            <h3>Déposez votre signature manuscrite ici</h3>
            <p>ou <span class="link">cliquez pour sélectionner</span></p>
            <small>Formats acceptés: PNG, JPEG, GIF, BMP, WEBP, SVG • Taille max: 10MB</small>
          </div>
        </label>
      </div>
      
      <div v-else class="signature-preview-section">
        <div class="signature-preview-container">
          <img :src="signatureImageUrl" alt="Signature" class="signature-preview-img">
          <div class="signature-controls-section">
            <div class="size-slider">
              <label for="signature-size">Taille: {{ signatureSize }}% de la page</label>
              <input 
                type="range" 
                id="signature-size" 
                v-model="signatureSize" 
                min="10" 
                max="100" 
                step="5"
                @input="updateSignatureSize"
              >
            </div>
            <button @click="removeSignature" class="remove-signature-btn">
              <i class="bi bi-trash3"></i> Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content-grid">
      <!-- Colonne de gauche : Aperçu du document -->
      <div class="document-preview-area">
        <div class="preview-header-section">
          <h5>Aperçu du document</h5>
          <div class="page-navigation">
            <button @click="previousPage" :disabled="currentPage === 1" class="nav-btn">
              <i class="bi bi-chevron-left"></i>
            </button>
            <span class="page-indicator">Page {{ currentPage }} / {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages" class="nav-btn">
              <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>

        <!-- Zone d'aperçu A4 -->
        <div class="document-container" ref="previewContainer">
          <div class="document-page" 
               @mousedown="handleDragStart"
               @touchstart="handleTouchStart">
            
            <!-- Affichage du PDF avec vue-pdf-embed -->
            <div class="pdf-content">
              <component
                :is="VuePdfEmbedComponent"
                v-if="pdfSource"
                :source="pdfSource"
                :page="currentPage"
                :width="595"
                :height="842"
                @loaded="onPdfLoaded"
                @loading-failed="onPdfLoadError"
                @rendered="onPdfRendered"
                class="pdf-viewer"
              />
              <div v-else class="pdf-loading-state">
                <i class="bi bi-file-earmark-pdf-fill"></i>
                <p>Chargement du document...</p>
              </div>
            </div>

            <!-- QR Code draggable -->
            <div 
              v-if="showQrOnCurrentPage && pdfLoaded"
              class="qr-element"
              :style="qrStyle"
              :class="{ 'dragging': isDraggingQr }"
              @mousedown.stop="startDragQr"
              @touchstart.stop="startDragQr"
            >
              <div class="qr-content">
                <div class="qr-code" :class="selectedQrSize">
                  <div class="qr-pattern"></div>
                </div>
                <div class="qr-label">GVB</div>
              </div>
            </div>
            
            <!-- Signature draggable -->
            <div 
              v-if="signatureImage && pdfLoaded"
              class="signature-element"
              :style="signatureStyle"
              :class="{ 'dragging': isDraggingSignature }"
              @mousedown.stop="startDragSignature($event)"
              @touchstart.stop="startDragSignature($event)"
            >
              <img :src="signatureImageUrl" alt="Signature" class="signature-img">
            </div>
          </div>
        </div>

        <!-- Indicateurs de position -->
        <div class="position-feedback" v-if="showPositionInfo">
          <span v-if="isDraggingQr">
            Position QR : X: {{ Math.round(getCurrentPagePosition().x) }}% | Y: {{ Math.round(getCurrentPagePosition().y) }}%
          </span>
          <span v-if="isDraggingSignature">
            Position Signature : X: {{ Math.round(getCurrentPageSignaturePosition().x) }}% | Y: {{ Math.round(getCurrentPageSignaturePosition().y) }}%
          </span>
        </div>
      </div>

      <!-- Colonne de droite : Contrôles -->
      <div class="controls-panel">
        <!-- Aperçu de toutes les pages -->
        <div class="pages-overview" v-if="totalPages > 1">
          <h5>Pages du document ({{ totalPages }} pages)</h5>
          <div class="pages-grid">
            <div 
              v-for="page in Math.min(totalPages, 20)" 
              :key="page"
              :class="['page-thumb', { active: currentPage === page }]"
              @click="goToPage(page)"
            >
              <div class="page-thumb-wrapper">
                <component
                  :is="VuePdfEmbedComponent"
                  v-if="pdfSource"
                  :source="pdfSource"
                  :page="page"
                  :width="80"
                  :height="113"
                  class="page-thumb-pdf"
                />
                <div v-else class="page-thumb-placeholder">
                  <i class="bi bi-file-earmark"></i>
                  <span>{{ page }}</span>
                </div>
              </div>
              <span class="page-label">Page {{ page }}</span>
            </div>
            <div v-if="totalPages > 20" class="more-pages-indicator">
              <i class="bi bi-three-dots"></i>
              <span>{{ totalPages - 20 }} pages supplémentaires</span>
            </div>
          </div>
        </div>

        <!-- Sélection des pages -->
        <div class="pages-selection-section">
          <h5>Pages...</h5>
          <div class="application-options">
            <label class="option-item">
              <input type="radio" v-model="pageApplication" value="all" />
              <span>Toutes</span>
            </label>
            <label class="option-item">
              <input type="radio" v-model="pageApplication" value="current" />
              <span>Actuelle</span>
            </label>
            <label class="option-item">
              <input type="radio" v-model="pageApplication" value="custom" />
              <span>Personnalisée</span>
            </label>
            <label class="option-item">
              <input type="radio" v-model="pageApplication" value="individual" />
              <span>Individuelle</span>
            </label>
          </div>

          <!-- Sélection personnalisée des pages -->
          <div v-if="pageApplication === 'custom'" class="custom-selection">
            <p class="selection-hint">Sélectionnez les pages :</p>
            <div class="pages-checkboxes">
              <label v-for="page in totalPages" :key="page" class="page-check">
                <input 
                  type="checkbox" 
                  :value="page" 
                  v-model="selectedPages"
                />
                <span>{{ page }}</span>
              </label>
            </div>
          </div>

          <!-- Pages avec positions individuelles -->
          <div v-if="pageApplication === 'individual'" class="individual-selection">
            <div class="individual-pages-list">
              <div 
                v-for="page in totalPages" 
                :key="page" 
                class="individual-page"
                :class="{ 
                  'has-elements': hasIndividualPosition(page), 
                  'current': currentPage === page,
                  'ready-to-position': currentPage === page && !hasIndividualPosition(page)
                }"
                @click="goToPage(page)"
              >
                <span class="page-number">Page {{ page }}</span>
                <span v-if="hasIndividualPosition(page)" class="status-indicator">
                  <i class="bi bi-check-circle-fill"></i>
                  Positionnés
                </span>
                <span v-else-if="currentPage === page" class="status-indicator ready">
                  <i class="bi bi-cursor-fill"></i>
                  Prêt à positionner
                </span>
                <button 
                  v-if="hasIndividualPosition(page)" 
                  @click.stop="removeIndividualPosition(page)"
                  class="remove-position-btn"
                  title="Supprimer les éléments de cette page"
                >
                  <i class="bi bi-x-lg"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Contrôles de taille du QR -->
        <div class="qr-size-controls">
          <h5>Taille du QR Code :</h5>
          <div class="size-options">
            <button 
              v-for="size in qrSizes" 
              :key="size.name"
              :class="['size-option', { active: selectedQrSize === size.name }]"
              @click="setQrSize(size.name)"
            >
              <div class="size-preview" :class="size.name"></div>
              <span>{{ size.label }}</span>
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="actions-panel">
          <button @click="resetPosition" class="action-btn primary">
            <i class="bi bi-arrow-clockwise"></i>
            Réinitialiser
          </button>
          
          <button @click="showFinalPreview" class="action-btn preview" :disabled="isGeneratingPdf">
            <i class="bi" :class="isGeneratingPdf ? 'bi-hourglass-split spin' : 'bi-eye-fill'"></i>
            {{ isGeneratingPdf ? 'Génération en cours...' : 'Aperçu final' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal d'aperçu final -->
    <div v-if="showPreviewModal" class="preview-modal-overlay" @click.self="closePreviewModal">
      <div class="preview-modal">
        <div class="modal-header">
          <div class="header-icon">
            <i class="bi bi-eye-fill"></i>
          </div>
          <div class="header-text">
            <h4>Aperçu final du document</h4>
            <p>Visualisation du document avec QR code et signature</p>
          </div>
          <button @click="closePreviewModal" class="close-modal-btn">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- États de chargement -->
          <div v-if="isGeneratingPdf" class="loading-state">
            <div class="loading-content">
              <div class="spinner"></div>
              <div class="loading-text">
                <h5>Génération du PDF en cours...</h5>
                <p>Veuillez patienter pendant que nous préparons votre document</p>
              </div>
            </div>
          </div>
          
          <!-- États d'erreur -->
          <div v-else-if="pdfGenerationError" class="error-state">
            <div class="error-content">
              <div class="error-icon">
                <i class="bi bi-exclamation-triangle-fill"></i>
              </div>
              <div class="error-text">
                <h5>Erreur de génération</h5>
                <p>{{ pdfGenerationError }}</p>
                <div class="error-details" v-if="pdfGenerationError.includes('Erreur:')">
                  <details>
                    <summary>Détails techniques</summary>
                    <pre>{{ pdfGenerationError.split('Erreur:')[1] }}</pre>
                  </details>
                </div>
              </div>
              <button @click="showFinalPreview" class="retry-btn">
                <i class="bi bi-arrow-clockwise"></i>
                Réessayer
              </button>
            </div>
          </div>
          
          <!-- Aperçu PDF -->
          <div v-else-if="generatedPdfDataUrl" class="pdf-preview">
            <div class="pdf-wrapper">
              <iframe 
                :src="generatedPdfDataUrl" 
                class="pdf-iframe" 
                title="Aperçu du document"
                frameborder="0"
              ></iframe>
            </div>
          </div>
          
          <!-- Fallback -->
          <div v-else class="fallback-state">
            <div class="fallback-content">
              <div class="fallback-icon">
                <i class="bi bi-file-earmark-x-fill"></i>
              </div>
              <div class="fallback-text">
                <h5>Aperçu indisponible</h5>
                <p>Impossible de générer l'aperçu du document.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <div class="footer-actions">
            <button @click="closePreviewModal" class="footer-btn cancel">
              <i class="bi bi-x-circle"></i>
              <span>Fermer</span>
            </button>
            <button @click="confirmAndClosePreview" class="footer-btn confirm" :disabled="!generatedPdfBlob">
              <i class="bi bi-check-circle-fill"></i>
              <span>Confirmer et continuer</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch, defineEmits, defineProps, nextTick } from 'vue';
import VuePdfEmbed from 'vue-pdf-embed';
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import QRCode from 'qrcode';

// Enregistrer le composant VuePdfEmbed
const VuePdfEmbedComponent = VuePdfEmbed;

// Props
const props = defineProps({
  pdfFile: {
    type: Object,
    required: true
  },
  totalPages: {
    type: Number,
    default: 1
  },
  preloadedPositions: {
    type: Object,
    default: null
  }
});

// Emits
const emit = defineEmits(['position-confirmed', 'position-changed', 'signature-uploaded', 'pdf-generated']);

// État du composant
const currentPage = ref(1);
const pdfSource = ref(null);
const pdfLoaded = ref(false);
const isDraggingQr = ref(false);
const isDraggingSignature = ref(false);
const showPreviewModal = ref(false);
const showPositionInfo = ref(false);

// État pour l'aperçu PDF généré
const generatedPdfDataUrl = ref('');
const generatedPdfBlob = ref(null);
const isGeneratingPdf = ref(false);
const pdfGenerationError = ref(null);

// État pour la signature
const signatureImage = ref(null);
const signatureImageUrl = ref('');
const signatureSize = ref(50); // Taille en pourcentage (1-100)

// Position du QR code par défaut (en pourcentage)
const defaultPosition = { x: 85, y: 90 };

// Position unique (pour les modes all et custom)
const qrPosition = reactive({
  x: defaultPosition.x,
  y: defaultPosition.y
});

// Position pour la signature
const signaturePosition = reactive({
  x: 50,
  y: 50
});

// Positions individuelles par page (pour le mode individual)
const qrPositions = ref({});
const signaturePositions = ref({});

// Application des pages
const pageApplication = ref('all');
const selectedPages = ref([]);

// Tailles du QR code
const qrSizes = [
  { name: 'small', label: 'Petit', size: 50 },
  { name: 'medium', label: 'Moyen', size: 70 },
  { name: 'large', label: 'Grand', size: 90 }
];
const selectedQrSize = ref('medium');

// Références DOM
const previewContainer = ref(null);

// Méthodes pour gérer l'upload de signature
async function handleSignatureUpload(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith('image/')) {
    // Vérifier que c'est un format d'image supporté
    const supportedFormats = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/webp', 'image/svg+xml'];
    
    if (supportedFormats.some(format => file.type.includes(format.split('/')[1]))) {
      signatureImage.value = file;
      
      // Convertir directement en data URL pour éviter les problèmes CORS
      try {
        const reader = new FileReader();
        signatureImageUrl.value = await new Promise((resolve, reject) => {
          reader.onload = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        
        console.log('Image de signature chargée et convertie en data URL:', {
          name: file.name,
          type: file.type,
          size: file.size,
          dataUrlLength: signatureImageUrl.value.length
        });
      } catch (error) {
        console.error('Erreur lors de la conversion de l\'image:', error);
        // Fallback sur Blob URL si la conversion échoue
        signatureImageUrl.value = URL.createObjectURL(file);
      }
    
      // Émettre un événement pour informer le composant parent de l'image de signature
      emit('signature-uploaded', file);
    } else {
      alert('Format d\'image non supporté. Formats acceptés: PNG, JPEG, JPG, GIF, BMP, WEBP, SVG.');
      event.target.value = null;
    }
  } else {
    alert('Veuillez sélectionner un fichier image valide.');
    event.target.value = null;
  }
}

function removeSignature() {
  if (signatureImageUrl.value) {
    URL.revokeObjectURL(signatureImageUrl.value);
  }
  signatureImage.value = null;
  signatureImageUrl.value = '';
  signaturePositions.value = {};
}

function updateSignatureSize() {
  // Cette fonction est appelée quand on change la taille avec le slider
  emit('position-changed', getPositionData());
}

// Méthodes pour gérer les positions individuelles
function hasIndividualPosition(page) {
  return qrPositions.value[page] !== undefined || signaturePositions.value[page] !== undefined;
}

function getCurrentPagePosition() {
  if (pageApplication.value === 'individual' && qrPositions.value[currentPage.value]) {
    return qrPositions.value[currentPage.value];
  }
  return qrPosition;
}

function getCurrentPageSignaturePosition() {
  if (pageApplication.value === 'individual' && signaturePositions.value[currentPage.value]) {
    return signaturePositions.value[currentPage.value];
  }
  return signaturePosition;
}

function removeIndividualPosition(page) {
  delete qrPositions.value[page];
  delete signaturePositions.value[page];
  emit('position-changed', getPositionData());
}

// Calculs
const showQrOnCurrentPage = computed(() => {
  if (pageApplication.value === 'all') return true;
  if (pageApplication.value === 'current') return true;
  if (pageApplication.value === 'custom') {
    return selectedPages.value.includes(currentPage.value);
  }
  if (pageApplication.value === 'individual') {
    // En mode individual, toujours afficher le QR pour permettre le positionnement
    return true;
  }
  return false;
});

const canConfirm = computed(() => {
  if (pageApplication.value === 'custom' && selectedPages.value.length === 0) {
    return false;
  }
  if (pageApplication.value === 'individual') {
    // Il faut au moins avoir positionné un élément sur une page
    if (Object.keys(qrPositions.value).length === 0) {
      return false;
    }
  }
  return true;
});

const qrStyle = computed(() => {
  const size = qrSizes.find(s => s.name === selectedQrSize.value);
  const position = getCurrentPagePosition();
  return {
    left: `${position.x}%`,
    top: `${position.y}%`,
    width: `${size.size}px`,
    height: `${size.size}px`,
    transform: 'translate(-50%, -50%)',
    cursor: isDraggingQr.value ? 'grabbing' : 'grab'
  };
});

const signatureStyle = computed(() => {
  const position = getCurrentPageSignaturePosition();
  // Récupérer dynamiquement la largeur réelle de la page affichée
  const pageEl = previewContainer.value?.querySelector('.document-page');
  const pageWidthPx = pageEl ? pageEl.getBoundingClientRect().width : 595; // fallback 595
  // Le backend applique width_percent = signature_size * 0.6
  const widthPx = (signatureSize.value * 0.6 / 100) * pageWidthPx;
  
  return {
    left: `${position.x}%`,
    top: `${position.y}%`,
    width: `${widthPx}px`,
    transform: 'translate(-50%, -50%)',
    cursor: isDraggingSignature.value ? 'grabbing' : 'grab'
  };
});

// Méthodes de navigation
function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function nextPage() {
  if (currentPage.value < props.totalPages) {
    currentPage.value++;
  }
}

// Navigation directe vers une page
function goToPage(pageNumber) {
  currentPage.value = pageNumber;
}

// Gestion du PDF
const actualTotalPages = ref(1);
const pdfInitialized = ref(false);

function onPdfLoaded(event) {
  console.log('onPdfLoaded appelé, event:', event);
  pdfLoaded.value = true;
  
  // Extraire le nombre de pages de l'objet PDF
  if (event && event._pdfInfo && event._pdfInfo.numPages) {
    actualTotalPages.value = event._pdfInfo.numPages;
    pdfInitialized.value = true;
    console.log(`Nombre de pages détecté depuis _pdfInfo: ${event._pdfInfo.numPages}`);
  } else if (event && event.numPages) {
    actualTotalPages.value = event.numPages;
    pdfInitialized.value = true;
    console.log(`Nombre de pages détecté depuis numPages: ${event.numPages}`);
  } else if (event && typeof event === 'number' && event > 0) {
    actualTotalPages.value = event;
    pdfInitialized.value = true;
    console.log(`Nombre de pages détecté directement: ${event}`);
  } else {
    console.log('PDF chargé, mais nombre de pages non détecté depuis l\'event');
    // Utiliser la prop comme fallback
    actualTotalPages.value = props.totalPages || 1;
  }
}

function onPdfLoadError(error) {
  console.error('Erreur lors du chargement du PDF:', error);
  pdfLoaded.value = false;
}

function onPdfRendered() {
  console.log(`Page ${currentPage.value} rendue`);
}

// Gestion du drag & drop spécifique
function startDragQr(event) {
  event.stopPropagation();
  event.preventDefault();
  isDraggingQr.value = true;
  showPositionInfo.value = true;
    
  // En mode individual, si la page n'a pas encore de position, la créer maintenant
  if (pageApplication.value === 'individual' && !qrPositions.value[currentPage.value]) {
    const currentPos = getCurrentPagePosition();
    qrPositions.value[currentPage.value] = { x: currentPos.x, y: currentPos.y };
  }
  
  // Ajouter les écouteurs d'événements directement sur le document
  document.addEventListener('mousemove', handleDragMove);
  document.addEventListener('mouseup', handleDragEnd);
  document.addEventListener('touchmove', handleTouchMove, { passive: false });
  document.addEventListener('touchend', handleTouchEnd);
}

function startDragSignature(event) {
  event.stopPropagation();
  event.preventDefault();
  isDraggingSignature.value = true;
  showPositionInfo.value = true;
  
  // En mode individual, si la page n'a pas encore de position, la créer maintenant
  if (pageApplication.value === 'individual' && !signaturePositions.value[currentPage.value]) {
    const currentPos = getCurrentPageSignaturePosition();
    signaturePositions.value[currentPage.value] = { x: currentPos.x, y: currentPos.y };
  }
  
  // Ajouter les écouteurs d'événements directement sur le document
  document.addEventListener('mousemove', handleDragMove);
  document.addEventListener('mouseup', handleDragEnd);
  document.addEventListener('touchmove', handleTouchMove, { passive: false });
  document.addEventListener('touchend', handleTouchEnd);
}

function handleDragMove(event) {
  if (!isDraggingQr.value && !isDraggingSignature.value) return;
  
  // Empêcher le comportement par défaut pour éviter les sélections de texte
  event.preventDefault();
  
  const container = previewContainer.value;
  const documentPage = container.querySelector('.document-page');
  const pageRect = documentPage.getBoundingClientRect();
  
  const x = ((event.clientX - pageRect.left) / pageRect.width) * 100;
  const y = ((event.clientY - pageRect.top) / pageRect.height) * 100;
  
  // Limiter aux bordures avec marge
  const newX = Math.max(5, Math.min(95, x));
  const newY = Math.max(5, Math.min(95, y));
  
  // Mettre à jour la position appropriée selon l'élément en cours de déplacement
  if (isDraggingQr.value) {
    if (pageApplication.value === 'individual') {
      // Pour les positions individuelles, créer ou mettre à jour la position de la page actuelle
      if (!qrPositions.value[currentPage.value]) {
        qrPositions.value[currentPage.value] = { x: newX, y: newY };
      } else {
        qrPositions.value[currentPage.value].x = newX;
        qrPositions.value[currentPage.value].y = newY;
      }
    } else {
      // Pour les autres modes, utiliser la position unique
      qrPosition.x = newX;
      qrPosition.y = newY;
    }
  } 
  
  if (isDraggingSignature.value) {
    if (pageApplication.value === 'individual') {
      // Pour les positions individuelles, créer ou mettre à jour la position de la page actuelle
      if (!signaturePositions.value[currentPage.value]) {
        signaturePositions.value[currentPage.value] = { x: newX, y: newY };
      } else {
        signaturePositions.value[currentPage.value].x = newX;
        signaturePositions.value[currentPage.value].y = newY;
      }
    } else {
      // Pour les autres modes, utiliser la position unique
      signaturePosition.x = newX;
      signaturePosition.y = newY;
    }
  }
  
  emit('position-changed', getPositionData());
}

function handleDragEnd() {
  if (isDraggingQr.value || isDraggingSignature.value) {
    // Supprimer les écouteurs d'événements
    document.removeEventListener('mousemove', handleDragMove);
    document.removeEventListener('mouseup', handleDragEnd);
    document.removeEventListener('touchmove', handleTouchMove);
    document.removeEventListener('touchend', handleTouchEnd);
    
    isDraggingQr.value = false;
    isDraggingSignature.value = false;
    showPositionInfo.value = false;
  }
}

// Support tactile
function handleTouchStart(event) {
  const touch = event.touches[0];
  const target = document.elementFromPoint(touch.clientX, touch.clientY);
  const qrElement = target && target.closest('.qr-element');
  const signatureElement = target && target.closest('.signature-element');
  
  if (qrElement) {
    startDragQr(event);
  } else if (signatureElement) {
    startDragSignature(event);
  }
}

function handleTouchMove(event) {
  if (!isDraggingQr.value && !isDraggingSignature.value) return;
  
  // Empêcher le défilement pendant le glisser-déposer
  event.preventDefault();
  
  const touch = event.touches[0];
  const container = previewContainer.value;
  const documentPage = container.querySelector('.document-page');
  const pageRect = documentPage.getBoundingClientRect();
  
  const x = ((touch.clientX - pageRect.left) / pageRect.width) * 100;
  const y = ((touch.clientY - pageRect.top) / pageRect.height) * 100;
  
  const newX = Math.max(5, Math.min(95, x));
  const newY = Math.max(5, Math.min(95, y));
  
  if (isDraggingQr.value) {
    if (pageApplication.value === 'individual') {
      if (!qrPositions.value[currentPage.value]) {
        qrPositions.value[currentPage.value] = { x: newX, y: newY };
      } else {
        qrPositions.value[currentPage.value].x = newX;
        qrPositions.value[currentPage.value].y = newY;
      }
    } else {
      qrPosition.x = newX;
      qrPosition.y = newY;
    }
  }
  
  if (isDraggingSignature.value) {
    if (pageApplication.value === 'individual') {
      if (!signaturePositions.value[currentPage.value]) {
        signaturePositions.value[currentPage.value] = { x: newX, y: newY };
      } else {
        signaturePositions.value[currentPage.value].x = newX;
        signaturePositions.value[currentPage.value].y = newY;
      }
    } else {
      signaturePosition.x = newX;
      signaturePosition.y = newY;
    }
  }
  
  emit('position-changed', getPositionData());
}

function handleTouchEnd() {
  handleDragEnd();
}

// Contrôles
function setQrSize(size) {
  selectedQrSize.value = size;
  emit('position-changed', getPositionData());
}

function resetPosition() {
  // Réinitialiser les positions et tailles du QR code
  qrPosition.x = defaultPosition.x;
  qrPosition.y = defaultPosition.y;
  qrPositions.value = {};
  selectedQrSize.value = 'medium';
  
  // Réinitialiser les positions et tailles de la signature
  signaturePosition.x = 50;
  signaturePosition.y = 50;
  signaturePositions.value = {};
  signatureSize.value = 50;
  
  pageApplication.value = 'all';
  selectedPages.value = [];
  emit('position-changed', getPositionData());
}

// Aperçu final et génération PDF
async function showFinalPreview() {
  isGeneratingPdf.value = true;
  pdfGenerationError.value = null;
  
  try {
    // Générer le PDF modifié
    await generateModifiedPdf();
    
    // Afficher la modal
    showPreviewModal.value = true;
  } catch (error) {
    console.error('Erreur lors de la génération du PDF:', error);
    pdfGenerationError.value = `Erreur: ${error.message}`;
  } finally {
    isGeneratingPdf.value = false;
  }
}

// Fonction pour générer le PDF avec modifications
async function generateModifiedPdf() {
  if (!props.pdfFile) {
    throw new Error('Aucun fichier PDF original fourni');
  }
  
  try {
    // Lire le fichier PDF original
    const originalPdfBytes = await props.pdfFile.arrayBuffer();
    
    // Charger le document avec pdf-lib
    const pdfDoc = await PDFDocument.load(originalPdfBytes);
    
    // Pages à traiter
    let pagesToProcess = [];
    
    if (pageApplication.value === 'all') {
      // Ajouter toutes les pages
      pagesToProcess = Array.from({ length: pdfDoc.getPageCount() }, (_, i) => i);
    } else if (pageApplication.value === 'current') {
      // Ajouter uniquement la page actuelle (attention: pdf-lib utilise un index commençant à 0)
      pagesToProcess = [currentPage.value - 1];
    } else if (pageApplication.value === 'custom') {
      // Ajouter les pages sélectionnées (avec conversion d'index)
      pagesToProcess = selectedPages.value.map(p => p - 1);
    } else if (pageApplication.value === 'individual') {
      // Ajouter les pages avec positions individuelles
      const qrPages = Object.keys(qrPositions.value).map(p => parseInt(p) - 1);
      const signaturePages = signatureImage.value ? Object.keys(signaturePositions.value).map(p => parseInt(p) - 1) : [];
      pagesToProcess = [...new Set([...qrPages, ...signaturePages])];
    }
    
    // Pour chaque page à traiter
    for (const pageIndex of pagesToProcess) {
      // Vérifier que l'index de page est valide
      if (pageIndex < 0 || pageIndex >= pdfDoc.getPageCount()) continue;
      
      const page = pdfDoc.getPage(pageIndex);
      const { width, height } = page.getSize();
      
      // Ajouter le QR code si nécessaire pour cette page
      if (shouldShowQrOnPage(pageIndex + 1)) {
        // Obtenir la position du QR pour cette page
        let position;
        if (pageApplication.value === 'individual' && qrPositions.value[pageIndex + 1]) {
          position = qrPositions.value[pageIndex + 1];
        } else {
          position = qrPosition;
        }
        
        // Générer un vrai QR code avec qrcode
        const qrSize = qrSizes.find(s => s.name === selectedQrSize.value).size;
        
        // Convertir la position de pourcentage à coordonnées absolues
        const qrPosX = (position.x / 100) * width;
        const qrPosY = (position.y / 100) * height;
        
        try {
          // Générer le QR code comme une URL de données
          const qrDataUrl = await QRCode.toDataURL('https://antic.cm/verify?id=DEMO-QR-CODE', {
            errorCorrectionLevel: 'H',
            margin: 1,
            width: qrSize * 2, // Plus grande résolution pour meilleure qualité
            color: {
              dark: '#000000',
              light: '#ffffff'
            }
          });
          
          // Convertir l'URL de données en ArrayBuffer
          const qrImageBytes = await fetch(qrDataUrl).then(res => res.arrayBuffer());
          
          // Intégrer l'image QR dans le PDF
          const qrImage = await pdfDoc.embedPng(qrImageBytes);
          
          // D'abord dessiner un rectangle blanc comme fond
          page.drawRectangle({
            x: qrPosX - (qrSize / 2) - 5, // Un peu plus grand que le QR code
            y: height - qrPosY - (qrSize / 2) - 5,
            width: qrSize + 10,
            height: qrSize + 10,
            color: rgb(1, 1, 1), // blanc
            opacity: 1,
            borderWidth: 1,
            borderColor: rgb(0.8, 0.8, 0.8), // gris clair
            borderOpacity: 0.5
          });
          
          // Ensuite dessiner le QR code
          page.drawImage(qrImage, {
            x: qrPosX - (qrSize / 2),
            y: height - qrPosY - (qrSize / 2), // Conversion des coordonnées Y
            width: qrSize,
            height: qrSize
          });
        } catch (qrError) {
          console.error('Erreur lors de la génération du QR code:', qrError);
          
          // Fallback: dessiner un rectangle noir si le QR code échoue
          page.drawRectangle({
            x: qrPosX - (qrSize / 2),
            y: height - qrPosY - (qrSize / 2),
            width: qrSize,
            height: qrSize,
            color: rgb(0, 0, 0),
            opacity: 0.8
          });
        }
        
        // Ajouter le texte "GVB" sous le QR code dans un rectangle blanc
        const font = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
        
        // Mesurer la largeur du texte pour centrer
        const textWidth = font.widthOfTextAtSize('GVB', 10);
        
        // Dessiner un rectangle blanc comme fond pour le texte
        page.drawRectangle({
          x: qrPosX - (textWidth / 2) - 5,
          y: height - qrPosY - (qrSize / 2) - 25,
          width: textWidth + 10,
          height: 16,
          color: rgb(1, 1, 1), // blanc
          opacity: 1,
          borderWidth: 0
        });
        
        // Dessiner le texte
        page.drawText('GVB', {
          x: qrPosX - (textWidth / 2),
          y: height - qrPosY - (qrSize / 2) - 22,
          size: 10,
          font: font,
          color: rgb(0, 0, 0)
        });
      }
      
      // Ajouter la signature si nécessaire pour cette page
      if (shouldShowSignatureOnPage(pageIndex + 1) && signatureImage.value) {
        // Convertir l'image de la signature en format utilisable par pdf-lib
        const signatureImageBytes = await fetch(signatureImageUrl.value).then(res => res.arrayBuffer());
        let signatureEmbed;
        
        // Détecter le type d'image en utilisant le type MIME du fichier original
        const mimeType = signatureImage.value.type || 'image/png';
        console.log('Type MIME de l\'image de signature:', mimeType);
        
        try {
          if (mimeType.includes('jpeg') || mimeType.includes('jpg')) {
            signatureEmbed = await pdfDoc.embedJpg(signatureImageBytes);
          } else if (mimeType.includes('png')) {
            signatureEmbed = await pdfDoc.embedPng(signatureImageBytes);
          } else {
            // Pour les autres formats (GIF, BMP, WEBP, etc.), convertir en PNG via canvas
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            // Charger l'image dans un canvas et la convertir en PNG
            await new Promise((resolve, reject) => {
              img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                canvas.toBlob(async (blob) => {
                  if (blob) {
                    const pngBytes = await blob.arrayBuffer();
                    signatureEmbed = await pdfDoc.embedPng(pngBytes);
                    resolve();
                  } else {
                    reject(new Error('Échec de la conversion en PNG'));
                  }
                }, 'image/png');
              };
              img.onerror = reject;
              img.src = signatureImageUrl.value;
            });
          }
        } catch (e) {
          console.error('Erreur lors de l\'intégration de l\'image de signature:', e);
          console.log('Tentative de fallback avec conversion PNG...');
          
          // Dernier recours : convertir via canvas
          try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            await new Promise((resolve, reject) => {
              img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                canvas.toBlob(async (blob) => {
                  if (blob) {
                    const pngBytes = await blob.arrayBuffer();
                    signatureEmbed = await pdfDoc.embedPng(pngBytes);
                    resolve();
                  } else {
                    reject(new Error('Échec de la conversion en PNG'));
                  }
                }, 'image/png');
              };
              img.onerror = reject;
              img.src = signatureImageUrl.value;
            });
          } catch (fallbackError) {
            console.error('Impossible d\'intégrer l\'image de signature:', fallbackError);
            continue; // Passer à la page suivante
          }
        }
        
        // Obtenir la position de signature pour cette page
        let position;
        if (pageApplication.value === 'individual' && signaturePositions.value[pageIndex + 1]) {
          position = signaturePositions.value[pageIndex + 1];
        } else {
          position = signaturePosition;
        }
        
        // Calculer la taille et position de l'image
        // Utiliser la même échelle que dans l'interface de positionnement
        // La taille dans l'interface est signatureSize.value * 2 (en pixels)
        // On calcule donc un facteur d'échelle proportionnel à la largeur de la page
        // Le backend convertit signature_size en width_percent = signature_size * 0.6
        const scaleFactor = (signatureSize.value * 0.6) / 100;
        const sigWidth = width * scaleFactor;
        const sigHeight = (signatureEmbed.height / signatureEmbed.width) * sigWidth;
        
        // Convertir la position de pourcentage à coordonnées absolues
        const sigPosX = (position.x / 100) * width - (sigWidth / 2);
        const sigPosY = (position.y / 100) * height - (sigHeight / 2);
        
        // Dessiner l'image
        page.drawImage(signatureEmbed, {
          x: sigPosX,
          y: height - sigPosY - sigHeight, // Conversion des coordonnées Y
          width: sigWidth,
          height: sigHeight,
          opacity: 0.9
        });
      }
    }
    
    // Sérialiser le PDF modifié
    const modifiedPdfBytes = await pdfDoc.save();
    
    // Créer un blob et une URL de données
    const blob = new Blob([modifiedPdfBytes], { type: 'application/pdf' });
    generatedPdfBlob.value = blob;
    generatedPdfDataUrl.value = URL.createObjectURL(blob);
    
    return true;
  } catch (error) {
    console.error('Erreur pendant la génération du PDF:', error);
    throw error;
  }
}

function closePreviewModal() {
  showPreviewModal.value = false;
  
  // Nettoyer les ressources du PDF généré pour libérer de la mémoire
  if (generatedPdfDataUrl.value) {
    URL.revokeObjectURL(generatedPdfDataUrl.value);
    generatedPdfDataUrl.value = '';
    generatedPdfBlob.value = null;
  }
}

async function confirmAndClosePreview() {
  if (generatedPdfBlob.value) {
    try {
      // Créer un nom de fichier pour le File object
      let fileName = 'document_modifié.pdf';
      if (props.pdfFile && props.pdfFile.name) {
        const originalName = props.pdfFile.name.replace(/\.pdf$/i, '');
        fileName = `${originalName}_modifié.pdf`;
      }
      
      const pdfFile = new File([generatedPdfBlob.value], fileName, { type: 'application/pdf' });

      // Émettre un événement au composant parent avec les données du PDF généré
      emit('pdf-generated', {
        file: pdfFile,
        dataUrl: generatedPdfDataUrl.value,
        blob: generatedPdfBlob.value
      });
    } catch (error) {
      console.error('Erreur lors de la préparation du PDF généré :', error);
    }
  }

  // Confirmer la position et fermer la modale
  await confirmPosition();
  closePreviewModal();
}

// Fonctions pour déterminer quelles pages doivent afficher les éléments
function shouldShowQrOnPage(page) {
  if (pageApplication.value === 'all') return true;
  if (pageApplication.value === 'current') return page === currentPage.value;
  if (pageApplication.value === 'custom') return selectedPages.value.includes(page);
  if (pageApplication.value === 'individual') return qrPositions.value[page] !== undefined;
  return false;
}

function shouldShowSignatureOnPage(page) {
  if (!signatureImage.value) return false;
  if (pageApplication.value === 'all') return true;
  if (pageApplication.value === 'current') return page === currentPage.value;
  if (pageApplication.value === 'custom') return selectedPages.value.includes(page);
  if (pageApplication.value === 'individual') return signaturePositions.value[page] !== undefined;
  return false;
}

// Confirmation
function getPositionData() {
  let pages = [];
  let positions = {};
  let signatureData = null;
  
  if (pageApplication.value === 'all') {
    pages = 'all';
    positions = { default: { x: qrPosition.x, y: qrPosition.y } };
  } else if (pageApplication.value === 'current') {
    pages = [currentPage.value];
    positions = { [currentPage.value]: { x: qrPosition.x, y: qrPosition.y } };
  } else if (pageApplication.value === 'custom') {
    pages = selectedPages.value;
    // Toutes les pages sélectionnées ont la même position
    selectedPages.value.forEach(page => {
      positions[page] = { x: qrPosition.x, y: qrPosition.y };
    });
  } else if (pageApplication.value === 'individual') {
    pages = Object.keys(qrPositions.value).map(Number);
    positions = { ...qrPositions.value };
  }
  
  // Ajout des données de signature si disponibles
  if (signatureImage.value) {
    let signaturePages = [];
    let signaturePositionsData = {};
    
    if (pageApplication.value === 'all') {
      signaturePages = 'all';
      signaturePositionsData = { default: { x: signaturePosition.x, y: signaturePosition.y } };
    } else if (pageApplication.value === 'current') {
      signaturePages = [currentPage.value];
      signaturePositionsData = { [currentPage.value]: { x: signaturePosition.x, y: signaturePosition.y } };
    } else if (pageApplication.value === 'custom') {
      signaturePages = selectedPages.value;
      selectedPages.value.forEach(page => {
        signaturePositionsData[page] = { x: signaturePosition.x, y: signaturePosition.y };
      });
    } else if (pageApplication.value === 'individual') {
      signaturePages = Object.keys(signaturePositions.value).map(Number);
      signaturePositionsData = { ...signaturePositions.value };
    }
    
    signatureData = {
      imageUrl: signatureImageUrl.value,
      size: signatureSize.value,
      pages: signaturePages,
      positions: signaturePositionsData
    };
  }
  
  return {
    qr: {
      size: selectedQrSize.value,
      pages: pages,
      positions: positions,
    },
    signature: signatureData,
    mode: pageApplication.value // Pour savoir comment interpréter les données
  };
}

async function confirmPosition() {
  // Si on n'a pas encore de PDF généré, le générer automatiquement
  if (!generatedPdfBlob.value) {
    console.log('Aucun PDF généré trouvé, génération automatique...');
    try {
      await generateModifiedPdf();
      
      // Créer un File object pour l'émission
      if (generatedPdfBlob.value) {
        let fileName = 'document_modifié.pdf';
        if (props.pdfFile && props.pdfFile.name) {
          const originalName = props.pdfFile.name.replace(/\.pdf$/i, '');
          fileName = `${originalName}_modifié.pdf`;
        }
        
        const pdfFile = new File([generatedPdfBlob.value], fileName, { type: 'application/pdf' });

        // Émettre l'événement pdf-generated
        emit('pdf-generated', {
          file: pdfFile,
          dataUrl: generatedPdfDataUrl.value,
          blob: generatedPdfBlob.value
        });
        
        console.log('PDF généré automatiquement et émis');
      }
    } catch (error) {
      console.error('Erreur lors de la génération automatique du PDF:', error);
      // Continuer quand même avec la confirmation
    }
  } else {
    console.log('PDF déjà généré, pas besoin de le régénérer');
  }
  
  emit('position-confirmed', getPositionData());
}

// Initialisation
onMounted(() => {
  console.log('Composant SignBase monté');
  console.log('Fichier PDF reçu:', props.pdfFile);
  console.log('Nombre total de pages (prop):', props.totalPages);
  
  if (props.pdfFile) {
    // Créer une URL pour le fichier PDF
    const fileUrl = URL.createObjectURL(props.pdfFile);
    pdfSource.value = fileUrl;
    console.log('URL PDF créée:', fileUrl);
    console.log('pdfSource.value défini:', pdfSource.value);
  } else {
    console.error('Aucun fichier PDF fourni au composant');
  }
  
  emit('position-changed', getPositionData());
});

// Watchers
watch(() => props.pdfFile, (newFile) => {
  if (newFile) {
    console.log('Nouveau fichier PDF détecté');
    // Nettoyer l'ancienne URL si elle existe
    if (pdfSource.value) {
      URL.revokeObjectURL(pdfSource.value);
    }
    // Créer une nouvelle URL
    const fileUrl = URL.createObjectURL(newFile);
    pdfSource.value = fileUrl;
    currentPage.value = 1;
  }
});

watch(pageApplication, (newVal) => {
  if (newVal === 'current') {
    selectedPages.value = [currentPage.value];
  } else if (newVal === 'individual') {
    // Lors du passage en mode individuel, ne pas créer automatiquement de position
    // L'utilisateur doit interagir avec le QR pour qu'il soit sauvegardé
  }
  emit('position-changed', getPositionData());
});

// Nettoyage
onUnmounted(() => {
  if (pdfSource.value) {
    URL.revokeObjectURL(pdfSource.value);
  }
  if (signatureImageUrl.value) {
    URL.revokeObjectURL(signatureImageUrl.value);
  }
  if (generatedPdfDataUrl.value) {
    URL.revokeObjectURL(generatedPdfDataUrl.value);
  }
});

// Propriété calculée pour le nombre total de pages (utilise la valeur détectée si disponible)
const totalPages = computed(() => {
  const detectedPages = actualTotalPages.value;
  const propPages = props.totalPages || 1;
  const finalPages = detectedPages > 1 ? detectedPages : propPages;
  console.log(`Total pages calculé: detected=${detectedPages}, prop=${propPages}, final=${finalPages}`);
  return finalPages;
});

// Gestion du drag & drop pour l'arrière-plan
function handleDragStart(event) {
  // Ne rien faire si on clique déjà sur un élément draggable
  if (event.target.closest('.qr-element') || event.target.closest('.signature-element')) {
    return;
  }
  
  // Si l'utilisateur clique sur l'arrière-plan, on peut
  // implémenter une fonctionnalité spécifique si nécessaire
  console.log("Clic sur l'arrière-plan de la page");
}

// Initialiser les positions depuis les données préchargées
function initializeFromPreloadedPositions() {
  if (!props.preloadedPositions) return;
  
  console.log('Initialisation des positions préchargées:', props.preloadedPositions);
  
  // Initialiser le mode d'application des pages
  if (props.preloadedPositions.mode) {
    pageApplication.value = props.preloadedPositions.mode;
  }
  
  // Initialiser les positions QR
  if (props.preloadedPositions.qr) {
    // Taille du QR
    if (props.preloadedPositions.qr.size) {
      selectedQrSize.value = props.preloadedPositions.qr.size;
    }
    
    // Pages sélectionnées pour l'application custom
    if (props.preloadedPositions.mode === 'custom' && Array.isArray(props.preloadedPositions.qr.pages)) {
      selectedPages.value = [...props.preloadedPositions.qr.pages];
    }
    
    // Positions du QR
    if (props.preloadedPositions.qr.positions) {
      if (props.preloadedPositions.mode === 'individual') {
        // Pour le mode individual, copier toutes les positions par page
        Object.entries(props.preloadedPositions.qr.positions).forEach(([page, pos]) => {
          qrPositions.value[Number(page)] = { x: pos.x, y: pos.y };
        });
      } else if (props.preloadedPositions.qr.positions.default) {
        // Pour le mode all ou autre, utiliser la position par défaut
        const pos = props.preloadedPositions.qr.positions.default;
        qrPosition.x = pos.x;
        qrPosition.y = pos.y;
      } else if (Object.values(props.preloadedPositions.qr.positions).length > 0) {
        // Fallback: utiliser la première position disponible
        const pos = Object.values(props.preloadedPositions.qr.positions)[0];
        qrPosition.x = pos.x;
        qrPosition.y = pos.y;
      }
    }
  }
  
  // Initialiser les positions de signature si disponibles
  if (props.preloadedPositions.signature) {
    // Taille de la signature
    if (props.preloadedPositions.signature.size) {
      signatureSize.value = props.preloadedPositions.signature.size;
    }
    
    // Positions de la signature
    if (props.preloadedPositions.signature.positions) {
      if (props.preloadedPositions.mode === 'individual') {
        // Pour le mode individual, copier toutes les positions par page
        Object.entries(props.preloadedPositions.signature.positions).forEach(([page, pos]) => {
          signaturePositions.value[Number(page)] = { x: pos.x, y: pos.y };
        });
      } else if (props.preloadedPositions.signature.positions.default) {
        // Pour le mode all ou autre, utiliser la position par défaut
        const pos = props.preloadedPositions.signature.positions.default;
        signaturePosition.x = pos.x;
        signaturePosition.y = pos.y;
      } else if (Object.values(props.preloadedPositions.signature.positions).length > 0) {
        // Fallback: utiliser la première position disponible
        const pos = Object.values(props.preloadedPositions.signature.positions)[0];
        signaturePosition.x = pos.x;
        signaturePosition.y = pos.y;
      }
    }
  }
  
  // Initialiser l'image de signature si fournie
  if (props.preloadedPositions.signature && props.preloadedPositions.signature.image) {
    try {
      const imageUrl = props.preloadedPositions.signature.image;
      // Récupérer l'image puis créer un File pour disposer d'un type mime
      fetch(imageUrl)
        .then(r => r.blob())
        .then(blob => {
          const imgExt = (blob.type && blob.type.split('/')[1]) ? blob.type.split('/')[1].replace('jpeg', 'jpg') : 'png';
          const file = new File([blob], `preloaded_signature.${imgExt}`, { type: blob.type || 'image/png' });
          signatureImage.value = file;
          if (signatureImageUrl.value) {
            URL.revokeObjectURL(signatureImageUrl.value);
          }
          signatureImageUrl.value = URL.createObjectURL(file);
        })
        .catch(err => console.warn('Impossible de précharger l\'image de signature:', err));
    } catch (e) {
      console.warn('Erreur lors du préchargement de l\'image de signature:', e);
    }
  }
  
  // Émettre un événement pour informer le composant parent des positions chargées
  emit('position-changed', getPositionData());
}

// Watchers
watch(() => props.preloadedPositions, (newVal) => {
  if (newVal) {
    initializeFromPreloadedPositions();
  }
}, { immediate: true, deep: true });
</script>

<style scoped>
/* Variables CSS personnalisées pour le dashboard */
:root {
  --primary-color: #3a86ff;
  --primary-dark: #2563eb;
  --primary-light: #60a5fa;
  --accent-color: #06d6a0;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --text-color: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-light: #f1f5f9;
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
}

/* Conteneur principal avec le style glassmorphique de la modale profil */
.sign-base-container {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1);
  position: relative;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  padding: 20px;
}



/* Section d'upload de signature avec style glassmorphique */
.signature-upload-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  text-align: center;
  width: 100%;
}



.signature-upload-section h5 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.signature-upload-section h5 i {
  color: var(--accent-color);
  font-size: 1.125rem;
}

/* Zone d'upload moderne */
.upload-dropzone {
  border: 3px dashed #e2e8f0;
  border-radius: 12px;
  padding: 30px 20px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8f9fa;
  position: relative;
  overflow: hidden;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-dropzone:hover {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.04);
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

.upload-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  color: var(--dark-gray);
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.upload-icon {
  width: 50px;
  height: 50px;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--primary-blue);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  flex-shrink: 0;
}

.upload-dropzone:hover .upload-icon {
  transform: scale(1.1) rotate(5deg);
  background: rgba(0, 102, 204, 0.15);
}

.upload-text h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 4px 0;
}

.upload-text p {
  margin: 0 0 8px 0;
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.upload-text .link {
  color: var(--primary-blue);
  font-weight: 600;
  text-decoration: underline;
}

.upload-text small {
  color: #6c757d;
  font-size: 0.75rem;
}

/* Prévisualisation de signature moderne */
.signature-preview-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  text-align: center;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.signature-preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.signature-preview-img {
  max-width: 180px;
  max-height: 90px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signature-controls-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.size-slider {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.size-slider label {
  font-weight: 600;
  color: var(--text-color);
  font-size: 0.9rem;
}

.size-slider input[type="range"] {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.2);
  outline: none;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  min-width: 200px;
}

.size-slider input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-blue);
  cursor: pointer;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.size-slider input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.remove-signature-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  min-width: 120px;
  justify-content: center;
  text-decoration: none;
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
}

.remove-signature-btn:hover {
  background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4);
}

.remove-signature-btn i {
  font-size: 1rem;
}

/* Grille principale avec style glassmorphique */
.main-content-grid {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 24px;
  align-items: start;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* Zone d'aperçu du document */
.document-preview-area {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.preview-header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.preview-header-section h5 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-dark);
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  letter-spacing: -0.025em;
}

.preview-header-section h5::before {
  content: '\F4C3';
  font-family: 'bootstrap-icons';
  font-size: 1.1rem;
  color: var(--primary-blue);
}

.preview-header-section h5::after {
  content: '';
  position: absolute;
  bottom: -16px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-blue), #007bff);
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
}

.page-navigation {
  display: flex;
  align-items: center;
  gap: 16px;
  user-select: none;
}

.nav-btn {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--text-color);
  font-weight: 500;
}

.nav-btn:hover:not(:disabled) {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.page-indicator {
  font-size: 0.9rem;
  color: var(--text-secondary);
  min-width: 120px;
  text-align: center;
  font-weight: 500;
}

/* Conteneur de document moderne */
.document-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.document-page {
  position: relative;
  width: 595px;
  height: 842px;
  max-width: 100%;
  aspect-ratio: 210 / 297;
  background: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  cursor: crosshair;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.pdf-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.pdf-viewer {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.pdf-loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
  background: var(--bg-light);
}

.pdf-loading-state i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.pdf-loading-state p {
  font-size: 1.1rem;
  font-weight: 500;
}

/* Éléments draggables avec style dashboard */
.qr-element, .signature-element {
  position: absolute;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  cursor: grab;
  z-index: 10;
}

.qr-element {
  background: white;
  border: 2px solid var(--primary-color);
  border-radius: var(--radius-sm);
  padding: 10px;
}

.signature-element {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid var(--accent-color);
  border-radius: 6px;
  padding: 4px;
  backdrop-filter: blur(4px);
}

.qr-element:hover, .signature-element:hover {
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
  transform: translateZ(4px);
}

.qr-element.dragging, .signature-element.dragging {
  opacity: 0.8;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.25);
  cursor: grabbing;
  transform: rotate(2deg) scale(1.05);
}

.qr-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.qr-code {
  background: white;
  border: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border-radius: 2px;
}

.qr-code.small {
  width: 40px;
  height: 40px;
}

.qr-code.medium {
  width: 60px;
  height: 60px;
}

.qr-code.large {
  width: 80px;
  height: 80px;
}

.qr-pattern {
  width: 85%;
  height: 85%;
  background-image: 
    linear-gradient(45deg, #000 25%, transparent 25%),
    linear-gradient(-45deg, #000 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #000 75%),
    linear-gradient(-45deg, transparent 75%, #000 75%);
  background-size: 6px 6px;
  background-position: 0 0, 0 3px, 3px -3px, -3px 0px;
}

.qr-label {
  font-size: 10px;
  font-weight: 700;
  color: #333;
  letter-spacing: 0.5px;
}

.signature-img {
  max-width: 100%;
  max-height: 100%;
  display: block;
  border-radius: 2px;
}

/* Feedback de position moderne */
.position-feedback {
  margin-top: 16px;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  background: var(--bg-light);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

/* Panneau de contrôles moderne */
.controls-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-width: 260px;
}

.pages-overview, .pages-selection-section, .qr-size-controls {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* Titres des sections avec style moderne */
.pages-overview h5, .pages-selection-section h5, .qr-size-controls h5 {
  margin: 0 0 16px 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  padding-bottom: 10px;
  letter-spacing: -0.025em;
}

/* Centrage spécifique pour le titre "Pages..." */
.pages-selection-section h5 {
  justify-content: center;
  text-align: center;
}



.pages-overview h5::after, 
.pages-selection-section h5::after, 
.qr-size-controls h5::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-blue), #007bff);
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
}

/* Grille de pages moderne */
.pages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(75px, 1fr));
  gap: 12px;
  max-height: 200px;
  overflow-y: auto;
  padding: 4px;
}

.page-thumb {
  cursor: pointer;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
  padding: 6px;
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.page-thumb:hover {
  transform: scale(1.08) translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.15);
  border-color: rgba(0, 102, 204, 0.3);
  background: rgba(255, 255, 255, 0.1);
}

.page-thumb.active {
  outline: none;
  border: 2px solid var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
  transform: scale(1.02);
}

.page-thumb.active::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, var(--primary-blue), #007bff);
  border-radius: 10px;
  z-index: -1;
  opacity: 0.3;
}

.page-thumb-wrapper {
  width: 100%;
  aspect-ratio: 210 / 297;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.page-thumb:hover .page-thumb-wrapper {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: rgba(0, 102, 204, 0.2);
}

.page-thumb.active .page-thumb-wrapper {
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.25);
  border-color: var(--primary-blue);
}

.page-thumb-pdf {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.page-thumb-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #6c757d;
  padding: 8px;
}

.page-thumb-placeholder i {
  font-size: 20px;
  color: #adb5bd;
}

.page-thumb-placeholder span {
  font-size: 10px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.page-label {
  font-size: 11px;
  color: var(--text-dark);
  margin-top: 8px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.8);
  padding: 2px 6px;
  border-radius: 4px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.more-pages-indicator {
  grid-column: 1 / -1;
  text-align: center;
  color: var(--text-muted);
  font-size: 11px;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
}

/* Options d'application modernes */
.application-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 102, 204, 0.3);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.option-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.1), transparent);
  transition: left 0.5s ease;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(0, 102, 204, 0.5);
  transform: translateX(3px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
}

.option-item:hover::before {
  left: 100%;
}

.option-item input[type="radio"] {
  cursor: pointer;
  accent-color: var(--primary-blue);
  transform: scale(1.1);
  margin: 0;
}

.option-item span {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary-blue);
  transition: color 0.3s ease;
}

.option-item:hover span {
  color: var(--primary-blue);
  font-weight: 700;
}

.option-item span {
  cursor: pointer;
  font-weight: 500;
  color: var(--text-color);
  font-size: 0.9rem;
}

/* Sélection personnalisée moderne */
.custom-selection {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.selection-hint {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
  padding: 12px;
  background: rgba(58, 134, 255, 0.05);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--primary-color);
  font-weight: 500;
}

.pages-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(55px, 1fr));
  gap: 8px;
  max-height: 120px;
  overflow-y: auto;
  padding: 8px;
  background: var(--bg-primary);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.page-check {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 0.8rem;
  font-weight: 500;
}

.page-check:hover {
  background: var(--bg-secondary);
}

.page-check input[type="checkbox"] {
  cursor: pointer;
  accent-color: var(--primary-color);
  transform: scale(0.95);
}

/* Sélection individuelle moderne */
.individual-selection {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.individual-hint {
  font-size: 0.8rem;
  color: var(--text-dark);
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.individual-hint i {
  color: var(--primary-blue);
  font-size: 0.85rem;
}

.individual-hint small {
  font-size: 0.7rem;
  color: var(--text-muted);
  opacity: 0.9;
  font-weight: 500;
}

.individual-pages-list {
  max-height: 140px;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 6px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.individual-page {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 3px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

.individual-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.1), transparent);
  transition: left 0.5s ease;
}

.individual-page:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(0, 102, 204, 0.3);
  transform: translateX(3px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.individual-page:hover::before {
  left: 100%;
}

.individual-page.has-elements {
  background: rgba(0, 102, 204, 0.1);
  border-color: var(--primary-blue);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.2);
}

.individual-page.current {
  border-color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.15);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
  transform: scale(1.02);
}

.individual-page.ready-to-position {
  background: rgba(0, 102, 204, 0.1);
  border-color: var(--primary-blue);
  animation: readyPulse 2s ease-in-out infinite;
}

@keyframes readyPulse {
  0% { opacity: 1; }
  50% { opacity: 0.8; }
  100% { opacity: 1; }
}

.page-number {
  font-weight: 600;
  color: var(--text-dark);
  font-size: 0.8rem;
  transition: color 0.3s ease;
}

.individual-page:hover .page-number {
  color: var(--primary-blue);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 0.7rem;
  color: var(--primary-blue);
  font-weight: 500;
  padding: 2px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.status-indicator i {
  font-size: 0.75rem;
}

.status-indicator.ready {
  color: var(--primary-blue);
  font-style: normal;
  background: rgba(0, 102, 204, 0.1);
  border-color: rgba(0, 102, 204, 0.2);
}

.remove-position-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ef4444;
  cursor: pointer;
  padding: 3px 5px;
  border-radius: 4px;
  transition: all 0.3s ease;
  font-size: 0.75rem;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}

.remove-position-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

/* Contrôles de taille QR modernes */
.size-options {
  display: flex;
  gap: 6px;
}

.size-option {
  flex: 1;
  padding: 10px 8px;
  border: 1px solid rgba(0, 102, 204, 0.3);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.size-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.1), transparent);
  transition: left 0.5s ease;
}

.size-option:hover {
  border-color: rgba(0, 102, 204, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
  background: rgba(255, 255, 255, 0.15);
}

.size-option:hover::before {
  left: 100%;
}

.size-option.active {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border-color: var(--primary-blue);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
}

.size-preview {
  border: 2px solid currentColor;
  border-radius: 4px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
}

.size-preview.small {
  width: 14px;
  height: 14px;
}

.size-preview.medium {
  width: 20px;
  height: 20px;
}

.size-preview.large {
  width: 26px;
  height: 26px;
}

.size-option span {
  font-weight: 600;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--primary-blue);
  transition: color 0.3s ease;
}

.size-option:hover span {
  color: var(--primary-blue);
}

.size-option.active span {
  color: var(--primary-blue);
}

/* Panneau d'actions moderne */
.actions-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 44px;
  text-transform: none;
  letter-spacing: 0.2px;
  width: 100%;
  text-decoration: none;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.action-btn:hover::before {
  left: 100%;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-dark);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(0, 102, 204, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
}

.action-btn.preview {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border: 1px solid rgba(0, 102, 204, 0.3);
}

.action-btn.preview:hover:not(:disabled) {
  background: rgba(0, 102, 204, 0.15);
  border-color: rgba(0, 102, 204, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
}

.action-btn.preview:disabled {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
  color: var(--text-muted);
}

.action-btn.primary {
  background: rgba(0, 102, 204, 0.15);
  color: var(--primary-blue);
  border: 1px solid rgba(0, 102, 204, 0.4);
}

.action-btn.primary:hover:not(:disabled) {
  background: rgba(0, 102, 204, 0.2);
  border-color: rgba(0, 102, 204, 0.6);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.action-btn.primary:disabled {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
  color: var(--text-muted);
}

.action-btn i {
  font-size: 1rem;
}

/* Animation pour les icônes de chargement */
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal d'aperçu final stylisée - Cohérent avec la modale du profil utilisateur */
.preview-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-out;
}

.preview-modal {
  background: rgba(255, 255, 255, 0.3) !important;
  backdrop-filter: blur(15px) saturate(120%) !important;
  -webkit-backdrop-filter: blur(15px) saturate(120%) !important;
  width: 90%;
  max-width: 1200px;
  height: 112vh;
  max-height: 1400px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 1px 0 0 rgba(255, 255, 255, 0.1) !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: translateY(100px) scale(0.9);
  animation: modalSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.modal-header {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.header-text {
  flex: 1;
  text-align: center;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: rgba(0, 102, 204, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: var(--primary-blue);
  backdrop-filter: blur(4px);
}

.header-text h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937 !important;
  letter-spacing: -0.025em;
  text-align: center;
}

.header-text p {
  margin: 0;
  color: #6b7280 !important;
  font-size: 0.875rem;
  font-weight: 400;
}

.close-modal-btn {
  background: #0066cc;
  border: 1px solid #0066cc;
  border-radius: 12px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.125rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-modal-btn:hover {
  background: #0052a3;
  border-color: #0052a3;
  transform: scale(1.05);
}

.modal-body {
  flex: 1;
  padding: 2.5rem;
  padding-bottom: 6rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.02) !important;
  min-height: 0;
}

/* États de chargement modernes */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-content {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-blue);
  animation: spinnerRotate 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spinnerRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

.loading-text h5 {
  margin: 0 0 12px 0;
  color: var(--text-color);
  font-size: 1.25rem;
  font-weight: 600;
}

.loading-text p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.5;
}

/* États d'erreur modernes */
.error-state, .fallback-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error-content, .fallback-content {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  max-width: 600px;
}

.fallback-content {
  border-left-color: var(--text-muted);
}

.error-icon, .fallback-icon {
  width: 64px;
  height: 64px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  color: var(--error-color);
}

.fallback-icon {
  background: rgba(156, 163, 175, 0.1);
  color: var(--text-muted);
}

.error-text h5, .fallback-text h5 {
  margin: 0 0 1rem 0;
  color: var(--text-dark);
  font-size: 1.125rem;
  font-weight: 600;
}

.error-text p, .fallback-text p {
  margin: 0 0 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.875rem;
  line-height: 1.6;
}

.error-details {
  margin-top: 20px;
  text-align: left;
}

.error-details summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 12px;
  padding: 8px 12px;
  background: var(--bg-light);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.error-details pre {
  background: var(--bg-light);
  padding: 16px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  overflow-x: auto;
  white-space: pre-wrap;
  border: 1px solid var(--border-color);
  color: var(--error-color);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.retry-btn {
  background: rgba(0, 102, 204, 0.15);
  color: var(--primary-blue);
  border: 1px solid rgba(0, 102, 204, 0.3);
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 auto;
  backdrop-filter: blur(4px);
}

.retry-btn:hover {
  background: rgba(0, 102, 204, 0.25);
  border-color: rgba(0, 102, 204, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
}

/* Aperçu PDF moderne */
.pdf-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 900px;
}

.pdf-wrapper {
  flex: 1;
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  min-height: 900px;
  border: none;
  display: block;
}

/* Footer de modal moderne */
.modal-footer {
  background: rgba(255, 255, 255, 0.3) !important;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb !important;
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.footer-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid;
  min-width: 140px;
  justify-content: center;
}

.footer-btn.cancel {
  background: white !important;
  color: #0066cc !important;
  border: 1px solid #0066cc !important;
}

.footer-btn.cancel:hover {
  background: #f8fafc !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
}

.footer-btn.confirm {
  background: #0066cc !important;
  color: white !important;
  border: 1px solid #0066cc !important;
}

.footer-btn.confirm:hover:not(:disabled) {
  background: #0052a3 !important;
  border-color: #0052a3 !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.3);
}

.footer-btn.confirm:disabled {
  background: #9ca3af !important;
  color: white !important;
  border-color: #9ca3af !important;
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
}

/* Scrollbars personnalisées pour la modale */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Pour Firefox */
.modal-body {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

/* Scrollbars personnalisées modernes */
.pages-grid::-webkit-scrollbar,
.pages-checkboxes::-webkit-scrollbar,
.individual-pages-list::-webkit-scrollbar {
  width: 6px;
}

.pages-grid::-webkit-scrollbar-track,
.pages-checkboxes::-webkit-scrollbar-track,
.individual-pages-list::-webkit-scrollbar-track {
  background: var(--bg-light);
  border-radius: 3px;
}

.pages-grid::-webkit-scrollbar-thumb,
.pages-checkboxes::-webkit-scrollbar-thumb,
.individual-pages-list::-webkit-scrollbar-thumb {
  background: var(--text-muted);
  border-radius: 3px;
  transition: all 0.2s ease;
}

.pages-grid::-webkit-scrollbar-thumb:hover,
.pages-checkboxes::-webkit-scrollbar-thumb:hover,
.individual-pages-list::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}

/* Responsive design moderne - Écrans PC */
@media (min-width: 1600px) {
  .main-content-grid {
    grid-template-columns: 1fr 300px;
    gap: 28px;
    padding: 28px;
  }
  
  .controls-panel {
    max-width: 280px;
  }
  
  .pages-overview, .pages-selection-section, .qr-size-controls {
    padding: 20px;
  }
}

@media (max-width: 1599px) and (min-width: 1400px) {
  .main-content-grid {
    grid-template-columns: 1fr 280px;
    gap: 24px;
    padding: 24px;
  }
  
  .controls-panel {
    max-width: 260px;
  }
  
  .pages-overview, .pages-selection-section, .qr-size-controls {
    padding: 18px;
  }
  
  .pages-grid {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
    gap: 10px;
    max-height: 180px;
  }
}

@media (max-width: 1399px) and (min-width: 1200px) {
  .main-content-grid {
    grid-template-columns: 1fr 260px;
    gap: 20px;
    padding: 20px;
  }
  
  .controls-panel {
    max-width: 240px;
  }
  
  .pages-overview, .pages-selection-section, .qr-size-controls {
    padding: 16px;
  }
  
  .pages-grid {
    grid-template-columns: repeat(auto-fill, minmax(65px, 1fr));
    gap: 8px;
    max-height: 160px;
  }
  
  .pages-overview h5, .pages-selection-section h5, .qr-size-controls h5 {
    font-size: 0.9rem;
    margin-bottom: 16px;
  }
}

@media (max-width: 1199px) and (min-width: 1024px) {
  .main-content-grid {
    grid-template-columns: 1fr 240px;
    gap: 16px;
    padding: 16px;
  }
  
  .controls-panel {
    max-width: 220px;
  }
  
  .pages-overview, .pages-selection-section, .qr-size-controls {
    padding: 14px;
  }
  
  .pages-grid {
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
    gap: 6px;
    max-height: 140px;
  }
  
  .pages-overview h5, .pages-selection-section h5, .qr-size-controls h5 {
    font-size: 0.85rem;
    margin-bottom: 14px;
  }
  
  .page-label {
    font-size: 9px;
  }
}

@media (max-width: 1023px) {
  .main-content-grid {
    grid-template-columns: 1fr 220px;
    gap: 12px;
    padding: 12px;
  }
  
  .controls-panel {
    max-width: 200px;
  }
  
  .pages-overview, .pages-selection-section, .qr-size-controls {
    padding: 12px;
  }
  
  .pages-grid {
    grid-template-columns: repeat(auto-fill, minmax(55px, 1fr));
    gap: 5px;
    max-height: 120px;
  }
  
  .pages-overview h5, .pages-selection-section h5, .qr-size-controls h5 {
    font-size: 0.8rem;
    margin-bottom: 12px;
  }
  
  .page-label {
    font-size: 8px;
  }
}

@media (max-width: 768px) {
  .preview-modal-overlay {
    padding: 12px;
  }
  
  .preview-modal {
    width: 95%;
    max-height: 80%;
  }
  
  .modal-header {
    padding: 20px;
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .header-content {
    flex-direction: column;
    gap: 12px;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .footer-actions {
    flex-direction: column;
  }
  
  .footer-btn {
    width: 100%;
  }
  
  .pdf-iframe {
    min-height: 400px;
  }

  .main-content-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 20px;
  }
  
  .controls-panel {
    order: -1;
  }
  
  .size-options {
    gap: 6px;
  }
  
  .size-option {
    padding: 12px 8px;
  }
  
  .action-btn {
    padding: 12px 16px;
    min-height: 44px;
    font-size: 0.85rem;
  }

  .signature-upload-section {
    padding: 24px 20px;
    margin-bottom: 24px;
  }

  .upload-zone {
    padding: 32px 20px;
  }

  .upload-label i {
    font-size: 2.5rem;
  }
}

@media (max-width: 480px) {
  .signature-upload-section,
  .main-content-grid {
    padding: 16px;
  }

  .upload-zone {
    padding: 24px 16px;
  }

  .document-container {
    padding: 16px;
  }

  .preview-header-section {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .page-navigation {
    align-self: flex-end;
  }

  .action-btn {
    padding: 10px 14px;
    min-height: 40px;
    font-size: 0.8rem;
  }
}

/* Mode sombre (optionnel) */
@media (prefers-color-scheme: dark) {
  :root {
    --primary-color: #60a5fa;
    --primary-dark: #3b82f6;
    --accent-color: #34d399;
    --text-color: #f9fafb;
    --text-secondary: #d1d5db;
    --text-muted: #9ca3af;
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --bg-light: #374151;
    --border-color: #4b5563;
  }

  .preview-modal {
    background: rgba(31, 41, 59, 0.95);
    backdrop-filter: blur(12px);
  }

  .loading-content,
  .error-content,
  .fallback-content {
    background: rgba(15, 23, 42, 0.9);
  }

  .pdf-wrapper {
    background: rgba(255, 255, 255, 0.98);
  }
}
</style>
