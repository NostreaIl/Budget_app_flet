"""
Script de test pour vérifier le nouveau schéma de base de données
"""
import sys
from pathlib import Path
from datetime import date
from decimal import Decimal

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backend.database.connection import SessionLocal, test_connection
from src.backend.database.models import Type, Compte, Categorie, SousCategorie, Operation


def test_schema():
    """Teste le nouveau schéma avec quelques opérations CRUD"""
    print("\n" + "=" * 60)
    print("🧪 TEST DU NOUVEAU SCHÉMA")
    print("=" * 60)

    if not test_connection():
        print("\n❌ Impossible de se connecter à la base de données.")
        return False

    db = SessionLocal()

    try:
        # 1. Vérifier les types
        print("\n1️⃣  Vérification des TYPES...")
        types = db.query(Type).all()
        print(f"   ✓ {len(types)} types trouvés: {[t.nom for t in types]}")

        # 2. Vérifier les catégories
        print("\n2️⃣  Vérification des CATÉGORIES...")
        categories = db.query(Categorie).all()
        print(f"   ✓ {len(categories)} catégories trouvées:")
        for cat in categories:
            print(f"      - {cat.nomcategorie}")

        # 3. Vérifier les sous-catégories
        print("\n3️⃣  Vérification des SOUS-CATÉGORIES...")
        sous_categories = db.query(SousCategorie).all()
        print(f"   ✓ {len(sous_categories)} sous-catégories trouvées:")
        for sc in sous_categories:
            print(f"      - {sc.nomsouscategorie} ({sc.nomcategorie})")

        # 4. Créer un compte de test
        print("\n4️⃣  Création d'un COMPTE de test...")
        compte_test = Compte(
            nom="Compte Test",
            solde=Decimal("1000.00"),
            type="Test"
        )
        db.add(compte_test)
        db.commit()
        db.refresh(compte_test)
        print(f"   ✓ Compte créé: {compte_test}")

        # 5. Créer une opération de test
        print("\n5️⃣  Création d'une OPÉRATION de test...")

        # Récupérer le type "depense"
        type_depense = db.query(Type).filter(Type.nom == "depense").first()

        # Récupérer une sous-catégorie existante
        sous_cat = db.query(SousCategorie).first()

        if type_depense and sous_cat:
            operation_test = Operation(
                date=date.today(),
                description="Test - Achat de test",
                montant=Decimal("-50.00"),
                idcompte=compte_test.idcompte,
                idtype=type_depense.idtype,
                nomsouscategorie=sous_cat.nomsouscategorie
            )
            db.add(operation_test)
            db.commit()
            db.refresh(operation_test)
            print(f"   ✓ Opération créée: {operation_test}")
            print(f"      - Compte: {operation_test.compte.nom}")
            print(f"      - Type: {operation_test.type_operation.nom}")
            print(f"      - Sous-catégorie: {operation_test.sous_categorie.nomsouscategorie}")
        else:
            print("   ⚠️  Type ou sous-catégorie non trouvés")

        # 6. Tester les relations
        print("\n6️⃣  Test des RELATIONS...")
        compte = db.query(Compte).filter(Compte.nom == "Compte Test").first()
        if compte:
            print(f"   ✓ Compte trouvé: {compte.nom}")
            print(f"   ✓ Nombre d'opérations: {len(compte.operations)}")

            for op in compte.operations:
                print(f"      - {op.description}: {op.montant}€")

        # 7. Nettoyer les données de test
        print("\n7️⃣  Nettoyage des données de test...")
        if compte_test:
            db.delete(compte_test)
            db.commit()
            print("   ✓ Données de test supprimées")

        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        db.close()


def main():
    """Point d'entrée principal"""
    success = test_schema()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
