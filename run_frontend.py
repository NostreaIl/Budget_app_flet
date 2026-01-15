"""
Point d'entrée pour lancer le frontend Flet
"""
if __name__ == "__main__":
    import flet as ft
    from src.frontend.main import main

    print("🚀 Démarrage de l'application Flet...")
    print("🔗 Backend API: http://localhost:8000")

    ft.app(target=main)
