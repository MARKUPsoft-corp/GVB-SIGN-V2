# Test du Système de Signature Complet

## 🎯 Objectif
Tester le flux complet de signature avec enregistrement dans la base de données.

## 📋 Étapes du Test

### 1. **Préparation**
- ✅ Certificat de l'organisation importé
- ✅ Document préparé pour signature
- ✅ Utilisateur connecté avec rôle "chef"

### 2. **Processus de Signature**
- ✅ Vérification des permissions
- ✅ Récupération du certificat depuis la BDD
- ✅ Téléchargement du PDF
- ✅ Calcul du hash SHA-256
- ✅ Signature cryptographique avec RSA
- ✅ Génération du QR Code
- ✅ Modification du PDF

### 3. **Enregistrement Backend**
- ✅ Envoi des données au backend
- ✅ Création de l'enregistrement `DocumentSignature`
- ✅ Mise à jour de `DocumentPreparation`
- ✅ Avancement du workflow
- ✅ Gestion des prochains signataires

## 🔧 Endpoints Utilisés

### Frontend → Backend
```
POST /api/signatures/document-preparation/{preparation_id}/save-signature/
```

**Payload:**
```json
{
  "document_id": "uuid-du-document",
  "document_hash": "sha256-hash",
  "signature": "signature-rsa-base64",
  "public_key": "public-key-pem",
  "signed_document_data": "base64-encoded-pdf",
  "signature_timestamp": "2024-01-20T10:30:00Z"
}
```

**Réponse:**
```json
{
  "success": true,
  "message": "Signature enregistrée avec succès",
  "signature_id": "uuid-de-la-signature",
  "workflow_advanced": true,
  "next_signer": {
    "id": 12,
    "name": "Prochain Signataire",
    "email": "prochain@example.com",
    "role": "chef+1"
  },
  "is_complete": false
}
```

## 📊 Modèles de Base de Données

### DocumentSignature
- `id`: UUID de la signature
- `document_id`: ID du document généré
- `document_preparation`: Lien vers DocumentPreparation
- `user`: Utilisateur qui a signé
- `signer_full_name`: Nom complet du signataire
- `original_document`: Fichier PDF original
- `signed_document`: Fichier PDF signé
- `document_hash`: Hash SHA-256
- `public_key`: Clé publique du certificat
- `signature`: Signature numérique
- `signature_timestamp`: Timestamp de signature

### DocumentPreparation (mis à jour)
- `current_document`: Fichier PDF actuel (signé)
- `status`: "in_progress" ou "completed"
- `current_step`: Étape actuelle du workflow
- `current_signer`: Prochain signataire

## 🚀 Test Manuel

1. **Connectez-vous** en tant que chef d'organisation
2. **Allez sur la page** de gestion des documents
3. **Cliquez sur "Signer"** pour un document préparé
4. **Confirmez** la signature
5. **Vérifiez** que le document est signé et enregistré
6. **Vérifiez** que le workflow avance correctement

## ✅ Résultats Attendus

- ✅ Document signé cryptographiquement
- ✅ QR Code ajouté au PDF
- ✅ Enregistrement dans `DocumentSignature`
- ✅ Mise à jour de `DocumentPreparation`
- ✅ Workflow avancé automatiquement
- ✅ Notification de succès affichée
- ✅ Prochain signataire identifié (si applicable)

## 🔍 Vérifications

### Console Frontend
```
✅ === SIGNATURE TERMINÉE AVEC SUCCÈS ===
💾 ÉTAPE 4: Enregistrement dans la base de données...
✅ Signature enregistrée avec succès!
✅ Signature ID: uuid-de-la-signature
✅ Workflow avancé: true
⏭️ Prochain signataire: Nom (rôle)
```

### Base de Données
- Nouvel enregistrement dans `DocumentSignature`
- `DocumentPreparation` mis à jour
- Workflow avancé si applicable

## 🎉 Succès
Le système de signature est maintenant **complètement fonctionnel** avec :
- Signature cryptographique sécurisée
- Enregistrement automatique en base
- Gestion du workflow hiérarchique
- Interface utilisateur intuitive
