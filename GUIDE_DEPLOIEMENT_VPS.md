# 📘 Guide Complet de Déploiement - GVB Sign sur VPS Ubuntu

## 📋 Table des Matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Prérequis](#prérequis)
3. [Préparation du VPS](#préparation-du-vps)
4. [Déploiement en Développement](#déploiement-en-développement)
5. [Déploiement en Production](#déploiement-en-production)
6. [Configuration Nginx](#configuration-nginx)
7. [Sécurité et Maintenance](#sécurité-et-maintenance)
8. [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble du projet

**GVB Sign** est une application de signature électronique moderne composée de trois parties :

### Architecture du Projet

```
GVB_Sign/
├── backend/          # API Django REST Framework (Python)
│   ├── authentication/    # Gestion des utilisateurs
│   ├── signatures/        # Gestion des signatures électroniques
│   ├── organizations/     # Gestion des organisations
│   └── gvb_backend/       # Configuration Django
│
├── frontend/         # Application Nuxt.js 4 (Vue.js 3)
│   ├── app/              # Pages et layouts
│   ├── components/       # Composants Vue
│   ├── services/         # Services API
│   └── stores/           # Gestion d'état Pinia
│
└── mobile/          # Application Flutter (non déployée sur VPS)
```

### Technologies Utilisées

**Backend :**
- Django 5.2.5 (Framework Python)
- Django REST Framework (API REST)
- SQLite (Base de données - développement)
- PostgreSQL (Base de données - production recommandée)
- Python 3.10+

**Frontend :**
- Nuxt.js 4 (Framework Vue.js)
- Vue.js 3 (Framework JavaScript)
- Bootstrap 5 (Framework CSS)
- Pinia (Gestion d'état)
- Node.js 22.x

**Fonctionnalités Principales :**
- ✅ Authentification utilisateur (email/mot de passe)
- ✅ Gestion des organisations et membres
- ✅ Signature électronique de documents PDF
- ✅ Workflow de signature hiérarchique
- ✅ Génération de QR codes pour vérification
- ✅ Vérification de signatures via API publique
- ✅ Gestion de certificats numériques

---

## 🔧 Prérequis

### Sur votre machine locale

- Accès SSH à votre VPS
- Client SSH (Terminal Linux/Mac ou PuTTY sur Windows)
- Connaissance basique de la ligne de commande Linux

### Sur le VPS Ubuntu

Votre VPS doit avoir :
- **Ubuntu 20.04 LTS ou 22.04 LTS** (recommandé)
- **Minimum 2 GB RAM** (4 GB recommandé)
- **Minimum 20 GB d'espace disque**
- **Accès root ou sudo**
- **Connexion Internet stable**

---

## 🚀 Préparation du VPS

### Étape 1 : Connexion au VPS

Connectez-vous à votre VPS via SSH :

```bash
# Connexion SSH au VPS
ssh root@92.112.184.194
```

**💡 Astuce :** Si vous utilisez Windows, vous pouvez utiliser PuTTY ou le terminal Windows (PowerShell/CMD avec OpenSSH).

### Étape 2 : Mise à jour du système

Une fois connecté, mettez à jour tous les paquets système :

```bash
# Mettre à jour la liste des paquets disponibles
sudo apt update

# Mettre à niveau tous les paquets installés
sudo apt upgrade -y

# Nettoyer les paquets inutiles
sudo apt autoremove -y
```

**📝 Explication :**
- `apt update` : Télécharge la liste des paquets disponibles
- `apt upgrade -y` : Installe les mises à jour (le `-y` répond automatiquement "oui")
- `apt autoremove -y` : Supprime les paquets qui ne sont plus nécessaires

### Étape 3 : Installation des dépendances système

Installez tous les outils nécessaires :

```bash
# Installer les outils de base
sudo apt install -y git curl wget vim nano build-essential

# Installer les dépendances Python
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Installer les dépendances pour PostgreSQL (base de données production)
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Installer Nginx (serveur web)
sudo apt install -y nginx

# Installer les outils de sécurité
sudo apt install -y ufw fail2ban
```

**📝 Explication des paquets :**
- `git` : Pour cloner votre projet depuis GitHub
- `curl, wget` : Pour télécharger des fichiers
- `vim, nano` : Éditeurs de texte en ligne de commande
- `build-essential` : Outils de compilation (gcc, make, etc.)
- `python3-*` : Python et ses outils
- `postgresql` : Base de données pour la production
- `nginx` : Serveur web haute performance
- `ufw` : Pare-feu simple
- `fail2ban` : Protection contre les attaques par force brute

### Étape 4 : Installation de Node.js

Node.js est nécessaire pour le frontend Nuxt.js :

```bash
# Télécharger et installer Node.js 20.x (version LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Vérifier les versions installées
node --version    # Devrait afficher v20.x.x
npm --version     # Devrait afficher 10.x.x
```

**💡 Pourquoi Node.js 20 ?** C'est une version LTS (Long Term Support) stable et compatible avec Nuxt.js 4.

### Étape 5 : Configuration du pare-feu

Configurez le pare-feu pour autoriser uniquement les connexions nécessaires :

```bash
# Autoriser SSH (IMPORTANT : à faire en premier pour ne pas vous bloquer)
sudo ufw allow OpenSSH
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Activer le pare-feu
sudo ufw enable

# Vérifier le statut
sudo ufw status
```

**⚠️ ATTENTION :** Assurez-vous d'autoriser SSH AVANT d'activer le pare-feu, sinon vous serez bloqué !

**📝 Explication des ports :**
- Port 22 : SSH (connexion à distance)
- Port 80 : HTTP (site web non sécurisé)
- Port 443 : HTTPS (site web sécurisé avec SSL)

### Étape 6 : Préparation du répertoire de travail

Créez le répertoire pour l'application :

```bash
# Créer le répertoire de travail
mkdir -p /root/GVB-Sign
cd /root/GVB-Sign
```

**💡 Note :** Ce guide utilise l'utilisateur root directement. Les chemins sont adaptés en conséquence (/root au lieu de /home).

---


## 📦 Déploiement en Développement

Cette section vous guide pour déployer l'application en mode développement, idéal pour tester et développer.

### Étape 1 : Cloner le projet

```bash
# Se placer dans le répertoire de travail
cd /root

# Cloner le projet depuis GitHub
git clone https://github.com/votre-username/GVB-Sign.git

# Entrer dans le répertoire du projet
cd GVB-Sign
```

**💡 Remplacez** `votre-username` par votre nom d'utilisateur GitHub.

### Étape 2 : Configuration du Backend Django (Développement)

#### 2.1 Créer et activer l'environnement virtuel Python

```bash
# Aller dans le dossier backend
cd /root/GVB-Sign/backend

# Créer un environnement virtuel Python
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Votre prompt devrait maintenant afficher (venv) au début
```

**📝 Explication :**
- `python3 -m venv venv` : Crée un environnement virtuel isolé nommé "venv"
- `source venv/bin/activate` : Active l'environnement virtuel
- Une fois activé, toutes les installations Python seront isolées dans cet environnement

**💡 Pour désactiver l'environnement virtuel plus tard :**
```bash
deactivate
```

#### 2.2 Installer les dépendances Python

```bash
# S'assurer que l'environnement virtuel est activé (vous devez voir (venv) dans le prompt)

# Créer le fichier requirements.txt avec les dépendances nécessaires
cat > requirements.txt << 'EOF'
Django==5.2.5
djangorestframework==3.15.2
django-cors-headers==4.6.0
python-decouple==3.8
Pillow==11.1.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
EOF

# Installer toutes les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

**📝 Explication des dépendances :**
- `Django` : Framework web Python
- `djangorestframework` : Pour créer des API REST
- `django-cors-headers` : Gestion des requêtes cross-origin (frontend ↔ backend)
- `python-decouple` : Gestion des variables d'environnement
- `Pillow` : Traitement d'images (signatures, QR codes)
- `psycopg2-binary` : Connecteur PostgreSQL
- `gunicorn` : Serveur WSGI pour la production

#### 2.3 Configuration de la base de données

```bash
# Toujours dans /root/GVB-Sign/backend avec l'environnement virtuel activé

# Créer les migrations de base de données
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (admin)
python manage.py createsuperuser
```

**📝 Lors de la création du superutilisateur, vous devrez fournir :**
- Email (utilisé comme identifiant)
- Prénom
- Nom
- Mot de passe (tapé deux fois, invisible à l'écran)

**💡 Exemple :**
```
Email: admin@gvbsign.com
Prénom: Admin
Nom: GVB
Password: ********
Password (again): ********
```

#### 2.4 Collecter les fichiers statiques

```bash
# Collecter tous les fichiers statiques (CSS, JS, images)
python manage.py collectstatic --noinput
```

#### 2.5 Démarrer le serveur de développement Django

```bash
# Démarrer le serveur sur toutes les interfaces (0.0.0.0) pour être accessible depuis l'extérieur
python manage.py runserver 0.0.0.0:8000
```

**📝 Explication :**
- `0.0.0.0` : Écoute sur toutes les interfaces réseau (accessible depuis l'extérieur)
- `8000` : Port d'écoute
- Le serveur sera accessible à `http://votre_ip:8000`

**⚠️ IMPORTANT :** Ce serveur est pour le développement uniquement. Pour la production, nous utiliserons Gunicorn.

**💡 Pour arrêter le serveur :** Appuyez sur `Ctrl + C`

**🔍 Tester le backend :**
Ouvrez votre navigateur et allez à :
- `http://92.112.184.194:8000/admin/` - Interface d'administration Django
- `http://92.112.184.194:8000/api/auth/` - API d'authentification

### Étape 3 : Configuration du Frontend Nuxt.js (Développement)

#### 3.1 Ouvrir un nouveau terminal SSH

Ouvrez une **nouvelle connexion SSH** à votre VPS (gardez le backend qui tourne dans l'autre terminal).

```bash
# Nouvelle connexion SSH
ssh root@92.112.184.194
```

#### 3.2 Installer les dépendances Node.js

```bash
# Aller dans le dossier frontend
cd /root/GVB-Sign/frontend

# Installer toutes les dépendances npm
npm install
```

**⏱️ Cette étape peut prendre 5-10 minutes** selon votre connexion Internet.

**📝 Explication :**
- `npm install` : Lit le fichier `package.json` et installe toutes les dépendances listées
- Les dépendances sont installées dans le dossier `node_modules/`

#### 3.3 Configuration de l'URL du backend

Avant de démarrer le frontend, configurez l'URL du backend :

```bash
# Créer un fichier .env pour les variables d'environnement
nano .env
```

Ajoutez le contenu suivant :

```env
# URL de l'API backend
NUXT_PUBLIC_API_URL=http://92.112.184.194:8000
```

**💾 Pour sauvegarder dans nano :**
1. Appuyez sur `Ctrl + O` (pour écrire)
2. Appuyez sur `Entrée` (pour confirmer)
3. Appuyez sur `Ctrl + X` (pour quitter)

#### 3.4 Mettre à jour les URLs dans les services

Modifiez les fichiers de services pour utiliser l'IP de votre VPS :

```bash
# Éditer le service d'authentification
nano services/AuthApiService.js
```

Changez la ligne :
```javascript
this.baseURL = 'http://127.0.0.1:8000/api/auth'
```

En :
```javascript
this.baseURL = 'http://92.112.184.194:8000/api/auth'
```

Faites de même pour les autres services :

```bash
# Service de signatures
nano services/SignatureApiService.js
```

Changez :
```javascript
this.baseURL = 'http://127.0.0.1:8000/api/signatures'
```

En :
```javascript
this.baseURL = 'http://92.112.184.194:8000/api/signatures'
```

**💡 Astuce :** Utilisez `Ctrl + W` dans nano pour rechercher rapidement "127.0.0.1"

#### 3.5 Mettre à jour le store d'authentification

```bash
# Éditer le store auth
nano stores/auth.js
```

Remplacez toutes les occurrences de `http://127.0.0.1:8000` par `http://92.112.184.194:8000`

**💡 Il y a plusieurs occurrences dans ce fichier, assurez-vous de toutes les remplacer.**

#### 3.6 Démarrer le serveur de développement Nuxt

```bash
# Toujours dans /root/GVB-Sign/frontend

# Démarrer le serveur de développement
npm run dev -- --host 0.0.0.0 --port 3000
```

**📝 Explication :**
- `npm run dev` : Lance le serveur de développement Nuxt
- `--host 0.0.0.0` : Écoute sur toutes les interfaces (accessible depuis l'extérieur)
- `--port 3000` : Port d'écoute

**⏱️ Le démarrage peut prendre 30-60 secondes.**

Vous devriez voir un message comme :
```
✔ Nuxt is ready!
  ➜ Local:    http://localhost:3000/
  ➜ Network:  http://92.112.184.194:3000/
```

**🔍 Tester le frontend :**
Ouvrez votre navigateur et allez à `http://92.112.184.194:3000`

### Étape 4 : Vérification du déploiement en développement

#### 4.1 Vérifier que les deux serveurs fonctionnent

Vous devriez avoir :
- **Terminal 1** : Backend Django sur le port 8000
- **Terminal 2** : Frontend Nuxt sur le port 3000

#### 4.2 Tester les fonctionnalités

1. **Page d'accueil** : `http://92.112.184.194:3000`
2. **Inscription** : Créez un nouveau compte
3. **Connexion** : Connectez-vous avec le compte créé
4. **Admin Django** : `http://92.112.184.194:8000/admin/`

#### 4.3 Vérifier les logs

**Backend (Terminal 1) :**
```
[07/May/2026 10:30:15] "GET /api/auth/profile/ HTTP/1.1" 200 156
[07/May/2026 10:30:20] "POST /api/auth/login/ HTTP/1.1" 200 245
```

**Frontend (Terminal 2) :**
```
✔ Vite server built in 1234ms
✔ Nitro built in 567ms
```

### Étape 5 : Garder les serveurs actifs

Pour que les serveurs continuent de fonctionner même après la déconnexion SSH, utilisez `screen` ou `tmux`.

#### Option A : Utiliser screen

```bash
# Installer screen
sudo apt install -y screen

# Créer une session pour le backend
screen -S backend
cd /root/GVB-Sign/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# Détacher la session : Ctrl + A, puis D

# Créer une session pour le frontend
screen -S frontend
cd /root/GVB-Sign/frontend
npm run dev -- --host 0.0.0.0 --port 3000

# Détacher la session : Ctrl + A, puis D

# Lister les sessions actives
screen -ls

# Se rattacher à une session
screen -r backend   # ou screen -r frontend
```

**📝 Commandes screen utiles :**
- `Ctrl + A, puis D` : Détacher la session (le processus continue)
- `screen -ls` : Lister toutes les sessions
- `screen -r nom` : Se rattacher à une session
- `exit` : Fermer une session (dans la session)

#### Option B : Utiliser tmux

```bash
# Installer tmux
sudo apt install -y tmux

# Créer une session pour le backend
tmux new -s backend
cd /root/GVB-Sign/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# Détacher la session : Ctrl + B, puis D

# Créer une session pour le frontend
tmux new -s frontend
cd /root/GVB-Sign/frontend
npm run dev -- --host 0.0.0.0 --port 3000

# Détacher la session : Ctrl + B, puis D

# Lister les sessions
tmux ls

# Se rattacher à une session
tmux attach -t backend   # ou tmux attach -t frontend
```

**📝 Commandes tmux utiles :**
- `Ctrl + B, puis D` : Détacher la session
- `tmux ls` : Lister toutes les sessions
- `tmux attach -t nom` : Se rattacher à une session
- `exit` : Fermer une session

---


## 🏭 Déploiement en Production

Le déploiement en production nécessite des configurations plus robustes et sécurisées.

### Étape 1 : Configuration de PostgreSQL (Base de données production)

#### 1.1 Créer la base de données et l'utilisateur

```bash
# Se connecter à PostgreSQL en tant que superutilisateur
sudo -u postgres psql

# Dans le shell PostgreSQL, exécutez les commandes suivantes :
```

```sql
-- Créer un utilisateur pour l'application
CREATE USER gvbsign_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Créer la base de données
CREATE DATABASE gvbsign_db OWNER gvbsign_user;

-- Donner tous les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON DATABASE gvbsign_db TO gvbsign_user;

-- Quitter PostgreSQL
\q
```

**💡 Remplacez** `votre_mot_de_passe_securise` par un mot de passe fort et unique.

**📝 Exemple de mot de passe fort :**
```
GvB$ign2026!Pr0d#Secure
```

#### 1.2 Tester la connexion

```bash
# Tester la connexion à la base de données
psql -U gvbsign_user -d gvbsign_db -h localhost

# Si la connexion réussit, vous verrez :
# gvbsign_db=>

# Quitter avec :
\q
```

### Étape 2 : Configuration du Backend pour la Production

#### 2.1 Créer un fichier de configuration d'environnement

```bash
# Aller dans le dossier backend
cd /root/GVB-Sign/backend

# Créer un fichier .env pour les variables d'environnement
nano .env
```

Ajoutez le contenu suivant :

```env
# Configuration Django
SECRET_KEY=votre_cle_secrete_django_tres_longue_et_aleatoire
DEBUG=False
ALLOWED_HOSTS=92.112.184.194,localhost,127.0.0.1

# Base de données PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gvbsign_db
DB_USER=gvbsign_user
DB_PASSWORD=votre_mot_de_passe_securise
DB_HOST=localhost
DB_PORT=5432

# CORS (Frontend)
CORS_ALLOWED_ORIGINS=http://92.112.184.194,http://92.112.184.194:3000

# URLs
FRONTEND_URL=http://92.112.184.194
BACKEND_URL=http://92.112.184.194:8000
```

**💡 Pour générer une SECRET_KEY Django :**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**📝 Explication des variables :**
- `SECRET_KEY` : Clé secrète Django (TRÈS IMPORTANT, gardez-la secrète !)
- `DEBUG=False` : Désactive le mode debug (OBLIGATOIRE en production)
- `ALLOWED_HOSTS` : Liste des domaines/IPs autorisés
- `DB_*` : Configuration de la base de données PostgreSQL
- `CORS_ALLOWED_ORIGINS` : Domaines autorisés pour les requêtes CORS

#### 2.2 Modifier settings.py pour utiliser les variables d'environnement

```bash
# Éditer le fichier settings.py
nano gvb_backend/settings.py
```

Modifiez les sections suivantes :

```python
from pathlib import Path
from decouple import config  # Ajouter cette ligne en haut

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-12nbr$1+0tn$z9t+d=7e2ndqlod*e0$ky#zt+sa43pexw+=_ba')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

**💾 Sauvegardez** le fichier (`Ctrl + O`, `Entrée`, `Ctrl + X`)

#### 2.3 Appliquer les migrations sur PostgreSQL

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur pour la production
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

#### 2.4 Tester avec Gunicorn

```bash
# Tester que Gunicorn fonctionne
gunicorn gvb_backend.wsgi:application --bind 0.0.0.0:8000

# Si tout fonctionne, arrêtez avec Ctrl + C
```

### Étape 3 : Configuration du Frontend pour la Production

#### 3.1 Créer le fichier de configuration d'environnement

```bash
# Aller dans le dossier frontend
cd /root/GVB-Sign/frontend

# Créer un fichier .env pour la production
nano .env.production
```

Ajoutez :

```env
# URL de l'API backend en production
NUXT_PUBLIC_API_URL=http://92.112.184.194:8000
```

#### 3.2 Mettre à jour les URLs dans les services (Production)

Créez un fichier de configuration centralisé :

```bash
# Créer un fichier de configuration
nano config/api.config.js
```

Ajoutez :

```javascript
// Configuration des URLs API selon l'environnement
export const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000',
    authURL: 'http://localhost:8000/api/auth',
    signaturesURL: 'http://localhost:8000/api/signatures',
    organizationsURL: 'http://localhost:8000/api/organizations'
  },
  production: {
    baseURL: process.env.NUXT_PUBLIC_API_URL || 'http://92.112.184.194:8000',
    authURL: `${process.env.NUXT_PUBLIC_API_URL || 'http://92.112.184.194:8000'}/api/auth`,
    signaturesURL: `${process.env.NUXT_PUBLIC_API_URL || 'http://92.112.184.194:8000'}/api/signatures`,
    organizationsURL: `${process.env.NUXT_PUBLIC_API_URL || 'http://92.112.184.194:8000'}/api/organizations`
  }
}

// Déterminer l'environnement actuel
const currentEnv = process.env.NODE_ENV || 'development'

// Exporter la configuration pour l'environnement actuel
export default API_CONFIG[currentEnv]
```

#### 3.3 Builder l'application pour la production

```bash
# Toujours dans /root/GVB-Sign/frontend

# Installer les dépendances si ce n'est pas déjà fait
npm install

# Builder l'application pour la production
npm run build

# Cela va créer un dossier .output/ avec l'application optimisée
```

**⏱️ Le build peut prendre 2-5 minutes.**

#### 3.4 Tester le build en production

```bash
# Prévisualiser le build de production
npm run preview
```

### Étape 4 : Configuration de Systemd (Services automatiques)

Créez des services systemd pour que les applications démarrent automatiquement.

#### 4.1 Service pour le Backend (Gunicorn)

```bash
# Créer le fichier de service
sudo nano /etc/systemd/system/gvbsign-backend.service
```

Ajoutez :

```ini
[Unit]
Description=GVB Sign Backend (Gunicorn)
After=network.target postgresql.service

[Service]
Type=notify
User=root
Group=root
WorkingDirectory=/root/GVB-Sign/backend
Environment="PATH=/root/GVB-Sign/backend/venv/bin"
ExecStart=/root/GVB-Sign/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/root/GVB-Sign/backend/gvbsign.sock \
    --timeout 120 \
    --access-logfile /root/GVB-Sign/backend/logs/access.log \
    --error-logfile /root/GVB-Sign/backend/logs/error.log \
    gvb_backend.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**📝 Explication :**
- `--workers 3` : 3 processus workers (recommandé : 2-4 × nombre de CPU)
- `--bind unix:...` : Utilise un socket Unix (plus rapide que TCP)
- `--timeout 120` : Timeout de 120 secondes pour les requêtes longues
- `Restart=always` : Redémarre automatiquement en cas d'erreur

#### 4.2 Créer le dossier de logs

```bash
# Créer le dossier de logs
mkdir -p /root/GVB-Sign/backend/logs

# Donner les bonnes permissions
chmod 755 /root/GVB-Sign/backend/logs
```

#### 4.3 Service pour le Frontend (Nuxt)

```bash
# Créer le fichier de service
sudo nano /etc/systemd/system/gvbsign-frontend.service
```

Ajoutez :

```ini
[Unit]
Description=GVB Sign Frontend (Nuxt.js)
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/GVB-Sign/frontend
Environment="NODE_ENV=production"
Environment="PORT=3000"
Environment="HOST=0.0.0.0"
ExecStart=/usr/bin/node /root/GVB-Sign/frontend/.output/server/index.mjs

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4.4 Activer et démarrer les services

```bash
# Recharger la configuration systemd
sudo systemctl daemon-reload

# Activer les services (démarrage automatique au boot)
sudo systemctl enable gvbsign-backend
sudo systemctl enable gvbsign-frontend

# Démarrer les services
sudo systemctl start gvbsign-backend
sudo systemctl start gvbsign-frontend

# Vérifier le statut
sudo systemctl status gvbsign-backend
sudo systemctl status gvbsign-frontend
```

**📝 Commandes systemctl utiles :**
```bash
# Démarrer un service
sudo systemctl start nom_service

# Arrêter un service
sudo systemctl stop nom_service

# Redémarrer un service
sudo systemctl restart nom_service

# Voir les logs d'un service
sudo journalctl -u nom_service -f

# Voir les dernières lignes de logs
sudo journalctl -u nom_service -n 50
```

---


## 🌐 Configuration Nginx

Nginx servira de reverse proxy et gérera les certificats SSL.

### Étape 1 : Configuration de base Nginx

#### 1.1 Supprimer la configuration par défaut

```bash
# Supprimer le lien symbolique de la configuration par défaut
sudo rm /etc/nginx/sites-enabled/default
```

#### 1.2 Créer la configuration pour GVB Sign

```bash
# Créer le fichier de configuration
sudo nano /etc/nginx/sites-available/gvbsign
```

Ajoutez la configuration suivante :

```nginx
# Configuration pour le Backend API
upstream backend {
    server unix:/root/GVB-Sign/backend/gvbsign.sock fail_timeout=0;
}

# Configuration pour le Frontend
upstream frontend {
    server 127.0.0.1:3000;
}

# Configuration HTTP
server {
    listen 80;
    listen [::]:80;
    server_name 92.112.184.194;

    # Logs
    access_log /var/log/nginx/gvbsign_access.log;
    error_log /var/log/nginx/gvbsign_error.log;

    # Taille maximale des uploads (pour les documents PDF)
    client_max_body_size 50M;

    # Frontend (Nuxt.js)
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Admin Django
    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Fichiers statiques Django
    location /static/ {
        alias /root/GVB-Sign/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Fichiers media (uploads)
    location /media/ {
        alias /root/GVB-Sign/backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

**💡 Note :** La configuration utilise directement l'IP 92.112.184.194. Si vous avez un nom de domaine, remplacez l'IP par votre domaine.

#### 1.3 Activer la configuration

```bash
# Créer un lien symbolique vers sites-enabled
sudo ln -s /etc/nginx/sites-available/gvbsign /etc/nginx/sites-enabled/

# Tester la configuration Nginx
sudo nginx -t

# Si le test réussit, vous verrez :
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status nginx
```

### Étape 2 : Configuration SSL avec Let's Encrypt (HTTPS)

**⚠️ Prérequis :** Vous devez avoir un nom de domaine pointant vers votre VPS.

#### 2.1 Installer Certbot

```bash
# Installer Certbot et le plugin Nginx
sudo apt install -y certbot python3-certbot-nginx
```

#### 2.2 Obtenir un certificat SSL

```bash
# ⚠️ IMPORTANT: Let's Encrypt ne fonctionne PAS avec une adresse IP
# Vous devez avoir un nom de domaine pour utiliser Let's Encrypt

# Si vous avez un nom de domaine, remplacez 92.112.184.194 par votre domaine dans la config Nginx
# puis exécutez :
sudo certbot --nginx -d votre_domaine.com -d www.votre_domaine.com

# Si vous utilisez uniquement l'IP 92.112.184.194, vous devrez :
# 1. Soit utiliser un certificat auto-signé (non recommandé pour la production)
# 2. Soit obtenir un nom de domaine (recommandé)

# Suivez les instructions :
# 1. Entrez votre email
# 2. Acceptez les conditions d'utilisation
# 3. Choisissez si vous voulez partager votre email (optionnel)
# 4. Choisissez de rediriger HTTP vers HTTPS (recommandé : option 2)
```

**📝 Certbot va automatiquement :**
- Obtenir le certificat SSL
- Modifier votre configuration Nginx
- Configurer le renouvellement automatique

#### 2.3 Vérifier le renouvellement automatique

```bash
# Tester le renouvellement automatique
sudo certbot renew --dry-run

# Si le test réussit, le renouvellement automatique est configuré
```

**💡 Les certificats Let's Encrypt sont valables 90 jours** et se renouvellent automatiquement.

#### 2.4 Configuration Nginx finale avec SSL

Après l'installation de Certbot, votre configuration devrait ressembler à :

```nginx
# Redirection HTTP vers HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name 92.112.184.194;
    return 301 https://$server_name$request_uri;
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name 92.112.184.194;

    # Certificats SSL (gérés par Certbot)
    # Note: Let's Encrypt ne fonctionne qu'avec un nom de domaine, pas avec une IP
    # Si vous utilisez une IP, vous devrez utiliser un certificat auto-signé
    ssl_certificate /etc/letsencrypt/live/92.112.184.194/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/92.112.184.194/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Logs
    access_log /var/log/nginx/gvbsign_access.log;
    error_log /var/log/nginx/gvbsign_error.log;

    # Taille maximale des uploads
    client_max_body_size 50M;

    # Headers de sécurité
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend (Nuxt.js)
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Admin Django
    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Fichiers statiques Django
    location /static/ {
        alias /root/GVB-Sign/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Fichiers media (uploads)
    location /media/ {
        alias /root/GVB-Sign/backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

### Étape 3 : Optimisations Nginx

#### 3.1 Configuration de la compression

```bash
# Éditer la configuration principale de Nginx
sudo nano /etc/nginx/nginx.conf
```

Ajoutez ou modifiez dans la section `http` :

```nginx
http {
    # ... autres configurations ...

    # Compression Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/rss+xml font/truetype font/opentype 
               application/vnd.ms-fontobject image/svg+xml;
    gzip_disable "msie6";

    # Buffers
    client_body_buffer_size 128k;
    client_max_body_size 50M;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 16k;

    # Timeouts
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 65;
    send_timeout 10;

    # ... autres configurations ...
}
```

#### 3.2 Redémarrer Nginx

```bash
# Tester la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx
```

### Étape 4 : Configuration du pare-feu pour Nginx

```bash
# Autoriser Nginx Full (HTTP + HTTPS)
sudo ufw allow 'Nginx Full'

# Supprimer les règles individuelles si elles existent
sudo ufw delete allow 80/tcp
sudo ufw delete allow 443/tcp

# Vérifier le statut
sudo ufw status
```

---

## 🔒 Sécurité et Maintenance

### Sécurité

#### 1. Configurer Fail2Ban

Fail2Ban protège contre les attaques par force brute.

```bash
# Créer une configuration pour Nginx
sudo nano /etc/fail2ban/jail.local
```

Ajoutez :

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/gvbsign_error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/gvbsign_access.log

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/gvbsign_access.log

[nginx-noproxy]
enabled = true
port = http,https
logpath = /var/log/nginx/gvbsign_access.log
```

```bash
# Redémarrer Fail2Ban
sudo systemctl restart fail2ban

# Vérifier le statut
sudo fail2ban-client status
```

#### 2. Sauvegardes automatiques

Créez un script de sauvegarde :

```bash
# Créer le script de sauvegarde
nano ~/backup.sh
```

Ajoutez :

```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="gvbsign_db"
DB_USER="gvbsign_user"

# Créer le dossier de sauvegarde s'il n'existe pas
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Sauvegarder les fichiers media
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /root/GVB-Sign/backend/media/

# Supprimer les sauvegardes de plus de 7 jours
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Sauvegarde terminée : $DATE"
```

```bash
# Rendre le script exécutable
chmod +x ~/backup.sh

# Tester le script
./backup.sh

# Ajouter une tâche cron pour exécuter le script tous les jours à 2h du matin
crontab -e

# Ajoutez cette ligne :
0 2 * * * /root/backup.sh >> /root/backup.log 2>&1
```

#### 3. Mises à jour de sécurité automatiques

```bash
# Installer unattended-upgrades
sudo apt install -y unattended-upgrades

# Configurer les mises à jour automatiques
sudo dpkg-reconfigure -plow unattended-upgrades

# Choisir "Oui" pour activer les mises à jour automatiques
```

### Maintenance

#### Commandes utiles

```bash
# Voir les logs du backend
sudo journalctl -u gvbsign-backend -f

# Voir les logs du frontend
sudo journalctl -u gvbsign-frontend -f

# Voir les logs Nginx
sudo tail -f /var/log/nginx/gvbsign_access.log
sudo tail -f /var/log/nginx/gvbsign_error.log

# Redémarrer tous les services
sudo systemctl restart gvbsign-backend gvbsign-frontend nginx

# Vérifier l'espace disque
df -h

# Vérifier l'utilisation de la RAM
free -h

# Vérifier les processus
htop  # ou top si htop n'est pas installé
```

#### Mise à jour de l'application

```bash
# Aller dans le dossier du projet
cd /root/GVB-Sign

# Récupérer les dernières modifications
git pull origin main

# Mettre à jour le backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gvbsign-backend

# Mettre à jour le frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart gvbsign-frontend

# Redémarrer Nginx
sudo systemctl restart nginx
```

---

## 🔧 Dépannage

### Problèmes courants

#### 1. Le backend ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u gvbsign-backend -n 50

# Vérifier que PostgreSQL fonctionne
sudo systemctl status postgresql

# Vérifier la connexion à la base de données
psql -U gvbsign_user -d gvbsign_db -h localhost

# Vérifier les permissions du socket
ls -la /root/GVB-Sign/backend/gvbsign.sock
```

#### 2. Le frontend ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u gvbsign-frontend -n 50

# Vérifier que le build existe
ls -la /root/GVB-Sign/frontend/.output/

# Rebuilder si nécessaire
cd /root/GVB-Sign/frontend
npm run build
sudo systemctl restart gvbsign-frontend
```

#### 3. Erreur 502 Bad Gateway

```bash
# Vérifier que les services fonctionnent
sudo systemctl status gvbsign-backend
sudo systemctl status gvbsign-frontend

# Vérifier les logs Nginx
sudo tail -f /var/log/nginx/gvbsign_error.log

# Vérifier que le socket existe
ls -la /root/GVB-Sign/backend/gvbsign.sock

# Redémarrer tous les services
sudo systemctl restart gvbsign-backend gvbsign-frontend nginx
```

#### 4. Erreur CORS

```bash
# Vérifier la configuration CORS dans settings.py
nano /root/GVB-Sign/backend/gvb_backend/settings.py

# Vérifier que CORS_ALLOWED_ORIGINS contient votre domaine
# Redémarrer le backend
sudo systemctl restart gvbsign-backend
```

#### 5. Fichiers statiques ne se chargent pas

```bash
# Recollecterles fichiers statiques
cd /root/GVB-Sign/backend
source venv/bin/activate
python manage.py collectstatic --noinput

# Vérifier les permissions
chmod -R 755 /root/GVB-Sign/backend/staticfiles/

# Redémarrer Nginx
sudo systemctl restart nginx
```

#### 6. Base de données corrompue

```bash
# Restaurer depuis une sauvegarde
psql -U gvbsign_user -d gvbsign_db < /root/backups/db_backup_YYYYMMDD_HHMMSS.sql

# Ou recréer la base de données
sudo -u postgres psql
DROP DATABASE gvbsign_db;
CREATE DATABASE gvbsign_db OWNER gvbsign_user;
\q

# Réappliquer les migrations
cd /root/GVB-Sign/backend
source venv/bin/activate
python manage.py migrate
```

### Vérifications de santé

```bash
# Script de vérification rapide
cat > ~/check_health.sh << 'EOF'
#!/bin/bash

echo "=== Vérification de santé GVB Sign ==="
echo ""

echo "1. Services systemd :"
systemctl is-active gvbsign-backend && echo "✅ Backend actif" || echo "❌ Backend inactif"
systemctl is-active gvbsign-frontend && echo "✅ Frontend actif" || echo "❌ Frontend inactif"
systemctl is-active nginx && echo "✅ Nginx actif" || echo "❌ Nginx inactif"
systemctl is-active postgresql && echo "✅ PostgreSQL actif" || echo "❌ PostgreSQL inactif"
echo ""

echo "2. Ports en écoute :"
sudo netstat -tlnp | grep -E ':(80|443|3000|5432)' || echo "Aucun port trouvé"
echo ""

echo "3. Espace disque :"
df -h | grep -E '(Filesystem|/$)'
echo ""

echo "4. Mémoire :"
free -h
echo ""

echo "5. Dernières erreurs backend :"
sudo journalctl -u gvbsign-backend -n 5 --no-pager
echo ""

echo "6. Dernières erreurs frontend :"
sudo journalctl -u gvbsign-frontend -n 5 --no-pager
echo ""

echo "=== Fin de la vérification ==="
EOF

chmod +x ~/check_health.sh
./check_health.sh
```

---

## 📚 Ressources supplémentaires

### Documentation officielle

- **Django** : https://docs.djangoproject.com/
- **Nuxt.js** : https://nuxt.com/docs
- **Nginx** : https://nginx.org/en/docs/
- **PostgreSQL** : https://www.postgresql.org/docs/
- **Let's Encrypt** : https://letsencrypt.org/docs/

### Commandes de référence rapide

```bash
# Systemd
sudo systemctl start|stop|restart|status nom_service
sudo journalctl -u nom_service -f

# Nginx
sudo nginx -t                    # Tester la configuration
sudo systemctl reload nginx      # Recharger sans interruption
sudo tail -f /var/log/nginx/*.log

# PostgreSQL
sudo -u postgres psql            # Se connecter à PostgreSQL
\l                               # Lister les bases de données
\c nom_db                        # Se connecter à une base
\dt                              # Lister les tables
\q                               # Quitter

# Python/Django
source venv/bin/activate         # Activer l'environnement virtuel
python manage.py shell           # Shell Django interactif
python manage.py dbshell         # Shell de base de données

# Git
git pull origin main             # Récupérer les modifications
git status                       # Voir l'état du dépôt
git log --oneline -10            # Voir les 10 derniers commits
```

---

## ✅ Checklist finale

### Avant la mise en production

- [ ] Toutes les dépendances sont installées
- [ ] PostgreSQL est configuré et fonctionne
- [ ] Les variables d'environnement sont configurées
- [ ] DEBUG=False dans settings.py
- [ ] SECRET_KEY est unique et sécurisée
- [ ] Les migrations sont appliquées
- [ ] Les fichiers statiques sont collectés
- [ ] Les services systemd sont configurés et actifs
- [ ] Nginx est configuré et fonctionne
- [ ] SSL/HTTPS est configuré (si domaine disponible)
- [ ] Le pare-feu est configuré
- [ ] Fail2Ban est actif
- [ ] Les sauvegardes automatiques sont configurées
- [ ] Les logs sont accessibles et surveillés
- [ ] L'application est testée et fonctionnelle

### Tests de fonctionnement

- [ ] Page d'accueil accessible
- [ ] Inscription d'un nouvel utilisateur
- [ ] Connexion avec un utilisateur existant
- [ ] Création d'une organisation
- [ ] Upload et signature d'un document
- [ ] Vérification d'une signature via QR code
- [ ] Interface d'administration accessible
- [ ] Fichiers media accessibles

---

## 🎉 Félicitations !

Vous avez maintenant une application GVB Sign complètement déployée et sécurisée sur votre VPS Ubuntu !

**Pour toute question ou problème**, consultez les logs et la section dépannage de ce guide.

**Bon déploiement ! 🚀**
