"""
Script de test de connexion à PostgreSQL
"""
import sys
sys.path.insert(0, '/home/user/Budget_app_flet')

from backend.database import test_connection, engine, DATABASE_URL
from backend import models

print("=" * 60)
print("TEST DE CONNEXION À POSTGRESQL")
print("=" * 60)
print(f"\n📌 URL de connexion: {DATABASE_URL}\n")

# Test de connexion
if test_connection():
    print("\n✅ Connexion établie avec succès!")

    # Afficher les tables existantes
    print("\n📊 Tables détectées dans la base de données:")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"  - {table_name}")

    print("\n✅ Tout est prêt! FastAPI peut maintenant se connecter à PostgreSQL.")
else:
    print("\n❌ Échec de la connexion!")
    print("Vérifiez vos credentials dans le fichier .env")

print("\n" + "=" * 60)
