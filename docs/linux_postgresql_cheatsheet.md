# 🚀 Cheatsheet Serveur Linux + PostgreSQL + Tailscale

## 📡 Connexion SSH

### Se connecter au serveur
```bash
ssh alban@100.77.237.80
```

### Vérifier le statut Tailscale
```bash
tailscale status
tailscale ip -4  # Afficher l'IP Tailscale du serveur
```

---

## 🐘 PostgreSQL - Commandes essentielles

### Connexion à la base de données

**Depuis le serveur (local) :**
```bash
psql -U budget_user -d budget_app -h localhost
# Mot de passe : [TON_MOT_DE_PASSE]
```

**Depuis Windows via Tailscale :**
```bash
psql -U budget_user -d budget_app -h 100.77.237.80
# Mot de passe : [TON_MOT_DE_PASSE]
```

**String de connexion pour FastAPI/Python :**
```python
DATABASE_URL = "postgresql://budget_user:[TON_MOT_DE_PASSE]@100.77.237.80:5432/budget_app"
```

### Commandes PostgreSQL interactives

**Une fois connecté avec psql :**
```sql
-- Lister les bases de données
\l

-- Se connecter à une base
\c budget_app

-- Lister les tables
\dt

-- Décrire une table
\d nom_table

-- Voir les utilisateurs
\du

-- Quitter psql
\q

-- Exécuter un fichier SQL
\i /chemin/vers/script.sql

-- Afficher les connexions actives
SELECT * FROM pg_stat_activity WHERE datname = 'budget_app';
```

### Requêtes SQL courantes

```sql
-- Voir toutes les données d'une table
SELECT * FROM nom_table;

-- Compter les lignes
SELECT COUNT(*) FROM nom_table;

-- Supprimer toutes les données d'une table (ATTENTION !)
TRUNCATE TABLE nom_table;

-- Supprimer une table
DROP TABLE nom_table;

-- Créer un backup des données
COPY nom_table TO '/tmp/backup.csv' CSV HEADER;
```

---

## 🔧 Gestion PostgreSQL (systemctl)

### Statut et contrôle du service

```bash
# Voir le statut
sudo systemctl status postgresql

# Démarrer PostgreSQL
sudo systemctl start postgresql

# Arrêter PostgreSQL
sudo systemctl stop postgresql

# Redémarrer PostgreSQL (arrêt + démarrage)
sudo systemctl restart postgresql

# Recharger la configuration (sans couper les connexions)
sudo systemctl reload postgresql

# Activer au démarrage
sudo systemctl enable postgresql

# Désactiver au démarrage
sudo systemctl disable postgresql
```

### Logs PostgreSQL

```bash
# Voir les logs en temps réel
sudo tail -f /var/log/postgresql/postgresql-16-main.log

# Voir les 50 dernières lignes
sudo tail -n 50 /var/log/postgresql/postgresql-16-main.log

# Chercher des erreurs
sudo grep ERROR /var/log/postgresql/postgresql-16-main.log
```

---

## 💾 Backups PostgreSQL

### Backup complet de la base

```bash
# Backup simple
pg_dump -U budget_user -h localhost budget_app > backup_budget_$(date +%Y%m%d_%H%M%S).sql

# Backup compressé
pg_dump -U budget_user -h localhost budget_app | gzip > backup_budget_$(date +%Y%m%d).sql.gz

# Backup avec mot de passe automatique
PGPASSWORD='[TON_MOT_DE_PASSE]' pg_dump -U budget_user -h localhost budget_app > backup.sql
```

### Restaurer un backup

```bash
# Restaurer depuis un fichier SQL
psql -U budget_user -h localhost -d budget_app < backup.sql

# Restaurer depuis un fichier compressé
gunzip -c backup.sql.gz | psql -U budget_user -h localhost -d budget_app
```

### Backup automatique (cron)

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour backup quotidien à 3h du matin
0 3 * * * PGPASSWORD='[TON_MOT_DE_PASSE]' pg_dump -U budget_user -h localhost budget_app | gzip > /home/alban/backups/budget_$(date +\%Y\%m\%d).sql.gz
```

---

## 🔐 Configuration PostgreSQL

### Fichiers de configuration importants

```bash
# Configuration principale
sudo nano /etc/postgresql/16/main/postgresql.conf

# Configuration d'accès réseau
sudo nano /etc/postgresql/16/main/pg_hba.conf

# Après modification, recharger :
sudo systemctl reload postgresql
```

### pg_hba.conf - Configuration actuelle

```
# Connexion via Tailscale
host    budget_app    budget_user    100.64.0.0/10    scram-sha-256
```

### Vérifier la configuration

```bash
# Tester la syntaxe du fichier de config
sudo -u postgres psql -c "SELECT pg_reload_conf();"

# Voir les paramètres actifs
psql -U budget_user -d budget_app -c "SHOW all;"

# Voir listen_addresses
psql -U budget_user -d budget_app -c "SHOW listen_addresses;"
```

---

## 🛡️ Firewall UFW

### Gestion du firewall

```bash
# Voir le statut
sudo ufw status verbose

# Voir les règles numérotées
sudo ufw status numbered

# Autoriser un port
sudo ufw allow 8000/tcp

# Supprimer une règle par numéro
sudo ufw delete [NUMERO]

# Activer/désactiver le firewall
sudo ufw enable
sudo ufw disable

# Recharger les règles
sudo ufw reload
```

---

## 🖥️ Gestion système

### Redémarrage et arrêt

```bash
# Redémarrer le serveur
sudo reboot
# ou
sudo systemctl reboot

# Arrêter le serveur
sudo shutdown -h now
sudo poweroff

# Redémarrer dans 5 minutes
sudo shutdown -r +5

# Annuler un shutdown programmé
sudo shutdown -c
```

### Monitoring système

```bash
# Utilisation disque
df -h

# Espace utilisé par répertoire
du -sh /var/lib/postgresql

# Mémoire RAM
free -h

# Processus actifs
top
htop  # Si installé (plus visuel)

# Charge système
uptime

# Voir les processus PostgreSQL
ps aux | grep postgres
```

### Gestion des services

```bash
# Lister tous les services
systemctl list-units --type=service

# Voir les services qui ont échoué
systemctl --failed

# Voir les logs d'un service
sudo journalctl -u postgresql -f  # Temps réel
sudo journalctl -u postgresql --since "1 hour ago"
```

---

## 📦 Gestion des paquets (apt)

```bash
# Mettre à jour la liste des paquets
sudo apt update

# Mettre à jour les paquets installés
sudo apt upgrade

# Mettre à jour tout (y compris kernel)
sudo apt full-upgrade

# Installer un paquet
sudo apt install nom_paquet

# Supprimer un paquet
sudo apt remove nom_paquet

# Nettoyer les paquets inutiles
sudo apt autoremove
sudo apt clean
```

---

## 🐍 Développement avec FastAPI

### Installation environnement Python

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install fastapi uvicorn psycopg2-binary sqlalchemy

# Générer requirements.txt
pip freeze > requirements.txt

# Installer depuis requirements.txt
pip install -r requirements.txt
```

### Lancer l'application

```bash
# Développement (avec auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production (sans reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# En arrière-plan avec nohup
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &

# Tuer le processus
pkill -f uvicorn
```

### Variables d'environnement

```bash
# Créer un fichier .env
nano .env

# Contenu exemple :
DATABASE_URL=postgresql://budget_user:[TON_MOT_DE_PASSE]@100.77.237.80:5432/budget_app
SECRET_KEY=ta_clé_secrète_très_longue
DEBUG=False

# Charger les variables
export $(cat .env | xargs)
```

---

## 🔍 Debugging et monitoring PostgreSQL

### Voir les connexions actives

```sql
-- Connexions en cours
SELECT pid, usename, application_name, client_addr, state 
FROM pg_stat_activity 
WHERE datname = 'budget_app';

-- Tuer une connexion spécifique
SELECT pg_terminate_backend(pid) WHERE pid = [PID];

-- Tuer toutes les connexions sauf la tienne
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'budget_app' AND pid <> pg_backend_pid();
```

### Performance et statistiques

```sql
-- Taille de la base
SELECT pg_size_pretty(pg_database_size('budget_app'));

-- Taille des tables
SELECT 
    schemaname, 
    tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Statistiques des requêtes lentes (si pg_stat_statements activé)
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

---

## 🌐 Réseau et tests de connexion

### Tests de connectivité

```bash
# Ping Tailscale
ping 100.77.237.80

# Tester le port PostgreSQL
nc -zv 100.77.237.80 5432
# ou
telnet 100.77.237.80 5432

# Voir les ports en écoute sur le serveur
sudo ss -tulpn | grep 5432
sudo netstat -tulpn | grep 5432

# Voir les connexions PostgreSQL actives
sudo ss -an | grep 5432
```

### Tailscale

```bash
# Voir tous les appareils du réseau
tailscale status

# Ping un autre appareil Tailscale
tailscale ping 100.101.182.68

# Sortir du réseau Tailscale
sudo tailscale down

# Rejoindre le réseau
sudo tailscale up

# Voir les logs Tailscale
sudo journalctl -u tailscaled -f
```

---

## 📝 Gestion des fichiers et Git

### Commandes fichiers utiles

```bash
# Lister les fichiers détaillés
ls -lah

# Éditer un fichier
nano fichier.txt
vim fichier.txt

# Voir le contenu
cat fichier.txt
less fichier.txt  # Pour gros fichiers

# Chercher dans les fichiers
grep -r "texte_recherché" /chemin/

# Copier/Déplacer
cp source destination
mv source destination

# Permissions
chmod 755 script.sh  # Exécutable
chmod 600 fichier_secret  # Lecture seule propriétaire
chown alban:alban fichier  # Changer propriétaire
```

### Git (si tu utilises version control)

```bash
# Cloner un repo
git clone https://github.com/ton-repo.git

# Statut
git status

# Ajouter des fichiers
git add .
git commit -m "Message de commit"

# Pousser sur GitHub
git push origin main

# Tirer les dernières modifications
git pull origin main

# Voir l'historique
git log --oneline
```

---

## 🔑 Gestion utilisateurs PostgreSQL

### Créer/modifier utilisateurs

```sql
-- Créer un nouvel utilisateur
CREATE USER nouveau_user WITH PASSWORD '[MOT_DE_PASSE]';

-- Donner tous les droits sur une base
GRANT ALL PRIVILEGES ON DATABASE budget_app TO nouveau_user;

-- Donner tous les droits sur toutes les tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nouveau_user;

-- Changer le mot de passe
ALTER USER budget_user WITH PASSWORD '[NOUVEAU_MOT_DE_PASSE]';

-- Supprimer un utilisateur
DROP USER nom_user;

-- Voir les privilèges
\du
```

---

## 🚨 Commandes d'urgence

### PostgreSQL ne démarre pas

```bash
# Voir les logs d'erreur
sudo journalctl -u postgresql -n 100

# Vérifier la syntaxe des configs
sudo -u postgres postgres -C /etc/postgresql/16/main/postgresql.conf

# Réinitialiser le cluster (⚠️ PERTE DE DONNÉES !)
sudo pg_dropcluster --stop 16 main
sudo pg_createcluster 16 main
```

### Espace disque plein

```bash
# Trouver les gros fichiers
sudo du -h /var/lib/postgresql | sort -h | tail -20

# Nettoyer les logs PostgreSQL
sudo truncate -s 0 /var/log/postgresql/postgresql-16-main.log

# Nettoyer apt
sudo apt clean
sudo apt autoremove
```

### Connexion SSH perdue

```bash
# Depuis un autre terminal
ssh alban@100.77.237.80

# Si échec, vérifier Tailscale sur le serveur (accès physique)
sudo systemctl status tailscaled
sudo tailscale status

# Redémarrer Tailscale si nécessaire
sudo systemctl restart tailscaled
```

---

## 📚 Ressources utiles

### Documentation

- PostgreSQL : https://www.postgresql.org/docs/
- FastAPI : https://fastapi.tiangolo.com/
- Tailscale : https://tailscale.com/kb/
- Ubuntu/Debian : https://help.ubuntu.com/

### Commandes aide

```bash
# Aide d'une commande
man commande
commande --help

# Chercher une commande
apropos "mot clé"

# Historique des commandes
history
history | grep postgres

# Réexécuter une commande de l'historique
!123  # Numéro de la commande
```

---

## 💡 Tips & Bonnes pratiques

### Sécurité

- ✅ **Toujours** faire un backup avant modification majeure
- ✅ Tester les requêtes SQL sur des données de test d'abord
- ✅ Ne jamais commit les mots de passe dans Git (utiliser .env)
- ✅ Garder PostgreSQL et le système à jour
- ✅ Monitorer l'espace disque régulièrement

### Performance

- Créer des index sur les colonnes fréquemment recherchées
- Utiliser EXPLAIN ANALYZE pour optimiser les requêtes lentes
- Vacuum régulier : `VACUUM ANALYZE;`

### Développement

- Utiliser des environnements virtuels Python
- Versionner ton code avec Git
- Documenter les changements de schéma de base de données
- Tester localement avant déployer sur le serveur

---

**📌 N'oublie pas de remplacer `[TON_MOT_DE_PASSE]` par ton vrai mot de passe !**
