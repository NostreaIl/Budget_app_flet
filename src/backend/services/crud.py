"""
Opérations CRUD (Create, Read, Update, Delete) pour la base de données
Mis à jour pour le nouveau schéma avec Operation, Categorie et SousCategorie
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from src.backend.database import models
from src.backend.api import schemas


# ==================== OPERATIONS CRUD ====================

def get_operation(db: Session, operation_id: int) -> Optional[models.Operation]:
    """Récupère une opération par son ID"""
    return db.query(models.Operation).filter(models.Operation.idoperation == operation_id).first()


def get_operations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Operation]:
    """Récupère toutes les opérations avec pagination"""
    return db.query(models.Operation).offset(skip).limit(limit).all()


def get_operations_by_compte(db: Session, compte_id: int) -> List[models.Operation]:
    """Récupère toutes les opérations d'un compte donné"""
    return db.query(models.Operation).filter(models.Operation.idcompte == compte_id).all()


def get_operations_by_sous_categorie(db: Session, id_sous_categorie: int) -> List[models.Operation]:
    """Récupère toutes les opérations d'une sous-catégorie donnée"""
    return db.query(models.Operation).filter(models.Operation.idsouscategorie == id_sous_categorie).all()


def create_operation(db: Session, operation: schemas.OperationCreate) -> models.Operation:
    """Crée une nouvelle opération"""
    db_operation = models.Operation(**operation.model_dump())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


def update_operation(
    db: Session,
    operation_id: int,
    operation_update: schemas.OperationUpdate
) -> Optional[models.Operation]:
    """Met à jour une opération existante"""
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        return None

    # Mise à jour uniquement des champs fournis
    update_data = operation_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_operation, field, value)

    db.commit()
    db.refresh(db_operation)
    return db_operation


def delete_operation(db: Session, operation_id: int) -> bool:
    """Supprime une opération"""
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        return False

    db.delete(db_operation)
    db.commit()
    return True


# ==================== COMPTES CRUD ====================

def get_compte(db: Session, compte_id: int) -> Optional[models.Compte]:
    """Récupère un compte par son ID"""
    return db.query(models.Compte).filter(models.Compte.idcompte == compte_id).first()


def get_comptes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Compte]:
    """Récupère tous les comptes avec pagination"""
    return db.query(models.Compte).offset(skip).limit(limit).all()


def create_compte(db: Session, compte: schemas.CompteCreate) -> models.Compte:
    """Crée un nouveau compte"""
    db_compte = models.Compte(**compte.model_dump())
    db.add(db_compte)
    db.commit()
    db.refresh(db_compte)
    return db_compte


def update_compte(
    db: Session,
    compte_id: int,
    compte_update: schemas.CompteUpdate
) -> Optional[models.Compte]:
    """Met à jour un compte existant"""
    db_compte = get_compte(db, compte_id)
    if not db_compte:
        return None

    update_data = compte_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_compte, field, value)

    db.commit()
    db.refresh(db_compte)
    return db_compte


def delete_compte(db: Session, compte_id: int) -> bool:
    """Supprime un compte"""
    db_compte = get_compte(db, compte_id)
    if not db_compte:
        return False

    db.delete(db_compte)
    db.commit()
    return True


# ==================== CATEGORIES CRUD ====================

def get_categorie(db: Session, categorie_id: int) -> Optional[models.Categorie]:
    """Récupère une catégorie par son ID"""
    return db.query(models.Categorie).filter(models.Categorie.idcategorie == categorie_id).first()


def get_categorie_by_nom(db: Session, nom_categorie: str) -> Optional[models.Categorie]:
    """Récupère une catégorie par son nom"""
    return db.query(models.Categorie).filter(models.Categorie.nomcategorie == nom_categorie).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Categorie]:
    """Récupère toutes les catégories avec pagination"""
    return db.query(models.Categorie).offset(skip).limit(limit).all()


def create_categorie(db: Session, categorie: schemas.CategorieCreate) -> models.Categorie:
    """Crée une nouvelle catégorie"""
    db_categorie = models.Categorie(**categorie.model_dump())
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie


def update_categorie(
    db: Session,
    categorie_id: int,
    categorie_update: schemas.CategorieUpdate
) -> Optional[models.Categorie]:
    """Met à jour une catégorie existante"""
    db_categorie = get_categorie(db, categorie_id)
    if not db_categorie:
        return None

    # Mise à jour du nom si fourni
    if categorie_update.nomcategorie:
        # Vérifier que le nouveau nom n'existe pas déjà
        existing = get_categorie_by_nom(db, categorie_update.nomcategorie)
        if existing and existing.idcategorie != categorie_id:
            return None
        db_categorie.nomcategorie = categorie_update.nomcategorie

    db.commit()
    db.refresh(db_categorie)
    return db_categorie


def delete_categorie(db: Session, categorie_id: int) -> bool:
    """Supprime une catégorie"""
    db_categorie = get_categorie(db, categorie_id)
    if not db_categorie:
        return False

    db.delete(db_categorie)
    db.commit()
    return True


# ==================== SOUS-CATEGORIES CRUD ====================

def get_sous_categorie(db: Session, sous_categorie_id: int) -> Optional[models.SousCategorie]:
    """Récupère une sous-catégorie par son ID"""
    return db.query(models.SousCategorie).filter(
        models.SousCategorie.idsouscategorie == sous_categorie_id
    ).first()


def get_sous_categorie_by_nom(db: Session, nom_sous_categorie: str) -> Optional[models.SousCategorie]:
    """Récupère une sous-catégorie par son nom"""
    return db.query(models.SousCategorie).filter(
        models.SousCategorie.nomsouscategorie == nom_sous_categorie
    ).first()


def get_sous_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.SousCategorie]:
    """Récupère toutes les sous-catégories avec pagination"""
    return db.query(models.SousCategorie).offset(skip).limit(limit).all()


def get_sous_categories_by_categorie(db: Session, categorie_id: int) -> List[models.SousCategorie]:
    """Récupère toutes les sous-catégories d'une catégorie donnée"""
    return db.query(models.SousCategorie).filter(
        models.SousCategorie.idcategorie == categorie_id
    ).all()


def create_sous_categorie(db: Session, sous_categorie: schemas.SousCategorieCreate) -> models.SousCategorie:
    """Crée une nouvelle sous-catégorie"""
    db_sous_categorie = models.SousCategorie(**sous_categorie.model_dump())
    db.add(db_sous_categorie)
    db.commit()
    db.refresh(db_sous_categorie)
    return db_sous_categorie


def update_sous_categorie(
    db: Session,
    sous_categorie_id: int,
    sous_categorie_update: schemas.SousCategorieUpdate
) -> Optional[models.SousCategorie]:
    """Met à jour une sous-catégorie existante"""
    db_sous_categorie = get_sous_categorie(db, sous_categorie_id)
    if not db_sous_categorie:
        return None

    # Mise à jour des champs fournis
    if sous_categorie_update.nomsouscategorie:
        db_sous_categorie.nomsouscategorie = sous_categorie_update.nomsouscategorie

    if sous_categorie_update.idcategorie:
        db_sous_categorie.idcategorie = sous_categorie_update.idcategorie

    db.commit()
    db.refresh(db_sous_categorie)
    return db_sous_categorie


def delete_sous_categorie(db: Session, sous_categorie_id: int) -> bool:
    """Supprime une sous-catégorie"""
    db_sous_categorie = get_sous_categorie(db, sous_categorie_id)
    if not db_sous_categorie:
        return False

    db.delete(db_sous_categorie)
    db.commit()
    return True


# ==================== TYPES CRUD ====================

def get_type(db: Session, type_id: int) -> Optional[models.Type]:
    """Récupère un type par son ID"""
    return db.query(models.Type).filter(models.Type.idtype == type_id).first()


def get_type_by_nom(db: Session, nom: str) -> Optional[models.Type]:
    """Récupère un type par son nom"""
    return db.query(models.Type).filter(models.Type.nom == nom).first()


def get_types(db: Session) -> List[models.Type]:
    """Récupère tous les types"""
    return db.query(models.Type).all()


def create_type(db: Session, type_data: schemas.TypeCreate) -> models.Type:
    """Crée un nouveau type"""
    db_type = models.Type(**type_data.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def update_type(
    db: Session,
    type_id: int,
    type_update: schemas.TypeUpdate
) -> Optional[models.Type]:
    """Met à jour un type existant"""
    db_type = get_type(db, type_id)
    if not db_type:
        return None

    update_data = type_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_type, field, value)

    db.commit()
    db.refresh(db_type)
    return db_type


def delete_type(db: Session, type_id: int) -> bool:
    """Supprime un type"""
    db_type = get_type(db, type_id)
    if not db_type:
        return False

    db.delete(db_type)
    db.commit()
    return True


# ==================== FONCTIONS UTILITAIRES ====================

def get_compte_with_operations(db: Session, compte_id: int) -> Optional[models.Compte]:
    """Récupère un compte avec toutes ses opérations"""
    return db.query(models.Compte).filter(models.Compte.idcompte == compte_id).first()


def get_total_solde(db: Session) -> float:
    """Calcule le solde total de tous les comptes"""
    comptes = get_comptes(db)
    return sum(float(compte.solde) for compte in comptes)


def get_statistics(db: Session) -> dict:
    """Récupère des statistiques générales"""
    return {
        "total_operations": db.query(models.Operation).count(),
        "total_comptes": db.query(models.Compte).count(),
        "total_categories": db.query(models.Categorie).count(),
        "total_sous_categories": db.query(models.SousCategorie).count(),
        "total_types": db.query(models.Type).count(),
        "solde_total": get_total_solde(db)
    }

def search_operations(db: Session, search: str, skip: int = 0, limit: int = 100):
    """Recherche les opérations par description"""
    return (
        db.query(models.Operation)
        .filter(models.Operation.description.ilike(f"%{search}%"))  # ILIKE = insensible à la casse
        .order_by(models.Operation.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


