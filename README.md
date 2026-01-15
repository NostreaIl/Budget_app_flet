# Budget App - Application de Gestion Budgétaire

Application complète de gestion budgétaire avec backend FastAPI et frontend Flet.

## 🚀 Démarrage Rapide

### Backend (API)
```bash
python run_backend.py
```
📝 Documentation API: http://localhost:8000/docs

### Frontend (Interface)
```bash
python run_frontend.py
```

## 📁 Structure du Projet

```
Budget_app_flet/
├── src/
│   ├── backend/      # 🔷 API FastAPI
│   └── frontend/     # 🔶 Application Flet
├── tests/            # ✅ Tests
├── docs/             # 📚 Documentation
└── scripts/          # 🔧 Scripts utilitaires
```

## 📚 Documentation

- **[Installation & Configuration](docs/SETUP.md)** - Guide d'installation complet
- **[API Documentation](docs/API.md)** - Documentation de l'API REST
- **[Base de Données](docs/DATABASE.md)** - Schéma et structure de la BDD
- **[Guide de Migration](docs/MIGRATION_GUIDE.md)** - Migration vers la nouvelle structure
- **[Structure du Projet](docs/NOUVELLE_STRUCTURE.md)** - Architecture détaillée

## 🛠️ Installation

### 1. Prérequis
- Python 3.9+
- PostgreSQL 12+

### 2. Installation
```bash
# Cloner le repository
git clone https://github.com/NostreaIl/Budget_app_flet.git
cd Budget_app_flet

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos paramètres
```

### 3. Initialiser la Base de Données
```bash
python scripts/reset_database.py
```

## 🏗️ Architecture

### Backend (src/backend/)
- **FastAPI** - API REST
- **SQLAlchemy** - ORM pour PostgreSQL
- **Pydantic** - Validation des données

### Frontend (src/frontend/)
- **Flet** - Interface utilisateur cross-platform
- **Material Design** - Design moderne et responsive

### Communication
- Frontend ↔️ Backend via API REST uniquement
- Séparation complète des responsabilités

## 🧪 Tests

```bash
# Tester le backend
python tests/backend/test_api.py

# Tester le schéma de base de données
python tests/backend/test_schema.py
```

## 📝 Configuration

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
```

## 🎯 Fonctionnalités

### Gestion des Opérations
- ✅ Ajout/Modification/Suppression d'opérations
- ✅ Catégorisation des transactions
- ✅ Opérations récurrentes

### Comptes
- ✅ Gestion multi-comptes
- ✅ Suivi du solde en temps réel
- ✅ Historique des transactions

### Catégories & Sous-catégories
- ✅ Catégories personnalisables
- ✅ Hiérarchie catégorie/sous-catégorie
- ✅ Attribution aux opérations

### Analytics
- ✅ Graphiques et statistiques
- ✅ Analyse des dépenses par catégorie
- ✅ Évolution du solde

## 🤝 Contribution

Les contributions sont les bienvenues! Consultez les [issues](https://github.com/NostreaIl/Budget_app_flet/issues) pour commencer.

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou problème:
- Ouvrez une [issue](https://github.com/NostreaIl/Budget_app_flet/issues)
- Consultez la [documentation](docs/)

---

**Version**: 2.0.0  
**Dernière mise à jour**: 2026-01-15
