"""
Schémas Pydantic pour validation des données API
Nouveau schéma avec OPERATION, CATEGORIE et SOUS_CATEGORIE

Support multi-utilisateurs avec authentification JWT
"""
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List
from decimal import Decimal
from datetime import date as DateType, datetime


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
    idcategorie: int

    model_config = ConfigDict(from_attributes=True)


# ==================== SOUS-CATEGORIE SCHEMAS ====================

class SousCategorieBase(BaseModel):
    """Schéma de base pour SousCategorie"""
    nomsouscategorie: str = Field(..., min_length=1, max_length=50, description="Nom de la sous-catégorie")
    idcategorie: int = Field(..., description="ID de la catégorie parente")


class SousCategorieCreate(SousCategorieBase):
    """Schéma pour créer une sous-catégorie"""
    pass


class SousCategorieUpdate(BaseModel):
    """Schéma pour mettre à jour une sous-catégorie (tous les champs optionnels)"""
    nomsouscategorie: Optional[str] = Field(None, min_length=1, max_length=50)
    idcategorie: Optional[int] = None


class SousCategorieResponse(SousCategorieBase):
    """Schéma de réponse pour SousCategorie"""
    idsouscategorie: int

    model_config = ConfigDict(from_attributes=True)


# ==================== OPERATION SCHEMAS ====================

class OperationBase(BaseModel):
    """Schéma de base pour Operation (anciennement Transaction)"""
    date: DateType = Field(..., description="Date de l'opération (format: YYYY-MM-DD)")
    description: str = Field(..., min_length=1, description="Description de l'opération")
    montant: Decimal = Field(..., description="Montant de l'opération")
    idcompte: int = Field(..., description="ID du compte associé")
    idtype: int = Field(..., description="ID du type d'opération")
    idsouscategorie: Optional[int] = Field(None, description="ID de la sous-catégorie (optionnel)")


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
    idsouscategorie: Optional[int] = None


class OperationResponse(OperationBase):
    """Schéma de réponse pour Operation (inclut l'ID)"""
    idoperation: int

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


# ==================== UTILISATEUR SCHEMAS ====================

class UtilisateurBase(BaseModel):
    """Schéma de base pour Utilisateur"""
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    nom_affichage: Optional[str] = Field(None, max_length=100, description="Nom d'affichage")


class UtilisateurCreate(UtilisateurBase):
    """Schéma pour créer un utilisateur (inscription)"""
    mot_de_passe: str = Field(..., min_length=8, description="Mot de passe (min 8 caractères)")


class UtilisateurUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    nom_affichage: Optional[str] = Field(None, max_length=100)
    mot_de_passe: Optional[str] = Field(None, min_length=8)


class UtilisateurResponse(UtilisateurBase):
    """Schéma de réponse pour Utilisateur"""
    idutilisateur: int
    date_creation: datetime
    derniere_connexion: Optional[datetime] = None
    actif: bool

    model_config = ConfigDict(from_attributes=True)


class UtilisateurSimple(BaseModel):
    """Schéma simplifié pour Utilisateur"""
    idutilisateur: int
    email: EmailStr
    nom_affichage: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ==================== AUTHENTIFICATION SCHEMAS ====================

class LoginRequest(BaseModel):
    """Schéma pour la requête de connexion"""
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    mot_de_passe: str = Field(..., description="Mot de passe")


class TokenResponse(BaseModel):
    """Schéma de réponse pour le token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Durée de validité en secondes")
    user: UtilisateurSimple


class RefreshTokenRequest(BaseModel):
    """Schéma pour rafraîchir le token"""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Schéma pour changer le mot de passe"""
    ancien_mot_de_passe: str = Field(..., description="Mot de passe actuel")
    nouveau_mot_de_passe: str = Field(..., min_length=8, description="Nouveau mot de passe")