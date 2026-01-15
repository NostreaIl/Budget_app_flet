# Nouvelle Structure du Projet Budget App

## 📁 Structure Proposée

```
Budget_app_flet/
├── src/
│   ├── backend/                    # API FastAPI (Backend)
│   │   ├── __init__.py
│   │   ├── main.py                # Point d'entrée FastAPI
│   │   ├── config.py              # Configuration
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py     # Connexion DB
│   │   │   ├── models.py         # Modèles SQLAlchemy
│   │   │   └── schema.sql        # Schéma SQL
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py   # Dépendances FastAPI
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── operations.py
│   │   │   │   ├── comptes.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── sous_categories.py
│   │   │   │   └── types.py
│   │   │   └── schemas/
│   │   │       ├── __init__.py
│   │   │       ├── operation.py
│   │   │       ├── compte.py
│   │   │       ├── categorie.py
│   │   │       └── type.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── crud.py           # Opérations CRUD
│   │       └── statistics.py     # Statistiques
│   │
│   └── frontend/                   # Application Flet (Frontend)
│       ├── __init__.py
│       ├── main.py               # Point d'entrée Flet
│       ├── config.py             # Configuration frontend
│       ├── app.py                # Application principale
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── dashboard.py
│       │   ├── transactions.py
│       │   ├── analytics.py
│       │   ├── categories.py
│       │   ├── recurring.py
│       │   └── settings.py
│       ├── components/
│       │   ├── __init__.py
│       │   ├── transaction_list.py
│       │   ├── stat_card.py
│       │   ├── categories_management.py
│       │   └── charts/
│       │       ├── __init__.py
│       │       ├── base.py
│       │       ├── pie_chart.py
│       │       ├── factory.py
│       │       └── theme.py
│       ├── dialogs/
│       │   ├── __init__.py
│       │   ├── add_category.py
│       │   ├── add_recurring.py
│       │   ├── category_settings.py
│       │   ├── import_export.py
│       │   ├── maintenance.py
│       │   ├── recurring_templates.py
│       │   └── set_budget.py
│       ├── theme/
│       │   ├── __init__.py
│       │   ├── colors.py
│       │   └── styles.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── api_client.py     # Client API pour communiquer avec le backend
│       └── models/
│           ├── __init__.py
│           ├── transaction.py
│           ├── category.py
│           ├── budget_manager.py
│           └── recurring_manager.py
│
├── tests/                          # Tests
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_crud.py
│   └── frontend/
│       ├── __init__.py
│       └── test_ui.py
│
├── scripts/                        # Scripts utilitaires
│   ├── __init__.py
│   ├── reset_database.py
│   ├── test_new_schema.py
│   └── test_api.py
│
├── docs/                          # Documentation
│   ├── API.md
│   ├── DATABASE.md
│   └── SETUP.md
│
├── .env.example                   # Exemple de configuration
├── .gitignore
├── requirements.txt               # Dépendances Python
├── README.md
└── run_backend.py                 # Script pour lancer le backend
└── run_frontend.py                # Script pour lancer le frontend
```

## 🎯 Avantages de cette structure

### 1. **Séparation claire Backend/Frontend**
- `src/backend/` - Tout le code API FastAPI
- `src/frontend/` - Tout le code interface Flet
- Communication via API REST uniquement

### 2. **Organisation modulaire**
- **Backend**: routes, schemas, services séparés
- **Frontend**: pages, components, dialogs séparés
- Facile à naviguer et maintenir

### 3. **Respect des conventions**
- Structure inspirée de projets Python professionnels
- Séparation des responsabilités
- Facilite les tests unitaires

### 4. **Scalabilité**
- Facile d'ajouter de nouvelles routes API
- Facile d'ajouter de nouvelles pages UI
- Code réutilisable et modulaire

## 📝 Changements principaux

### Actuellement
```
Budget_app_flet/
├── backend/          # API (mélangé)
├── src/              # Code app (confus)
├── ui/               # Composants UI (séparé)
├── main.py           # À la racine
└── scripts/          # Scripts
```

### Nouvelle structure
```
Budget_app_flet/
├── src/
│   ├── backend/      # TOUT le backend ici
│   └── frontend/     # TOUT le frontend ici
├── tests/            # Tests organisés
├── scripts/          # Scripts utilitaires
└── docs/             # Documentation
```

## 🚀 Migration

La migration sera effectuée en plusieurs étapes:

1. ✅ Créer la nouvelle structure de dossiers
2. ✅ Déplacer les fichiers backend
3. ✅ Déplacer les fichiers frontend
4. ✅ Mettre à jour tous les imports
5. ✅ Créer les nouveaux points d'entrée
6. ✅ Tester que tout fonctionne

## 📌 Points d'entrée

### Backend API
```bash
python run_backend.py
# ou
python -m src.backend.main
```

### Frontend Flet
```bash
python run_frontend.py
# ou
python -m src.frontend.main
```

## 🔗 Communication

Le frontend communique avec le backend uniquement via:
- `src/frontend/services/api_client.py`
- Appels HTTP REST vers l'API
- Pas de dépendance directe aux modèles backend
