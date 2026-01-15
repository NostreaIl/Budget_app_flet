# Guide de mise à jour de la base de données

## Nouveau schéma

Le schéma a été mis à jour avec les changements suivants:

### Changements principaux

1. **Table OPERATION** (anciennement TRANSACTION)
   - Renommée pour plus de clarté
   - Nouvelle colonne `nomSousCategorie` pour lier aux sous-catégories

2. **Tables CATEGORIE et SOUS_CATEGORIE séparées**
   - `CATEGORIE`: Catégories principales (Alimentation, Transport, etc.)
   - `SOUS_CATEGORIE`: Sous-catégories liées aux catégories (Courses, Restaurant, etc.)
   - Utilise des noms (VARCHAR) comme clés primaires au lieu d'IDs

3. **Suppression de la table APPARTIENT_A**
   - La relation many-to-many entre catégories et comptes a été supprimée
   - Les opérations sont maintenant directement liées aux sous-catégories

## Comment réinitialiser la base de données

### Étape 1: Vérifier votre fichier .env

Assurez-vous que votre fichier `.env` contient les bonnes informations de connexion:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Budget_app
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

### Étape 2: Lancer le script de réinitialisation

```bash
cd /home/user/Budget_app_flet
python scripts/reset_database.py
```

Le script va:
1. Supprimer toutes les tables existantes
2. Recréer les tables avec le nouveau schéma
3. Insérer les données par défaut (types, catégories, sous-catégories)

### Étape 3: Tester le nouveau schéma

```bash
python scripts/test_new_schema.py
```

Ce script vérifie que:
- Toutes les tables sont créées correctement
- Les relations fonctionnent
- Les opérations CRUD sont possibles

## Structure du nouveau schéma

```
COMPTE (1) ----< (N) OPERATION
TYPE (1) ----< (N) OPERATION
CATEGORIE (1) ----< (N) SOUS_CATEGORIE
SOUS_CATEGORIE (1) ----< (N) OPERATION
```

## Fichiers importants

- `database/schema.sql` - Définition complète du schéma
- `backend/models.py` - Modèles SQLAlchemy mis à jour
- `scripts/reset_database.py` - Script de réinitialisation
- `scripts/test_new_schema.py` - Tests du nouveau schéma

## Notes

- Les opérations peuvent avoir une sous-catégorie optionnelle
- Les types par défaut sont: `depense`, `revenu`, `transfert`
- Les catégories et sous-catégories par défaut sont définies dans `schema.sql`
