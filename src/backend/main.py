"""
Backend FastAPI pour Budget App
API REST connectée à PostgreSQL via SQLAlchemy
Mis à jour pour le nouveau schéma avec Operation, Categorie et SousCategorie
Support multi-utilisateurs avec Row-Level Security (RLS)
"""
import os
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

load_dotenv()

from src.backend.database.connection import get_db, test_connection, set_user_context
from src.backend.database import models
from src.backend.services import crud
from src.backend.services import auth
from src.backend.api import schemas

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Budget API",
    description="API REST pour gérer les opérations, comptes, catégories et sous-catégories budgétaires avec authentification multi-utilisateurs",
    version="3.0.0"
)

# Configuration CORS pour permettre les appels depuis l'app Flet
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== ENDPOINTS DE BASE ====================

@app.get("/")
async def root():
    """Endpoint racine pour vérifier que l'API fonctionne"""
    return {
        "message": "Budget FastAPI backend is running!",
        "version": "3.0.0",
        "database": "PostgreSQL connected via SQLAlchemy",
        "schema": "Multi-utilisateur avec RLS",
        "features": ["Authentication JWT", "Row-Level Security", "Multi-user isolation"]
    }


@app.get("/health")
async def health_check():
    """Vérifie la santé de l'API et la connexion à la base de données"""
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }


# ==================== ENDPOINTS AUTHENTIFICATION ====================

@app.post("/api/auth/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: schemas.UtilisateurCreate,
        db: Session = Depends(get_db)
):
    """
    Inscription d'un nouvel utilisateur.
    Crée le compte et retourne un token JWT.
    """
    # Vérifier si l'email existe déjà
    existing_user = auth.get_utilisateur_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà"
        )

    # Créer l'utilisateur
    user = auth.create_utilisateur(db, user_data)

    # Créer les catégories par défaut
    auth.create_default_categories_for_user(db, user.idutilisateur)

    # Générer le token
    access_token = auth.create_access_token(
        data={"sub": str(user.idutilisateur)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=schemas.UtilisateurSimple(
            idutilisateur=user.idutilisateur,
            email=user.email,
            nom_affichage=user.nom_affichage
        )
    )


@app.post("/api/auth/login", response_model=schemas.TokenResponse)
async def login(
        login_data: schemas.LoginRequest,
        db: Session = Depends(get_db)
):
    """
    Connexion d'un utilisateur existant.
    Retourne un token JWT si les identifiants sont valides.
    """
    user = auth.authenticate_user(db, login_data.email, login_data.mot_de_passe)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Mettre à jour la dernière connexion
    auth.update_last_login(db, user)

    # Générer le token
    access_token = auth.create_access_token(
        data={"sub": str(user.idutilisateur)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=schemas.UtilisateurSimple(
            idutilisateur=user.idutilisateur,
            email=user.email,
            nom_affichage=user.nom_affichage
        )
    )


@app.get("/api/auth/me", response_model=schemas.UtilisateurResponse)
async def get_current_user_info(
        current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Récupère les informations de l'utilisateur connecté."""
    return current_user


@app.put("/api/auth/me", response_model=schemas.UtilisateurResponse)
async def update_current_user(
        user_update: schemas.UtilisateurUpdate,
        current_user: models.Utilisateur = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    """Met à jour les informations de l'utilisateur connecté."""
    if user_update.email:
        existing = auth.get_utilisateur_by_email(db, user_update.email)
        if existing and existing.idutilisateur != current_user.idutilisateur:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé"
            )
        current_user.email = user_update.email

    if user_update.nom_affichage is not None:
        current_user.nom_affichage = user_update.nom_affichage

    if user_update.mot_de_passe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pour changer votre mot de passe, utilisez l'endpoint /api/auth/change-password"
        )
    db.commit()
    db.refresh(current_user)
    return current_user


@app.post("/api/auth/change-password", response_model=schemas.MessageResponse)
async def change_password(
        password_data: schemas.PasswordChangeRequest,
        current_user: models.Utilisateur = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    """Change le mot de passe de l'utilisateur connecté."""
    if not auth.verify_password(password_data.ancien_mot_de_passe, current_user.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect"
        )

    current_user.mot_de_passe_hash = auth.hash_password(password_data.nouveau_mot_de_passe)
    db.commit()

    return schemas.MessageResponse(message="Mot de passe modifié avec succès")


# ==================== ENDPOINTS STATISTIQUES (avec RLS) ====================

@app.get("/api/stats")
async def get_statistics(db: Session = Depends(auth.get_db_with_rls)):
    """Récupère les statistiques générales (filtrées par utilisateur via RLS)"""
    stats = crud.get_statistics(db)
    return stats


# ==================== ENDPOINTS OPERATIONS (avec RLS) ====================

@app.get("/api/operations", response_model=List[schemas.OperationResponse])
async def read_operations(
        search: str = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Récupère toutes les opérations de l'utilisateur avec pagination et recherche optionnelle"""
    if search:
        return crud.search_operations(db, search, skip, limit)
    return crud.get_operations(db, skip=skip, limit=limit)


@app.get("/api/operations/{operation_id}", response_model=schemas.OperationResponse)
async def read_operation(operation_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère une opération par son ID"""
    operation = crud.get_operation(db, operation_id=operation_id)
    if operation is None:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return operation


@app.post("/api/operations", response_model=schemas.OperationResponse, status_code=status.HTTP_201_CREATED)
async def create_operation(
        operation: schemas.OperationCreate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Crée une nouvelle opération"""
    return crud.create_operation(db=db, operation=operation)


@app.put("/api/operations/{operation_id}", response_model=schemas.OperationResponse)
async def update_operation(
        operation_id: int,
        operation: schemas.OperationUpdate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Met à jour une opération existante"""
    updated_operation = crud.update_operation(db, operation_id, operation)
    if updated_operation is None:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return updated_operation


@app.delete("/api/operations/{operation_id}", response_model=schemas.MessageResponse)
async def delete_operation(operation_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Supprime une opération"""
    success = crud.delete_operation(db, operation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return {"message": "Opération supprimée avec succès", "success": True}


# ==================== ENDPOINTS COMPTES (avec RLS) ====================

@app.get("/api/comptes", response_model=List[schemas.CompteResponse])
async def read_comptes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Récupère tous les comptes de l'utilisateur avec pagination"""
    comptes = crud.get_comptes(db, skip=skip, limit=limit)
    return comptes


@app.get("/api/comptes/{compte_id}", response_model=schemas.CompteResponse)
async def read_compte(compte_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère un compte par son ID avec ses opérations"""
    compte = crud.get_compte(db, compte_id=compte_id)
    if compte is None:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return compte


@app.post("/api/comptes", response_model=schemas.CompteResponse, status_code=status.HTTP_201_CREATED)
async def create_compte(
        compte: schemas.CompteCreate,
        current_user: models.Utilisateur = Depends(auth.get_current_user),
        db: Session = Depends(auth.get_db_with_rls)
):
    """Crée un nouveau compte pour l'utilisateur connecté"""
    # Ajouter l'ID utilisateur au compte
    compte_data = compte.model_dump()
    compte_data["idutilisateur"] = current_user.idutilisateur
    db_compte = models.Compte(**compte_data)
    db.add(db_compte)
    db.commit()
    db.refresh(db_compte)
    return db_compte


@app.put("/api/comptes/{compte_id}", response_model=schemas.CompteResponse)
async def update_compte(
        compte_id: int,
        compte: schemas.CompteUpdate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Met à jour un compte existant"""
    updated_compte = crud.update_compte(db, compte_id, compte)
    if updated_compte is None:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return updated_compte


@app.delete("/api/comptes/{compte_id}", response_model=schemas.MessageResponse)
async def delete_compte(compte_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Supprime un compte"""
    success = crud.delete_compte(db, compte_id)
    if not success:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return {"message": "Compte supprimé avec succès", "success": True}


@app.get("/api/comptes/{compte_id}/operations", response_model=List[schemas.OperationResponse])
async def read_compte_operations(compte_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère toutes les opérations d'un compte spécifique"""
    operations = crud.get_operations_by_compte(db, compte_id=compte_id)
    return operations


# ==================== ENDPOINTS CATEGORIES (avec RLS) ====================

@app.get("/api/categories", response_model=List[schemas.CategorieResponse])
async def read_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Récupère toutes les catégories de l'utilisateur avec pagination"""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/api/categories/{categorie_id}", response_model=schemas.CategorieResponse)
async def read_categorie(categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère une catégorie par son ID"""
    categorie = crud.get_categorie(db, categorie_id=categorie_id)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return categorie


@app.get("/api/categories/{categorie_id}/sous-categories", response_model=List[schemas.SousCategorieResponse])
async def read_categorie_sous_categories(categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère toutes les sous-catégories d'une catégorie"""
    sous_categories = crud.get_sous_categories_by_categorie(db, categorie_id=categorie_id)
    return sous_categories


@app.post("/api/categories", response_model=schemas.CategorieResponse, status_code=status.HTTP_201_CREATED)
async def create_categorie(
        categorie: schemas.CategorieCreate,
        current_user: models.Utilisateur = Depends(auth.get_current_user),
        db: Session = Depends(auth.get_db_with_rls)
):
    """Crée une nouvelle catégorie pour l'utilisateur connecté"""
    # Vérifier si la catégorie existe déjà pour cet utilisateur
    existing = crud.get_categorie_by_nom(db, nom_categorie=categorie.nomcategorie)
    if existing:
        raise HTTPException(status_code=400, detail="Cette catégorie existe déjà")

    # Créer avec l'ID utilisateur
    db_categorie = models.Categorie(
        nomcategorie=categorie.nomcategorie,
        idutilisateur=current_user.idutilisateur
    )
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie


@app.put("/api/categories/{categorie_id}", response_model=schemas.CategorieResponse)
async def update_categorie(
        categorie_id: int,
        categorie: schemas.CategorieUpdate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Met à jour une catégorie existante"""
    updated_categorie = crud.update_categorie(db, categorie_id, categorie)
    if updated_categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée ou conflit de nom")
    return updated_categorie


@app.delete("/api/categories/{categorie_id}", response_model=schemas.MessageResponse)
async def delete_categorie(categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Supprime une catégorie"""
    success = crud.delete_categorie(db, categorie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {"message": "Catégorie supprimée avec succès", "success": True}


# ==================== ENDPOINTS SOUS-CATEGORIES (avec RLS) ====================

@app.get("/api/sous-categories", response_model=List[schemas.SousCategorieResponse])
async def read_sous_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Récupère toutes les sous-catégories de l'utilisateur avec pagination"""
    sous_categories = crud.get_sous_categories(db, skip=skip, limit=limit)
    return sous_categories


@app.get("/api/sous-categories/{sous_categorie_id}", response_model=schemas.SousCategorieResponse)
async def read_sous_categorie(sous_categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère une sous-catégorie par son ID"""
    sous_categorie = crud.get_sous_categorie(db, sous_categorie_id=sous_categorie_id)
    if sous_categorie is None:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée")
    return sous_categorie


@app.get("/api/sous-categories/{sous_categorie_id}/operations", response_model=List[schemas.OperationResponse])
async def read_sous_categorie_operations(sous_categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère toutes les opérations d'une sous-catégorie"""
    operations = crud.get_operations_by_sous_categorie(db, id_sous_categorie=sous_categorie_id)
    return operations


@app.post("/api/sous-categories", response_model=schemas.SousCategorieResponse, status_code=status.HTTP_201_CREATED)
async def create_sous_categorie(
        sous_categorie: schemas.SousCategorieCreate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Crée une nouvelle sous-catégorie"""
    # Vérifier que la catégorie parente existe (RLS vérifie qu'elle appartient à l'utilisateur)
    categorie = crud.get_categorie(db, categorie_id=sous_categorie.idcategorie)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie parente non trouvée")

    return crud.create_sous_categorie(db=db, sous_categorie=sous_categorie)


@app.put("/api/sous-categories/{sous_categorie_id}", response_model=schemas.SousCategorieResponse)
async def update_sous_categorie(
        sous_categorie_id: int,
        sous_categorie: schemas.SousCategorieUpdate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Met à jour une sous-catégorie existante"""
    if sous_categorie.idcategorie:
        categorie = crud.get_categorie(db, categorie_id=sous_categorie.idcategorie)
        if not categorie:
            raise HTTPException(status_code=404, detail="Catégorie parente non trouvée")

    updated_sous_categorie = crud.update_sous_categorie(db, sous_categorie_id, sous_categorie)
    if updated_sous_categorie is None:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée ou conflit de nom")
    return updated_sous_categorie


@app.delete("/api/sous-categories/{sous_categorie_id}", response_model=schemas.MessageResponse)
async def delete_sous_categorie(sous_categorie_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Supprime une sous-catégorie"""
    success = crud.delete_sous_categorie(db, sous_categorie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée")
    return {"message": "Sous-catégorie supprimée avec succès", "success": True}


# ==================== ENDPOINTS TYPES (avec RLS) ====================

@app.get("/api/types", response_model=List[schemas.TypeResponse])
async def read_types(db: Session = Depends(auth.get_db_with_rls)):
    """Récupère tous les types d'opération de l'utilisateur"""
    types = crud.get_types(db)
    return types


@app.get("/api/types/{type_id}", response_model=schemas.TypeResponse)
async def read_type(type_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère un type par son ID"""
    type_obj = crud.get_type(db, type_id=type_id)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return type_obj


@app.get("/api/types/nom/{nom}", response_model=schemas.TypeResponse)
async def read_type_by_nom(nom: str, db: Session = Depends(auth.get_db_with_rls)):
    """Récupère un type par son nom"""
    type_obj = crud.get_type_by_nom(db, nom=nom)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return type_obj


@app.post("/api/types", response_model=schemas.TypeResponse, status_code=status.HTTP_201_CREATED)
async def create_type(
        type_data: schemas.TypeCreate,
        current_user: models.Utilisateur = Depends(auth.get_current_user),
        db: Session = Depends(auth.get_db_with_rls)
):
    """Crée un nouveau type d'opération pour l'utilisateur connecté"""
    # Vérifie si le type existe déjà pour cet utilisateur
    existing = crud.get_type_by_nom(db, nom=type_data.nom)
    if existing:
        raise HTTPException(status_code=400, detail="Ce type existe déjà")

    db_type = models.Type(nom=type_data.nom, idutilisateur=current_user.idutilisateur)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


@app.put("/api/types/{type_id}", response_model=schemas.TypeResponse)
async def update_type(
        type_id: int,
        type_update: schemas.TypeUpdate,
        db: Session = Depends(auth.get_db_with_rls)
):
    """Met à jour un type existant"""
    updated_type = crud.update_type(db, type_id, type_update)
    if updated_type is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return updated_type


@app.delete("/api/types/{type_id}", response_model=schemas.MessageResponse)
async def delete_type(type_id: int, db: Session = Depends(auth.get_db_with_rls)):
    """Supprime un type"""
    success = crud.delete_type(db, type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return {"message": "Type supprimé avec succès", "success": True}


# ==================== POINT D'ENTRÉE ====================

if __name__ == "__main__":
    import uvicorn

    print("🚀 Démarrage du serveur FastAPI...")
    print("📝 Documentation interactive: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("🔐 Authentification: JWT Bearer Token")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)