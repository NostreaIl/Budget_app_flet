"""
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
