"""
Script pour réinitialiser complètement la base de données
ATTENTION: Ce script supprime TOUTES les données existantes!
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from backend.database import engine, test_connection

def drop_all_tables():
    """Supprime toutes les tables de la base de données"""
    print("\n🗑️  Suppression des tables existantes...")

    with engine.begin() as conn:
        # Ordre de suppression respectant les contraintes de clés étrangères
        tables = [
            'operation',      # Anciennement 'transaction'
            'transaction',    # Table de l'ancien schéma
            'sous_categorie',
            'appartient_a',   # Table de l'ancien schéma
            'categorie',
            'type',
            'compte'
        ]

        for table in tables:
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS {table} CASCADE'))
                print(f"   ✓ Table {table} supprimée")
            except Exception as e:
                print(f"   ⚠️  Erreur lors de la suppression de {table}: {e}")


def create_schema():
    """Crée le nouveau schéma à partir du fichier schema.sql"""
    print("\n📝 Création du nouveau schéma...")

    schema_file = Path(__file__).parent.parent / "database" / "schema.sql"

    if not schema_file.exists():
        print(f"❌ Fichier schema.sql introuvable: {schema_file}")
        return False

    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Exécuter le script SQL
    with engine.begin() as conn:
        # Séparer les commandes SQL (simple split sur ';')
        commands = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip()]

        for cmd in commands:
            try:
                conn.execute(text(cmd))
            except Exception as e:
                # Ignorer les erreurs de duplication (ON CONFLICT)
                if "duplicate" not in str(e).lower() and "already exists" not in str(e).lower():
                    print(f"   ⚠️  Erreur: {e}")

    print("   ✓ Schéma créé avec succès!")
    return True


def verify_schema():
    """Vérifie que les tables ont bien été créées"""
    print("\n🔍 Vérification du schéma...")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))

        tables = [row[0] for row in result]

        expected_tables = ['compte', 'categorie', 'type', 'sous_categorie', 'operation']

        print("\n📊 Tables créées:")
        for table in tables:
            status = "✓" if table in expected_tables else "ℹ️"
            print(f"   {status} {table}")

        missing = set(expected_tables) - set(tables)
        if missing:
            print(f"\n⚠️  Tables manquantes: {', '.join(missing)}")
            return False

        print("\n✅ Toutes les tables attendues sont présentes!")
        return True


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🔄 RÉINITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)

    # Tester la connexion
    if not test_connection():
        print("\n❌ Impossible de se connecter à la base de données.")
        print("Vérifiez votre fichier .env et que PostgreSQL est démarré.")
        return 1

    # Confirmation
    print("\n⚠️  ATTENTION: Cette opération va:")
    print("   - Supprimer TOUTES les tables existantes")
    print("   - Supprimer TOUTES les données")
    print("   - Recréer le schéma à partir de database/schema.sql")

    response = input("\n❓ Êtes-vous sûr de vouloir continuer? (oui/non): ")

    if response.lower() not in ['oui', 'yes', 'o', 'y']:
        print("\n❌ Opération annulée.")
        return 0

    # Exécution
    drop_all_tables()

    if not create_schema():
        print("\n❌ Erreur lors de la création du schéma.")
        return 1

    if not verify_schema():
        print("\n⚠️  Le schéma semble incomplet.")
        return 1

    print("\n" + "=" * 60)
    print("✅ BASE DE DONNÉES RÉINITIALISÉE AVEC SUCCÈS!")
    print("=" * 60)
    print("\n💡 Prochaines étapes:")
    print("   1. Mettez à jour vos modèles SQLAlchemy (models.py)")
    print("   2. Testez la connexion et les opérations CRUD")
    print("   3. Ajoutez des données de test si nécessaire")

    return 0


if __name__ == "__main__":
    exit(main())
