"""
Configuration de la connexion à la base de données PostgreSQL avec SQLAlchemy
Support de Row-Level Security (RLS) pour l'isolation des données par utilisateur
"""
import os
from pathlib import Path
from urllib.parse import quote_plus
from typing import Generator, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine, text, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Charger les variables d'environnement depuis la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    print(f"✅ Fichier .env chargé depuis: {ENV_PATH}")
else:
    print(f"⚠️  Fichier .env non trouvé à: {ENV_PATH}")
    print("   Utilisation des valeurs par défaut ou variables d'environnement système")
    load_dotenv()

# Récupérer les credentials depuis .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Budget_app")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Debug: afficher les paramètres de connexion (sans le mot de passe)
print(f"📊 Connexion BDD: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Construire l'URL de connexion PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer le moteur SQLAlchemy
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=DEBUG_MODE,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Créer une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def set_user_context(session: Session, user_id: int) -> None:
    """
    Définit le contexte utilisateur pour RLS dans la session courante.
    Cette fonction DOIT être appelée avant toute requête pour activer RLS.

    Args:
        session: Session SQLAlchemy active
        user_id: ID de l'utilisateur connecté

    Usage:
        db = SessionLocal()
        set_user_context(db, current_user.idutilisateur)
        # Maintenant toutes les requêtes sont filtrées par RLS
    """
    session.execute(text(f"SET app.user_id = '{user_id}'"))


def clear_user_context(session: Session) -> None:
    """
    Efface le contexte utilisateur RLS.
    Utile pour réinitialiser la session entre les requêtes.

    Args:
        session: Session SQLAlchemy active
    """
    session.execute(text("RESET app.user_id"))


@contextmanager
def get_db_with_user(user_id: int) -> Generator[Session, None, None]:
    """
    Context manager qui fournit une session DB avec le contexte utilisateur RLS configuré.

    Args:
        user_id: ID de l'utilisateur connecté

    Yields:
        Session SQLAlchemy avec RLS activé pour l'utilisateur

    Usage:
        with get_db_with_user(user_id) as db:
            comptes = db.query(Compte).all()  # Retourne uniquement les comptes de l'utilisateur
    """
    db = SessionLocal()
    try:
        set_user_context(db, user_id)
        yield db
    finally:
        clear_user_context(db)
        db.close()


def get_db() -> Generator[Session, None, None]:
    """
    Générateur de session de base de données pour FastAPI (sans contexte utilisateur).
    Le contexte utilisateur doit être défini par le middleware d'authentification.

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


def get_db_for_user(user_id: int):
    """
    Factory function pour créer un dependency FastAPI avec contexte utilisateur.

    Args:
        user_id: ID de l'utilisateur

    Returns:
        Générateur de session avec RLS configuré

    Usage dans FastAPI:
        @app.get("/api/comptes")
        async def get_comptes(
            current_user: User = Depends(get_current_user),
            db: Session = Depends(lambda: get_db_for_user(current_user.idutilisateur))
        ):
            ...
    """

    def _get_db():
        db = SessionLocal()
        try:
            set_user_context(db, user_id)
            yield db
        finally:
            clear_user_context(db)
            db.close()

    return _get_db


def test_connection() -> bool:
    """Teste la connexion à la base de données"""
    try:
        with engine.connect() as conn:
            print(f"✅ Connexion réussie à PostgreSQL: {DB_NAME}")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à PostgreSQL: {e}")
        return False


def test_rls_isolation(user_id_1: int, user_id_2: int) -> dict:
    """
    Teste l'isolation RLS entre deux utilisateurs.
    Utile pour vérifier que RLS fonctionne correctement.

    Args:
        user_id_1: Premier utilisateur
        user_id_2: Deuxième utilisateur

    Returns:
        dict avec les résultats du test
    """
    results = {}

    with get_db_with_user(user_id_1) as db1:
        count1 = db1.execute(text("SELECT COUNT(*) FROM compte")).scalar()
        results[f"user_{user_id_1}_comptes"] = count1

    with get_db_with_user(user_id_2) as db2:
        count2 = db2.execute(text("SELECT COUNT(*) FROM compte")).scalar()
        results[f"user_{user_id_2}_comptes"] = count2

    return results