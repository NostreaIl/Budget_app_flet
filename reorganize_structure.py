"""
Script pour réorganiser la structure du projet Budget App
Transformation d'une structure désorganisée vers une structure professionnelle
"""
import os
import shutil
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Affiche une étape avec style"""
    print(f"\n{Colors.BLUE}▶ {message}{Colors.END}")

def print_success(message):
    """Affiche un succès"""
    print(f"  {Colors.GREEN}✓ {message}{Colors.END}")

def print_warning(message):
    """Affiche un avertissement"""
    print(f"  {Colors.YELLOW}⚠ {message}{Colors.END}")

def print_error(message):
    """Affiche une erreur"""
    print(f"  {Colors.RED}✗ {message}{Colors.END}")


def create_directory_structure(base_path):
    """Crée la nouvelle structure de dossiers"""
    print_step("Création de la nouvelle structure de dossiers...")

    directories = [
        # Backend structure
        "src/backend",
        "src/backend/database",
        "src/backend/api/routes",
        "src/backend/api/schemas",
        "src/backend/services",

        # Frontend structure
        "src/frontend",
        "src/frontend/pages",
        "src/frontend/components/charts",
        "src/frontend/dialogs",
        "src/frontend/theme",
        "src/frontend/services",
        "src/frontend/models",

        # Tests
        "tests/backend",
        "tests/frontend",

        # Documentation
        "docs",
    ]

    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

        # Créer __init__.py pour les packages Python
        if not directory.startswith("docs"):
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()

        print_success(f"Créé: {directory}")


def move_backend_files(base_path):
    """Déplace les fichiers backend"""
    print_step("Déplacement des fichiers backend...")

    moves = [
        # Fichiers principaux backend
        ("backend/main.py", "src/backend/main.py"),
        ("backend/database.py", "src/backend/database/connection.py"),
        ("backend/models.py", "src/backend/database/models.py"),
        ("backend/crud.py", "src/backend/services/crud.py"),
        ("backend/schemas.py", "src/backend/api/schemas/__init__.py"),

        # Database
        ("database/schema.sql", "src/backend/database/schema.sql"),
        ("database/README.md", "docs/DATABASE.md"),
    ]

    for src, dst in moves:
        src_path = base_path / src
        dst_path = base_path / dst

        if src_path.exists():
            # Créer le dossier parent si nécessaire
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print_success(f"{src} → {dst}")
        else:
            print_warning(f"Fichier non trouvé: {src}")


def move_frontend_files(base_path):
    """Déplace les fichiers frontend"""
    print_step("Déplacement des fichiers frontend...")

    # Main app
    src_main = base_path / "main.py"
    if src_main.exists():
        shutil.copy2(src_main, base_path / "src/frontend/main.py")
        print_success("main.py → src/frontend/main.py")

    # Déplacer ui/ vers src/frontend/
    ui_mappings = [
        ("ui/pages", "src/frontend/pages"),
        ("ui/components", "src/frontend/components"),
        ("ui/dialogs", "src/frontend/dialogs"),
        ("ui/theme", "src/frontend/theme"),
    ]

    for src_dir, dst_dir in ui_mappings:
        src_path = base_path / src_dir
        dst_path = base_path / dst_dir

        if src_path.exists():
            # Copier tous les fichiers du dossier
            for file_path in src_path.rglob("*.py"):
                relative_path = file_path.relative_to(src_path)
                dest_file = dst_path / relative_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_file)
            print_success(f"{src_dir}/ → {dst_dir}/")
        else:
            print_warning(f"Dossier non trouvé: {src_dir}")

    # Déplacer src/ models et services vers frontend
    src_models = base_path / "src/models"
    if src_models.exists():
        for file_path in src_models.rglob("*.py"):
            relative_path = file_path.relative_to(src_models)
            dest_file = base_path / "src/frontend/models" / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_file)
        print_success("src/models/ → src/frontend/models/")

    src_services = base_path / "src/services"
    if src_services.exists():
        for file_path in src_services.rglob("*.py"):
            relative_path = file_path.relative_to(src_services)
            dest_file = base_path / "src/frontend/services" / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_file)
        print_success("src/services/ → src/frontend/services/")


def move_other_files(base_path):
    """Déplace les autres fichiers"""
    print_step("Déplacement des autres fichiers...")

    # Scripts de test vers tests/
    test_files = [
        ("scripts/test_api.py", "tests/backend/test_api.py"),
        ("scripts/test_new_schema.py", "tests/backend/test_schema.py"),
    ]

    for src, dst in test_files:
        src_path = base_path / src
        dst_path = base_path / dst
        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print_success(f"{src} → {dst}")

    # Garder reset_database.py dans scripts/
    reset_script = base_path / "scripts/reset_database.py"
    if reset_script.exists():
        print_success("scripts/reset_database.py conservé")

    # Déplacer CHANGELOG_API.md vers docs/
    changelog = base_path / "CHANGELOG_API.md"
    if changelog.exists():
        shutil.copy2(changelog, base_path / "docs/API.md")
        print_success("CHANGELOG_API.md → docs/API.md")


def create_entry_points(base_path):
    """Crée les points d'entrée pour lancer l'app"""
    print_step("Création des points d'entrée...")

    # run_backend.py
    backend_runner = base_path / "run_backend.py"
    backend_runner.write_text('''"""
Point d'entrée pour lancer le backend FastAPI
"""
if __name__ == "__main__":
    import uvicorn
    from src.backend.main import app

    print("🚀 Démarrage du serveur FastAPI...")
    print("📝 Documentation: http://localhost:8000/docs")
    print("🔗 API: http://localhost:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
''')
    print_success("Créé: run_backend.py")

    # run_frontend.py
    frontend_runner = base_path / "run_frontend.py"
    frontend_runner.write_text('''"""
Point d'entrée pour lancer le frontend Flet
"""
if __name__ == "__main__":
    from src.frontend.main import main

    print("🚀 Démarrage de l'application Flet...")
    print("🔗 Backend API: http://localhost:8000")

    main()
''')
    print_success("Créé: run_frontend.py")


def create_config_files(base_path):
    """Crée les fichiers de configuration"""
    print_step("Création des fichiers de configuration...")

    # src/backend/config.py
    backend_config = base_path / "src/backend/config.py"
    backend_config.write_text('''"""
Configuration du backend FastAPI
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "Budget_app"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# URL de connexion PostgreSQL
DATABASE_URL = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# Configuration de l'API
API_VERSION = "2.0.0"
API_TITLE = "Budget API"
API_DESCRIPTION = "API REST pour gérer les opérations budgétaires"

# Configuration CORS
CORS_ORIGINS = ["*"]  # À restreindre en production
''')
    print_success("Créé: src/backend/config.py")

    # src/frontend/config.py
    frontend_config = base_path / "src/frontend/config.py"
    frontend_config.write_text('''"""
Configuration du frontend Flet
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Configuration de l'application
APP_NAME = "Budget App"
APP_VERSION = "2.0.0"
APP_WINDOW_WIDTH = 1200
APP_WINDOW_HEIGHT = 800
''')
    print_success("Créé: src/frontend/config.py")


def create_readme_updates(base_path):
    """Met à jour le README avec la nouvelle structure"""
    print_step("Création de la documentation...")

    setup_doc = base_path / "docs/SETUP.md"
    setup_doc.write_text('''# Installation et Configuration

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
source .venv/bin/activate  # Sur Windows: .venv\\Scripts\\activate
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
''')
    print_success("Créé: docs/SETUP.md")


def print_summary():
    """Affiche un résumé de la réorganisation"""
    print("\n" + "="*60)
    print(f"{Colors.BOLD}{Colors.GREEN}✅ RÉORGANISATION TERMINÉE!{Colors.END}")
    print("="*60)

    print(f"\n{Colors.BOLD}📁 Nouvelle structure créée:{Colors.END}")
    print("  • src/backend/     - API FastAPI complète")
    print("  • src/frontend/    - Application Flet complète")
    print("  • tests/           - Tests organisés")
    print("  • docs/            - Documentation")
    print("  • scripts/         - Scripts utilitaires")

    print(f"\n{Colors.BOLD}🚀 Points d'entrée créés:{Colors.END}")
    print("  • run_backend.py   - Lance l'API")
    print("  • run_frontend.py  - Lance l'interface")

    print(f"\n{Colors.BOLD}📝 Prochaines étapes:{Colors.END}")
    print("  1. Vérifiez la nouvelle structure")
    print("  2. Testez le backend: python run_backend.py")
    print("  3. Testez le frontend: python run_frontend.py")
    print("  4. Supprimez les anciens dossiers une fois vérifié")

    print(f"\n{Colors.BOLD}⚠️  Important:{Colors.END}")
    print("  • Les anciens fichiers sont CONSERVÉS")
    print("  • Nouveaux fichiers dans src/")
    print("  • Testez avant de supprimer l'ancien code")

    print("\n" + "="*60 + "\n")


def main():
    """Fonction principale"""
    base_path = Path("/home/user/Budget_app_flet")

    print("\n" + "="*60)
    print(f"{Colors.BOLD}🔄 RÉORGANISATION DE LA STRUCTURE DU PROJET{Colors.END}")
    print("="*60)

    try:
        create_directory_structure(base_path)
        move_backend_files(base_path)
        move_frontend_files(base_path)
        move_other_files(base_path)
        create_entry_points(base_path)
        create_config_files(base_path)
        create_readme_updates(base_path)

        print_summary()
        return 0

    except Exception as e:
        print_error(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
