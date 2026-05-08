#!/bin/bash

# Script de déploiement automatique pour GVB Sign
# Ce script sera exécuté par un cron job sur le VPS

# Configuration
PROJECT_DIR="/home/GVB-Sign"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_FILE="/var/log/gvb-deploy.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Fonction de log
log() {
    echo "[$DATE] $1" | tee -a "$LOG_FILE"
}

# Début du déploiement
log "=========================================="
log "🚀 Début du déploiement automatique"
log "=========================================="

# Aller dans le répertoire du projet
cd "$PROJECT_DIR" || {
    log "❌ Erreur: Impossible d'accéder au répertoire $PROJECT_DIR"
    exit 1
}

# Vérifier s'il y a des modifications sur GitHub
log "🔍 Vérification des mises à jour sur GitHub..."
git fetch origin master

# Comparer avec la version locale
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
    log "✅ Aucune mise à jour disponible. Code déjà à jour."
    exit 0
fi

log "📥 Nouvelles modifications détectées. Début du déploiement..."

# Sauvegarder le commit actuel
PREVIOUS_COMMIT=$(git rev-parse --short HEAD)
log "📌 Commit actuel: $PREVIOUS_COMMIT"

# Pull les modifications
log "⬇️  Git pull..."
git pull origin master >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    log "❌ Erreur lors du git pull"
    exit 1
fi

NEW_COMMIT=$(git rev-parse --short HEAD)
log "📌 Nouveau commit: $NEW_COMMIT"

# Vérifier si le backend a été modifié
BACKEND_CHANGED=$(git diff --name-only $PREVIOUS_COMMIT $NEW_COMMIT | grep "^backend/" | wc -l)
FRONTEND_CHANGED=$(git diff --name-only $PREVIOUS_COMMIT $NEW_COMMIT | grep "^frontend/" | wc -l)

# Déploiement du Backend si modifié
if [ "$BACKEND_CHANGED" -gt 0 ]; then
    log "🔧 Modifications détectées dans le backend"
    
    cd "$BACKEND_DIR" || exit 1
    
    # Activer l'environnement virtuel
    log "🐍 Activation de l'environnement virtuel Python..."
    source venv/bin/activate
    
    # Installer/Mettre à jour les dépendances
    if git diff --name-only $PREVIOUS_COMMIT $NEW_COMMIT | grep -q "requirements.txt"; then
        log "📦 Mise à jour des dépendances Python..."
        pip install -r requirements.txt >> "$LOG_FILE" 2>&1
    fi
    
    # Appliquer les migrations
    log "🗄️  Application des migrations..."
    python manage.py migrate >> "$LOG_FILE" 2>&1
    
    # Collecter les fichiers statiques
    log "📁 Collecte des fichiers statiques..."
    python manage.py collectstatic --noinput >> "$LOG_FILE" 2>&1
    
    # Redémarrer le service backend
    log "🔄 Redémarrage du service backend..."
    systemctl restart gvbsign-backend
    
    if [ $? -eq 0 ]; then
        log "✅ Backend redémarré avec succès"
    else
        log "❌ Erreur lors du redémarrage du backend"
        exit 1
    fi
    
    deactivate
else
    log "ℹ️  Aucune modification dans le backend"
fi

# Déploiement du Frontend si modifié
if [ "$FRONTEND_CHANGED" -gt 0 ]; then
    log "🎨 Modifications détectées dans le frontend"
    
    cd "$FRONTEND_DIR" || exit 1
    
    # Installer/Mettre à jour les dépendances
    if git diff --name-only $PREVIOUS_COMMIT $NEW_COMMIT | grep -q "package.json"; then
        log "📦 Mise à jour des dépendances Node.js..."
        npm install >> "$LOG_FILE" 2>&1
    fi
    
    # Rebuild le frontend
    log "🏗️  Build du frontend..."
    npm run build >> "$LOG_FILE" 2>&1
    
    if [ $? -ne 0 ]; then
        log "❌ Erreur lors du build du frontend"
        exit 1
    fi
    
    # Redémarrer le service frontend
    log "🔄 Redémarrage du service frontend..."
    systemctl restart gvbsign-frontend
    
    if [ $? -eq 0 ]; then
        log "✅ Frontend redémarré avec succès"
    else
        log "❌ Erreur lors du redémarrage du frontend"
        exit 1
    fi
else
    log "ℹ️  Aucune modification dans le frontend"
fi

# Redémarrer Nginx si nécessaire
if git diff --name-only $PREVIOUS_COMMIT $NEW_COMMIT | grep -q "nginx"; then
    log "🌐 Redémarrage de Nginx..."
    systemctl restart nginx
fi

# Vérifier l'état des services
log "🔍 Vérification de l'état des services..."
systemctl is-active --quiet gvbsign-backend && log "✅ Backend: actif" || log "❌ Backend: inactif"
systemctl is-active --quiet gvbsign-frontend && log "✅ Frontend: actif" || log "❌ Frontend: inactif"
systemctl is-active --quiet nginx && log "✅ Nginx: actif" || log "❌ Nginx: inactif"

log "=========================================="
log "🎉 Déploiement terminé avec succès!"
log "=========================================="

exit 0
