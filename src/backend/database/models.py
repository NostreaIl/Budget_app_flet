"""
Modèles SQLAlchemy pour la base de données PostgreSQL Budget_app
Nouveau schéma avec CATEGORIE/SOUS_CATEGORIE séparées
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.backend.database.connection import Base


class Type(Base):
    """
    Modèle pour la table 'type'
    Représente le type d'une opération (depense, revenu, transfert)
    """
    __tablename__ = "type"

    idtype = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(50), nullable=False, unique=True)

    # Relation avec Operation
    operations = relationship("Operation", back_populates="type_operation")

    def __repr__(self):
        return f"<Type(id={self.idtype}, nom='{self.nom}')>"


class Compte(Base):
    """
    Modèle pour la table 'compte'
    Représente un compte bancaire
    """
    __tablename__ = "compte"

    idcompte = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String, nullable=False)
    solde = Column(Numeric(10, 2), nullable=False)
    type = Column(String(50), nullable=False)

    # Relation avec Operation
    operations = relationship("Operation", back_populates="compte", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Compte(id={self.idcompte}, nom='{self.nom}', solde={self.solde}, type='{self.type}')>"


class Categorie(Base):
    """
    Modèle pour la table 'categorie'
    Représente une catégorie principale (Alimentation, Transport, etc.)
    """
    __tablename__ = "categorie"

    idcategorie = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nomcategorie = Column(String(50), nullable=False, unique=True)

    # Relation avec SousCategorie
    sous_categories = relationship("SousCategorie", back_populates="categorie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Categorie(id={self.idcategorie}, nom='{self.nomcategorie}')>"


class SousCategorie(Base):
    """
    Modèle pour la table 'sous_categorie'
    Représente une sous-catégorie (Courses, Restaurant, etc.)
    """
    __tablename__ = "sous_categorie"

    idsouscategorie = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nomsouscategorie = Column(String(50), nullable=False)
    idcategorie = Column(Integer, ForeignKey('categorie.idcategorie', ondelete='CASCADE'), nullable=False)

    # Relations
    categorie = relationship("Categorie", back_populates="sous_categories")
    operations = relationship("Operation", back_populates="sous_categorie")

    def __repr__(self):
        return f"<SousCategorie(id={self.idsouscategorie}, nom='{self.nomsouscategorie}', categorie_id={self.idcategorie})>"


class Operation(Base):
    """
    Modèle pour la table 'operation' (anciennement 'transaction')
    Représente une opération financière
    """
    __tablename__ = "operation"

    idoperation = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    montant = Column(Numeric(10, 2), nullable=False)
    idcompte = Column(Integer, ForeignKey('compte.idcompte', ondelete='RESTRICT'), nullable=False)
    idtype = Column(Integer, ForeignKey('type.idtype', ondelete='RESTRICT'), nullable=False)
    idsouscategorie = Column(Integer, ForeignKey('sous_categorie.idsouscategorie', ondelete='SET NULL'), nullable=True)

    # Relations
    compte = relationship("Compte", back_populates="operations")
    type_operation = relationship("Type", back_populates="operations")
    sous_categorie = relationship("SousCategorie", back_populates="operations")

    def __repr__(self):
        return f"<Operation(id={self.idoperation}, montant={self.montant}, type={self.idtype}, description='{self.description}')>"
