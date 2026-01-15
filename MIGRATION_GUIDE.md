# Guide de Migration vers la Nouvelle Structure

## 🎯 Objectif

Ce projet a été réorganisé pour suivre les meilleures pratiques de développement Python avec une séparation claire entre backend et frontend.

## 📁 Ancienne vs Nouvelle Structure

### Avant (Désorganisée)
```
Budget_app_flet/
├── backend/          # API mélangée
├── src/              # Code confus
├── ui/               # Composants séparés
├── main.py           # À la racine
└── scripts/          # Scripts
```

### Après (Organisée)
```
Budget_app_flet/
├── src/
│   ├── backend/      # 🔷 API FastAPI complète
│   └── frontend/     # 🔶 Application Flet complète
├── tests/            # ✅ Tests organisés
├── docs/             # 📚 Documentation
└── scripts/          # 🔧 Scripts utilitaires
```

## 🚀 Utilisation de la Nouvelle Structure

### 1. Backend (API)

#### Lancer le backend
```bash
python run_backend.py
```

L'API sera disponible sur:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

#### Structure du backend
```
src/backend/
├── main.py              # Point d'entrée FastAPI
├── config.py            # Configuration
├── database/
│   ├── connection.py   # Connexion PostgreSQL
│   ├── models.py       # Modèles SQLAlchemy
│   └── schema.sql      # Schéma SQL
├── api/
│   ├── routes/         # Endpoints (à venir)
│   └── schemas/        # Schémas Pydantic
└── services/
    └── crud.py         # Opérations CRUD
```

### 2. Frontend (Application Flet)

#### Lancer le frontend
```bash
python run_frontend.py
```

#### Structure du frontend
```
src/frontend/
├── main.py              # Point d'entrée Flet
├── config.py            # Configuration
├── pages/              # Pages de l'application
├── components/         # Composants réutilisables
├── dialogs/            # Boîtes de dialogue
├── theme/              # Thème et styles
├── services/
│   └── api_client.py   # Client pour communiquer avec l'API
└── models/             # Modèles de données frontend
```

## 🔧 Configuration

### Fichier .env

Créez un fichier `.env` à la racine:

```env
# Base de données
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Budget_app
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe

# API
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
```

## 📦 Installation

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python scripts/reset_database.py
```

## 🧪 Tests

```bash
# Tester le backend
python tests/backend/test_api.py
python tests/backend/test_schema.py

# Lancer tous les tests (si pytest installé)
pytest tests/
```

## 📝 Imports - Guide de Migration

### Backend

#### Avant
```python
from backend.database import get_db
from backend import models, schemas, crud
```

#### Après
```python
from src.backend.database import get_db
from src.backend.database.models import Operation, Compte
from src.backend.api import schemas
from src.backend.services import crud
```

### Frontend

#### Avant
```python
from src.models.transaction import Transaction
from src.services.api_client import APIClient
from ui.components.stat_card import StatCard
```

#### Après
```python
from src.frontend.models.transaction import Transaction
from src.frontend.services.api_client import APIClient
from src.frontend.components.stat_card import StatCard
```

## 🎨 Avantages de la Nouvelle Structure

### ✅ Séparation des Responsabilités
- Backend et Frontend complètement séparés
- Communication uniquement via API REST
- Testable indépendamment

### ✅ Clarté et Maintenance
- Structure claire et intuitive
- Facile à naviguer
- Suit les conventions Python

### ✅ Scalabilité
- Facile d'ajouter de nouvelles fonctionnalités
- Code modulaire et réutilisable
- Prêt pour le déploiement

### ✅ Documentation
- Docs organisées dans `docs/`
- README clairs
- Exemples de code

## 🔄 Migration de Votre Code Local

Si vous avez des modifications locales dans l'ancienne structure:

### 1. Sauvegarder vos modifications
```bash
git stash
```

### 2. Pull la nouvelle structure
```bash
git pull origin claude/update-database-schema-xcH9P
```

### 3. Adapter vos modifications
- Déplacer vos fichiers dans la nouvelle structure
- Mettre à jour les imports

### 4. Tester
```bash
# Tester le backend
python run_backend.py

# Tester le frontend (dans un autre terminal)
python run_frontend.py
```

## 📚 Documentation Complète

- **Setup**: `docs/SETUP.md`
- **API**: `docs/API.md`
- **Database**: `docs/DATABASE.md`
- **Structure**: `NOUVELLE_STRUCTURE.md`

## 🐛 Dépannage

### Erreur d'import
```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Assurez-vous d'exécuter les scripts depuis la racine du projet:
```bash
cd /path/to/Budget_app_flet
python run_backend.py
```

### Erreur de connexion DB
```
Erreur de connexion à PostgreSQL
```

**Solution**: Vérifiez votre fichier `.env` et que PostgreSQL est démarré

### Port déjà utilisé
```
Address already in use: 8000
```

**Solution**: Arrêtez le processus utilisant le port ou changez le port dans `run_backend.py`

## 🎉 C'est Fait!

Votre projet est maintenant organisé professionnellement avec:
- ✅ Backend FastAPI dans `src/backend/`
- ✅ Frontend Flet dans `src/frontend/`
- ✅ Tests dans `tests/`
- ✅ Documentation dans `docs/`
- ✅ Scripts utilitaires dans `scripts/`

**Enjoy coding! 🚀**
