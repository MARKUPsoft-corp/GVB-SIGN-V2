# API des Signatures de Documents

Cette API permet d'enregistrer et de gérer les signatures numériques de documents PDF.

## Endpoints

### 1. Créer une signature unique
**POST** `/api/signatures/create/`

Enregistre une signature de document unique.

**Body:**
```json
{
  "document_id": "uuid-du-document",
  "signer_full_name": "Nom complet du signataire",
  "original_filename": "document.pdf",
  "document_hash": "hash-sha256-du-document",
  "public_key": "-----BEGIN PUBLIC KEY-----...",
  "signature": "signature-numerique-base64",
  "signature_timestamp": "2024-01-01T12:00:00Z",
  "file_size_original": 12345,
  "file_size_signed": 12500,
  "execution_time": 1.5,
  "original_document_base64": "base64-encoded-pdf",
  "signed_document_base64": "base64-encoded-signed-pdf"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Signature enregistrée avec succès",
  "signature_id": "uuid-de-la-signature",
  "document_id": "uuid-du-document"
}
```

### 2. Créer plusieurs signatures
**POST** `/api/signatures/bulk-create/`

Enregistre plusieurs signatures en une seule requête.

**Body:**
```json
{
  "signatures": [
    {
      "document_id": "uuid-du-document-1",
      "signer_full_name": "Nom complet",
      "original_filename": "document1.pdf",
      // ... autres champs comme pour l'endpoint unique
    },
    {
      "document_id": "uuid-du-document-2",
      // ... autres champs
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "2 signature(s) créée(s), 0 erreur(s)",
  "created_signatures": [
    {
      "index": 0,
      "signature_id": "uuid-signature-1",
      "document_id": "uuid-document-1",
      "status": "created"
    }
  ],
  "errors": [],
  "total_processed": 2,
  "total_created": 2,
  "total_errors": 0
}
```

### 3. Lister les signatures de l'utilisateur
**GET** `/api/signatures/list/`

Récupère la liste des signatures de l'utilisateur connecté.

**Response:**
```json
[
  {
    "id": "uuid-signature",
    "document_id": "uuid-document",
    "signer_full_name": "Nom complet",
    "user_email": "user@example.com",
    "original_filename": "document.pdf",
    "signature_timestamp": "2024-01-01T12:00:00Z",
    "created_at": "2024-01-01T12:00:00Z",
    "file_size_original": 12345,
    "file_size_signed": 12500,
    "execution_time": 1.5,
    "is_verified": true
  }
]
```

### 4. Détails d'une signature
**GET** `/api/signatures/{signature_id}/`

Récupère les détails complets d'une signature.

**Response:**
```json
{
  "id": "uuid-signature",
  "document_id": "uuid-document",
  "signer_full_name": "Nom complet",
  "user_email": "user@example.com",
  "original_filename": "document.pdf",
  "document_hash": "hash-sha256",
  "public_key": "-----BEGIN PUBLIC KEY-----...",
  "signature": "signature-numerique-base64",
  "signature_timestamp": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z",
  "file_size_original": 12345,
  "file_size_signed": 12500,
  "execution_time": 1.5,
  "is_verified": true,
  "original_document_url": "http://localhost:8000/media/documents/original/...",
  "signed_document_url": "http://localhost:8000/media/documents/signed/..."
}
```

## Authentification

Toutes les requêtes nécessitent une authentification. L'utilisateur doit être connecté via les sessions Django.

## Modèle de données

### DocumentSignature

- `id`: UUID (primary key)
- `document_id`: ID du document généré côté frontend
- `user`: Référence vers l'utilisateur qui a signé
- `signer_full_name`: Nom complet du signataire
- `original_document`: Fichier PDF original
- `signed_document`: Fichier PDF signé
- `original_filename`: Nom original du fichier
- `document_hash`: Hash SHA-256 du document original
- `public_key`: Clé publique du certificat
- `signature`: Signature numérique
- `signature_timestamp`: Timestamp de la signature
- `file_size_original`: Taille du fichier original
- `file_size_signed`: Taille du fichier signé
- `execution_time`: Temps d'exécution de la signature
- `created_at`: Date de création de l'enregistrement
- `updated_at`: Date de dernière modification

## Utilisation côté Frontend

Le service `SignatureApiService.js` fournit les méthodes pour interagir avec cette API :

```javascript
import { SignatureApiService } from './services/SignatureApiService.js'

const apiService = new SignatureApiService()

// Enregistrer plusieurs signatures
const response = await apiService.saveMultipleSignatures(signaturesData)
```

## Structure des fichiers

- Les fichiers originaux sont stockés dans `media/documents/original/`
- Les fichiers signés sont stockés dans `media/documents/signed/`
- Les noms de fichiers incluent l'ID du document pour éviter les conflits
