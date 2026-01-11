"""
Schémas Pydantic pour validation des données API
Séparation entre données entrantes (Create/Update) et sortantes (Response)
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from decimal import Decimal
from datetime import date


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


# ==================== TRANSACTION SCHEMAS ====================

class TransactionBase(BaseModel):
    """Schéma de base pour Transaction"""
    date: date = Field(..., description="Date de la transaction (format: YYYY-MM-DD)")
    description: str = Field(..., min_length=1, description="Description de la transaction")
    montant: Decimal = Field(..., description="Montant de la transaction")
    idcompte: int = Field(..., description="ID du compte associé")
    idtype: int = Field(..., description="ID du type de transaction (1=depense, 2=revenu, 3=transfert)")


class TransactionCreate(TransactionBase):
    """Schéma pour créer une transaction"""
    pass


class TransactionUpdate(BaseModel):
    """Schéma pour mettre à jour une transaction (tous les champs optionnels)"""
    date: Optional[date] = None
    description: Optional[str] = None
    montant: Optional[Decimal] = None
    idcompte: Optional[int] = None
    idtype: Optional[int] = None


class TransactionResponse(TransactionBase):
    """Schéma de réponse pour Transaction (inclut l'ID)"""
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
    """Schéma de réponse pour Compte (inclut l'ID et les transactions)"""
    idcompte: int
    transactions: List[TransactionResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ==================== CATEGORIE SCHEMAS ====================

class CategorieBase(BaseModel):
    """Schéma de base pour Categorie"""
    nom: str = Field(..., min_length=1, description="Nom de la catégorie")
    idcategorie_enfant: Optional[int] = Field(None, description="ID de la catégorie parent (si sous-catégorie)")


class CategorieCreate(CategorieBase):
    """Schéma pour créer une catégorie"""
    pass


class CategorieUpdate(BaseModel):
    """Schéma pour mettre à jour une catégorie (tous les champs optionnels)"""
    nom: Optional[str] = None
    idcategorie_enfant: Optional[int] = None


class CategorieResponse(CategorieBase):
    """Schéma de réponse pour Categorie (inclut l'ID)"""
    idcategorie: int

    model_config = ConfigDict(from_attributes=True)


# ==================== SCHEMAS SUPPLÉMENTAIRES ====================

class CompteSimpleResponse(BaseModel):
    """Réponse simplifiée pour Compte (sans transactions pour éviter récursion)"""
    idcompte: int
    nom: str
    solde: Decimal
    type: str

    model_config = ConfigDict(from_attributes=True)


class TransactionWithCompte(TransactionResponse):
    """Transaction avec informations du compte"""
    compte: CompteSimpleResponse

    model_config = ConfigDict(from_attributes=True)


# ==================== MESSAGES ====================

class MessageResponse(BaseModel):
    """Schéma pour les messages de réponse génériques"""
    message: str
    success: bool = True
