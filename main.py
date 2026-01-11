# main.py - Point d'entrée principal de BudgetApp Python/Flet
"""
Point d'entrée simplifié - Configuration Flet au lieu de Qt
Port exact du main.cpp vers Python
"""

import flet as ft
import sys
import os
from pathlib import Path

# Ajouter le répertoire source au path
sys.path.insert(0, str(Path(__file__).parent))

from src.app import BudgetApp
from src.models.budget_manager import BudgetManager


def create_application_directories():
    """Crée les répertoires nécessaires pour l'application"""
    app_data_path = Path.home() / "BudgetApp_NatureTech"
    app_data_path.mkdir(exist_ok=True)

    # Créer les sous-répertoires
    (app_data_path / "backups").mkdir(exist_ok=True)
    (app_data_path / "exports").mkdir(exist_ok=True)

    print(f"✅ Répertoires créés dans: {app_data_path}")
    return str(app_data_path)


def main(page: ft.Page):
    """
    Fonction principale Flet - équivalent du main() C++

    Args:
        page: Page principale Flet
    """
    print("=== DÉMARRAGE DE BUDGETAPP 2025 PYTHON - VERSION FLET ===")

    # Configuration de la page principale
    page.title = "BudgetApp 2025 - Nature & Tech Edition"
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 1200
    page.window_min_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    # Couleurs exactes DA 2025
    from ui.theme.colors import COLORS

    # Configuration du thème personnalisé
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=COLORS.ACCENT_PRINCIPAL,
            primary_container=COLORS.CARTES_COMPOSANTS,
            secondary=COLORS.ACCENT_SECONDAIRE,
            secondary_container=COLORS.BACKGROUND_SECONDAIRE,
            surface=COLORS.BACKGROUND_PRINCIPAL,
            background=COLORS.BACKGROUND_PRINCIPAL,
            error=COLORS.ERREUR_DEPENSES,
            on_primary=COLORS.BACKGROUND_PRINCIPAL,
            on_secondary=COLORS.TEXTE_PRINCIPAL,
            on_surface=COLORS.TEXTE_PRINCIPAL,
            on_background=COLORS.TEXTE_PRINCIPAL,
            on_error=COLORS.TEXTE_PRINCIPAL,
            outline=COLORS.BORDURES
        )
    )

    try:
        # Créer les répertoires nécessaires
        data_directory = create_application_directories()

        # Initialiser le gestionnaire de budget
        print("🔧 Initialisation du BudgetManager...")
        budget_manager = BudgetManager(data_directory=data_directory)

        print(f"✅ BudgetManager initialisé:")
        print(f"   💰 Solde: {budget_manager.get_solde():.2f}€")
        print(f"   📝 Transactions: {budget_manager.nombre_transactions}")
        print(f"   📂 Catégories: {len(budget_manager.categories_budgets)}")
        print(f"   🎯 Données de démo: {'Oui' if budget_manager.has_demo_data else 'Non'}")

        # Créer et démarrer l'application principale
        print("🚀 Lancement de l'interface Flet...")
        app = BudgetApp(page, budget_manager)

        # Configuration des callbacks pour fermeture propre
        def on_window_close(e):
            print("🔚 Fermeture de l'application...")
            page.window_destroy()

        page.on_window_event = lambda e: on_window_close(e) if e.data == "close" else None

        # Démarrer l'application
        app.start()

        print("✅ Application prête - Interface chargée avec succès!")
        print("🌱⚡ BudgetApp 2025 - Edition Nature & Tech pour développeurs passionnés!")

    except Exception as e:
        print(f"❌ ERREUR CRITIQUE lors du démarrage: {e}")
        import traceback
        traceback.print_exc()

        # Afficher un message d'erreur dans l'interface
        error_message = ft.Column([
            ft.Text(
                "❌ Erreur de démarrage",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED
            ),
            ft.Text(
                str(e),
                size=16,
                color=ft.Colors.RED_300
            ),
            ft.Text(
                "Vérifiez les logs pour plus de détails.",
                size=14,
                color=ft.Colors.GREY
            )
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        page.add(
            ft.Container(
                content=error_message,
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=COLORS.BACKGROUND_PRINCIPAL
            )
        )


if __name__ == "__main__":
    print("🚀 Démarrage de BudgetApp 2025 - Nature & Tech Edition")
    print("📱 Framework: Python + Flet (Flutter backend)")
    print("🎨 Thème: DA 2025 avec couleurs exactes du QML")
    print("🎯 Cible: Développeurs Python/C++ passionnés de plantes et électronique")
    print("")

    # Vérifier que Flet est installé
    try:
        import flet
        print("✅ Flet détecté et disponible")
    except ImportError:
        print("❌ Flet n'est pas installé!")
        print("📦 Installation: pip install flet")
        sys.exit(1)

    # Lancer l'application Flet
    try:
        ft.app(
            target=main,
            view=ft.AppView.FLET_APP,  # Application native
            # Optionnel: ft.AppView.WEB_BROWSER pour version web
        )
    except KeyboardInterrupt:
        print("\n🔚 Application interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)