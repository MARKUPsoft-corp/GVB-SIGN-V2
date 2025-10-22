# 📋 Système de Signature de Documents - Documentation

## 🎯 Vue d'ensemble

Ce système permet à un chef d'organisation de signer un document qui lui a été assigné dans un workflow hiérarchique. Le processus récupère automatiquement toutes les données nécessaires de la base de données, effectue la signature cryptographique, et prépare le document pour l'étape suivante.

---

## 🔄 Flux de Signature Complet

### **Étape 1 : Initialisation**
Le chef clique sur le bouton "Signer" pour un document dans son tableau de bord.

### **Étape 2 : Vérifications préalables**
1. ✅ Vérifier qu'un certificat valide est disponible en sessionStorage
2. ✅ Vérifier que l'utilisateur est autorisé à signer ce document
3. ✅ Demander confirmation à l'utilisateur

### **Étape 3 : Récupération des données (DocumentSigningService)**

#### 3.1 Document Préparation
```javascript
// API: GET /api/signatures/document-preparation/{id}/
{
  id: "uuid",
  document_id: "doc_xxx",
  organization: {...},
  prepared_by: {...},
  current_signer: {...},  // Le chef actuel
  
  // Fichiers
  original_document: "url/to/original.pdf",
  current_document: "url/to/current.pdf",  // Avec signatures partielles
  
  // Configuration
  elements_configuration: {...},
  qr_code_x, qr_code_y, qr_code_size,
  signature_x, signature_y, signature_width, signature_height,
  page_mode, applied_pages,
  
  // Workflow
  signature_workflow: [...],
  current_step: 1,
  total_steps: 3,
  status: 'in_progress'
}
```

#### 3.2 Téléchargement du PDF
```javascript
// Le PDF actuel avec ou sans signatures partielles
const pdfUrl = documentPreparation.current_document || documentPreparation.original_document
const pdfData = await fetch(pdfUrl).then(r => r.arrayBuffer())
```

#### 3.3 Configuration des éléments
```javascript
{
  qr_code: {
    x: 85,    // Position en %
    y: 10,    // Position en %
    size: 'medium',
    mode: 'all',
    pages: [],
    positions: {}
  },
  signature: {
    x: 50,
    y: 80,
    width: 200,
    height: 100,
    mode: 'all',
    pages: [],
    positions: {}
  }
}
```

#### 3.4 Certificat et clés cryptographiques
```javascript
// Chargé depuis sessionStorage
{
  certificateInfo: {
    subject: { commonName, organization, ... },
    validity: { isValid: true, notBefore, notAfter }
  },
  privateKey: forge.pki.PrivateKey,  // Clé privée pour signer
  publicKey: forge.pki.PublicKey,    // Clé publique
  privateKeyPem: "-----BEGIN PRIVATE KEY-----...",
  publicKeyPem: "-----BEGIN PUBLIC KEY-----..."
}
```

#### 3.5 Informations du workflow
```javascript
{
  workflow: [...],
  currentStep: 1,
  totalSteps: 3,
  currentSigner: { user_id, user_name, role },
  nextSigner: { user_id, user_name, role },
  isLastStep: false,
  progressPercentage: 33
}
```

---

### **Étape 4 : Préparation des métadonnées**
```javascript
const metadata = {
  qr_position: {
    x: 85, y: 10, size: 'medium',
    mode: 'all', pages: [], positions: {}
  },
  signature_position: {
    signature_image: null,  // Pas d'image pour le chef
    positions: { default: { x: 50, y: 80 } },
    pages: 'all',
    signature_size: 50
  },
  workflow_info: {
    current_step: 1,
    total_steps: 3,
    is_last_step: false,
    signer_info: { user_id, user_name, user_email, role }
  }
}
```

---

### **Étape 5 : Signature du document (SignatureService)**

#### 5.1 Calcul du hash SHA-256
```javascript
const originalHash = signatureService.calculateDocumentHash(pdfData)
// Ex: "a3f5b2c8d1e4f7a9b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5f8a1b4c7d0e3f6a9"
```

#### 5.2 Signature cryptographique
```javascript
const signature = signatureService.signDocument(pdfData, privateKey)
// Signature RSA avec SHA-256 en base64
```

#### 5.3 Génération du QR Code
```javascript
const documentId = generateDocumentId()  // UUID unique
const qrCode = await generateQRCode(documentId)
```

#### 5.4 Ajout du QR Code au PDF
```javascript
const pdfWithQR = await addQRCodeToPDF(pdfData, documentId, qrPosition)
```

#### 5.5 Résultat de la signature
```javascript
{
  success: true,
  documentId: "uuid-generated",
  originalHash: "sha256-hash",
  signature: "base64-signature",
  publicKeyPem: "-----BEGIN PUBLIC KEY-----...",
  signedDocument: Uint8Array,  // PDF avec QR code
  executionTime: 2.5,
  timestamp: "2024-01-15T10:30:00Z"
}
```

---

## 🛠️ Services Utilisés

### 1. **DocumentSigningService** (Orchestrateur)
Fichier : `/frontend/services/DocumentSigningService.js`

**Rôle** : Orchestrer tout le processus de signature
- Récupérer les données de la BDD
- Préparer les métadonnées
- Appeler SignatureService
- Gérer les erreurs

**Méthodes principales** :
```javascript
// Méthode principale - Tout en un
await documentSigningService.signDocument(preparationId, organizationId, userInfo)

// Méthodes internes
fetchSigningData()              // Récupère toutes les données
fetchDocumentPreparation()      // API call pour le document
downloadCurrentPDF()            // Télécharge le PDF
extractElementsConfiguration()  // Extrait la config QR + Signature
loadCertificateData()          // Charge le certificat
extractWorkflowInfo()          // Extrait les infos workflow
prepareSignatureMetadata()     // Prépare les métadonnées
canUserSignDocument()          // Vérifie les permissions
hasCertificate()               // Vérifie le certificat
```

---

### 2. **SignatureService** (Signature cryptographique)
Fichier : `/frontend/services/SignatureService.js`

**Rôle** : Effectuer la signature cryptographique et modifier le PDF
- Calculer le hash SHA-256
- Signer avec la clé privée
- Générer et ajouter le QR Code
- Ajouter l'image de signature (si applicable)

**Méthodes principales** :
```javascript
signDocumentComplete(pdfData, privateKey, publicKey, metadata)
calculateDocumentHash(pdfData)
signDocument(pdfData, privateKey)
generateQRCode(documentId, options)
addQRCodeToPDF(pdfData, documentId, qrPosition)
addSignatureImageToPDF(pdfData, signatureImage, positions)
```

---

### 3. **CertificateService** (Gestion des certificats)
Fichier : `/frontend/services/CertificateService.js`

**Rôle** : Gérer les certificats numériques
- Décoder les certificats PKCS#12
- Extraire les clés publiques/privées
- Stocker en sessionStorage
- Vérifier la validité

**Méthodes principales** :
```javascript
decodeCertificate(file, password)
loadFromSessionStorage()
saveToSessionStorage()
hasCertificate()
canUseCertificate()
getPrivateKeyPem()
getPublicKeyPem()
```

---

## 📊 Données Récupérées de la Base de Données

| Donnée | Source API | Table BDD | Utilisation |
|--------|-----------|-----------|-------------|
| DocumentPreparation | `/api/signatures/document-preparation/{id}/` | `signatures_documentpreparation` | Document à signer |
| PDF actuel | FileField → URL | Fichier sur disque | Fichier à modifier |
| Configuration QR | JSONField `elements_configuration` | `signatures_documentpreparation` | Position du QR code |
| Configuration Signature | JSONField `elements_configuration` | `signatures_documentpreparation` | Position de la signature |
| Workflow | JSONField `signature_workflow` | `signatures_documentpreparation` | Ordre des signataires |
| Étape actuelle | `current_step` | `signatures_documentpreparation` | Progression |
| Organisation | ForeignKey | `organizations_organization` | Contexte |
| Signataire actuel | ForeignKey `current_signer` | `authentication_user` | Vérification permission |
| Certificat | sessionStorage (frontend) | N/A | Signature cryptographique |

---

## 🔐 Sécurité

### Vérifications effectuées
1. ✅ Utilisateur authentifié (session Django)
2. ✅ Certificat valide et non expiré
3. ✅ Utilisateur est le signataire actuel du document
4. ✅ Document dans un état signable (`prepared`, `in_progress`)
5. ✅ Hash SHA-256 du document pour intégrité
6. ✅ Signature RSA avec clé privée du certificat

### Données sensibles
- ⚠️ Clés privées stockées en **sessionStorage** (temporaire, disparaît à la fermeture)
- ⚠️ **NE JAMAIS** envoyer la clé privée au backend
- ✅ Seule la signature (résultat) et la clé publique sont envoyées

---

## 💡 Exemple d'utilisation

```vue
<template>
  <button @click="signDocument(document)">
    <i class="bi bi-pen"></i>
    Signer
  </button>
</template>

<script setup>
import { DocumentSigningService } from '../../services/DocumentSigningService'
import { useAuthStore } from '../../stores/auth'

const documentSigningService = new DocumentSigningService()
const authStore = useAuthStore()

const signDocument = async (document) => {
  // 1. Initialiser
  documentSigningService.initialize()
  
  // 2. Vérifier le certificat
  if (!documentSigningService.hasCertificate()) {
    alert('Importez d\'abord un certificat')
    return
  }
  
  // 3. Vérifier les permissions
  if (!documentSigningService.canUserSignDocument(document, authStore.user.id)) {
    alert('Non autorisé')
    return
  }
  
  // 4. SIGNER (tout est automatique !)
  const result = await documentSigningService.signDocument(
    document.id,
    organizationId,
    {
      id: authStore.user.id,
      full_name: authStore.user.full_name,
      email: authStore.user.email,
      role: userRole
    }
  )
  
  console.log('✅ Document signé !', result)
  
  // 5. Le résultat contient :
  // - documentPreparation
  // - signatureResult (documentId, hash, signature, PDF signé)
  // - metadata (configuration)
  // - workflowInfo (prochaine étape, progression)
}
</script>
```

---

## 🚀 Prochaines étapes (À implémenter)

Cette implémentation s'arrête juste **après la signature**. Les prochaines étapes seraient :

1. **Enregistrement dans la BDD**
   - Envoyer le résultat au backend
   - Mettre à jour `DocumentSignatureStep`
   - Avancer le workflow (`advance_workflow`)
   - Mettre à jour `current_document`

2. **Gestion du workflow**
   - Notifier le prochain signataire
   - Créer `DocumentSignature` finale si dernière étape
   - Gérer les rejets

3. **Optimisations**
   - Cache des documents
   - Signature en lot
   - Compression des PDFs

---

## 📝 Notes importantes

- ⚠️ Le certificat DOIT être importé avant de signer (sessionStorage)
- ⚠️ Un seul document peut être signé à la fois par cette méthode
- ⚠️ La signature est **irréversible** une fois envoyée au backend
- ✅ Le système gère automatiquement les signatures partielles (workflow)
- ✅ Le QR code contient l'ID unique du document pour traçabilité

---

**Créé le** : 22 octobre 2025  
**Version** : 1.0  
**Status** : ✅ Signature implémentée - ⏳ Enregistrement à implémenter

