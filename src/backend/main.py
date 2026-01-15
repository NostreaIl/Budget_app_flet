"""
Backend FastAPI pour Budget App
API REST connectée à PostgreSQL via SQLAlchemy
Mis à jour pour le nouveau schéma avec Operation, Categorie et SousCategorie
"""
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

load_dotenv()

from src.backend.database.connection import get_db, test_connection
from src.backend.services import crud
from src.backend.api import schemas

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Budget API",
    description="API REST pour gérer les opérations, comptes, catégories et sous-catégories budgétaires",
    version="2.0.0"
)

# Configuration CORS pour permettre les appels depuis l'app Flet
# Utiliser les origines depuis .env en production
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Origines configurées via .env
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
        "version": "2.0.0",
        "database": "PostgreSQL connected via SQLAlchemy",
        "schema": "Operation + Categorie + SousCategorie"
    }


@app.get("/health")
async def health_check():
    """Vérifie la santé de l'API et la connexion à la base de données"""
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }


@app.get("/api/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Récupère les statistiques générales"""
    stats = crud.get_statistics(db)
    return stats


# ==================== ENDPOINTS OPERATIONS ====================

@app.get("/api/operations", response_model=List[schemas.OperationResponse])
async def read_operations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère toutes les opérations avec pagination"""
    operations = crud.get_operations(db, skip=skip, limit=limit)
    return operations


@app.get("/api/operations/{operation_id}", response_model=schemas.OperationResponse)
async def read_operation(operation_id: int, db: Session = Depends(get_db)):
    """Récupère une opération par son ID"""
    operation = crud.get_operation(db, operation_id=operation_id)
    if operation is None:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return operation


@app.post("/api/operations", response_model=schemas.OperationResponse, status_code=status.HTTP_201_CREATED)
async def create_operation(
    operation: schemas.OperationCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle opération"""
    return crud.create_operation(db=db, operation=operation)


@app.put("/api/operations/{operation_id}", response_model=schemas.OperationResponse)
async def update_operation(
    operation_id: int,
    operation: schemas.OperationUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une opération existante"""
    updated_operation = crud.update_operation(db, operation_id, operation)
    if updated_operation is None:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return updated_operation


@app.delete("/api/operations/{operation_id}", response_model=schemas.MessageResponse)
async def delete_operation(operation_id: int, db: Session = Depends(get_db)):
    """Supprime une opération"""
    success = crud.delete_operation(db, operation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Opération non trouvée")
    return {"message": "Opération supprimée avec succès", "success": True}


# ==================== ENDPOINTS TRANSACTIONS (Rétro-compatibilité) ====================

@app.get("/api/transactions", response_model=List[schemas.TransactionResponse])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère toutes les transactions (alias pour opérations)"""
    return await read_operations(skip, limit, db)


@app.get("/api/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
async def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Récupère une transaction par son ID (alias pour opération)"""
    return await read_operation(transaction_id, db)


@app.post("/api/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle transaction (alias pour opération)"""
    return crud.create_transaction(db=db, transaction=transaction)


@app.put("/api/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une transaction existante (alias pour opération)"""
    updated_transaction = crud.update_transaction(db, transaction_id, transaction)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return updated_transaction


@app.delete("/api/transactions/{transaction_id}", response_model=schemas.MessageResponse)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Supprime une transaction (alias pour opération)"""
    return await delete_operation(transaction_id, db)


# ==================== ENDPOINTS COMPTES ====================

@app.get("/api/comptes", response_model=List[schemas.CompteResponse])
async def read_comptes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère tous les comptes avec pagination"""
    comptes = crud.get_comptes(db, skip=skip, limit=limit)
    return comptes


@app.get("/api/comptes/{compte_id}", response_model=schemas.CompteResponse)
async def read_compte(compte_id: int, db: Session = Depends(get_db)):
    """Récupère un compte par son ID avec ses opérations"""
    compte = crud.get_compte(db, compte_id=compte_id)
    if compte is None:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return compte


@app.post("/api/comptes", response_model=schemas.CompteResponse, status_code=status.HTTP_201_CREATED)
async def create_compte(
    compte: schemas.CompteCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau compte"""
    return crud.create_compte(db=db, compte=compte)


@app.put("/api/comptes/{compte_id}", response_model=schemas.CompteResponse)
async def update_compte(
    compte_id: int,
    compte: schemas.CompteUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un compte existant"""
    updated_compte = crud.update_compte(db, compte_id, compte)
    if updated_compte is None:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return updated_compte


@app.delete("/api/comptes/{compte_id}", response_model=schemas.MessageResponse)
async def delete_compte(compte_id: int, db: Session = Depends(get_db)):
    """Supprime un compte"""
    success = crud.delete_compte(db, compte_id)
    if not success:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return {"message": "Compte supprimé avec succès", "success": True}


@app.get("/api/comptes/{compte_id}/operations", response_model=List[schemas.OperationResponse])
async def read_compte_operations(compte_id: int, db: Session = Depends(get_db)):
    """Récupère toutes les opérations d'un compte spécifique"""
    operations = crud.get_operations_by_compte(db, compte_id=compte_id)
    return operations


@app.get("/api/comptes/{compte_id}/transactions", response_model=List[schemas.TransactionResponse])
async def read_compte_transactions(compte_id: int, db: Session = Depends(get_db)):
    """Récupère toutes les transactions d'un compte (alias pour opérations)"""
    return await read_compte_operations(compte_id, db)


# ==================== ENDPOINTS CATEGORIES ====================

@app.get("/api/categories", response_model=List[schemas.CategorieResponse])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère toutes les catégories avec pagination"""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/api/categories/{nom_categorie}", response_model=schemas.CategorieResponse)
async def read_categorie(nom_categorie: str, db: Session = Depends(get_db)):
    """Récupère une catégorie par son nom"""
    categorie = crud.get_categorie(db, nom_categorie=nom_categorie)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return categorie


@app.get("/api/categories/{nom_categorie}/sous-categories", response_model=List[schemas.SousCategorieResponse])
async def read_categorie_sous_categories(nom_categorie: str, db: Session = Depends(get_db)):
    """Récupère toutes les sous-catégories d'une catégorie"""
    sous_categories = crud.get_sous_categories_by_categorie(db, nom_categorie=nom_categorie)
    return sous_categories


@app.post("/api/categories", response_model=schemas.CategorieResponse, status_code=status.HTTP_201_CREATED)
async def create_categorie(
    categorie: schemas.CategorieCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle catégorie"""
    # Vérifier si la catégorie existe déjà
    existing = crud.get_categorie(db, nom_categorie=categorie.nomcategorie)
    if existing:
        raise HTTPException(status_code=400, detail="Cette catégorie existe déjà")
    return crud.create_categorie(db=db, categorie=categorie)


@app.put("/api/categories/{nom_categorie}", response_model=schemas.CategorieResponse)
async def update_categorie(
    nom_categorie: str,
    categorie: schemas.CategorieUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une catégorie existante"""
    updated_categorie = crud.update_categorie(db, nom_categorie, categorie)
    if updated_categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée ou conflit de nom")
    return updated_categorie


@app.delete("/api/categories/{nom_categorie}", response_model=schemas.MessageResponse)
async def delete_categorie(nom_categorie: str, db: Session = Depends(get_db)):
    """Supprime une catégorie"""
    success = crud.delete_categorie(db, nom_categorie)
    if not success:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {"message": "Catégorie supprimée avec succès", "success": True}


# ==================== ENDPOINTS SOUS-CATEGORIES ====================

@app.get("/api/sous-categories", response_model=List[schemas.SousCategorieResponse])
async def read_sous_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère toutes les sous-catégories avec pagination"""
    sous_categories = crud.get_sous_categories(db, skip=skip, limit=limit)
    return sous_categories


@app.get("/api/sous-categories/{nom_sous_categorie}", response_model=schemas.SousCategorieResponse)
async def read_sous_categorie(nom_sous_categorie: str, db: Session = Depends(get_db)):
    """Récupère une sous-catégorie par son nom"""
    sous_categorie = crud.get_sous_categorie(db, nom_sous_categorie=nom_sous_categorie)
    if sous_categorie is None:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée")
    return sous_categorie


@app.get("/api/sous-categories/{nom_sous_categorie}/operations", response_model=List[schemas.OperationResponse])
async def read_sous_categorie_operations(nom_sous_categorie: str, db: Session = Depends(get_db)):
    """Récupère toutes les opérations d'une sous-catégorie"""
    operations = crud.get_operations_by_sous_categorie(db, nom_sous_categorie=nom_sous_categorie)
    return operations


@app.post("/api/sous-categories", response_model=schemas.SousCategorieResponse, status_code=status.HTTP_201_CREATED)
async def create_sous_categorie(
    sous_categorie: schemas.SousCategorieCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle sous-catégorie"""
    # Vérifier que la catégorie parente existe
    categorie = crud.get_categorie(db, nom_categorie=sous_categorie.nomcategorie)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie parente non trouvée")

    # Vérifier si la sous-catégorie existe déjà
    existing = crud.get_sous_categorie(db, nom_sous_categorie=sous_categorie.nomsouscategorie)
    if existing:
        raise HTTPException(status_code=400, detail="Cette sous-catégorie existe déjà")

    return crud.create_sous_categorie(db=db, sous_categorie=sous_categorie)


@app.put("/api/sous-categories/{nom_sous_categorie}", response_model=schemas.SousCategorieResponse)
async def update_sous_categorie(
    nom_sous_categorie: str,
    sous_categorie: schemas.SousCategorieUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une sous-catégorie existante"""
    # Si on change la catégorie parente, vérifier qu'elle existe
    if sous_categorie.nomcategorie:
        categorie = crud.get_categorie(db, nom_categorie=sous_categorie.nomcategorie)
        if not categorie:
            raise HTTPException(status_code=404, detail="Catégorie parente non trouvée")

    updated_sous_categorie = crud.update_sous_categorie(db, nom_sous_categorie, sous_categorie)
    if updated_sous_categorie is None:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée ou conflit de nom")
    return updated_sous_categorie


@app.delete("/api/sous-categories/{nom_sous_categorie}", response_model=schemas.MessageResponse)
async def delete_sous_categorie(nom_sous_categorie: str, db: Session = Depends(get_db)):
    """Supprime une sous-catégorie"""
    success = crud.delete_sous_categorie(db, nom_sous_categorie)
    if not success:
        raise HTTPException(status_code=404, detail="Sous-catégorie non trouvée")
    return {"message": "Sous-catégorie supprimée avec succès", "success": True}


# ==================== ENDPOINTS TYPES ====================

@app.get("/api/types", response_model=List[schemas.TypeResponse])
async def read_types(db: Session = Depends(get_db)):
    """Récupère tous les types d'opération"""
    types = crud.get_types(db)
    return types


@app.get("/api/types/{type_id}", response_model=schemas.TypeResponse)
async def read_type(type_id: int, db: Session = Depends(get_db)):
    """Récupère un type par son ID"""
    type_obj = crud.get_type(db, type_id=type_id)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return type_obj


@app.get("/api/types/nom/{nom}", response_model=schemas.TypeResponse)
async def read_type_by_nom(nom: str, db: Session = Depends(get_db)):
    """Récupère un type par son nom"""
    type_obj = crud.get_type_by_nom(db, nom=nom)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return type_obj


@app.post("/api/types", response_model=schemas.TypeResponse, status_code=status.HTTP_201_CREATED)
async def create_type(
    type_data: schemas.TypeCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau type d'opération"""
    # Vérifie si le type existe déjà
    existing = crud.get_type_by_nom(db, nom=type_data.nom)
    if existing:
        raise HTTPException(status_code=400, detail="Ce type existe déjà")
    return crud.create_type(db=db, type_data=type_data)


@app.put("/api/types/{type_id}", response_model=schemas.TypeResponse)
async def update_type(
    type_id: int,
    type_update: schemas.TypeUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un type existant"""
    updated_type = crud.update_type(db, type_id, type_update)
    if updated_type is None:
        raise HTTPException(status_code=404, detail="Type non trouvé")
    return updated_type


@app.delete("/api/types/{type_id}", response_model=schemas.MessageResponse)
async def delete_type(type_id: int, db: Session = Depends(get_db)):
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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
