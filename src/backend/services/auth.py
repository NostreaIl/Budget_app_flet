"""
Service d'authentification avec JWT et hachage de mots de passe
Support de Row-Level Security (RLS) pour l'isolation des données
Utilise Argon2id (recommandé OWASP 2024+) pour le hachage sécurisé
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.backend.database.connection import get_db, set_user_context, SessionLocal
from src.backend.database import models
from src.backend.api import schemas

load_dotenv()

# Configuration JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "votre-cle-secrete-a-changer-en-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Configuration du hachage de mots de passe avec Argon2id
# Argon2id : algorithme recommandé OWASP 2024+ pour la protection maximale
# Résistant aux attaques GPU/ASIC, pas de limite de taille de mot de passe
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,    # 64 MB RAM (protection contre attaques GPU)
    argon2__time_cost=3,           # 3 itérations (équilibre sécurité/performance)
    argon2__parallelism=4,         # 4 threads CPU
    argon2__hash_len=32,           # 256 bits de hash
    argon2__type="id",             # Argon2id (hybride data-independent et data-dependent)
)

# Security scheme pour FastAPI
security = HTTPBearer()


# ==================== FONCTIONS DE HACHAGE ====================

def hash_password(password: str) -> str:
    """
    Hache un mot de passe avec Argon2id (algorithme recommandé OWASP).

    Argon2id offre une protection maximale contre :
    - Attaques par force brute (GPU/ASIC)
    - Attaques par canal auxiliaire (side-channel)
    - Attaques par compromission mémoire

    Pas de limite de taille de mot de passe (contrairement à bcrypt).

    Args:
        password: Mot de passe en clair (taille illimitée)

    Returns:
        Hash du mot de passe au format Argon2id
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe correspond à son hash Argon2id.

    Utilise une comparaison à temps constant pour éviter les attaques
    par analyse temporelle.

    Args:
        plain_password: Mot de passe en clair
        hashed_password: Hash Argon2id du mot de passe

    Returns:
        True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)


# ==================== FONCTIONS JWT ====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT signé pour l'authentification.

    Args:
        data: Données à encoder dans le token (ex: {"sub": user_id})
        expires_delta: Durée de validité du token (défaut: JWT_EXPIRE_MINUTES)

    Returns:
        Token JWT encodé et signé
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Décode et valide un token JWT.
    """
    try:
        print(f"🔑 SECRET_KEY (10 chars): {SECRET_KEY[:10]}...")
        print(f"🔑 ALGORITHM: {ALGORITHM}")
        print(f"🔑 Token à décoder: {token[:50]}...")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Payload décodé: {payload}")
        return payload
    except JWTError as e:
        print(f"❌ Erreur JWT: {type(e).__name__}")
        print(f"❌ Détail: {str(e)}")
        return None





# ==================== CRUD UTILISATEURS ====================

def get_utilisateur_by_email(db: Session, email: str) -> Optional[models.Utilisateur]:
    """Récupère un utilisateur par son email."""
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()


def get_utilisateur_by_id(db: Session, user_id: int) -> Optional[models.Utilisateur]:
    """Récupère un utilisateur par son ID."""
    return db.query(models.Utilisateur).filter(models.Utilisateur.idutilisateur == user_id).first()


def create_utilisateur(db: Session, user_data: schemas.UtilisateurCreate) -> models.Utilisateur:
    """
    Crée un nouvel utilisateur avec mot de passe haché.

    Args:
        db: Session de base de données
        user_data: Données de l'utilisateur (email, mot_de_passe, nom_affichage)

    Returns:
        Utilisateur créé avec types et catégories par défaut
    """
    hashed_password = hash_password(user_data.mot_de_passe)

    db_user = models.Utilisateur(
        email=user_data.email,
        mot_de_passe_hash=hashed_password,
        nom_affichage=user_data.nom_affichage
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Créer les types par défaut pour le nouvel utilisateur
    create_default_types_for_user(db, db_user.idutilisateur)

    return db_user


def create_default_types_for_user(db: Session, user_id: int) -> None:
    """
    Crée les types d'opération par défaut pour un nouvel utilisateur.

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
    """
    default_types = ["depense", "revenu", "transfert"]

    for type_nom in default_types:
        db_type = models.Type(nom=type_nom, idutilisateur=user_id)
        db.add(db_type)

    db.commit()


def create_default_categories_for_user(db: Session, user_id: int) -> None:
    """
    Crée les catégories et sous-catégories par défaut pour un nouvel utilisateur.

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
    """
    default_categories = {
        "Alimentation": ["Courses", "Restaurant"],
        "Transport": ["Essence", "Transports publics"],
        "Logement": [],
        "Loisirs": [],
        "Santé": [],
        "Revenus": ["Salaire", "Prime"],
        "Shopping": ["Vêtements"],
        "Factures": []
    }

    for cat_nom, sous_cats in default_categories.items():
        db_cat = models.Categorie(nomcategorie=cat_nom, idutilisateur=user_id)
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)

        for sous_cat_nom in sous_cats:
            db_sous_cat = models.SousCategorie(
                nomsouscategorie=sous_cat_nom,
                idcategorie=db_cat.idcategorie
            )
            db.add(db_sous_cat)

    db.commit()


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.Utilisateur]:
    """
    Authentifie un utilisateur avec email et mot de passe.

    Args:
        db: Session de base de données
        email: Email de l'utilisateur
        password: Mot de passe en clair

    Returns:
        Utilisateur si authentification réussie, None sinon
    """
    user = get_utilisateur_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.mot_de_passe_hash):
        return None
    if not user.actif:
        return None
    return user


def update_last_login(db: Session, user: models.Utilisateur) -> None:
    """Met à jour la date de dernière connexion de l'utilisateur."""
    user.derniere_connexion = datetime.now(timezone.utc)
    db.commit()


# ==================== DEPENDENCIES FASTAPI ====================

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> models.Utilisateur:
    """
    Dependency FastAPI pour récupérer l'utilisateur courant à partir du token JWT.
    """
    print(f"\n🔍 === GET_CURRENT_USER APPELÉ ===")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    print(f"🔍 Token reçu: {token[:50]}...")

    payload = decode_token(token)

    if payload is None:
        print("❌ decode_token a retourné None")
        raise credentials_exception

    user_id: int = payload.get("sub")
    print(f"🔍 User ID du payload: {user_id}")

    if user_id is None:
        print("❌ Pas de 'sub' dans le payload")
        raise credentials_exception

    user = get_utilisateur_by_id(db, user_id)

    if user is None:
        print(f"❌ Aucun utilisateur trouvé avec ID {user_id}")
        raise credentials_exception

    if not user.actif:
        print(f"❌ Utilisateur {user_id} inactif")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )

    print(f"✅ Utilisateur authentifié: {user.email} (ID: {user.idutilisateur})")
    return user


async def get_current_active_user(
        current_user: models.Utilisateur = Depends(get_current_user)
) -> models.Utilisateur:
    """
    Dependency FastAPI pour vérifier que l'utilisateur est actif.
    """
    if not current_user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )
    return current_user


def get_db_with_rls(
        current_user: models.Utilisateur = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Session:
    """
    Dependency FastAPI qui configure le contexte RLS pour l'utilisateur courant.

    Active Row-Level Security en définissant app.user_id dans la session PostgreSQL.
    Toutes les requêtes suivantes seront automatiquement filtrées par l'ID utilisateur.

    Usage:
        @app.get("/api/comptes")
        async def get_comptes(db: Session = Depends(get_db_with_rls)):
            return db.query(Compte).all()  # Retourne uniquement les comptes de l'utilisateur
    """
    set_user_context(db, current_user.idutilisateur)
    return db


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.Utilisateur]:
    """
    Authentifie un utilisateur avec email et mot de passe.
    """
    print(f"🔍 Tentative de connexion pour: {email}")

    user = get_utilisateur_by_email(db, email)
    if not user:
        print(f"❌ Utilisateur non trouvé: {email}")
        return None

    print(f"✅ Utilisateur trouvé: {user.email}, actif: {user.actif}")

    password_match = verify_password(password, user.mot_de_passe_hash)
    print(f"🔑 Vérification mot de passe: {password_match}")

    if not password_match:
        print(f"❌ Mot de passe incorrect")
        return None

    if not user.actif:
        print(f"❌ Compte désactivé")
        return None

    print(f"✅ Authentification réussie pour {email}")
    return user


