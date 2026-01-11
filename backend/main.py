"""
Backend FastAPI pour Budget App
API REST connectée à PostgreSQL via SQLAlchemy
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db, test_connection
from backend import crud, schemas

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Budget API",
    description="API REST pour gérer les transactions, comptes et catégories budgétaires",
    version="1.0.0"
)

# Configuration CORS pour permettre les appels depuis l'app Flet
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
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
        "version": "1.0.0",
        "database": "PostgreSQL connected via SQLAlchemy"
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


# ==================== ENDPOINTS TRANSACTIONS ====================

@app.get("/api/transactions", response_model=List[schemas.TransactionResponse])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère toutes les transactions avec pagination"""
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions


@app.get("/api/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
async def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Récupère une transaction par son ID"""
    transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return transaction


@app.post("/api/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle transaction"""
    return crud.create_transaction(db=db, transaction=transaction)


@app.put("/api/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une transaction existante"""
    updated_transaction = crud.update_transaction(db, transaction_id, transaction)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return updated_transaction


@app.delete("/api/transactions/{transaction_id}", response_model=schemas.MessageResponse)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Supprime une transaction"""
    success = crud.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return {"message": "Transaction supprimée avec succès", "success": True}


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
    """Récupère un compte par son ID avec ses transactions"""
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


@app.get("/api/comptes/{compte_id}/transactions", response_model=List[schemas.TransactionResponse])
async def read_compte_transactions(compte_id: int, db: Session = Depends(get_db)):
    """Récupère toutes les transactions d'un compte spécifique"""
    transactions = crud.get_transactions_by_compte(db, compte_id=compte_id)
    return transactions


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


@app.get("/api/categories/{categorie_id}", response_model=schemas.CategorieResponse)
async def read_categorie(categorie_id: int, db: Session = Depends(get_db)):
    """Récupère une catégorie par son ID"""
    categorie = crud.get_categorie(db, categorie_id=categorie_id)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return categorie


@app.post("/api/categories", response_model=schemas.CategorieResponse, status_code=status.HTTP_201_CREATED)
async def create_categorie(
    categorie: schemas.CategorieCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle catégorie"""
    return crud.create_categorie(db=db, categorie=categorie)


@app.put("/api/categories/{categorie_id}", response_model=schemas.CategorieResponse)
async def update_categorie(
    categorie_id: int,
    categorie: schemas.CategorieUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une catégorie existante"""
    updated_categorie = crud.update_categorie(db, categorie_id, categorie)
    if updated_categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return updated_categorie


@app.delete("/api/categories/{categorie_id}", response_model=schemas.MessageResponse)
async def delete_categorie(categorie_id: int, db: Session = Depends(get_db)):
    """Supprime une catégorie"""
    success = crud.delete_categorie(db, categorie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {"message": "Catégorie supprimée avec succès", "success": True}


# ==================== ENDPOINTS TYPES ====================

@app.get("/api/types", response_model=List[schemas.TypeResponse])
async def read_types(db: Session = Depends(get_db)):
    """Récupère tous les types de transaction"""
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
    """Crée un nouveau type de transaction"""
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
