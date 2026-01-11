"""
Opérations CRUD (Create, Read, Update, Delete) pour la base de données
Fonctions réutilisables pour manipuler les données
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from backend import models, schemas


# ==================== TRANSACTIONS CRUD ====================

def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transaction]:
    """Récupère une transaction par son ID"""
    return db.query(models.Transaction).filter(models.Transaction.idtransaction == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Transaction]:
    """Récupère toutes les transactions avec pagination"""
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def get_transactions_by_compte(db: Session, compte_id: int) -> List[models.Transaction]:
    """Récupère toutes les transactions d'un compte donné"""
    return db.query(models.Transaction).filter(models.Transaction.idcompte == compte_id).all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate) -> models.Transaction:
    """Crée une nouvelle transaction"""
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate
) -> Optional[models.Transaction]:
    """Met à jour une transaction existante"""
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None

    # Mise à jour uniquement des champs fournis
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int) -> bool:
    """Supprime une transaction"""
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return False

    db.delete(db_transaction)
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

    update_data = categorie_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_categorie, field, value)

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


# ==================== FONCTIONS UTILITAIRES ====================

def get_compte_with_transactions(db: Session, compte_id: int) -> Optional[models.Compte]:
    """Récupère un compte avec toutes ses transactions"""
    return db.query(models.Compte).filter(models.Compte.idcompte == compte_id).first()


def get_total_solde(db: Session) -> float:
    """Calcule le solde total de tous les comptes"""
    comptes = get_comptes(db)
    return sum(float(compte.solde) for compte in comptes)


def get_statistics(db: Session) -> dict:
    """Récupère des statistiques générales"""
    return {
        "total_transactions": db.query(models.Transaction).count(),
        "total_comptes": db.query(models.Compte).count(),
        "total_categories": db.query(models.Categorie).count(),
        "solde_total": get_total_solde(db)
    }
