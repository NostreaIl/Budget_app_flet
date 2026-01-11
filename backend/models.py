"""
Modèles SQLAlchemy pour la base de données PostgreSQL Budget_app
Correspond aux tables existantes : transaction, compte, categorie, appartient_a
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.database import Base


# Table d'association pour la relation many-to-many entre Categorie et Compte
appartient_a = Table(
    'appartient_a',
    Base.metadata,
    Column('idcategorie', Integer, ForeignKey('categorie.idcategorie'), primary_key=True),
    Column('idcompte', Integer, ForeignKey('compte.idcompte'), primary_key=True)
)


class Transaction(Base):
    """
    Modèle pour la table 'transaction'
    Représente une transaction financière
    """
    __tablename__ = "transaction"

    idtransaction = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(String(50), nullable=False)  # Format: 'character varying(50)'
    description = Column(String, nullable=False)  # Format: 'text'
    montant = Column(Numeric(10, 2), nullable=False)  # Format: numeric(10,2)
    idcompte = Column(Integer, ForeignKey('compte.idcompte'), nullable=False)

    # Relation avec Compte
    compte = relationship("Compte", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.idtransaction}, montant={self.montant}, description='{self.description}')>"


class Compte(Base):
    """
    Modèle pour la table 'compte'
    Représente un compte bancaire
    """
    __tablename__ = "compte"

    idcompte = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String, nullable=False)  # Format: 'text'
    solde = Column(Numeric(10, 2), nullable=False)  # Format: numeric(10,2)
    type = Column(String(50), nullable=False)  # Format: 'character varying(50)'

    # Relations
    transactions = relationship("Transaction", back_populates="compte", cascade="all, delete-orphan")
    categories = relationship("Categorie", secondary=appartient_a, back_populates="comptes")

    def __repr__(self):
        return f"<Compte(id={self.idcompte}, nom='{self.nom}', solde={self.solde}, type='{self.type}')>"


class Categorie(Base):
    """
    Modèle pour la table 'categorie'
    Représente une catégorie de transaction avec hiérarchie (catégorie parent/enfant)
    """
    __tablename__ = "categorie"

    idcategorie = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String, nullable=False)  # Format: 'text'
    idcategorie_enfant = Column(Integer, ForeignKey('categorie.idcategorie'), nullable=True)

    # Auto-référence pour la hiérarchie des catégories
    parent = relationship("Categorie", remote_side=[idcategorie], backref="enfants")

    # Relation many-to-many avec Compte via appartient_a
    comptes = relationship("Compte", secondary=appartient_a, back_populates="categories")

    def __repr__(self):
        return f"<Categorie(id={self.idcategorie}, nom='{self.nom}')>"
