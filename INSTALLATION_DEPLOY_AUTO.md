# 🚀 Installation du Déploiement Automatique

Ce guide explique comment mettre en place le déploiement automatique pour GVB Sign.

## 📋 Fonctionnement

Le système vérifie toutes les 2 minutes s'il y a de nouvelles modifications sur GitHub. Si oui, il :
1. ✅ Fait un `git pull`
2. ✅ Installe les nouvelles dépendances si nécessaire
3. ✅ Applique les migrations de base de données
4. ✅ Rebuild le frontend si modifié
5. ✅ Redémarre les services concernés
6. ✅ Log toutes les opérations

---

## 🔧 Installation sur le VPS

### Étape 1 : Copier le script sur le VPS

```bash
# Sur votre machine locale, copiez le script vers le VPS
scp deploy-vps.sh root@92.112.184.194:/root/

# Ou créez-le directement sur le VPS
ssh root@92.112.184.194
nano /root/deploy-vps.sh
# Copiez le contenu du fichier deploy-vps.sh
```

### Étape 2 : Rendre le script exécutable

```bash
# Sur le VPS
chmod +x /root/deploy-vps.sh
```

### Étape 3 : Créer le fichier de log

```bash
# Créer le fichier de log
sudo touch /var/log/gvb-deploy.log

# Donner les permissions
sudo chmod 644 /var/log/gvb-deploy.log
```

### Étape 4 : Tester le script manuellement

```bash
# Exécuter le script pour vérifier qu'il fonctionne
sudo /root/deploy-vps.sh

# Voir les logs
tail -f /var/log/gvb-deploy.log
```

### Étape 5 : Configurer le Cron Job

```bash
# Ouvrir l'éditeur crontab
crontab -e

# Ajouter cette ligne à la fin du fichier :
# Vérifie les mises à jour toutes les 2 minutes
*/2 * * * * /root/deploy-vps.sh >> /var/log/gvb-deploy-cron.log 2>&1
```

**Explication de la ligne cron :**
- `*/2 * * * *` : Toutes les 2 minutes
- `/root/deploy-vps.sh` : Script à exécuter
- `>> /var/log/gvb-deploy-cron.log 2>&1` : Rediriger les sorties vers un log

**Autres fréquences possibles :**
```bash
# Toutes les 5 minutes
*/5 * * * * /root/deploy-vps.sh >> /var/log/gvb-deploy-cron.log 2>&1

# Toutes les 10 minutes
*/10 * * * * /root/deploy-vps.sh >> /var/log/gvb-deploy-cron.log 2>&1

# Toutes les heures
0 * * * * /root/deploy-vps.sh >> /var/log/gvb-deploy-cron.log 2>&1
```

### Étape 6 : Vérifier que le cron fonctionne

```bash
# Voir les cron jobs actifs
crontab -l

# Voir les logs du cron
tail -f /var/log/gvb-deploy-cron.log

# Voir les logs du déploiement
tail -f /var/log/gvb-deploy.log
```

---

## 🧪 Test du Déploiement Automatique

### Test 1 : Modification simple

```bash
# Sur votre machine locale
cd ~/Documents/GVB_Sign

# Créer un fichier de test
echo "Test déploiement automatique" > TEST.txt

# Commit et push
git add TEST.txt
git commit -m "Test: déploiement automatique"
git push origin master

# Attendre 2-3 minutes et vérifier sur le VPS
ssh root@92.112.184.194
cd /home/GVB-Sign
ls -la TEST.txt  # Le fichier devrait être là
tail -20 /var/log/gvb-deploy.log  # Voir les logs
```

### Test 2 : Modification du backend

```bash
# Modifier un fichier Python
nano backend/authentication/models.py
# Ajouter un commentaire

git add backend/authentication/models.py
git commit -m "Test: modification backend"
git push origin master

# Le script devrait redémarrer le backend automatiquement
```

### Test 3 : Modification du frontend

```bash
# Modifier un composant
nano frontend/components/Header.vue
# Ajouter un commentaire

git add frontend/components/Header.vue
git commit -m "Test: modification frontend"
git push origin master

# Le script devrait rebuilder et redémarrer le frontend
```

---

## 📊 Surveillance et Logs

### Voir les logs en temps réel

```bash
# Logs du déploiement
tail -f /var/log/gvb-deploy.log

# Logs du cron
tail -f /var/log/gvb-deploy-cron.log

# Logs du backend
sudo journalctl -u gvbsign-backend -f

# Logs du frontend
sudo journalctl -u gvbsign-frontend -f
```

### Voir les derniers déploiements

```bash
# Voir les 50 dernières lignes
tail -50 /var/log/gvb-deploy.log

# Rechercher les déploiements réussis
grep "Déploiement terminé" /var/log/gvb-deploy.log

# Rechercher les erreurs
grep "❌" /var/log/gvb-deploy.log
```

---

## 🔧 Dépannage

### Le cron ne s'exécute pas

```bash
# Vérifier que le service cron est actif
sudo systemctl status cron

# Redémarrer le service cron
sudo systemctl restart cron

# Vérifier les logs système
sudo tail -f /var/log/syslog | grep CRON
```

### Le script échoue

```bash
# Exécuter manuellement pour voir l'erreur
sudo /root/deploy-vps.sh

# Vérifier les permissions
ls -la /root/deploy-vps.sh

# Vérifier que Git fonctionne
cd /home/GVB-Sign
git status
git pull origin master
```

### Git demande un mot de passe

```bash
# Configurer Git pour utiliser HTTPS avec token ou SSH
cd /home/GVB-Sign

# Option 1 : Utiliser un token GitHub
git remote set-url origin https://TOKEN@github.com/MARKUPsoft-corp/GVB-Sign.git

# Option 2 : Utiliser SSH (recommandé)
# Générer une clé SSH sur le VPS
ssh-keygen -t ed25519 -C "vps@gvbsign.com"

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub

# Ajouter la clé dans GitHub : Settings > SSH and GPG keys > New SSH key

# Changer l'URL du remote
git remote set-url origin git@github.com:MARKUPsoft-corp/GVB-Sign.git
```

---

## 🛑 Désactiver le Déploiement Automatique

```bash
# Désactiver temporairement
crontab -e
# Commenter la ligne avec #
# */2 * * * * /root/deploy-vps.sh >> /var/log/gvb-deploy-cron.log 2>&1

# Supprimer complètement
crontab -r
```

---

## 🎯 Améliorations Futures

### Option 1 : Webhooks GitHub (Déploiement instantané)

Au lieu d'attendre 2 minutes, GitHub peut notifier le VPS immédiatement.

**Avantages :**
- Déploiement instantané
- Pas de vérifications inutiles
- Plus efficace

**À faire :**
1. Créer un serveur webhook sur le VPS
2. Configurer GitHub pour envoyer des webhooks
3. Sécuriser avec un secret token

### Option 2 : GitHub Actions (CI/CD complet)

Exécuter des tests avant le déploiement.

**Avantages :**
- Tests automatiques
- Déploiement conditionnel
- Notifications

---

## 📝 Checklist d'Installation

- [ ] Script copié sur le VPS
- [ ] Script rendu exécutable (`chmod +x`)
- [ ] Fichier de log créé
- [ ] Script testé manuellement
- [ ] Cron job configuré
- [ ] Cron job vérifié (`crontab -l`)
- [ ] Test de déploiement effectué
- [ ] Logs surveillés

---

## 🎉 C'est Prêt !

Maintenant, à chaque fois que vous faites un `git push`, votre VPS se mettra à jour automatiquement dans les 2 minutes !

**Workflow de développement :**
1. Modifier le code localement
2. Tester localement
3. `git add .`
4. `git commit -m "Description"`
5. `git push origin master`
6. ☕ Attendre 2 minutes
7. ✅ Le VPS est à jour !
