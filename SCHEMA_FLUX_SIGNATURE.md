# 🔄 Schéma du Flux de Signature de Document

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TABLEAU DE BORD DU CHEF                                  │
│                      (OrganizationManagerPage.vue)                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 1️⃣ Clic sur "Signer"
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   Vérifications préalables          │
                    │   ✓ Certificat valide ?             │
                    │   ✓ Autorisé à signer ?             │
                    │   ✓ Confirmation utilisateur ?      │
                    └─────────────────────────────────────┘
                                      │
                                      │ ✅ OK
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      2️⃣ RÉCUPÉRATION DES DONNÉES                                 │
│                     (DocumentSigningService)                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌────────────────┐           ┌──────────────────┐
│  API Django   │            │  sessionStorage│           │   Fichier PDF    │
│               │            │                │           │                  │
│  GET /api/    │            │  Certificat    │           │  URL du PDF      │
│  signatures/  │            │  + Clés        │           │  actuel          │
│  document-    │            │  cryptographiques          │                  │
│  preparation/ │            │                │           │                  │
│  {id}/        │            └────────────────┘           └──────────────────┘
│               │
└───────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│  DONNÉES RÉCUPÉRÉES :                                                          │
│                                                                                │
│  📄 DocumentPreparation                                                        │
│     ├─ id, document_id, organization                                          │
│     ├─ prepared_by, current_signer                                            │
│     ├─ current_document (PDF avec signatures partielles)                      │
│     ├─ elements_configuration (QR + Signature positions)                      │
│     └─ signature_workflow (ordre des signataires)                             │
│                                                                                │
│  📊 Elements Configuration                                                     │
│     ├─ qr_code: { x: 85%, y: 10%, size: 'medium' }                           │
│     └─ signature: { x: 50%, y: 80%, width: 200, height: 100 }                │
│                                                                                │
│  🔐 Certificat                                                                 │
│     ├─ privateKey (RSA)                                                        │
│     ├─ publicKey (RSA)                                                         │
│     └─ certificateInfo (validité, sujet, émetteur)                            │
│                                                                                │
│  📋 Workflow Info                                                              │
│     ├─ currentStep: 1/3                                                        │
│     ├─ currentSigner: { user_id, name, role: 'chef' }                        │
│     └─ nextSigner: { user_id, name, role: 'chef+1' }                         │
│                                                                                │
│  📦 PDF Data (Uint8Array)                                                      │
│     └─ Document téléchargé prêt à être modifié                                │
└───────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 3️⃣ Préparation métadonnées
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      MÉTADONNÉES DE SIGNATURE                                   │
│                                                                                  │
│  {                                                                               │
│    qr_position: { x, y, size, mode, pages },                                   │
│    signature_position: { positions, pages, signature_size },                   │
│    workflow_info: { current_step, total_steps, signer_info }                  │
│  }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 4️⃣ Appel SignatureService
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     SIGNATURE DU DOCUMENT                                        │
│                     (SignatureService)                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐            ┌────────────────┐           ┌──────────────────┐
│  Calcul Hash  │            │   Signature    │           │  Génération      │
│   SHA-256     │            │  Cryptographique           │  QR Code         │
│               │            │                │           │                  │
│  a3f5b2c8...  │            │  RSA + SHA-256 │           │  UUID document   │
│               │            │  Base64        │           │  Image PNG       │
└───────────────┘            └────────────────┘           └──────────────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                            ┌──────────────────────┐
                            │  Modification PDF    │
                            │  (pdf-lib)           │
                            │                      │
                            │  1. Ajout QR Code    │
                            │  2. Ajout signature  │
                            │     (si image)       │
                            └──────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         5️⃣ RÉSULTAT DE LA SIGNATURE                             │
│                                                                                  │
│  {                                                                               │
│    success: true,                                                                │
│    documentId: "550e8400-e29b-41d4-a716-446655440000",                         │
│    originalHash: "a3f5b2c8d1e4f7a9b0c3d6e9f2a5b8c1...",                        │
│    signature: "ZGF0YTppbWFnZS9wbmc7YmFzZTY0L...",                                │
│    publicKeyPem: "-----BEGIN PUBLIC KEY-----\n...",                            │
│    signedDocument: Uint8Array [PDF modifié avec QR],                           │
│    executionTime: 2.5,                                                           │
│    timestamp: "2024-01-15T10:30:00Z"                                            │
│  }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ ✅ SIGNATURE TERMINÉE
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      AFFICHAGE DU RÉSULTAT                                       │
│                                                                                  │
│  ✅ Notification de succès                                                       │
│  📊 Document ID, Hash, Temps d'exécution                                         │
│  📋 Information workflow (prochaine étape)                                       │
│  🔄 Rafraîchissement de la liste des documents                                   │
└─────────────────────────────────────────────────────────────────────────────────┘




═══════════════════════════════════════════════════════════════════════════════════
                          LÉGENDE DES COMPOSANTS
═══════════════════════════════════════════════════════════════════════════════════

📦 SERVICES FRONTEND
├─ DocumentSigningService.js   → Orchestrateur principal
├─ SignatureService.js          → Signature cryptographique + PDF
└─ CertificateService.js        → Gestion des certificats

📡 API BACKEND (Django REST Framework)
├─ GET  /api/signatures/document-preparation/{id}/
├─ POST /api/signatures/document-preparation/{id}/advance-workflow/
└─ GET  /api/organizations/{id}/certificates/

💾 STOCKAGE
├─ Base de données PostgreSQL/SQLite
│  ├─ signatures_documentpreparation
│  ├─ signatures_documentsignaturestep
│  ├─ organizations_organization
│  └─ authentication_user
│
└─ sessionStorage (Navigateur)
   └─ gvb_certificate_info (certificat + clés)

🔐 CRYPTOGRAPHIE
├─ Librairie: node-forge
├─ Hash: SHA-256
├─ Signature: RSA (PKCS#1 v1.5)
└─ Format: PEM (clés), Base64 (signature)

📄 MANIPULATION PDF
├─ Librairie: pdf-lib
├─ QR Code: qrcode (npm)
└─ Format: Uint8Array




═══════════════════════════════════════════════════════════════════════════════════
                        FLUX DÉTAILLÉ DES DONNÉES
═══════════════════════════════════════════════════════════════════════════════════

ENTRÉE                           TRAITEMENT                      SORTIE
──────────────────────────────────────────────────────────────────────────────────

Document à signer         ──►  Récupération BDD           ──►  DocumentPreparation
(ID: preparation_id)            API Call                        + Métadonnées

PDF URL                   ──►  Téléchargement HTTP        ──►  Uint8Array
(current_document)              fetch()                         (données binaires)

Configuration JSON        ──►  Extraction                 ──►  Positions QR + Sig
(elements_configuration)        Parsing                         { x, y, size, ... }

Certificat PKCS#12        ──►  Décodage                   ──►  Clés RSA
(sessionStorage)                node-forge                      (privateKey, publicKey)

PDF + Clé privée          ──►  Calcul Hash SHA-256        ──►  Hash hexadécimal
(Uint8Array + RSA)              MD5 digest                      "a3f5b2c8..."

Hash + Clé privée         ──►  Signature RSA              ──►  Signature Base64
(SHA-256 + RSA)                 PKCS#1 v1.5                    "ZGF0YTpp..."

Document ID               ──►  Génération QR Code         ──►  PNG Base64
(UUID)                          qrcode lib                      (data URL)

PDF + QR + Config         ──►  Modification PDF           ──►  PDF modifié
(pdf-lib)                       drawImage()                     (Uint8Array)

Résultat signature        ──►  Affichage UI               ──►  Notification
(success, hash, ...)            Vue.js                          Toast message




═══════════════════════════════════════════════════════════════════════════════════
                        ÉTAT DU SYSTÈME APRÈS SIGNATURE
═══════════════════════════════════════════════════════════════════════════════════

✅ COMPLÉTÉ DANS CETTE PHASE :
  1. Récupération automatique des données depuis la BDD
  2. Vérification des permissions et du certificat
  3. Signature cryptographique du document
  4. Ajout du QR Code au PDF
  5. Génération du document signé (Uint8Array)
  6. Calcul du hash SHA-256
  7. Affichage du résultat à l'utilisateur

⏳ À IMPLÉMENTER DANS LA PHASE SUIVANTE :
  1. Envoi du résultat au backend Django
  2. Enregistrement dans DocumentSignatureStep
  3. Mise à jour de DocumentPreparation.current_document
  4. Avancement du workflow (advance_workflow)
  5. Notification du prochain signataire
  6. Création de DocumentSignature finale (si dernière étape)
  7. Gestion des erreurs backend
  8. Rollback en cas d'échec




═══════════════════════════════════════════════════════════════════════════════════
                           POINTS CLÉS À RETENIR
═══════════════════════════════════════════════════════════════════════════════════

🔹 TOUT EST AUTOMATIQUE : Un seul appel à documentSigningService.signDocument()
🔹 DONNÉES CENTRALISÉES : Toutes les données viennent de la BDD
🔹 SÉCURITÉ : Vérifications multiples (certificat, permissions, validité)
🔹 TRAÇABILITÉ : Hash SHA-256, signature RSA, QR Code avec UUID
🔹 WORKFLOW : Gestion automatique des étapes de signature hiérarchique
🔹 UX : Notifications en temps réel, indicateurs de chargement
🔹 ERREURS : Gestion complète avec messages utilisateur clairs




═══════════════════════════════════════════════════════════════════════════════════
                              FIN DU SCHÉMA
═══════════════════════════════════════════════════════════════════════════════════
```

