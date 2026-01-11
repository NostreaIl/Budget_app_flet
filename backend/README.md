# Backend FastAPI - Budget App

## Architecture

```
backend/
├── __init__.py          # Package Python
├── main.py              # Application FastAPI + Endpoints
├── database.py          # Configuration SQLAlchemy + Connexion PostgreSQL
├── models.py            # Modèles SQLAlchemy (Transaction, Compte, Categorie)
├── schemas.py           # Schémas Pydantic (validation)
└── crud.py              # Opérations CRUD
```

## Installation

1. **Installer les dépendances** :
```bash
pip install -r requirement.txt
```

2. **Configurer la base de données** :
- Copier `.env.example` en `.env`
- Modifier les credentials PostgreSQL dans `.env` :

```env
DB_HOST=localhost        # ou l'IP de ton serveur PostgreSQL
DB_PORT=5432
DB_NAME=Budget_app
DB_USER=postgres
DB_PASSWORD=ton_mot_de_passe
```

3. **Vérifier que PostgreSQL est démarré** :
```bash
# Sur Linux/Mac
sudo systemctl status postgresql

# Sur Windows avec XAMPP/WAMP
# Vérifier dans le panneau de contrôle

# Tester la connexion
psql -U postgres -d Budget_app
```

## Démarrage du serveur

### Option 1 : Depuis le dossier backend
```bash
cd backend
python main.py
```

### Option 2 : Avec uvicorn directement
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3 : En tant que module Python
```bash
python -m uvicorn backend.main:app --reload
```

## Tester la connexion

```bash
python test_connection.py
```

## Endpoints disponibles

### Documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints de base
- `GET /` - Info sur l'API
- `GET /health` - Vérifier la santé de l'API et la connexion DB
- `GET /api/stats` - Statistiques générales

### Transactions
- `GET /api/transactions` - Liste toutes les transactions
- `GET /api/transactions/{id}` - Récupère une transaction
- `POST /api/transactions` - Crée une transaction
- `PUT /api/transactions/{id}` - Met à jour une transaction
- `DELETE /api/transactions/{id}` - Supprime une transaction

### Comptes
- `GET /api/comptes` - Liste tous les comptes
- `GET /api/comptes/{id}` - Récupère un compte
- `GET /api/comptes/{id}/transactions` - Transactions d'un compte
- `POST /api/comptes` - Crée un compte
- `PUT /api/comptes/{id}` - Met à jour un compte
- `DELETE /api/comptes/{id}` - Supprime un compte

### Catégories
- `GET /api/categories` - Liste toutes les catégories
- `GET /api/categories/{id}` - Récupère une catégorie
- `POST /api/categories` - Crée une catégorie
- `PUT /api/categories/{id}` - Met à jour une catégorie
- `DELETE /api/categories/{id}` - Supprime une catégorie

## Exemples d'utilisation

### Créer une transaction (curl)
```bash
curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-01-11",
    "description": "Courses alimentaires",
    "montant": -45.50,
    "idcompte": 1
  }'
```

### Créer une transaction (Python)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/transactions",
    json={
        "date": "2026-01-11",
        "description": "Courses alimentaires",
        "montant": -45.50,
        "idcompte": 1
    }
)
print(response.json())
```

## Structure de la base de données

### Table `transaction`
- `idtransaction` (INT) - Clé primaire
- `date` (VARCHAR) - Date de la transaction
- `description` (TEXT) - Description
- `montant` (NUMERIC) - Montant
- `idcompte` (INT) - Clé étrangère vers `compte`

### Table `compte`
- `idcompte` (INT) - Clé primaire
- `nom` (TEXT) - Nom du compte
- `solde` (NUMERIC) - Solde actuel
- `type` (VARCHAR) - Type de compte

### Table `categorie`
- `idcategorie` (INT) - Clé primaire
- `nom` (TEXT) - Nom de la catégorie
- `idcategorie_enfant` (INT) - Catégorie parent (auto-référence)

### Table `appartient_a`
- `idcategorie` (INT) - Clé étrangère vers `categorie`
- `idcompte` (INT) - Clé étrangère vers `compte`

## Dépannage

### Erreur de connexion PostgreSQL
1. Vérifier que PostgreSQL est démarré
2. Vérifier les credentials dans `.env`
3. Vérifier que le port 5432 n'est pas bloqué par le firewall
4. Tester manuellement : `psql -U postgres -d Budget_app`

### Port 8000 déjà utilisé
```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
uvicorn backend.main:app --port 8001
```

## Notes de développement

- SQLAlchemy 2.0+ avec syntaxe moderne
- Pydantic v2 pour validation
- Les modèles SQLAlchemy reflètent exactement le schéma PostgreSQL existant
- CORS activé pour permettre les appels depuis l'app Flet
- Mode `echo=True` en développement pour voir les requêtes SQL
