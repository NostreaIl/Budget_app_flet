# Installation et Configuration

## Prérequis

- Python 3.9+
- PostgreSQL 12+
- pip

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/NostreaIl/Budget_app_flet.git
cd Budget_app_flet
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copiez `.env.example` vers `.env` et configurez vos paramètres:

```bash
cp .env.example .env
```

Éditez `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Budget_app
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe

API_BASE_URL=http://localhost:8000
```

### 5. Initialiser la base de données

```bash
python scripts/reset_database.py
```

## Lancer l'application

### Backend (API)

```bash
python run_backend.py
```

L'API sera disponible sur: http://localhost:8000
Documentation: http://localhost:8000/docs

### Frontend (Interface)

```bash
python run_frontend.py
```

## Tests

```bash
# Tests backend
python -m pytest tests/backend/

# Tests complets
python -m pytest tests/
```

## Structure du projet

Voir `NOUVELLE_STRUCTURE.md` pour la documentation complète de la structure.
