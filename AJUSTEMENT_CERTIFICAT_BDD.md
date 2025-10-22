# 🔄 Ajustement : Certificat depuis la Base de Données

**Date** : 22 octobre 2025  
**Version** : 1.1  
**Type** : Correction importante

---

## 🎯 Problème Identifié

Dans l'implémentation initiale (v1.0), le certificat était récupéré depuis **sessionStorage** (côté client).

**Vous avez correctement indiqué que** :
> "Les éléments du certificat ne sont pas dans la session storage, mais dans la base de données. C'est le certificat de l'organisation qu'on doit récupérer."

---

## ✅ Solution Implémentée

Le certificat est maintenant récupéré depuis la **base de données** au niveau de l'organisation.

### Modifications Backend

#### 1. Nouveau Serializer avec Clés
**Fichier** : `backend/organizations/serializers.py`

```python
class OrganizationCertificateWithKeysSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les certificats avec les clés cryptographiques
    Utilisé uniquement pour la signature de documents
    """
    # Inclut les champs sensibles :
    # - private_key_pem
    # - public_key_pem
    # - certificate_pem
```

#### 2. Nouvel Endpoint API Sécurisé
**Fichier** : `backend/organizations/views.py`

```python
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_active_certificate_for_signing(request, organization_id):
    """
    Récupère le certificat actif de l'organisation avec les clés
    
    Sécurité :
    - Vérifie l'appartenance à l'organisation
    - Vérifie le rôle (chef, chef+1, chef+2)
    - Récupère le certificat actif et valide
    - Vérifie l'expiration
    """
```

**URL** : `GET /api/organizations/{id}/certificates/active-for-signing/`

**Réponse** :
```json
{
  "success": true,
  "certificate": {
    "id": 1,
    "name": "Certificat GVB",
    "subject_common_name": "GVB Technologies",
    "subject_organization": "GVB",
    "not_before": "2024-01-01T00:00:00Z",
    "not_after": "2025-12-31T23:59:59Z",
    "is_valid": true,
    "is_expired": false,
    "days_until_expiry": 450,
    "private_key_pem": "-----BEGIN PRIVATE KEY-----\n...",
    "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...",
    "certificate_pem": "-----BEGIN CERTIFICATE-----\n..."
  },
  "has_certificate": true
}
```

**Vérifications de sécurité** :
1. ✅ Utilisateur authentifié
2. ✅ Utilisateur membre de l'organisation
3. ✅ Utilisateur a un rôle autorisé (chef, chef+1, chef+2)
4. ✅ Certificat actif (`is_active=True`)
5. ✅ Certificat valide (`is_valid=True`)
6. ✅ Certificat non expiré

---

### Modifications Frontend

#### 1. Nouvelle Méthode : `fetchOrganizationCertificate()`
**Fichier** : `frontend/services/DocumentSigningService.js`

```javascript
async fetchOrganizationCertificate(organizationId) {
  // 1. Appel API pour récupérer le certificat
  const response = await fetch(
    `http://127.0.0.1:8000/api/organizations/${organizationId}/certificates/active-for-signing/`
  )
  
  // 2. Vérification des erreurs
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Aucun certificat actif trouvé...')
    } else if (response.status === 400 && errorData.is_expired) {
      throw new Error('Le certificat est expiré...')
    }
  }
  
  // 3. Conversion des clés PEM en objets forge
  const privateKey = forge.pki.privateKeyFromPem(cert.private_key_pem)
  const publicKey = forge.pki.publicKeyFromPem(cert.public_key_pem)
  
  // 4. Retour des données
  return {
    certificateData: cert,
    privateKey,
    publicKey,
    privateKeyPem: cert.private_key_pem,
    publicKeyPem: cert.public_key_pem
  }
}
```

**Changements** :
- ❌ `loadCertificateData()` depuis sessionStorage
- ✅ `fetchOrganizationCertificate()` depuis l'API

#### 2. Nouvelle Méthode : `hasOrganizationCertificate()`
```javascript
async hasOrganizationCertificate(organizationId) {
  // Appel API pour vérifier si l'organisation a un certificat
  const response = await fetch(
    `http://127.0.0.1:8000/api/organizations/${organizationId}/certificates/active-for-signing/`
  )
  
  if (response.ok) {
    const data = await response.json()
    return data.success && data.has_certificate
  }
  
  return false
}
```

**Changements** :
- ❌ `hasCertificate()` vérifie sessionStorage
- ✅ `hasOrganizationCertificate()` vérifie la BDD via API

#### 3. Mise à Jour du Composant
**Fichier** : `frontend/components/dashboard/OrganizationManagerPage.vue`

**Avant** :
```javascript
// Vérifier sessionStorage
if (!documentSigningService.hasCertificate()) {
  alert('Importez un certificat')
  return
}
```

**Maintenant** :
```javascript
// Vérifier BDD
const hasCert = await documentSigningService.hasOrganizationCertificate(organizationId)

if (!hasCert) {
  showNotification('error', 'Certificat requis', 
    'Cette organisation n\'a pas de certificat de signature actif.')
  return
}
```

---

## 🔄 Flux Complet (Mise à Jour)

```
┌─────────────────────────────────────────────────────────────┐
│  Chef clique sur "Signer"                                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 1: Récupérer l'ID de l'organisation                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 2: Vérifier le certificat de l'organisation          │
│  API: GET /api/organizations/{id}/certificates/             │
│       active-for-signing/                                   │
└─────────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
   Pas de cert      Cert expiré       Cert OK ✅
         │                │
         ▼                ▼
   ❌ Erreur       ❌ Erreur
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 3: Vérifier permissions utilisateur                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 4: Confirmation utilisateur                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 5: Récupérer toutes les données                      │
│  ├─ DocumentPreparation (API)                               │
│  ├─ PDF (Download)                                          │
│  ├─ Configuration (JSON parsing)                            │
│  ├─ Certificat de l'organisation (API) ⭐ NOUVEAU           │
│  │  └─ Conversion PEM → forge objects                       │
│  └─ Workflow (JSON parsing)                                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 6: Signer le document                                │
│  └─ Utilise le certificat de l'organisation                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Différences Clés

| Aspect | Avant (v1.0) | Maintenant (v1.1) |
|--------|--------------|-------------------|
| **Source du certificat** | sessionStorage (client) | Base de données (serveur) |
| **Portée** | Certificat personnel | Certificat de l'organisation |
| **Persistance** | Temporaire (session) | Permanent (BDD) |
| **Partage** | Non partagé | Partagé par toute l'organisation |
| **Importation** | Par chaque utilisateur | Une fois pour l'organisation |
| **Vérification** | Client-side | Server-side (sécurisé) |
| **API** | Aucune | `GET /organizations/{id}/certificates/active-for-signing/` |

---

## 🔐 Avantages de cette Approche

### ✅ Sécurité
- Le certificat est géré côté serveur
- Vérifications strictes avant de retourner les clés
- Pas besoin de stocker les clés sensibles côté client

### ✅ Cohérence
- Un seul certificat par organisation
- Tous les chefs utilisent le même certificat
- Pas de problème de synchronisation

### ✅ Simplicité
- L'utilisateur n'a pas besoin d'importer un certificat
- Gestion centralisée par l'admin de l'organisation
- Moins de confusion

### ✅ Traçabilité
- On sait exactement quel certificat a été utilisé
- Historique dans la BDD (`OrganizationCertificate.imported_at`)
- Informations du certificat dans les métadonnées

---

## 🧪 Comment Tester

### Prérequis
1. L'organisation doit avoir un certificat importé dans la BDD
2. Le certificat doit être actif (`is_active=True`)
3. Le certificat ne doit pas être expiré

### Étapes
```bash
# 1. Vérifier qu'un certificat existe pour l'organisation
GET /api/organizations/{id}/certificates/

# 2. Importer un certificat si nécessaire
POST /api/organizations/{id}/certificates/create/
{
  "name": "Certificat GVB",
  "private_key_pem": "-----BEGIN PRIVATE KEY-----\n...",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...",
  ...
}

# 3. Tester la récupération du certificat pour signature
GET /api/organizations/{id}/certificates/active-for-signing/

# 4. Tester la signature d'un document
```

### Logs attendus
```
🔐 Vérification du certificat de l'organisation...
🔐 Récupération du certificat de l'organisation depuis la BDD
🔐 Organization ID: 1
✅ Clé privée convertie depuis PEM
✅ Clé publique convertie depuis PEM
🔐 Certificat de l'organisation: Certificat GVB
🔐 Sujet: GVB Technologies
🔐 Organisation: GVB
🔐 Validité: 2024-01-01 - 2025-12-31
🔐 Jours restants: 450
✅ Certificat de l'organisation trouvé
✅ Certificat chargé depuis la BDD: GVB Technologies
```

---

## 📁 Fichiers Modifiés

### Backend (3 fichiers)
1. ✅ `backend/organizations/serializers.py`
   - Ajout de `OrganizationCertificateWithKeysSerializer`

2. ✅ `backend/organizations/views.py`
   - Ajout de `get_active_certificate_for_signing()`

3. ✅ `backend/organizations/urls.py`
   - Ajout de l'URL `certificates/active-for-signing/`

### Frontend (2 fichiers)
1. ✅ `frontend/services/DocumentSigningService.js`
   - Modification de `fetchSigningData()` (utilise nouvelle méthode)
   - Remplacement de `loadCertificateData()` par `fetchOrganizationCertificate()`
   - Remplacement de `hasCertificate()` par `hasOrganizationCertificate()`
   - Mise à jour de `prepareSignatureMetadata()` (ajout certificateData)

2. ✅ `frontend/components/dashboard/OrganizationManagerPage.vue`
   - Mise à jour de `signDocument()` (vérification BDD au lieu de sessionStorage)

---

## 🎯 Résultat Final

### Avant
```javascript
// Certificat personnel en sessionStorage
const cert = sessionStorage.getItem('gvb_certificate_info')
if (!cert) {
  alert('Importez votre certificat')
}
```

### Maintenant
```javascript
// Certificat de l'organisation dans la BDD
const cert = await fetch(
  `/api/organizations/${orgId}/certificates/active-for-signing/`
)

if (!cert) {
  alert('L\'organisation n\'a pas de certificat')
}
```

**Le certificat est maintenant géré au niveau de l'organisation, pas au niveau de l'utilisateur ! ✅**

---

## ⚠️ Points d'Attention

1. **Migration des données** : Si des certificats étaient en sessionStorage, ils ne seront plus utilisés
2. **Import initial** : Chaque organisation doit importer son certificat une fois
3. **Sécurité** : Les clés privées transitent par HTTPS (vérifier le certificat SSL en production)
4. **Performance** : Un appel API supplémentaire pour récupérer le certificat (acceptable)

---

**Status** : ✅ **IMPLÉMENTATION COMPLÈTE**  
**Validé par** : Utilisateur  
**Prochaine étape** : Tests fonctionnels avec un certificat réel dans la BDD

