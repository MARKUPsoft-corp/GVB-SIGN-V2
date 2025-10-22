# 📋 Exemple de Logs lors de la Signature d'un Document

## Scénario
**Chef** : Emmanuel KANA (emmanuel@example.com)  
**Organisation** : GVB Technologies  
**Document** : Rapport_Mensuel_Janvier_2024.pdf  
**Workflow** : Secrétaire → Chef → Chef+1 → Chef+2  
**Étape actuelle** : Chef (étape 1/3)

---

## 🖥️ Console du Navigateur (Logs Complets)

```javascript
// ═══════════════════════════════════════════════════════════════
// 1️⃣ DÉBUT DU PROCESSUS
// ═══════════════════════════════════════════════════════════════

🖊️ === DÉBUT DE LA SIGNATURE DU DOCUMENT ===
🖊️ Document: Rapport Mensuel Janvier 2024
🖊️ Document ID: 3c8f5b2a-1d4e-4f7a-9b0c-3d6e9f2a5b8c

🔧 Initialisation du DocumentSigningService
🔐 Chargement du certificat depuis sessionStorage
✅ Certificat trouvé: Emmanuel KANA
✅ Validité: 2024-01-01 - 2025-12-31
✅ Statut: Valide

✅ Signature confirmée, début du processus...

👤 Utilisateur: {
  id: 42,
  full_name: "Emmanuel KANA",
  email: "emmanuel@example.com",
  role: "chef"
}


// ═══════════════════════════════════════════════════════════════
// 2️⃣ RÉCUPÉRATION DES DONNÉES DE LA BASE DE DONNÉES
// ═══════════════════════════════════════════════════════════════

✍️ Appel du service de signature...

📥 === RÉCUPÉRATION DES DONNÉES DE SIGNATURE ===
📥 Preparation ID: 3c8f5b2a-1d4e-4f7a-9b0c-3d6e9f2a5b8c
📥 Organization ID: 1


// ─────────────────────────────────────────────────────────────
// 2.1 Récupération du DocumentPreparation
// ─────────────────────────────────────────────────────────────

📡 Récupération du document préparation ID: 3c8f5b2a-1d4e-4f7a-9b0c-3d6e9f2a5b8c

API Call: GET http://127.0.0.1:8000/api/signatures/document-preparation/3c8f5b2a-1d4e-4f7a-9b0c-3d6e9f2a5b8c/
Response Status: 200 OK

✅ Document préparation récupéré: {
  id: "3c8f5b2a-1d4e-4f7a-9b0c-3d6e9f2a5b8c",
  document_id: "doc_a7b3c5d1e9f2",
  document_title: "Rapport Mensuel Janvier 2024",
  original_filename: "Rapport_Mensuel_Janvier_2024.pdf",
  
  organization: {
    id: 1,
    name: "GVB Technologies"
  },
  
  prepared_by: {
    id: 15,
    full_name: "Marie DUBOIS",
    email: "marie@gvb.com",
    role: "secretaire"
  },
  
  current_signer: {
    id: 42,
    full_name: "Emmanuel KANA",
    email: "emmanuel@example.com",
    role: "chef"
  },
  
  original_document: "http://127.0.0.1:8000/media/documents/preparation/original/doc_a7b3c5d1e9f2_original_Rapport_Mensuel_Janvier_2024.pdf",
  current_document: "http://127.0.0.1:8000/media/documents/preparation/current/doc_a7b3c5d1e9f2_current_Rapport_Mensuel_Janvier_2024.pdf",
  
  qr_code_x: 85,
  qr_code_y: 10,
  qr_code_size: "medium",
  signature_x: 50,
  signature_y: 80,
  signature_width: 200,
  signature_height: 100,
  page_mode: "all",
  applied_pages: [],
  
  signature_workflow: [
    {
      step: 1,
      user_id: 42,
      user_name: "Emmanuel KANA",
      user_email: "emmanuel@example.com",
      role: "chef",
      organization_member_id: 23
    },
    {
      step: 2,
      user_id: 56,
      user_name: "Pierre MARTIN",
      user_email: "pierre@gvb.com",
      role: "chef+1",
      organization_member_id: 24
    },
    {
      step: 3,
      user_id: 78,
      user_name: "Sophie BERNARD",
      user_email: "sophie@gvb.com",
      role: "chef+2",
      organization_member_id: 25
    }
  ],
  
  current_step: 0,
  total_steps: 3,
  status: "prepared",
  
  created_at: "2024-01-15T08:30:00Z",
  prepared_at: "2024-01-15T09:15:00Z"
}


// ─────────────────────────────────────────────────────────────
// 2.2 Téléchargement du PDF
// ─────────────────────────────────────────────────────────────

📄 Téléchargement du PDF actuel
📄 URL du PDF: http://127.0.0.1:8000/media/documents/preparation/current/doc_a7b3c5d1e9f2_current_Rapport_Mensuel_Janvier_2024.pdf

Downloading PDF...
Transfer: [##################################################] 100%
Size: 125,847 bytes (122.9 KB)

✅ PDF téléchargé, taille: 125847 octets


// ─────────────────────────────────────────────────────────────
// 2.3 Extraction de la Configuration
// ─────────────────────────────────────────────────────────────

⚙️ Extraction de la configuration des éléments

⚙️ QR Config: {
  x: 85,
  y: 10,
  size: "medium",
  mode: "all",
  pages: [],
  positions: {}
}

⚙️ Signature Config: {
  x: 50,
  y: 80,
  width: 200,
  height: 100,
  mode: "all",
  pages: [],
  positions: {}
}

✅ Configuration des éléments extraite: {
  qr_code: { x: 85, y: 10, size: "medium", mode: "all", pages: [] },
  signature: { x: 50, y: 80, width: 200, height: 100, mode: "all", pages: [] },
  page_mode: "all",
  applied_pages: []
}


// ─────────────────────────────────────────────────────────────
// 2.4 Chargement du Certificat
// ─────────────────────────────────────────────────────────────

🔐 Chargement du certificat

✅ Certificat valide: Emmanuel KANA
✅ Validité: 2024-01-01T00:00:00.000Z - 2025-12-31T23:59:59.000Z
🔐 Clés privée et publique chargées avec succès


// ─────────────────────────────────────────────────────────────
// 2.5 Extraction du Workflow
// ─────────────────────────────────────────────────────────────

📋 Extraction des informations du workflow

📋 Étape actuelle: 1 / 3
📋 Signataire actuel: {
  step: 1,
  user_id: 42,
  user_name: "Emmanuel KANA",
  user_email: "emmanuel@example.com",
  role: "chef"
}
📋 Prochain signataire: {
  step: 2,
  user_id: 56,
  user_name: "Pierre MARTIN",
  user_email: "pierre@gvb.com",
  role: "chef+1"
}

✅ Informations workflow extraites: {
  workflow: [...],
  currentStep: 0,
  totalSteps: 3,
  currentSigner: {...},
  nextSigner: {...},
  isLastStep: false,
  progressPercentage: 33
}

✅ === TOUTES LES DONNÉES RÉCUPÉRÉES AVEC SUCCÈS ===


// ═══════════════════════════════════════════════════════════════
// 3️⃣ PRÉPARATION DES MÉTADONNÉES
// ═══════════════════════════════════════════════════════════════

🔧 ÉTAPE 2: Préparation des métadonnées...

🔧 Préparation des métadonnées de signature

✅ Métadonnées préparées: {
  qr_position: {
    x: 85,
    y: 10,
    size: "medium",
    mode: "all",
    pages: [],
    positions: {}
  },
  signature_position: {
    signature_image: null,
    positions: {
      default: { x: 50, y: 80 }
    },
    pages: "all",
    signature_size: 50
  },
  workflow_info: {
    current_step: 0,
    total_steps: 3,
    is_last_step: false,
    signer_info: {
      user_id: 42,
      user_name: "Emmanuel KANA",
      user_email: "emmanuel@example.com",
      role: "chef"
    }
  }
}


// ═══════════════════════════════════════════════════════════════
// 4️⃣ SIGNATURE DU DOCUMENT
// ═══════════════════════════════════════════════════════════════

✍️ ÉTAPE 3: Signature du document...

=== DÉBUT DE LA SIGNATURE COMPLÈTE ===
Temps de début: 2024-01-15T10:30:25.847Z


// ─────────────────────────────────────────────────────────────
// 4.1 Calcul du Hash
// ─────────────────────────────────────────────────────────────

=== DÉBUT CALCUL HASH ===
Type de documentData: object
Instance de Uint8Array: true
Taille: 125847

Hash MD créé
Uint8Array créé, taille: 125847
Traitement par chunks de 1024 octets...
Chunk 1/123 traité
Chunk 2/123 traité
...
Chunk 123/123 traité
Hash MD mis à jour par chunks

Hash du document calculé: a3f5b2c8d1...
🔐 Hash calculé dans signDocumentComplete: a3f5b2c8d1e4f7a9b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5f8a1b4c7d0e3f6a9

=== FIN CALCUL HASH ===


// ─────────────────────────────────────────────────────────────
// 4.2 Signature Cryptographique
// ─────────────────────────────────────────────────────────────

🔐 DÉBUT DE LA SIGNATURE DU DOCUMENT
📊 Type de documentData: object
📊 Taille du document: 125847
📊 Données converties en Uint8Array, taille: 125847

Création du hash SHA-256 pour signature...
Traitement par chunks de 1024 octets...
🔐 Hash calculé pour signature: a3f5b2c8d1e4f7a9b0...
🔐 Hash complet: a3f5b2c8d1e4f7a9b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5f8a1b4c7d0e3f6a9

Signature avec RSA + SHA-256...
✅ Signature créée avec l'objet digest
🔐 Signature (premiers 50 chars): ZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhF...

Document signé avec succès


// ─────────────────────────────────────────────────────────────
// 4.3 Génération du QR Code
// ─────────────────────────────────────────────────────────────

Ajout du QR code au document
Début du processus d'ajout du QR code au PDF

Taille du QR code: 57.6 points (medium)
Génération du QR code pour le document: 550e8400-e29b-41d4-a716-446655440000

QR Options: {
  errorCorrectionLevel: "H",
  type: "image/png",
  quality: 0.92,
  margin: 4,
  color: { dark: "#000000", light: "#FFFFFF" },
  width: 256
}

QR code généré avec succès
Data URL: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...


// ─────────────────────────────────────────────────────────────
// 4.4 Modification du PDF
// ─────────────────────────────────────────────────────────────

Chargement du PDF avec pdf-lib...
PDF chargé: 5 pages
Traitement des 5 pages du PDF

Application du QR code sur la page 1
Position finale du QR code: x=420, y=25

Application du QR code sur la page 2
Position finale du QR code: x=420, y=25

Application du QR code sur la page 3
Position finale du QR code: x=420, y=25

Application du QR code sur la page 4
Position finale du QR code: x=420, y=25

Application du QR code sur la page 5
Position finale du QR code: x=420, y=25

Sauvegarde du PDF modifié avec le QR code...
QR code contenant l'ID 550e8400-e29b-41d4-a716-446655440000 ajouté au document

Processus d'ajout du QR code terminé avec succès


// ─────────────────────────────────────────────────────────────
// 4.5 Résultat Final
// ─────────────────────────────────────────────────────────────

Signature terminée en 2.53 secondes

=== RÉSULTAT DE LA SIGNATURE ===
{
  success: true,
  documentId: "550e8400-e29b-41d4-a716-446655440000",
  originalHash: "a3f5b2c8d1e4f7a9b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5f8a1b4c7d0e3f6a9",
  signature: "ZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFRQUFBQUVBQ0FZQUFBQi...",
  publicKeyPem: "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\n-----END PUBLIC KEY-----",
  signedDocument: Uint8Array[128453],
  executionTime: 2.53,
  timestamp: "2024-01-15T10:30:28.377Z"
}


// ═══════════════════════════════════════════════════════════════
// 5️⃣ AFFICHAGE DU RÉSULTAT
// ═══════════════════════════════════════════════════════════════

✅ Document signé avec succès!
✅ Document ID: 550e8400-e29b-41d4-a716-446655440000
✅ Hash original: a3f5b2c8d1e4f7a9b0...
✅ Signature: ZGF0YTppbWFnZS9wbmc7YmFzZTY0L...
✅ Temps d'exécution: 2.53 secondes

✅ === SIGNATURE TERMINÉE AVEC SUCCÈS ===

✅ === SIGNATURE RÉUSSIE ===
✅ Résultat: {
  success: true,
  documentPreparation: {...},
  signatureResult: {...},
  metadata: {...},
  workflowInfo: {
    workflow: [...],
    currentStep: 0,
    totalSteps: 3,
    currentSigner: {...},
    nextSigner: {
      user_id: 56,
      user_name: "Pierre MARTIN",
      role: "chef+1"
    },
    isLastStep: false,
    progressPercentage: 33
  },
  message: "Document signé avec succès"
}


// ═══════════════════════════════════════════════════════════════
// 6️⃣ NOTIFICATIONS UTILISATEUR
// ═══════════════════════════════════════════════════════════════

💬 Notification Success:
   Titre: "Document signé avec succès !"
   Message: "Le document "Rapport Mensuel Janvier 2024" a été signé.
   
   Document ID: 550e8400-e29b-41d4-a716-446655440000
   Hash: a3f5b2c8d1e4f7a9b0...
   Temps: 2.53s"

⏭️ Prochain signataire: {
  user_name: "Pierre MARTIN",
  role: "chef+1"
}

💬 Notification Info:
   Titre: "Prochaine étape"
   Message: "Le document va maintenant être envoyé à Pierre MARTIN (chef+1)"


// ═══════════════════════════════════════════════════════════════
// 7️⃣ RAFRAÎCHISSEMENT DE LA LISTE
// ═══════════════════════════════════════════════════════════════

🔄 Rafraîchissement de la liste des documents...

📡 Récupération des documents préparés
API Call: GET http://127.0.0.1:8000/api/signatures/document-preparation/?organization_id=1

✅ Liste rafraîchie: 12 documents trouvés


// ═══════════════════════════════════════════════════════════════
// ✅ FIN DU PROCESSUS
// ═══════════════════════════════════════════════════════════════

Temps total: 3.15 secondes
Statut: SUCCESS ✅
```

---

## 📊 Résumé des Métriques

| Métrique | Valeur |
|----------|--------|
| **Temps total** | 3.15 secondes |
| **Téléchargement PDF** | 0.32 secondes |
| **Calcul hash** | 0.08 secondes |
| **Signature RSA** | 0.12 secondes |
| **Génération QR** | 0.05 secondes |
| **Modification PDF** | 1.96 secondes |
| **Taille PDF original** | 122.9 KB |
| **Taille PDF signé** | 125.4 KB (+2.5 KB) |
| **Hash** | SHA-256 (64 caractères hex) |
| **Signature** | RSA 2048 bits (Base64) |

---

## 🎯 Points Clés des Logs

1. ✅ **Toutes les données** sont récupérées automatiquement
2. ✅ **Chaque étape** est logguée clairement
3. ✅ **Les erreurs** seraient visibles immédiatement
4. ✅ **Le workflow** est tracé (prochain signataire)
5. ✅ **Les performances** sont mesurées (temps d'exécution)
6. ✅ **L'utilisateur** est informé en temps réel

---

## 📝 Remarques

- 🟢 Les logs utilisent des emojis pour faciliter la lecture
- 🟢 Chaque section est clairement séparée
- 🟢 Les données sensibles ne sont jamais loggées en entier
- 🟢 Les performances sont optimales (< 3 secondes)
- 🟢 L'utilisateur voit des notifications claires, pas les logs techniques

