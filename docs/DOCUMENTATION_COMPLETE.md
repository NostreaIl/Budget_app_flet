# Documentation Complète - Budget App Flet

> **Version**: 2.0.0
> **Architecture**: FastAPI (Backend) + Flet (Frontend) + PostgreSQL (Database)
> **Date de mise à jour**: Janvier 2026

---

## Table des Matières

1. [Vue d'Ensemble du Projet](#1-vue-densemble-du-projet)
2. [Architecture Générale](#2-architecture-générale)
3. [Backend - Documentation Détaillée](#3-backend---documentation-détaillée)
4. [Modèles de Données Métier](#4-modèles-de-données-métier)
5. [Frontend - Documentation](#5-frontend---documentation)
6. [Flux de Données](#6-flux-de-données)
7. [Configuration et Déploiement](#7-configuration-et-déploiement)

---

## 1. Vue d'Ensemble du Projet

### 1.1 Qu'est-ce que Budget App ?

Budget App est une application de gestion budgétaire personnelle permettant de :
- **Suivre les transactions** (dépenses et revenus)
- **Gérer les comptes bancaires** multiples
- **Organiser par catégories** et sous-catégories
- **Analyser les dépenses** via des graphiques
- **Définir des budgets** par catégorie
- **Automatiser** les transactions récurrentes

### 1.2 Stack Technique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Backend API | **FastAPI** | Serveur REST API |
| Base de données | **PostgreSQL** | Stockage persistant |
| ORM | **SQLAlchemy** | Mapping objet-relationnel |
| Validation | **Pydantic** | Schémas de validation |
| Frontend | **Flet** | Interface utilisateur |
| Thème | **DA 2025** | Design system personnalisé |

### 1.3 Structure des Dossiers

```
Budget_app_flet/
├── src/
│   ├── backend/              # API REST FastAPI
│   │   ├── api/
│   │   │   ├── routes/       # Endpoints (non utilisé actuellement)
│   │   │   └── schemas/      # Schémas Pydantic
│   │   ├── database/
│   │   │   ├── connection.py # Connexion PostgreSQL
│   │   │   └── models.py     # Modèles SQLAlchemy
│   │   ├── services/
│   │   │   └── crud.py       # Opérations CRUD
│   │   ├── main.py           # Application FastAPI
│   │   └── config.py         # Configuration
│   │
│   ├── frontend/             # Interface Flet
│   │   ├── pages/            # Pages de l'application
│   │   ├── dialogs/          # Fenêtres modales
│   │   ├── components/       # Composants réutilisables
│   │   ├── theme/            # Couleurs et styles
│   │   └── services/         # Client API
│   │
│   ├── models/               # Modèles métier Python
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── budget_manager.py
│   │   └── recurring_manager.py
│   │
│   └── app.py                # Application principale
│
├── docs/                     # Documentation
├── tests/                    # Tests unitaires
├── scripts/                  # Scripts utilitaires
├── run_backend.py            # Lanceur backend
├── run_frontend.py           # Lanceur frontend
└── requirements.txt          # Dépendances Python
```

---

## 2. Architecture Générale

### 2.1 Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Flet)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Dashboard  │  │Transactions │  │ Categories  │  │  Settings  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘ │
│         │                │                │                │        │
│         └────────────────┴────────────────┴────────────────┘        │
│                                   │                                  │
│                          ┌───────▼───────┐                          │
│                          │  API Client   │                          │
│                          │ (api_client)  │                          │
│                          └───────┬───────┘                          │
└──────────────────────────────────┼──────────────────────────────────┘
                                   │ HTTP REST
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          BACKEND (FastAPI)                          │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      main.py (Endpoints)                     │   │
│  │  /api/operations  /api/comptes  /api/categories  /api/types │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                    │
│  ┌─────────────────────────────▼───────────────────────────────┐   │
│  │                    services/crud.py                          │   │
│  │         (Logique métier et opérations CRUD)                  │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                    │
│  ┌─────────────────────────────▼───────────────────────────────┐   │
│  │                   database/models.py                         │   │
│  │              (Modèles SQLAlchemy ORM)                        │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                    │
│  ┌─────────────────────────────▼───────────────────────────────┐   │
│  │                 database/connection.py                       │   │
│  │              (Connexion et sessions DB)                      │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
└──────────────────────────────────┼──────────────────────────────────┘
                                   │ SQL
                                   ▼
                    ┌──────────────────────────┐
                    │      PostgreSQL          │
                    │   (Base de données)      │
                    └──────────────────────────┘
```

### 2.2 Principe de Séparation

L'application suit le principe de **séparation des responsabilités** :

1. **Frontend** : Uniquement l'affichage et l'interaction utilisateur
2. **Backend** : Logique métier, validation, persistance
3. **Database** : Stockage des données

Toute communication entre Frontend et Backend passe par des **appels HTTP REST**.

---

## 3. Backend - Documentation Détaillée

Le backend est le cœur de l'application. Il gère toute la logique métier et la persistance des données.

---

### 3.1 Configuration (`src/backend/config.py`)

**Rôle** : Centralise toutes les configurations du backend.

```python
# Variables d'environnement chargées depuis .env
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),      # Hôte PostgreSQL
    "port": int(os.getenv("DB_PORT", "5432")),      # Port (défaut: 5432)
    "database": os.getenv("DB_NAME", "Budget_app"), # Nom de la BDD
    "user": os.getenv("DB_USER", "postgres"),       # Utilisateur
    "password": os.getenv("DB_PASSWORD", ""),       # Mot de passe
}

# URL de connexion construite automatiquement
DATABASE_URL = "postgresql://user:password@host:port/database"

# Métadonnées de l'API
API_VERSION = "2.0.0"
API_TITLE = "Budget API"
API_DESCRIPTION = "API REST pour gérer les opérations budgétaires"

# CORS - Origines autorisées (à restreindre en production)
CORS_ORIGINS = ["*"]
```

**Comment ça marche** :
1. Au démarrage, `load_dotenv()` charge le fichier `.env`
2. Les variables sont lues avec `os.getenv()` avec des valeurs par défaut
3. L'URL de connexion PostgreSQL est construite automatiquement
4. Ces valeurs sont importées par les autres modules

---

### 3.2 Connexion Base de Données (`src/backend/database/connection.py`)

**Rôle** : Établit et gère la connexion à PostgreSQL via SQLAlchemy.

#### 3.2.1 Composants Principaux

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. MOTEUR DE CONNEXION
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifie que la connexion est vivante
    echo=False           # Pas de logs SQL (True pour debug)
)

# 2. FABRIQUE DE SESSIONS
SessionLocal = sessionmaker(
    autocommit=False,    # Commit manuel requis
    autoflush=False,     # Flush manuel requis
    bind=engine          # Lié au moteur
)

# 3. CLASSE DE BASE POUR LES MODÈLES
Base = declarative_base()
```

#### 3.2.2 Fonction `get_db()`

```python
def get_db():
    """
    Générateur de session pour injection de dépendance FastAPI.

    Utilisation dans un endpoint:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()  # Crée une nouvelle session
    try:
        yield db         # Fournit la session à l'endpoint
    finally:
        db.close()       # Ferme la session après utilisation
```

**Pourquoi ce pattern ?**
- Chaque requête HTTP obtient sa propre session
- La session est automatiquement fermée après la requête
- Évite les fuites de connexions

#### 3.2.3 Fonction `test_connection()`

```python
def test_connection() -> bool:
    """
    Teste si la connexion à la base de données fonctionne.

    Returns:
        True si connexion OK, False sinon
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # Requête simple de test
        db.close()
        return True
    except Exception:
        return False
```

---

### 3.3 Modèles SQLAlchemy (`src/backend/database/models.py`)

**Rôle** : Définit la structure des tables et leurs relations via l'ORM SQLAlchemy.

#### 3.3.1 Schéma de la Base de Données

```
┌─────────────────┐       ┌─────────────────────┐       ┌─────────────────┐
│      Type       │       │      Operation      │       │     Compte      │
├─────────────────┤       ├─────────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────│ idtype (FK)         │       │ id (PK)         │
│ nom             │       │ id (PK)             │──────►│ nom             │
│ description     │       │ date                │       │ solde           │
└─────────────────┘       │ description         │       │ type_compte     │
                          │ montant             │       │ description     │
┌─────────────────┐       │ idcompte (FK)       │       └─────────────────┘
│    Categorie    │       │ nom_sous_categorie  │
├─────────────────┤       │ (FK)                │
│ nom (PK)        │◄──┐   └─────────────────────┘
│ description     │   │
│ icone           │   │   ┌─────────────────────┐
│ couleur         │   │   │   SousCategorie     │
└─────────────────┘   │   ├─────────────────────┤
                      └───│ nom_categorie (FK)  │
                          │ nom (PK)            │
                          │ description         │
                          │ icone               │
                          │ couleur             │
                          │ budget_mensuel      │
                          └─────────────────────┘
```

#### 3.3.2 Modèle `Type`

```python
class Type(Base):
    """
    Types d'opérations financières.

    Exemples: 'depense', 'revenu', 'transfert'
    """
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))

    # Relation: Un type peut avoir plusieurs opérations
    operations = relationship("Operation", back_populates="type_operation")
```

**Explication** :
- `__tablename__` : Nom de la table dans PostgreSQL
- `primary_key=True` : Clé primaire auto-incrémentée
- `unique=True` : Pas de doublons (ex: un seul type "depense")
- `relationship` : Crée un lien ORM avec les opérations

#### 3.3.3 Modèle `Compte`

```python
class Compte(Base):
    """
    Comptes bancaires de l'utilisateur.

    Exemples: 'Compte Courant', 'Livret A', 'PEL'
    """
    __tablename__ = "comptes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, nullable=False)
    solde = Column(Float, default=0.0)           # Solde actuel
    type_compte = Column(String(50))             # 'courant', 'epargne', etc.
    description = Column(String(200))

    # Relation: Un compte peut avoir plusieurs opérations
    operations = relationship(
        "Operation",
        back_populates="compte",
        cascade="all, delete-orphan"  # Supprime les opérations si compte supprimé
    )
```

**Cascade expliqué** :
- `cascade="all, delete-orphan"` signifie que si on supprime un compte, toutes ses opérations sont aussi supprimées automatiquement

#### 3.3.4 Modèle `Categorie`

```python
class Categorie(Base):
    """
    Catégories principales de dépenses/revenus.

    Exemples: 'Alimentation', 'Transport', 'Loisirs'

    Note: La clé primaire est le NOM, pas un ID.
    Cela permet des requêtes plus naturelles.
    """
    __tablename__ = "categories"

    nom = Column(String(100), primary_key=True)  # Clé primaire = nom
    description = Column(String(200))
    icone = Column(String(50))                   # Nom de l'icône
    couleur = Column(String(20))                 # Code couleur hex

    # Relation: Une catégorie contient plusieurs sous-catégories
    sous_categories = relationship(
        "SousCategorie",
        back_populates="categorie",
        cascade="all, delete-orphan"
    )
```

**Pourquoi le nom comme clé primaire ?**
- Plus intuitif pour les requêtes : `/api/categories/Alimentation`
- Évite les JOINs inutiles pour afficher le nom
- Le nom doit être unique de toute façon

#### 3.3.5 Modèle `SousCategorie`

```python
class SousCategorie(Base):
    """
    Sous-catégories pour classification fine.

    Exemple: Catégorie 'Alimentation' → Sous-catégories:
        - 'Courses', 'Restaurant', 'Livraison'
    """
    __tablename__ = "sous_categories"

    nom = Column(String(100), primary_key=True)  # Clé primaire = nom
    nom_categorie = Column(
        String(100),
        ForeignKey("categories.nom", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    description = Column(String(200))
    icone = Column(String(50))
    couleur = Column(String(20))
    budget_mensuel = Column(Float, default=0.0)  # Budget alloué par mois

    # Relations
    categorie = relationship("Categorie", back_populates="sous_categories")
    operations = relationship("Operation", back_populates="sous_categorie")
```

**Clés étrangères expliquées** :
- `ForeignKey("categories.nom")` : Référence la colonne `nom` de la table `categories`
- `onupdate="CASCADE"` : Si le nom de la catégorie change, met à jour automatiquement
- `ondelete="CASCADE"` : Si la catégorie est supprimée, supprime les sous-catégories

#### 3.3.6 Modèle `Operation`

```python
class Operation(Base):
    """
    Opérations financières (transactions).

    C'est l'entité CENTRALE de l'application.
    Chaque mouvement d'argent est une opération.
    """
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)          # Date de l'opération
    description = Column(String(200))            # Description libre
    montant = Column(Float, nullable=False)      # Montant (positif ou négatif)

    # Clés étrangères
    idtype = Column(Integer, ForeignKey("types.id"), nullable=False)
    idcompte = Column(Integer, ForeignKey("comptes.id"), nullable=False)
    nom_sous_categorie = Column(
        String(100),
        ForeignKey("sous_categories.nom"),
        nullable=True  # Peut être NULL si pas de catégorie
    )

    # Relations ORM (pour accès facile aux objets liés)
    type_operation = relationship("Type", back_populates="operations")
    compte = relationship("Compte", back_populates="operations")
    sous_categorie = relationship("SousCategorie", back_populates="operations")
```

**Comprendre les relations** :
```python
# Exemple d'utilisation dans le code:
operation = db.query(Operation).first()

# Accès direct aux objets liés (grâce aux relationships)
print(operation.type_operation.nom)      # "depense"
print(operation.compte.nom)              # "Compte Courant"
print(operation.sous_categorie.nom)      # "Courses"
print(operation.sous_categorie.categorie.nom)  # "Alimentation"
```

---

### 3.4 Schémas Pydantic (`src/backend/api/schemas/__init__.py`)

**Rôle** : Valider les données entrantes et formater les données sortantes de l'API.

#### 3.4.1 Pourquoi Pydantic ?

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Client HTTP     │     │   Pydantic       │     │   SQLAlchemy     │
│  (JSON)          │────►│   Schema         │────►│   Model          │
│                  │     │   (Validation)   │     │   (Database)     │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
   Données brutes         Données validées          Données persistées
   (peut être faux)       (format garanti)          (en BDD)
```

Pydantic assure que :
- Les champs requis sont présents
- Les types sont corrects
- Les contraintes sont respectées

#### 3.4.2 Pattern Base/Create/Update/Response

Pour chaque entité, on définit 4 schémas :

```python
# BASE: Champs communs à tous les schémas
class OperationBase(BaseModel):
    date: date
    description: Optional[str] = None
    montant: float
    idtype: int
    idcompte: int
    nom_sous_categorie: Optional[str] = None

# CREATE: Pour créer (hérite de Base, peut ajouter des champs)
class OperationCreate(OperationBase):
    pass  # Utilise les mêmes champs que Base

# UPDATE: Pour modifier (tous les champs optionnels)
class OperationUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    montant: Optional[float] = None
    idtype: Optional[int] = None
    idcompte: Optional[int] = None
    nom_sous_categorie: Optional[str] = None

# RESPONSE: Pour les réponses (ajoute l'ID généré)
class OperationResponse(OperationBase):
    id: int

    class Config:
        from_attributes = True  # Permet la conversion depuis SQLAlchemy
```

**Pourquoi ce pattern ?**
- **Create** : Tous les champs requis (sans ID, car auto-généré)
- **Update** : Tous optionnels (mise à jour partielle possible)
- **Response** : Inclut l'ID pour identifier l'objet créé

#### 3.4.3 Schémas Enrichis

```python
class OperationWithDetails(OperationResponse):
    """
    Opération avec tous les détails des relations.
    Évite de faire plusieurs appels API.
    """
    type_operation: Optional[TypeResponse] = None
    compte: Optional[CompteResponse] = None
    sous_categorie: Optional[SousCategorieResponse] = None

class CategorieWithSousCategories(CategorieResponse):
    """
    Catégorie avec toutes ses sous-catégories.
    Utile pour afficher l'arbre complet.
    """
    sous_categories: List[SousCategorieResponse] = []
```

#### 3.4.4 Rétrocompatibilité

```python
# Anciens noms (pour code existant)
TransactionCreate = OperationCreate
TransactionUpdate = OperationUpdate
TransactionResponse = OperationResponse
```

L'application utilisait "Transaction" avant d'être renommée en "Operation". Ces alias permettent à l'ancien code de fonctionner.

---

### 3.5 Service CRUD (`src/backend/services/crud.py`)

**Rôle** : Contient toute la logique métier et les opérations de base de données.

#### 3.5.1 Structure du Fichier

```python
# Imports
from sqlalchemy.orm import Session
from ..database.models import Type, Compte, Categorie, SousCategorie, Operation
from ..api.schemas import *

# ═══════════════════════════════════════════════
#              OPÉRATIONS (CRUD)
# ═══════════════════════════════════════════════

def get_operation(db: Session, operation_id: int):
    ...

def get_operations(db: Session, skip: int = 0, limit: int = 100):
    ...

# ... etc pour chaque entité
```

#### 3.5.2 Opérations CRUD - Détail

##### GET (Lecture)

```python
def get_operation(db: Session, operation_id: int) -> Operation | None:
    """
    Récupère une opération par son ID.

    Args:
        db: Session de base de données
        operation_id: ID de l'opération recherchée

    Returns:
        L'objet Operation ou None si non trouvé
    """
    return db.query(Operation).filter(Operation.id == operation_id).first()


def get_operations(
    db: Session,
    skip: int = 0,      # Pagination: nombre à sauter
    limit: int = 100    # Pagination: nombre max à retourner
) -> list[Operation]:
    """
    Récupère toutes les opérations avec pagination.

    Triées par date décroissante (plus récentes en premier).
    """
    return (
        db.query(Operation)
        .order_by(Operation.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
```

##### CREATE (Création)

```python
def create_operation(db: Session, operation: OperationCreate) -> Operation:
    """
    Crée une nouvelle opération.

    Args:
        db: Session de base de données
        operation: Données validées par Pydantic

    Returns:
        L'opération créée avec son ID généré
    """
    # 1. Créer l'objet SQLAlchemy à partir des données Pydantic
    db_operation = Operation(
        date=operation.date,
        description=operation.description,
        montant=operation.montant,
        idtype=operation.idtype,
        idcompte=operation.idcompte,
        nom_sous_categorie=operation.nom_sous_categorie
    )

    # 2. Ajouter à la session (pas encore en BDD)
    db.add(db_operation)

    # 3. Valider la transaction (écriture en BDD)
    db.commit()

    # 4. Rafraîchir pour obtenir l'ID généré
    db.refresh(db_operation)

    return db_operation
```

**Comprendre le cycle de vie** :
```
db.add(obj)     → L'objet est "pending" (en attente)
db.commit()     → Écriture en BDD, transaction validée
db.refresh(obj) → Recharge l'objet depuis la BDD (récupère l'ID auto-généré)
```

##### UPDATE (Modification)

```python
def update_operation(
    db: Session,
    operation_id: int,
    operation_data: OperationUpdate
) -> Operation | None:
    """
    Met à jour une opération existante.

    Seuls les champs fournis sont modifiés (mise à jour partielle).
    """
    # 1. Récupérer l'opération existante
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        return None

    # 2. Convertir en dictionnaire, ignorer les None
    update_data = operation_data.model_dump(exclude_unset=True)

    # 3. Mettre à jour chaque champ fourni
    for field, value in update_data.items():
        setattr(db_operation, field, value)

    # 4. Valider les changements
    db.commit()
    db.refresh(db_operation)

    return db_operation
```

**`exclude_unset=True` expliqué** :
```python
# Si l'utilisateur envoie: {"description": "Nouveau texte"}
# operation_data.model_dump(exclude_unset=True) retourne:
{"description": "Nouveau texte"}  # Seulement les champs fournis

# Sans exclude_unset, on aurait:
{"date": None, "description": "Nouveau texte", "montant": None, ...}
# Ce qui écraserait les valeurs existantes avec None !
```

##### DELETE (Suppression)

```python
def delete_operation(db: Session, operation_id: int) -> bool:
    """
    Supprime une opération.

    Returns:
        True si supprimé, False si non trouvé
    """
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        return False

    db.delete(db_operation)
    db.commit()
    return True
```

#### 3.5.3 Cas Spéciaux

##### Gestion des Catégories (clé primaire = nom)

```python
def update_categorie(
    db: Session,
    nom: str,  # Clé primaire actuelle
    categorie_data: CategorieUpdate
) -> Categorie | None:
    """
    Met à jour une catégorie, y compris son nom.

    Problème: Si on change le nom (= la clé primaire),
    il faut mettre à jour toutes les références.
    """
    db_categorie = get_categorie(db, nom)
    if not db_categorie:
        return None

    update_data = categorie_data.model_dump(exclude_unset=True)

    # CAS SPECIAL: Changement de nom (= changement de clé primaire)
    if "nom" in update_data and update_data["nom"] != nom:
        new_nom = update_data["nom"]

        # 1. Mettre à jour toutes les sous-catégories qui référencent ce nom
        db.query(SousCategorie)\
          .filter(SousCategorie.nom_categorie == nom)\
          .update({"nom_categorie": new_nom})

        # 2. Puis mettre à jour la catégorie elle-même
        for field, value in update_data.items():
            setattr(db_categorie, field, value)
    else:
        # Cas normal: pas de changement de nom
        for field, value in update_data.items():
            setattr(db_categorie, field, value)

    db.commit()
    db.refresh(db_categorie)
    return db_categorie
```

##### Fonctions Statistiques

```python
def get_total_solde(db: Session) -> float:
    """
    Calcule le solde total de tous les comptes.

    Utilise func.sum() de SQLAlchemy pour faire
    le calcul côté base de données (plus efficace).
    """
    from sqlalchemy import func
    result = db.query(func.sum(Compte.solde)).scalar()
    return result or 0.0


def get_statistics(db: Session) -> dict:
    """
    Retourne des statistiques globales pour le dashboard.
    """
    from sqlalchemy import func

    # Nombre total d'opérations
    total_operations = db.query(func.count(Operation.id)).scalar() or 0

    # Somme des montants par type
    # ... (requêtes agrégées)

    return {
        "total_operations": total_operations,
        "total_solde": get_total_solde(db),
        "total_depenses": ...,
        "total_revenus": ...,
    }
```

---

### 3.6 Endpoints API (`src/backend/main.py`)

**Rôle** : Définit tous les points d'entrée HTTP de l'API.

#### 3.6.1 Initialisation FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Création de l'application
app = FastAPI(
    title=API_TITLE,           # "Budget API"
    description=API_DESCRIPTION,
    version=API_VERSION         # "2.0.0"
)

# Configuration CORS (Cross-Origin Resource Sharing)
# Permet au frontend (autre origine) d'appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # ["*"] = toutes origines
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Création des tables au démarrage
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
```

#### 3.6.2 Structure des Endpoints

##### Pattern Standard

```python
@app.get("/api/operations", response_model=List[OperationResponse])
def list_operations(
    skip: int = 0,                    # Query param: ?skip=10
    limit: int = 100,                 # Query param: ?limit=50
    db: Session = Depends(get_db)     # Injection de dépendance
):
    """
    Liste toutes les opérations avec pagination.

    - **skip**: Nombre d'éléments à sauter (défaut: 0)
    - **limit**: Nombre max d'éléments (défaut: 100)
    """
    return crud.get_operations(db, skip=skip, limit=limit)
```

**Décorateur `@app.get()` expliqué** :
- `"/api/operations"` : URL de l'endpoint
- `response_model=List[OperationResponse]` : Format de la réponse (pour doc et validation)

**`Depends(get_db)` expliqué** :
- FastAPI appelle automatiquement `get_db()`
- La session est injectée dans le paramètre `db`
- Après l'exécution, la session est fermée automatiquement

##### Endpoint avec Paramètre de Chemin

```python
@app.get("/api/operations/{operation_id}", response_model=OperationWithDetails)
def get_operation(
    operation_id: int,                # Paramètre de chemin
    db: Session = Depends(get_db)
):
    """
    Récupère une opération par son ID avec tous les détails.
    """
    db_operation = crud.get_operation(db, operation_id)

    if db_operation is None:
        # Lève une erreur HTTP 404
        raise HTTPException(status_code=404, detail="Opération non trouvée")

    return db_operation
```

##### Endpoint POST (Création)

```python
@app.post("/api/operations", response_model=OperationResponse, status_code=201)
def create_operation(
    operation: OperationCreate,       # Corps de la requête (JSON)
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle opération.

    Le corps de la requête doit contenir:
    - date (YYYY-MM-DD)
    - montant (float)
    - idtype (int)
    - idcompte (int)
    - description (optionnel)
    - nom_sous_categorie (optionnel)
    """
    return crud.create_operation(db, operation)
```

**`status_code=201`** : Code HTTP "Created" (au lieu de 200 par défaut)

##### Endpoint PUT (Modification)

```python
@app.put("/api/operations/{operation_id}", response_model=OperationResponse)
def update_operation(
    operation_id: int,
    operation: OperationUpdate,       # Corps avec champs optionnels
    db: Session = Depends(get_db)
):
    """
    Met à jour une opération existante.

    Seuls les champs fournis dans le corps sont modifiés.
    """
    db_operation = crud.update_operation(db, operation_id, operation)

    if db_operation is None:
        raise HTTPException(status_code=404, detail="Opération non trouvée")

    return db_operation
```

##### Endpoint DELETE (Suppression)

```python
@app.delete("/api/operations/{operation_id}")
def delete_operation(
    operation_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime une opération.

    Returns:
        {"message": "Opération supprimée"} ou erreur 404
    """
    success = crud.delete_operation(db, operation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Opération non trouvée")

    return {"message": "Opération supprimée"}
```

#### 3.6.3 Liste Complète des Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| **Health** |
| GET | `/` | Status de l'API |
| GET | `/health` | Test de connexion BDD |
| GET | `/api/stats` | Statistiques globales |
| **Operations** |
| GET | `/api/operations` | Liste paginée |
| GET | `/api/operations/{id}` | Détails d'une opération |
| POST | `/api/operations` | Créer une opération |
| PUT | `/api/operations/{id}` | Modifier une opération |
| DELETE | `/api/operations/{id}` | Supprimer une opération |
| **Transactions** (alias) |
| GET | `/api/transactions` | Alias de /api/operations |
| GET | `/api/transactions/{id}` | Alias |
| POST | `/api/transactions` | Alias |
| PUT | `/api/transactions/{id}` | Alias |
| DELETE | `/api/transactions/{id}` | Alias |
| **Comptes** |
| GET | `/api/comptes` | Liste des comptes |
| GET | `/api/comptes/{id}` | Détails d'un compte |
| POST | `/api/comptes` | Créer un compte |
| PUT | `/api/comptes/{id}` | Modifier un compte |
| DELETE | `/api/comptes/{id}` | Supprimer un compte |
| GET | `/api/comptes/{id}/operations` | Opérations d'un compte |
| **Categories** |
| GET | `/api/categories` | Liste des catégories |
| GET | `/api/categories/{nom}` | Détails (par nom) |
| POST | `/api/categories` | Créer une catégorie |
| PUT | `/api/categories/{nom}` | Modifier une catégorie |
| DELETE | `/api/categories/{nom}` | Supprimer une catégorie |
| GET | `/api/categories/{nom}/sous-categories` | Sous-catégories |
| **Sous-Categories** |
| GET | `/api/sous-categories` | Liste |
| GET | `/api/sous-categories/{nom}` | Détails |
| POST | `/api/sous-categories` | Créer |
| PUT | `/api/sous-categories/{nom}` | Modifier |
| DELETE | `/api/sous-categories/{nom}` | Supprimer |
| GET | `/api/sous-categories/{nom}/operations` | Opérations liées |
| **Types** |
| GET | `/api/types` | Liste des types |
| GET | `/api/types/{id}` | Par ID |
| GET | `/api/types/nom/{nom}` | Par nom |
| POST | `/api/types` | Créer |
| PUT | `/api/types/{id}` | Modifier |
| DELETE | `/api/types/{id}` | Supprimer |

---

## 4. Modèles de Données Métier

Ces modèles (`src/models/`) représentent la logique métier côté Python, indépendamment de la base de données.

### 4.1 Transaction (`src/models/transaction.py`)

**Rôle** : Représente une transaction avec toute sa logique métier.

```python
class Transaction:
    """
    Modèle métier pour une transaction financière.

    Attributs:
        montant: Montant de la transaction
        description: Description textuelle
        categorie: Catégorie associée
        date_transaction: Date de la transaction
        type_transaction: 'depense' ou 'revenu'
        tags: Liste de tags pour filtrage
        recurrente: Si c'est une transaction récurrente
        frequence_recurrence: 'mensuel', 'hebdomadaire', etc.
    """
```

#### Méthodes Principales

```python
# Gestion des tags
transaction.ajouter_tag("important")
transaction.supprimer_tag("important")
if transaction.has_tag("urgent"):
    ...

# Filtrage temporel
if transaction.est_dans_mois(2025, 1):  # Janvier 2025
    ...
if transaction.est_dans_periode(date_debut, date_fin):
    ...

# Sérialisation
data = transaction.to_dict()     # Vers dictionnaire
json_str = transaction.to_json() # Vers JSON

# Désérialisation
tx = Transaction.from_dict(data)
tx = Transaction.from_json(json_str)

# Clonage
copie = transaction.clone()

# Affichage
print(transaction.montant_affichage)  # "+150,00 €" ou "-50,00 €"
print(transaction.couleur_type)       # Vert pour revenu, rouge pour dépense
```

### 4.2 CategoryBudget (`src/models/category.py`)

**Rôle** : Gère les catégories avec suivi de budget.

```python
class CategoryBudget:
    """
    Catégorie avec gestion de budget.

    Attributs:
        name: Nom de la catégorie
        budget: Budget mensuel alloué
        spent: Montant déjà dépensé
        icon: Icône de la catégorie
        color: Couleur d'affichage
        description: Description
    """
```

#### Propriétés de Statut

```python
# Statuts possibles
category.status  # 'ok', 'warning', 'over', 'inactive'

# Vérifications
category.is_over_budget    # True si dépenses > budget
category.is_near_limit     # True si dépenses > 80% du budget

# Calculs
remaining = category.remaining_budget  # Budget restant
percent = category.progress_bar_value  # 0.0 à 1.0 pour barre de progression
```

#### Méthodes de Budget

```python
# Ajouter une dépense
category.add_spending(50.0)

# Retirer une dépense (annulation)
category.remove_spending(50.0)

# Réinitialiser (nouveau mois)
category.reset_spent()

# Vérifier si on peut dépenser
if category.can_spend(100.0):
    ...

# Montant de dépassement
overspend = category.get_overspend_amount()
```

#### Catégories par Défaut

```python
default_categories = CategoryBudget.create_default_categories()
# Retourne: [Tech, Electronics, Gardening, Housing, Food,
#            Transport, Leisure, Health, Professional, Savings]
```

### 4.3 BudgetManager (`src/models/budget_manager.py`)

**Rôle** : Orchestrateur principal qui combine API et modèles locaux.

```python
class BudgetManager:
    """
    Gestionnaire central du budget.

    Fait le lien entre:
    - L'API backend (données persistantes)
    - Les modèles locaux (logique métier)
    - L'interface utilisateur (Flet)
    """

    def __init__(self):
        self.transactions: list[Transaction] = []
        self.categories_budgets: list[CategoryBudget] = []
        self.api_client = BudgetAPIClient()
```

#### Chargement des Données

```python
async def load_transactions_from_api(self):
    """
    Charge les transactions depuis l'API backend.
    Convertit les réponses JSON en objets Transaction.
    """
    response = await self.api_client.get_operations()
    self.transactions = [Transaction.from_dict(tx) for tx in response]
```

#### Calculs Financiers

```python
# Solde total (revenus - dépenses)
solde = manager.get_solde()

# Totaux par type
revenus = manager.get_revenus_total()
depenses = manager.get_depenses_total()

# Filtrage
tx_alimentation = manager.get_operations_by_category("Alimentation")
tx_janvier = manager.get_transactions_by_month(2025, 1)
```

#### Statistiques

```python
# Résumé mensuel
summary = manager.get_monthly_summary(2025, 1)
# {
#     "revenus": 3000.0,
#     "depenses": 2500.0,
#     "solde": 500.0,
#     "nb_transactions": 45
# }

# Dépenses par catégorie
spending = manager.get_category_spending()
# {
#     "Alimentation": 450.0,
#     "Transport": 150.0,
#     "Loisirs": 200.0,
#     ...
# }

# Statistiques complètes
stats = manager.get_statistics()
```

### 4.4 RecurringManager (`src/models/recurring_manager.py`)

**Rôle** : Gère les transactions récurrentes (en développement).

```python
class RecurringManager:
    """
    Gestionnaire des transactions récurrentes.

    Permet de:
    - Définir des transactions automatiques
    - Les exécuter selon leur fréquence
    - Gérer les templates de récurrence
    """
```

---

## 5. Frontend - Documentation

### 5.1 Thème DA 2025 (`src/frontend/theme/colors.py`)

```python
class COLORS:
    """Design system DA 2025 - Palette de couleurs"""

    # Accents
    ACCENT_PRINCIPAL = "#6B46C1"     # Violet principal
    ACCENT_SECONDAIRE = "#00D9FF"    # Cyan secondaire
    VIOLET_LUMINEUX = "#9F7AEA"      # Violet clair

    # Fonds
    BACKGROUND_PRINCIPAL = "#0D1117"  # Fond principal (très sombre)
    BACKGROUND_SECONDAIRE = "#161B22" # Fond secondaire
    CARTES_COMPOSANTS = "#21262D"     # Fond des cartes

    # Textes
    TEXTE_PRINCIPAL = "#E6EDF3"       # Texte principal (clair)
    TEXTE_SECONDAIRE = "#8B949E"      # Texte secondaire (grisé)

    # États
    SUCCESS_REVENUS = "#3FB950"       # Vert (revenus, succès)
    ERREUR_DEPENSES = "#F85149"       # Rouge (dépenses, erreurs)
    AVERTISSEMENT = "#D29922"         # Orange (avertissements)

    # Autres
    BORDURES = "#30363D"              # Bordures
```

### 5.2 Application Principale (`src/app.py`)

```python
class BudgetApp:
    """Application principale avec navigation"""

    def __init__(self, page: ft.Page, budget_manager: BudgetManager):
        self.page = page
        self.budget_manager = budget_manager
        self.current_page = "dashboard"

    def start(self):
        """Démarre l'application"""
        self._build_interface()  # Construit la navigation
        self._load_dashboard()   # Charge la page initiale
```

#### Navigation

L'application utilise `NavigationRail` avec 6 destinations :

1. **Dashboard** - Vue d'ensemble
2. **Transactions** - Gestion des transactions
3. **Catégories** - Gestion des catégories
4. **Analytics** - Graphiques et analyses
5. **Récurrence** - Transactions automatiques
6. **Paramètres** - Configuration

### 5.3 Client API (`src/frontend/services/api_client.py`)

```python
class BudgetAPIClient:
    """Client HTTP pour communiquer avec le backend"""

    BASE_URL = "http://localhost:8000/api"

    async def get_transactions(self) -> list[dict]:
        """GET /api/transactions"""
        response = await httpx.get(f"{self.BASE_URL}/transactions")
        return response.json()

    async def create_transaction(self, data: dict) -> dict:
        """POST /api/transactions"""
        response = await httpx.post(
            f"{self.BASE_URL}/transactions",
            json=data
        )
        return response.json()

    # ... autres méthodes
```

### 5.4 Pages

| Fichier | Description |
|---------|-------------|
| `dashboard.py` | Vue d'ensemble avec statistiques, graphiques et transactions récentes |
| `transactions.py` | Liste et gestion des transactions |
| `categories.py` | Gestion des catégories et budgets |
| `analytics.py` | Graphiques d'analyse |
| `recurring.py` | Transactions récurrentes |
| `settings.py` | Paramètres de l'application |

### 5.5 Composants Réutilisables

| Fichier | Description |
|---------|-------------|
| `stat_card.py` | Carte de statistique (solde, dépenses, etc.) |
| `transaction_list.py` | Liste de transactions avec filtres |
| `categories_management.py` | Gestionnaire de catégories |
| `charts/pie_chart.py` | Graphique camembert |
| `charts/chart_factory.py` | Fabrique de graphiques |

### 5.6 Dialogues

| Fichier | Description |
|---------|-------------|
| `add_transaction.py` | Ajouter une transaction |
| `edit_transaction.py` | Modifier une transaction |
| `add_category.py` | Ajouter une catégorie |
| `edit_category.py` | Modifier une catégorie |
| `set_budget.py` | Définir un budget |
| `import_export.py` | Import/Export de données |

---

## 6. Flux de Données

### 6.1 Création d'une Transaction

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. UTILISATEUR                                                      │
│    Remplit le formulaire "Nouvelle Transaction"                     │
│    - Date: 2025-01-15                                               │
│    - Montant: -50.00                                                │
│    - Description: "Courses Carrefour"                               │
│    - Compte: "Compte Courant"                                       │
│    - Catégorie: "Alimentation > Courses"                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND (Flet)                                                  │
│    Validation locale + Appel API                                    │
│                                                                     │
│    api_client.create_transaction({                                  │
│        "date": "2025-01-15",                                        │
│        "montant": -50.00,                                           │
│        "description": "Courses Carrefour",                          │
│        "idcompte": 1,                                               │
│        "idtype": 1,                                                 │
│        "nom_sous_categorie": "Courses"                              │
│    })                                                               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP POST /api/operations
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND - ENDPOINT (main.py)                                     │
│                                                                     │
│    @app.post("/api/operations")                                     │
│    def create_operation(operation: OperationCreate, db):            │
│        return crud.create_operation(db, operation)                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. BACKEND - PYDANTIC VALIDATION (schemas)                          │
│                                                                     │
│    OperationCreate valide automatiquement:                          │
│    ✓ date est bien une date                                         │
│    ✓ montant est bien un float                                      │
│    ✓ idcompte est bien un int                                       │
│    ✓ idtype est bien un int                                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. BACKEND - CRUD (services/crud.py)                                │
│                                                                     │
│    def create_operation(db, operation):                             │
│        db_operation = Operation(...)                                │
│        db.add(db_operation)                                         │
│        db.commit()                                                  │
│        db.refresh(db_operation)                                     │
│        return db_operation                                          │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6. DATABASE (PostgreSQL)                                            │
│                                                                     │
│    INSERT INTO operations                                           │
│    (date, montant, description, idcompte, idtype, nom_sous_cat)     │
│    VALUES ('2025-01-15', -50.00, 'Courses Carrefour', 1, 1, ...)   │
│    RETURNING id;  → id = 42                                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 7. RÉPONSE (JSON)                                                   │
│                                                                     │
│    {                                                                │
│        "id": 42,                                                    │
│        "date": "2025-01-15",                                        │
│        "montant": -50.00,                                           │
│        "description": "Courses Carrefour",                          │
│        "idcompte": 1,                                               │
│        "idtype": 1,                                                 │
│        "nom_sous_categorie": "Courses"                              │
│    }                                                                │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 8. FRONTEND - MISE À JOUR UI                                        │
│                                                                     │
│    - Ferme le dialogue                                              │
│    - Ajoute la transaction à la liste                               │
│    - Met à jour les statistiques                                    │
│    - Affiche une notification de succès                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Chargement du Dashboard

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │      │   Backend   │      │  Database   │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │  GET /api/stats    │                    │
       │───────────────────►│                    │
       │                    │  SELECT COUNT(*)   │
       │                    │───────────────────►│
       │                    │◄───────────────────│
       │                    │  SELECT SUM(...)   │
       │                    │───────────────────►│
       │                    │◄───────────────────│
       │◄───────────────────│                    │
       │  {stats JSON}      │                    │
       │                    │                    │
       │  GET /operations   │                    │
       │   ?limit=10        │                    │
       │───────────────────►│                    │
       │                    │  SELECT * LIMIT 10 │
       │                    │───────────────────►│
       │                    │◄───────────────────│
       │◄───────────────────│                    │
       │  [{...}, {...}]    │                    │
       │                    │                    │
       │  Render Dashboard  │                    │
       │                    │                    │
```

---

## 7. Configuration et Déploiement

### 7.1 Variables d'Environnement

Créer un fichier `.env` à la racine :

```env
# Base de données PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Budget_app
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe

# Mode debug
DEBUG=False

# Frontend
API_BASE_URL=http://localhost:8000
```

### 7.2 Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le backend (terminal 1)
python run_backend.py
# → API disponible sur http://localhost:8000
# → Documentation Swagger sur http://localhost:8000/docs

# 3. Lancer le frontend (terminal 2)
python run_frontend.py
# → Application Flet démarre
```

### 7.3 Documentation API Interactive

Accéder à `http://localhost:8000/docs` pour :
- Voir tous les endpoints disponibles
- Tester les requêtes directement
- Voir les schémas de données

---

## Annexes

### A. Commandes SQL Utiles

```sql
-- Voir toutes les opérations avec détails
SELECT o.*, t.nom as type_nom, c.nom as compte_nom, sc.nom as sous_cat
FROM operations o
JOIN types t ON o.idtype = t.id
JOIN comptes c ON o.idcompte = c.id
LEFT JOIN sous_categories sc ON o.nom_sous_categorie = sc.nom;

-- Dépenses par catégorie ce mois
SELECT cat.nom, SUM(o.montant) as total
FROM operations o
JOIN sous_categories sc ON o.nom_sous_categorie = sc.nom
JOIN categories cat ON sc.nom_categorie = cat.nom
WHERE o.montant < 0
  AND DATE_TRUNC('month', o.date) = DATE_TRUNC('month', CURRENT_DATE)
GROUP BY cat.nom
ORDER BY total;

-- Solde total de tous les comptes
SELECT SUM(solde) FROM comptes;
```

### B. Glossaire

| Terme | Définition |
|-------|------------|
| **ORM** | Object-Relational Mapping - Permet de manipuler la BDD avec des objets Python |
| **CRUD** | Create, Read, Update, Delete - Les 4 opérations de base |
| **Endpoint** | Point d'entrée de l'API (URL + méthode HTTP) |
| **Schema** | Structure de validation des données (Pydantic) |
| **Model** | Représentation d'une table en base de données (SQLAlchemy) |
| **Session** | Connexion temporaire à la base de données |
| **Cascade** | Propagation automatique des actions (ex: suppression) |
| **FK** | Foreign Key - Clé étrangère, référence vers une autre table |
| **PK** | Primary Key - Clé primaire, identifiant unique |

---

*Documentation générée pour Budget App Flet v2.0.0*
