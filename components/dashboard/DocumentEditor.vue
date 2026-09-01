<template>
  <div class="document-editor">
    <!-- Header avec titre du document et boutons de contrôle -->
    <div class="editor-header">
      <div class="editor-header-left">
        <span class="document-status">{{ documentStatus }}</span>
      </div>
      
      <div class="editor-header-center">
        <div class="document-title-section">
          <div class="title-with-badge">
            <input 
              v-model="documentTitle" 
              class="document-title-input"
              placeholder="Nom du document..."
              :style="{ width: titleWidth + 'px' }"
              ref="titleInput"
              @input="adjustTitleWidth"
            />
          </div>
        </div>
      </div>
      <div class="editor-header-controls">
        <button class="control-btn minimize-btn" title="Réduire">
          <i class="bi bi-dash"></i>
        </button>
        <button class="control-btn maximize-btn" title="Agrandir">
          <i class="bi bi-square"></i>
        </button>
        <button class="control-btn close-btn" title="Fermer" @click="$emit('back')">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <!-- Barre d'outils de l'éditeur -->
    <div class="editor-toolbar">
      <div class="toolbar-section">
        <!-- Formatage du texte -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="formatText('bold')" :class="{ active: isActive('bold') }">
            <i class="bi bi-type-bold"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('italic')" :class="{ active: isActive('italic') }">
            <i class="bi bi-type-italic"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('underline')" :class="{ active: isActive('underline') }">
            <i class="bi bi-type-underline"></i>
          </button>
        </div>

        <div class="toolbar-separator"></div>

        <!-- Alignement -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="formatText('align', 'left')" :class="{ active: isActive('align', 'left') }">
            <i class="bi bi-text-left"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('align', 'center')" :class="{ active: isActive('align', 'center') }">
            <i class="bi bi-text-center"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('align', 'right')" :class="{ active: isActive('align', 'right') }">
            <i class="bi bi-text-right"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('align', 'justify')" :class="{ active: isActive('align', 'justify') }">
            <i class="bi bi-justify"></i>
          </button>
        </div>

        <div class="toolbar-separator"></div>

        <!-- Listes -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="formatText('list', 'ordered')" :class="{ active: isActive('list', 'ordered') }">
            <i class="bi bi-list-ol"></i>
          </button>
          <button class="toolbar-btn" @click="formatText('list', 'bullet')" :class="{ active: isActive('list', 'bullet') }">
            <i class="bi bi-list-ul"></i>
          </button>
        </div>

        <div class="toolbar-separator"></div>

        <!-- Insertion -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="insertImage">
            <i class="bi bi-image"></i>
          </button>
          <button class="toolbar-btn" @click="insertTable">
            <i class="bi bi-table"></i>
          </button>
          <button class="toolbar-btn" @click="insertLink">
            <i class="bi bi-link-45deg"></i>
          </button>
        </div>

        <div class="toolbar-separator"></div>

        <!-- Actions -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="undo">
            <i class="bi bi-arrow-counterclockwise"></i>
          </button>
          <button class="toolbar-btn" @click="redo">
            <i class="bi bi-arrow-clockwise"></i>
          </button>
        </div>

        <div class="toolbar-separator"></div>

        <!-- Import -->
        <div class="toolbar-group">
          <button class="toolbar-btn" @click="importDocument" title="Importer un document Word">
            <i class="bi bi-file-earmark-arrow-up"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Zone d'édition -->
    <div class="editor-container">
      <div class="editor-page">
        <div id="quill-editor" class="editor-content"></div>
      </div>
    </div>

    <!-- Barre de statut -->
    <div class="editor-status-bar">
      <div class="status-left">
        <span class="word-count">{{ wordCount }} mots</span>
        <span class="character-count">{{ characterCount }} caractères</span>
      </div>
      <div class="status-right">
        <span class="save-status">{{ saveStatus }}</span>
        <span class="zoom-level">{{ zoomLevel }}%</span>
      </div>
    </div>
    
    <!-- Input file caché pour l'import -->
    <input 
      ref="fileInput" 
      type="file" 
      accept=".docx,.doc" 
      style="display: none;" 
      @change="handleFileImport"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

// Props et événements
const emit = defineEmits(['back', 'save', 'share'])

// État du document
const documentTitle = ref('Nouveau document')
const documentStatus = ref('Brouillon')
const wordCount = ref(0)
const characterCount = ref(0)
const saveStatus = ref('Sauvegardé')
const zoomLevel = ref(100)
const titleWidth = ref(200)
const titleInput = ref(null)
const fileInput = ref(null)

// Instance Quill
let quill = null
let Quill = null

// Initialisation de l'éditeur
onMounted(async () => {
  // Import dynamique côté client uniquement
  if (process.client) {
    try {
      const QuillModule = await import('quill')
      Quill = QuillModule.default
      
      // Import du CSS
      await import('quill/dist/quill.snow.css')
      
      await nextTick()
      
      // Configuration de Quill
      quill = new Quill('#quill-editor', {
    theme: 'snow',
    modules: {
      toolbar: false, // On utilise notre propre toolbar
      history: {
        delay: 1000,
        maxStack: 50,
        userOnly: true
      }
    },
    formats: [
      'bold', 'italic', 'underline', 'strike',
      'align', 'list', 'indent',
      'size', 'header',
      'color', 'background',
      'font', 'code-block', 'blockquote',
      'link', 'image', 'video'
    ],
    placeholder: 'Commencez à écrire votre document...'
  })

  // Contenu initial pour documents DOC/DOCX
  quill.setContents([
    { insert: 'Éditeur de Documents Microsoft Word\n', attributes: { header: 1, align: 'center' } },
    { insert: '\n' },
    { insert: 'Cet éditeur est optimisé pour les fichiers DOC et DOCX.\n\n' },
    { insert: 'Fonctionnalités compatibles Word :\n', attributes: { bold: true } },
    { insert: '• Formatage de texte (gras, italique, souligné)\n' },
    { insert: '• Alignement et justification\n' },
    { insert: '• Listes et puces\n' },
    { insert: '• Tableaux et images\n' },
    { insert: '• En-têtes et pieds de page\n' },
    { insert: '• Styles de paragraphe\n\n' },
    { insert: 'Votre document sera sauvegardé au format DOCX.\n\n' },
    { insert: 'Commencez à éditer votre document Word ci-dessous...\n' }
  ])

  // Écouter les changements de contenu
  quill.on('text-change', () => {
    updateWordCount()
    updateSaveStatus()
  })

      // Mise à jour initiale du compteur de mots
      updateWordCount()
      
      // Ajuster la largeur du titre initial
      nextTick(() => {
        adjustTitleWidth()
      })
    } catch (error) {
      console.error('Erreur lors de l\'initialisation de l\'éditeur:', error)
    }
  }
})

// Nettoyage
onUnmounted(() => {
  if (quill) {
    quill = null
  }
})

// Fonctions de formatage
const formatText = (format, value = true) => {
  if (!quill || !process.client) return
  
  if (format === 'align') {
    quill.format('align', value === 'left' ? false : value)
  } else if (format === 'list') {
    quill.format('list', value)
  } else {
    quill.format(format, value)
  }
}

// Vérifier si un format est actif
const isActive = (format, value = true) => {
  if (!quill || !process.client) return false
  
  const selection = quill.getSelection()
  if (!selection) return false
  
  const formats = quill.getFormat(selection)
  
  if (format === 'align') {
    return formats.align === (value === 'left' ? undefined : value)
  } else if (format === 'list') {
    return formats.list === value
  } else {
    return !!formats[format]
  }
}

// Actions de la barre d'outils
const insertImage = () => {
  if (!quill || !process.client) return
  const url = prompt('URL de l\'image:')
  if (url) {
    const range = quill.getSelection()
    quill.insertEmbed(range.index, 'image', url)
  }
}

const insertTable = () => {
  if (!quill || !process.client) return
  // Insertion d'un tableau simple
  const tableHTML = `
    <table style="border-collapse: collapse; width: 100%;">
      <tr>
        <td style="border: 1px solid #ccc; padding: 8px;">Cellule 1</td>
        <td style="border: 1px solid #ccc; padding: 8px;">Cellule 2</td>
      </tr>
      <tr>
        <td style="border: 1px solid #ccc; padding: 8px;">Cellule 3</td>
        <td style="border: 1px solid #ccc; padding: 8px;">Cellule 4</td>
      </tr>
    </table>
  `
  const range = quill.getSelection()
  quill.clipboard.dangerouslyPasteHTML(range.index, tableHTML)
}

const insertLink = () => {
  if (!quill || !process.client) return
  const url = prompt('URL du lien:')
  if (url) {
    const range = quill.getSelection()
    if (range.length > 0) {
      quill.format('link', url)
    } else {
      quill.insertText(range.index, url, 'link', url)
    }
  }
}

const undo = () => {
  if (quill && process.client) quill.history.undo()
}

const redo = () => {
  if (quill && process.client) quill.history.redo()
}

// Fonctions utilitaires
const updateWordCount = () => {
  if (!quill || !process.client) return
  
  const text = quill.getText()
  const words = text.trim().split(/\s+/).filter(word => word.length > 0)
  wordCount.value = words.length
  characterCount.value = text.length
}

const updateSaveStatus = () => {
  saveStatus.value = 'Non sauvegardé'
  // Simulation de sauvegarde automatique
  setTimeout(() => {
    saveStatus.value = 'Sauvegardé'
  }, 2000)
}

// Actions du header
const saveDocument = () => {
  if (!quill || !process.client) return
  const content = quill.getContents()
  console.log('Sauvegarde du document DOCX:', { title: documentTitle.value, content })
  emit('save', { title: documentTitle.value, content, format: 'docx' })
  saveStatus.value = 'Sauvegardé au format DOCX'
}

const shareDocument = () => {
  console.log('Partage du document:', documentTitle.value)
  emit('share', { title: documentTitle.value })
}

// Fonction d'import de document
const importDocument = () => {
  if (process.client && fileInput.value) {
    fileInput.value.click()
  }
}

// Gestion de l'import de fichier
const handleFileImport = async (event) => {
  if (!process.client) return
  
  const file = event.target.files[0]
  if (!file) return
  
  // Vérifier le type de fichier
  if (!file.name.toLowerCase().endsWith('.docx') && !file.name.toLowerCase().endsWith('.doc')) {
    alert('Veuillez sélectionner un fichier Word (.docx ou .doc)')
    return
  }
  
  try {
    // Mettre à jour le titre avec le nom du fichier
    const fileName = file.name.replace(/\.(docx|doc)$/i, '')
    documentTitle.value = fileName
    
    // Importer mammoth.js dynamiquement
    const mammoth = await import('mammoth')
    
    // Lire le fichier comme ArrayBuffer
    const arrayBuffer = await readFileAsArrayBuffer(file)
    
    // Convertir le document Word en HTML
    const result = await mammoth.default.convertToHtml({ arrayBuffer })
    
    // Insérer le HTML dans l'éditeur Quill
    if (quill) {
      // Vider l'éditeur d'abord
      quill.setText('')
      
      // Insérer le contenu HTML
      quill.clipboard.dangerouslyPasteHTML(result.value)
      
      // Mettre à jour les compteurs
      updateWordCount()
      updateSaveStatus()
    }
    
    // Mettre à jour le statut
    documentStatus.value = 'Document importé'
    
    console.log('Document Word importé avec succès:', fileName)
    
  } catch (error) {
    console.error('Erreur lors de l\'import:', error)
    
    alert('Erreur lors de l\'import du document. Vérifiez que le fichier est un document Word valide.')
  }
  
  // Réinitialiser l'input file
  event.target.value = ''
}

// Fonction utilitaire pour lire un fichier comme ArrayBuffer
const readFileAsArrayBuffer = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = (e) => reject(e)
    reader.readAsArrayBuffer(file)
  })
}

// Fonction pour ajuster la largeur du titre
const adjustTitleWidth = () => {
  if (process.client && titleInput.value) {
    const input = titleInput.value
    const text = input.value || input.placeholder
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    
    // Utiliser la même police que le placeholder si le champ est vide
    const computedStyle = window.getComputedStyle(input)
    const fontSize = input.value ? '1.2rem' : '1.1rem'
    const fontWeight = input.value ? '600' : '400'
    context.font = `${fontWeight} ${fontSize} ${computedStyle.fontFamily}`
    
    const textWidth = context.measureText(text).width
    titleWidth.value = Math.max(150, textWidth + 20) // Minimum 150px, +20px pour le padding
  }
}
</script>

<style scoped>
/* VARIABLES CSS */
:root {
  --primary-blue: #0066cc;
  --text-dark: #2c3e50;
  --background-light: #f8f9fa;
  --shadow-light: rgba(0, 102, 204, 0.1);
}

/* CONTENEUR PRINCIPAL */
.document-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f8f9fa;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* HEADER */
.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  box-shadow: 0 4px 20px rgba(0, 102, 204, 0.1);
  position: relative;
  z-index: 10;
  border-radius: 16px 16px 0 0;
}



.editor-header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.editor-header-center {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.document-title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.title-with-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.document-title-input {
  font-size: 1.2rem;
  font-weight: 600;
  border: none;
  background: transparent;
  padding: 0.5rem 0;
  color: var(--text-dark);
  min-width: 150px;
  border-bottom: 2px solid transparent;
  transition: width 0.1s ease;
}

.document-title-input:focus {
  outline: none;
  border-bottom-color: var(--primary-blue);
}

.document-title-input::placeholder {
  color: #6c757d;
  font-weight: 400;
  font-size: 1.1rem;
}

.document-status {
  font-size: 0.75rem;
  color: var(--primary-blue);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 0.2rem 0.6rem;
  background: rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  display: inline-block;
  width: fit-content;
  white-space: nowrap;
}

.editor-header-controls {
  display: flex;
  align-items: center;
  gap: 0;
  position: absolute;
  top: 0;
  right: 20px;
  height: 100%;
  transform: translateY(-10px);
}

.format-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.6rem;
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border-radius: 16px;
  font-size: 0.7rem;
  font-weight: 600;
  border: 1px solid rgba(0, 102, 204, 0.2);
}

.format-badge i {
  font-size: 0.85rem;
}

.control-btn {
  width: 16px;
  height: 16px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: transparent;
  font-size: 0.8rem;
  position: relative;
  margin: 0 6px;
}

.minimize-btn {
  background: #ffbd2e;
}

.maximize-btn {
  background: #28ca42;
}

.close-btn {
  background: #ff5f57;
}

.control-btn:hover {
  filter: brightness(0.8);
}

.control-btn:hover i {
  color: rgba(0, 0, 0, 0.6);
}

/* BOUTONS */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  border: 1px solid #e9ecef;
  background: white;
  color: #495057;
  cursor: pointer;
}

.btn:hover {
  background: rgba(0, 102, 204, 0.05);
  border-color: var(--primary-blue);
  color: var(--primary-blue);
  transform: translateY(-1px);
}

.btn-outline-primary {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  border-color: rgba(0, 102, 204, 0.3);
}

.btn-outline-primary:hover {
  background: rgba(0, 102, 204, 0.15);
  border-color: var(--primary-blue);
}

.btn-outline-secondary {
  background: white;
  color: #495057;
  border-color: #e9ecef;
}

.btn-outline-secondary:hover {
  background: rgba(0, 102, 204, 0.05);
  border-color: var(--primary-blue);
  color: var(--primary-blue);
}

.btn-primary {
  background: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
}

.btn-primary:hover {
  background: #0056b3;
  border-color: #0056b3;
}

/* TOOLBAR */
.editor-toolbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 102, 204, 0.1);
  padding: 0.4rem 2rem;
  position: relative;
  z-index: 5;
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  justify-content: center;
}

.toolbar-group {
  display: flex;
  gap: 0.4rem;
  padding: 0.4rem;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 10px;
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.toolbar-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #495057;
  font-size: 0.9rem;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.toolbar-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.toolbar-btn:hover::before {
  left: 100%;
}

.toolbar-btn:hover {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
  border-color: rgba(0, 102, 204, 0.3);
}

.toolbar-btn.active {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary-blue);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.2);
  border-color: rgba(0, 102, 204, 0.3);
}

.toolbar-separator {
  width: 2px;
  height: 24px;
  background: linear-gradient(180deg, transparent, #dee2e6, transparent);
  border-radius: 1px;
}

/* ÉDITEUR - FORMAT A4 */
.editor-container {
  flex: 1;
  padding: 3rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  position: relative;
}

.editor-page {
  width: 210mm; /* Largeur A4 */
  min-height: 297mm; /* Hauteur A4 */
  background: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border-radius: 16px;
  overflow: visible;
  position: relative;
  border: 1px solid rgba(0, 102, 204, 0.1);
  margin: 1rem auto 4rem auto;
  transform-origin: top center;
  transition: transform 0.3s ease;
  z-index: 1;
}

.editor-page:hover {
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.2);
}

.editor-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-blue), #4facfe);
  border-radius: 16px 16px 0 0;
}

.editor-content {
  width: 100%;
  height: 100%;
  padding: 25mm 20mm; /* Marges A4 standard */
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 12pt; /* Taille standard pour A4 */
  line-height: 1.6;
  color: var(--text-dark);
  background: white;
  position: relative;
  box-sizing: border-box;
  min-height: 247mm; /* Hauteur A4 moins les marges */
  border-radius: 0 0 16px 16px;
}

/* BARRE DE STATUT */
.editor-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(0, 102, 204, 0.1);
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
  border-radius: 0 0 16px 16px;
}

.status-left,
.status-right {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.word-count,
.character-count,
.save-status,
.zoom-level {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 20px;
  border: 1px solid rgba(0, 102, 204, 0.1);
  font-size: 0.85rem;
  font-weight: 600;
}

.save-status {
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  .editor-page {
    width: 90vw;
    max-width: 210mm;
  }
}

@media (max-width: 768px) {
  .editor-header {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .editor-header-left,
  .editor-header-right {
    width: 100%;
    justify-content: center;
  }

  .document-title-input {
    min-width: 250px;
    text-align: center;
    font-size: 1.25rem;
  }

  .editor-toolbar {
    padding: 0.75rem 1rem;
    overflow-x: auto;
  }

  .toolbar-section {
    min-width: 700px;
    justify-content: flex-start;
  }

  .editor-container {
    padding: 1rem 0.5rem;
  }

  .editor-page {
    width: calc(100vw - 1rem);
    min-height: auto;
    margin: 1rem auto;
    transform: none;
  }

  .editor-page:hover {
    transform: none;
  }

  .editor-content {
    padding: 15mm 10mm;
    font-size: 11pt;
    min-height: 60vh;
  }

  .editor-status-bar {
    padding: 0.75rem 1rem;
    flex-direction: column;
    gap: 0.75rem;
  }

  .status-left,
  .status-right {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .editor-page {
    margin: 0.5rem auto;
    width: calc(100vw - 1rem);
  }

  .editor-content {
    padding: 10mm 8mm;
    font-size: 10pt;
  }

  .toolbar-section {
    min-width: 600px;
  }
}

/* STYLES QUILL PERSONNALISÉS */
:deep(.ql-editor) {
  border: none !important;
  padding: 0 !important;
  position: relative;
  z-index: 1;
  font-size: 12pt;
  line-height: 1.6;
  color: var(--text-dark);
}

:deep(.ql-editor.ql-blank::before) {
  color: #6c757d;
  font-style: italic;
  font-size: 12pt;
  opacity: 0.7;
}

:deep(.ql-editor h1) {
  font-size: 18pt;
  font-weight: 700;
  margin: 24pt 0 12pt 0;
  color: #1a1a1a;
  border-bottom: 2pt solid var(--primary-blue);
  padding-bottom: 6pt;
}

:deep(.ql-editor h2) {
  font-size: 16pt;
  font-weight: 600;
  margin: 18pt 0 9pt 0;
  color: var(--text-dark);
  border-bottom: 1pt solid rgba(0, 102, 204, 0.3);
  padding-bottom: 4pt;
}

:deep(.ql-editor h3) {
  font-size: 14pt;
  font-weight: 600;
  margin: 14pt 0 7pt 0;
  color: #34495e;
}

:deep(.ql-editor p) {
  margin: 6pt 0;
  text-align: justify;
}

:deep(.ql-editor ul),
:deep(.ql-editor ol) {
  margin: 6pt 0;
  padding-left: 24pt;
}

:deep(.ql-editor li) {
  margin: 3pt 0;
}

:deep(.ql-editor blockquote) {
  border-left: 3pt solid var(--primary-blue);
  padding-left: 18pt;
  margin: 12pt 0;
  font-style: italic;
  color: #495057;
  background: rgba(0, 102, 204, 0.03);
  padding: 9pt 18pt;
  border-radius: 0 6pt 6pt 0;
}

:deep(.ql-editor a) {
  color: var(--primary-blue);
  text-decoration: none;
  border-bottom: 0.5pt solid var(--primary-blue);
  transition: all 0.3s ease;
}

:deep(.ql-editor a:hover) {
  color: #4facfe;
  border-bottom-color: #4facfe;
}

:deep(.ql-editor strong) {
  font-weight: 700;
  color: #1a1a1a;
}

:deep(.ql-editor em) {
  font-style: italic;
  color: #495057;
}

:deep(.ql-editor table) {
  border-collapse: collapse;
  width: 100%;
  margin: 12pt 0;
  font-size: 11pt;
}

:deep(.ql-editor table td),
:deep(.ql-editor table th) {
  border: 1pt solid #dee2e6;
  padding: 6pt 9pt;
  text-align: left;
}

:deep(.ql-editor table th) {
  background: rgba(0, 102, 204, 0.05);
  font-weight: 600;
  color: var(--text-dark);
}

:deep(.ql-editor img) {
  max-width: 100%;
  height: auto;
  margin: 12pt 0;
  border-radius: 4pt;
  box-shadow: 0 2pt 8pt rgba(0, 0, 0, 0.1);
}

/* ANIMATIONS */
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

.document-editor {
  animation: fadeInUp 0.6s ease-out;
}

.toolbar-btn {
  animation: fadeInUp 0.4s ease-out;
}

.toolbar-btn:nth-child(1) { animation-delay: 0.1s; }
.toolbar-btn:nth-child(2) { animation-delay: 0.2s; }
.toolbar-btn:nth-child(3) { animation-delay: 0.3s; }
.toolbar-btn:nth-child(4) { animation-delay: 0.4s; }
.toolbar-btn:nth-child(5) { animation-delay: 0.5s; }

/* SCROLLBAR PERSONNALISÉE */
.editor-container::-webkit-scrollbar {
  width: 8px;
}

.editor-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.editor-container::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--primary-blue), #4facfe);
  border-radius: 4px;
}

.editor-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #4facfe, var(--primary-blue));
}

/* STYLES POUR L'IMPRESSION */
@media print {
  .editor-page {
    box-shadow: none;
    border: none;
    margin: 0;
    transform: none;
    width: 210mm;
    height: 297mm;
  }
  
  .editor-content {
    padding: 20mm 15mm;
  }
  
  :deep(.ql-editor) {
    font-size: 12pt;
  }
}
</style>
