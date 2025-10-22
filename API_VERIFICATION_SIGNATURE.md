# API de Vérification de Signature - Documentation

## 🎯 Objectif
API publique pour vérifier la validité d'une signature numérique via l'ID du document (contenu dans le QR code).

## 📡 Endpoint

### **GET** `/api/signatures/verify-signature/{document_id}/`

**Description**: Vérifie la validité d'une signature numérique par l'ID du document

**Paramètres**:
- `document_id` (string) - ID unique du document (contenu dans le QR code)

**Authentification**: Aucune requise (API publique)

## 📥 Entrée

### URL d'exemple
```
GET http://127.0.0.1:8000/api/signatures/verify-signature/cc3f1b70-7bad-43d7-a028-785510adf614/
```

### Paramètres d'URL
- `document_id`: L'ID unique du document (UUID ou string)

## 📤 Sortie

### Réponse de Succès (200 OK)
```json
{
  "success": true,
  "document_info": {
    "document_id": "cc3f1b70-7bad-43d7-a028-785510adf614",
    "filename": "emmanuel_CV.pdf",
    "signer_name": "Emmanuel YAKAM TCHAMEGNI",
    "signer_email": "emmanuelyakam4@gmail.com",
    "signature_timestamp": "2024-01-20T10:30:00Z",
    "created_at": "2024-01-20T10:30:00Z",
    "file_size_original": 123065,
    "file_size_signed": 170300,
    "execution_time": 0.163
  },
  "organization_info": {
    "name": "Legrandprof",
    "id": "18"
  },
  "verification": {
    "valid": true,
    "message": "Signature valide - Le document est authentique et non modifié",
    "document_hash": "deae78cbc554051d099e37b4c05f7674046caf7f98e2c51195104cd281937af7",
    "verification_method": "RSA-SHA256 with PKCS#1 v1.5",
    "signature_algorithm": "RSA",
    "hash_algorithm": "SHA-256"
  },
  "document_urls": {
    "signed_document_url": "/media/documents/signed/cc3f1b70-7bad-43d7-a028-785510adf614_signed_emmanuel_CV.pdf",
    "original_document_url": "/media/documents/original/cc3f1b70-7bad-43d7-a028-785510adf614_original_emmanuel_CV.pdf"
  },
  "workflow_info": {
    "is_workflow_document": true,
    "workflow_history": [
      {
        "step": 1,
        "user_id": 11,
        "user_name": "Emmanuel YAKAM TCHAMEGNI",
        "user_email": "emmanuelyakam4@gmail.com",
        "role": "chef",
        "organization_member_id": 41
      }
    ],
    "total_steps": 1
  }
}
```

### Réponse d'Erreur (404 Not Found)
```json
{
  "success": false,
  "error": "Document non trouvé",
  "document_id": "cc3f1b70-7bad-43d7-a028-785510adf614"
}
```

### Réponse d'Erreur (500 Internal Server Error)
```json
{
  "success": false,
  "error": "Erreur lors de la vérification: [détails de l'erreur]",
  "document_id": "cc3f1b70-7bad-43d7-a028-785510adf614"
}
```

## 🔍 Processus de Vérification

### 1. **Recherche du Document**
```python
signature_record = DocumentSignature.objects.get(document_id=document_id)
```

### 2. **Vérification Cryptographique**
```python
# Lecture du document signé
document_data = signature_record.signed_document.read()

# Vérification RSA-SHA256
public_key.verify(
    signature_bytes,
    document_data,
    padding.PKCS1v15(),
    hashes.SHA256()
)
```

### 3. **Validation des Résultats**
- ✅ **Signature valide** : Le document n'a pas été modifié
- ❌ **Signature invalide** : Le document a été corrompu ou falsifié

## 📊 Informations Retournées

### Document Info
- **document_id**: ID unique du document
- **filename**: Nom du fichier original
- **signer_name**: Nom complet du signataire
- **signer_email**: Email du signataire
- **signature_timestamp**: Date et heure de signature
- **created_at**: Date de création de l'enregistrement
- **file_size_original**: Taille du fichier original (bytes)
- **file_size_signed**: Taille du fichier signé (bytes)
- **execution_time**: Temps d'exécution de la signature (secondes)

### Organization Info
- **name**: Nom de l'organisation
- **id**: ID de l'organisation

### Verification Info
- **valid**: Boolean - Signature valide ou non
- **message**: Message descriptif du résultat
- **document_hash**: Hash SHA-256 du document
- **verification_method**: Méthode de vérification utilisée
- **signature_algorithm**: Algorithme de signature (RSA)
- **hash_algorithm**: Algorithme de hash (SHA-256)

### Document URLs
- **signed_document_url**: URL pour télécharger le document signé
- **original_document_url**: URL pour télécharger le document original

### Workflow Info (si applicable)
- **is_workflow_document**: Boolean - Document de workflow
- **workflow_history**: Historique des signatures
- **total_steps**: Nombre total d'étapes du workflow

## 🔐 Sécurité

### Vérifications Cryptographiques
1. **Intégrité du Document** : Hash SHA-256 vérifié
2. **Authenticité de la Signature** : Clé publique RSA validée
3. **Non-répudiation** : Seule la clé privée correspondante peut créer la signature

### Algorithme de Vérification
- **Signature** : RSA avec PKCS#1 v1.5 padding
- **Hash** : SHA-256 (256 bits de sécurité)
- **Bibliothèque** : Python cryptography

## 🧪 Tests

### Test avec cURL
```bash
curl -X GET "http://127.0.0.1:8000/api/signatures/verify-signature/cc3f1b70-7bad-43d7-a028-785510adf614/"
```

### Test avec JavaScript
```javascript
fetch('http://127.0.0.1:8000/api/signatures/verify-signature/cc3f1b70-7bad-43d7-a028-785510adf614/')
  .then(response => response.json())
  .then(data => {
    if (data.success && data.verification.valid) {
      console.log('✅ Document authentique:', data.document_info.filename);
      console.log('👤 Signé par:', data.document_info.signer_name);
      console.log('🏢 Organisation:', data.organization_info.name);
    } else {
      console.log('❌ Signature invalide:', data.verification.message);
    }
  });
```

## 📱 Utilisation avec QR Code

### Flux d'Utilisation
1. **Scanner le QR Code** sur le document signé
2. **Extraire l'ID** du document du QR code
3. **Appeler l'API** avec cet ID
4. **Vérifier le résultat** de la vérification
5. **Afficher les informations** du document et du signataire

### Exemple d'ID de Document
```
cc3f1b70-7bad-43d7-a028-785510adf614
```

## 🎯 Cas d'Usage

### 1. **Vérification Publique**
- Scanner un QR code sur un document
- Vérifier l'authenticité sans authentification

### 2. **Audit de Documents**
- Vérifier l'intégrité de documents archivés
- Valider les signatures dans un workflow

### 3. **Intégration Externe**
- API publique pour systèmes tiers
- Vérification automatisée de documents

## ⚠️ Gestion d'Erreurs

### Erreurs Possibles
- **404** : Document non trouvé
- **500** : Erreur de vérification cryptographique
- **500** : Erreur de lecture du fichier

### Codes de Statut
- **200** : Vérification réussie
- **404** : Document introuvable
- **500** : Erreur serveur

## 🎉 **API Prête !**

L'API de vérification est maintenant **complètement fonctionnelle** et peut être utilisée pour vérifier les signatures via QR code ! 🚀
