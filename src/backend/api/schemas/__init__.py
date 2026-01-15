"""
Schémas Pydantic pour validation des données API
Nouveau schéma avec OPERATION, CATEGORIE et SOUS_CATEGORIE
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from decimal import Decimal
from datetime import date as DateType


# ==================== TYPE SCHEMAS ====================

class TypeBase(BaseModel):
    """Schéma de base pour Type"""
    nom: str = Field(..., min_length=1, max_length=50, description="Nom du type (depense, revenu, transfert)")


class TypeCreate(TypeBase):
    """Schéma pour créer un type"""
    pass


class TypeUpdate(BaseModel):
    """Schéma pour mettre à jour un type (tous les champs optionnels)"""
    nom: Optional[str] = Field(None, min_length=1, max_length=50)


class TypeResponse(TypeBase):
    """Schéma de réponse pour Type (inclut l'ID)"""
    idtype: int

    model_config = ConfigDict(from_attributes=True)


# ==================== CATEGORIE SCHEMAS ====================

class CategorieBase(BaseModel):
    """Schéma de base pour Categorie (catégories principales)"""
    nomcategorie: str = Field(..., min_length=1, max_length=50, description="Nom de la catégorie principale")


class CategorieCreate(CategorieBase):
    """Schéma pour créer une catégorie"""
    pass


class CategorieUpdate(BaseModel):
    """Schéma pour mettre à jour une catégorie (tous les champs optionnels)"""
    nomcategorie: Optional[str] = Field(None, min_length=1, max_length=50)


class CategorieResponse(CategorieBase):
    """Schéma de réponse pour Categorie"""
    model_config = ConfigDict(from_attributes=True)


# ==================== SOUS-CATEGORIE SCHEMAS ====================

class SousCategorieBase(BaseModel):
    """Schéma de base pour SousCategorie"""
    nomsouscategorie: str = Field(..., min_length=1, max_length=50, description="Nom de la sous-catégorie")
    nomcategorie: str = Field(..., min_length=1, max_length=50, description="Nom de la catégorie parente")


class SousCategorieCreate(SousCategorieBase):
    """Schéma pour créer une sous-catégorie"""
    pass


class SousCategorieUpdate(BaseModel):
    """Schéma pour mettre à jour une sous-catégorie (tous les champs optionnels)"""
    nomsouscategorie: Optional[str] = Field(None, min_length=1, max_length=50)
    nomcategorie: Optional[str] = Field(None, min_length=1, max_length=50)


class SousCategorieResponse(SousCategorieBase):
    """Schéma de réponse pour SousCategorie"""
    model_config = ConfigDict(from_attributes=True)


# ==================== OPERATION SCHEMAS ====================

class OperationBase(BaseModel):
    """Schéma de base pour Operation (anciennement Transaction)"""
    date: DateType = Field(..., description="Date de l'opération (format: YYYY-MM-DD)")
    description: str = Field(..., min_length=1, description="Description de l'opération")
    montant: Decimal = Field(..., description="Montant de l'opération")
    idcompte: int = Field(..., description="ID du compte associé")
    idtype: int = Field(..., description="ID du type d'opération")
    nomsouscategorie: Optional[str] = Field(None, max_length=50, description="Nom de la sous-catégorie (optionnel)")


class OperationCreate(OperationBase):
    """Schéma pour créer une opération"""
    pass


class OperationUpdate(BaseModel):
    """Schéma pour mettre à jour une opération (tous les champs optionnels)"""
    date: Optional[DateType] = None
    description: Optional[str] = None
    montant: Optional[Decimal] = None
    idcompte: Optional[int] = None
    idtype: Optional[int] = None
    nomsouscategorie: Optional[str] = None


class OperationResponse(OperationBase):
    """Schéma de réponse pour Operation (inclut l'ID)"""
    idtransaction: int

    model_config = ConfigDict(from_attributes=True)


# ==================== COMPTE SCHEMAS ====================

class CompteBase(BaseModel):
    """Schéma de base pour Compte"""
    nom: str = Field(..., min_length=1, description="Nom du compte")
    solde: Decimal = Field(..., description="Solde du compte")
    type: str = Field(..., min_length=1, description="Type de compte")


class CompteCreate(CompteBase):
    """Schéma pour créer un compte"""
    pass


class CompteUpdate(BaseModel):
    """Schéma pour mettre à jour un compte (tous les champs optionnels)"""
    nom: Optional[str] = None
    solde: Optional[Decimal] = None
    type: Optional[str] = None


class CompteResponse(CompteBase):
    """Schéma de réponse pour Compte (inclut l'ID et les opérations)"""
    idcompte: int
    operations: List[OperationResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ==================== SCHEMAS SUPPLÉMENTAIRES ====================

class CompteSimpleResponse(BaseModel):
    """Réponse simplifiée pour Compte (sans opérations pour éviter récursion)"""
    idcompte: int
    nom: str
    solde: Decimal
    type: str

    model_config = ConfigDict(from_attributes=True)


class OperationWithDetails(OperationResponse):
    """Opération avec informations du compte et sous-catégorie"""
    compte: CompteSimpleResponse
    sous_categorie: Optional[SousCategorieResponse] = None

    model_config = ConfigDict(from_attributes=True)


class CategorieWithSousCategories(CategorieResponse):
    """Catégorie avec ses sous-catégories"""
    sous_categories: List[SousCategorieResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ==================== MESSAGES ====================

class MessageResponse(BaseModel):
    """Schéma pour les messages de réponse génériques"""
    message: str
    success: bool = True


# ==================== RÉTRO-COMPATIBILITÉ (Transaction -> Operation) ====================
# Alias pour assurer la rétro-compatibilité avec l'ancien code

TransactionBase = OperationBase
TransactionCreate = OperationCreate
TransactionUpdate = OperationUpdate
TransactionResponse = OperationResponse
TransactionWithCompte = OperationWithDetails
