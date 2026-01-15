"""
Script de test rapide pour vérifier que l'API FastAPI fonctionne avec le nouveau schéma
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backend.database.connection import test_connection
from src.backend.database import models


def test_models_import():
    """Teste que les modèles sont correctement importés"""
    print("\n1️⃣  Test d'import des modèles...")

    try:
        # Vérifier que tous les modèles sont accessibles
        assert hasattr(models, 'Operation'), "Modèle Operation manquant"
        assert hasattr(models, 'Compte'), "Modèle Compte manquant"
        assert hasattr(models, 'Categorie'), "Modèle Categorie manquant"
        assert hasattr(models, 'SousCategorie'), "Modèle SousCategorie manquant"
        assert hasattr(models, 'Type'), "Modèle Type manquant"

        print("   ✓ Tous les modèles sont correctement importés")
        return True
    except AssertionError as e:
        print(f"   ❌ Erreur: {e}")
        return False


def test_database_connection():
    """Teste la connexion à la base de données"""
    print("\n2️⃣  Test de connexion à la base de données...")

    if test_connection():
        print("   ✓ Connexion à la base de données réussie")
        return True
    else:
        print("   ❌ Impossible de se connecter à la base de données")
        return False


def test_api_imports():
    """Teste que tous les imports API sont corrects"""
    print("\n3️⃣  Test des imports API...")

    try:
        from src.backend.services import crud
        from src.backend.api import schemas
        from src.backend.main import app

        # Vérifier que les nouveaux schémas existent
        assert hasattr(schemas, 'OperationCreate'), "Schema OperationCreate manquant"
        assert hasattr(schemas, 'OperationResponse'), "Schema OperationResponse manquant"
        assert hasattr(schemas, 'SousCategorieCreate'), "Schema SousCategorieCreate manquant"
        assert hasattr(schemas, 'SousCategorieResponse'), "Schema SousCategorieResponse manquant"

        # Vérifier les fonctions CRUD
        assert hasattr(crud, 'get_operation'), "Fonction get_operation manquante"
        assert hasattr(crud, 'get_sous_categorie'), "Fonction get_sous_categorie manquante"
        assert hasattr(crud, 'create_operation'), "Fonction create_operation manquante"

        # Vérifier que l'app FastAPI est initialisée
        assert app is not None, "App FastAPI non initialisée"

        print("   ✓ Tous les imports API sont corrects")
        return True
    except (ImportError, AssertionError) as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_attributes():
    """Teste que les modèles ont les bons attributs"""
    print("\n4️⃣  Test des attributs des modèles...")

    try:
        # Tester le modèle Operation
        operation_attrs = ['idtransaction', 'date', 'description', 'montant',
                          'idcompte', 'idtype', 'nomsouscategorie']
        for attr in operation_attrs:
            assert hasattr(models.Operation, attr), f"Attribut {attr} manquant dans Operation"

        # Tester le modèle Categorie
        categorie_attrs = ['nomcategorie', 'sous_categories']
        for attr in categorie_attrs:
            assert hasattr(models.Categorie, attr), f"Attribut {attr} manquant dans Categorie"

        # Tester le modèle SousCategorie
        sous_cat_attrs = ['nomsouscategorie', 'nomcategorie', 'categorie', 'operations']
        for attr in sous_cat_attrs:
            assert hasattr(models.SousCategorie, attr), f"Attribut {attr} manquant dans SousCategorie"

        print("   ✓ Tous les attributs des modèles sont corrects")
        return True
    except AssertionError as e:
        print(f"   ❌ Erreur: {e}")
        return False


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🧪 TEST DE L'API AVEC LE NOUVEAU SCHÉMA")
    print("=" * 60)

    results = []

    # Exécuter les tests
    results.append(("Import des modèles", test_models_import()))
    results.append(("Connexion BDD", test_database_connection()))
    results.append(("Imports API", test_api_imports()))
    results.append(("Attributs des modèles", test_model_attributes()))

    # Afficher le résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")

    print("\n" + "=" * 60)
    if passed == total:
        print(f"✅ TOUS LES TESTS SONT PASSÉS ({passed}/{total})")
        print("=" * 60)
        print("\n💡 Prochaines étapes:")
        print("   1. Lancez le serveur FastAPI: python backend/main.py")
        print("   2. Testez les endpoints: http://localhost:8000/docs")
        print("   3. Vérifiez les opérations CRUD avec la nouvelle structure")
        return 0
    else:
        print(f"⚠️  CERTAINS TESTS ONT ÉCHOUÉ ({passed}/{total})")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
