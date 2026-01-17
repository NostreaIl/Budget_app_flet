"""
Configuration de la connexion à la base de données PostgreSQL avec SQLAlchemy
"""
import os
from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement depuis la racine du projet
# Cherche le .env dans le dossier parent (racine du projet)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    print(f"✅ Fichier .env chargé depuis: {ENV_PATH}")
else:
    print(f"⚠️  Fichier .env non trouvé à: {ENV_PATH}")
    print("   Utilisation des valeurs par défaut ou variables d'environnement système")
    load_dotenv()  # Essaie quand même de charger depuis le répertoire courant

# Récupérer les credentials depuis .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Budget_app")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Debug: afficher les paramètres de connexion (sans le mot de passe)
print(f"📊 Connexion BDD: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Construire l'URL de connexion PostgreSQL
# Note: quote_plus encode les caractères spéciaux du mot de passe (@ % ! etc.)
DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer le moteur SQLAlchemy
# echo=True seulement en mode DEBUG
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=DEBUG_MODE,  # Affiche les requêtes SQL seulement en mode debug
    pool_pre_ping=True,  # Vérifie que la connexion est vivante avant de l'utiliser
    pool_size=5,  # Nombre de connexions dans le pool
    max_overflow=10  # Connexions supplémentaires possibles
)

# Créer une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


# Dependency pour FastAPI - obtenir une session DB
def get_db():
    """
    Générateur de session de base de données pour FastAPI
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fonction pour tester la connexion
def test_connection():
    """Teste la connexion à la base de données"""
    try:
        with engine.connect() as conn:
            print(f"✅ Connexion réussie à PostgreSQL: {DB_NAME}")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à PostgreSQL: {e}")
        return False
