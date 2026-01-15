# Changelog API - Mise à jour du schéma v2.0.0

## Résumé des changements

L'API a été mise à jour pour supporter le nouveau schéma de base de données avec les tables séparées `CATEGORIE` et `SOUS_CATEGORIE`, et le renommage de `TRANSACTION` en `OPERATION`.

## Changements majeurs

### 1. Nouveaux endpoints - Operations

Les opérations remplacent les transactions (avec rétro-compatibilité):

```
GET    /api/operations              - Liste toutes les opérations
GET    /api/operations/{id}         - Détails d'une opération
POST   /api/operations              - Crée une nouvelle opération
PUT    /api/operations/{id}         - Met à jour une opération
DELETE /api/operations/{id}         - Supprime une opération
```

**Nouveau champ**: `nomsouscategorie` (optionnel) pour lier à une sous-catégorie

### 2. Nouveaux endpoints - Sous-catégories

```
GET    /api/sous-categories                         - Liste toutes les sous-catégories
GET    /api/sous-categories/{nom}                   - Détails d'une sous-catégorie
GET    /api/sous-categories/{nom}/operations        - Opérations d'une sous-catégorie
POST   /api/sous-categories                         - Crée une sous-catégorie
PUT    /api/sous-categories/{nom}                   - Met à jour une sous-catégorie
DELETE /api/sous-categories/{nom}                   - Supprime une sous-catégorie
```

### 3. Endpoints Catégories modifiés

**BREAKING CHANGE**: Les catégories utilisent maintenant leur nom comme identifiant au lieu d'un ID:

```
GET    /api/categories/{nom_categorie}                    - Détails (était /{id})
GET    /api/categories/{nom_categorie}/sous-categories    - Sous-catégories d'une catégorie
PUT    /api/categories/{nom_categorie}                    - Met à jour (était /{id})
DELETE /api/categories/{nom_categorie}                    - Supprime (était /{id})
```

### 4. Rétro-compatibilité

Les anciens endpoints `/api/transactions` continuent de fonctionner:

```
GET    /api/transactions              - Alias vers /api/operations
POST   /api/transactions              - Alias vers /api/operations
etc.
```

## Nouveaux schémas Pydantic

### OperationCreate
```python
{
  "date": "2024-01-15",
  "description": "Achat supermarché",
  "montant": -50.00,
  "idcompte": 1,
  "idtype": 1,
  "nomsouscategorie": "Courses"  # NOUVEAU - optionnel
}
```

### SousCategorieCreate
```python
{
  "nomsouscategorie": "Courses",
  "nomcategorie": "Alimentation"
}
```

### CategorieCreate
```python
{
  "nomcategorie": "Alimentation"  # Plus d'idcategorie_enfant
}
```

## Migration de votre code client

### Avant (ancien schéma)
```python
# Créer une transaction
transaction = {
    "date": "2024-01-15",
    "description": "Achat",
    "montant": -50.00,
    "idcompte": 1,
    "idtype": 1
}
response = requests.post("http://localhost:8000/api/transactions", json=transaction)
```

### Après (nouveau schéma)
```python
# Créer une opération avec sous-catégorie
operation = {
    "date": "2024-01-15",
    "description": "Achat",
    "montant": -50.00,
    "idcompte": 1,
    "idtype": 1,
    "nomsouscategorie": "Courses"  # Nouveau champ optionnel
}
response = requests.post("http://localhost:8000/api/operations", json=operation)
```

## Tester l'API

### 1. Lancer le serveur FastAPI

```bash
cd /home/user/Budget_app_flet
python backend/main.py
```

### 2. Accéder à la documentation interactive

Ouvrez votre navigateur: `http://localhost:8000/docs`

Vous verrez tous les nouveaux endpoints avec la possibilité de les tester directement.

### 3. Tester les endpoints

**Récupérer toutes les catégories:**
```bash
curl http://localhost:8000/api/categories
```

**Récupérer les sous-catégories d'une catégorie:**
```bash
curl http://localhost:8000/api/categories/Alimentation/sous-categories
```

**Créer une opération:**
```bash
curl -X POST http://localhost:8000/api/operations \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-15",
    "description": "Achat supermarché",
    "montant": -50.00,
    "idcompte": 1,
    "idtype": 1,
    "nomsouscategorie": "Courses"
  }'
```

## Statistiques API

Le endpoint `/api/stats` a été mis à jour pour inclure les sous-catégories:

```json
{
  "total_operations": 10,
  "total_comptes": 2,
  "total_categories": 8,
  "total_sous_categories": 15,  // NOUVEAU
  "total_types": 3,
  "solde_total": 1000.00
}
```

## Notes importantes

1. **Catégories**: Identifiées par leur nom (VARCHAR) au lieu d'un ID (INTEGER)
2. **Sous-catégories**: Nouvelle table liée aux catégories
3. **Operations**: Peuvent avoir une sous-catégorie optionnelle
4. **Rétro-compatibilité**: Ancien code utilisant `/api/transactions` continue de fonctionner

## Prochaines étapes

1. Mettre à jour votre frontend Flet pour utiliser les nouveaux endpoints
2. Adapter les appels API pour utiliser `nomsouscategorie` au lieu de l'ancienne structure
3. Tester les nouvelles fonctionnalités avec la documentation interactive

## Version

- **API Version**: 2.0.0
- **Date**: 2026-01-15
- **Schéma**: Operation + Categorie + SousCategorie
