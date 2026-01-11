# src/app.py - Application principale avec navigation (Port de Main.qml)
"""
Application principale Flet avec NavigationRail
Remplace Main.qml avec navigation et couleurs DA 2025 exactes
"""

import flet as ft
from typing import Optional

from src.models.budget_manager import BudgetManager
from ui.theme.colors import COLORS
from ui.pages.dashboard import DashboardPage


class BudgetApp:
    """
    Application principale BudgetApp avec navigation
    Port de Main.qml vers Flet avec interface identique
    """

    def __init__(self, page: ft.Page, budget_manager: BudgetManager):
        """
        Initialise l'application principale

        Args:
            page: Page Flet principale
            budget_manager: Gestionnaire de budget initialisé
        """
        self.page = page
        self.budget_manager = budget_manager
        self.current_page = "dashboard"
        self.sidebar_expanded = True

        # Containers pour les pages
        self.main_content = ft.Container()
        self.navigation_rail = None

        # Configuration de la page
        self._setup_page()

    def _setup_page(self):
        """Configure la page principale avec le thème DA 2025"""
        # Couleur de fond exacte
        self.page.bgcolor = COLORS.BACKGROUND_PRINCIPAL

        # Configuration de la fenêtre
        self.page.title = "BudgetApp 2025 - Nature & Tech Edition"
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.spacing = 0

        # Thème personnalisé DA 2025
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=COLORS.ACCENT_PRINCIPAL,
                secondary=COLORS.ACCENT_SECONDAIRE,
                surface=COLORS.CARTES_COMPOSANTS,
                background=COLORS.BACKGROUND_PRINCIPAL,
                error=COLORS.ERREUR_DEPENSES,
                on_primary=COLORS.BACKGROUND_PRINCIPAL,
                on_surface=COLORS.TEXTE_PRINCIPAL,
                on_background=COLORS.TEXTE_PRINCIPAL,
                outline=COLORS.BORDURES
            )
        )

    def start(self):
        """Démarre l'application et construit l'interface"""
        self._build_interface()
        self._load_dashboard()

    def _build_interface(self):
        """Construit l'interface principale avec navigation"""
        # Navigation Rail
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            leading=self._build_navigation_header(),
            bgcolor=COLORS.BACKGROUND_SECONDAIRE,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.RECEIPT_LONG_OUTLINED,
                    selected_icon=ft.Icons.RECEIPT_LONG,
                    label="Transactions"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CATEGORY_OUTLINED,
                    selected_icon=ft.Icons.CATEGORY,
                    label="Catégories"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS,
                    label="Analytics"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.REFRESH_OUTLINED,
                    selected_icon=ft.Icons.REFRESH,
                    label="Récurrence"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Paramètres"
                )
            ],
            on_change=self._on_navigation_change
        )

        # Container de navigation avec bordure
        nav_container = ft.Container(
            content=self.navigation_rail,
            bgcolor=COLORS.BACKGROUND_SECONDAIRE,
            border=ft.border.only(right=ft.BorderSide(1, COLORS.BORDURES))
        )

        # Container principal pour le contenu
        self.main_content = ft.Container(
            bgcolor=COLORS.BACKGROUND_PRINCIPAL,
            expand=True
        )

        # Layout principal
        main_layout = ft.Row([
            nav_container,
            self.main_content
        ], spacing=0, expand=True)

        # Ajouter à la page
        self.page.add(main_layout)

    def _build_navigation_header(self) -> ft.Container:
        """Construit l'en-tête de navigation"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    size=32,
                    color=COLORS.ACCENT_PRINCIPAL
                ),
                ft.Text(
                    "BudgetApp",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS.TEXTE_PRINCIPAL
                ),
                ft.Text(
                    "2025",
                    size=12,
                    color=COLORS.VIOLET_LUMINEUX
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(20)
        )

    def _on_navigation_change(self, e):
        """Gère les changements de navigation"""
        pages = ["dashboard", "transactions", "categories", "analytics", "recurring", "settings"]

        if 0 <= e.control.selected_index < len(pages):
            self.current_page = pages[e.control.selected_index]
            self._load_page(self.current_page)

    def _load_page(self, page_name: str):
        """Charge une page spécifique"""
        if page_name == "dashboard":
            self._load_dashboard()
        elif page_name == "transactions":
            self._load_transactions()
        elif page_name == "categories":
            self._load_categories()
        elif page_name == "analytics":
            self._load_analytics()
        elif page_name == "recurring":
            self._load_recurring()
        elif page_name == "settings":
            self._load_settings()

    def _load_dashboard(self):
        """Charge la page Dashboard"""
        dashboard = DashboardPage(
            budget_manager=self.budget_manager,
            on_add_transaction=self._show_add_transaction_dialog,
            on_view_transactions=lambda: self._navigate_to("transactions"),
            on_view_categories=lambda: self._navigate_to("categories"),
            on_view_analytics=lambda: self._navigate_to("analytics"),
            on_view_settings=lambda: self._navigate_to("settings")
        )

        self.main_content.content = ft.ListView(
            controls=[dashboard.build()],
            expand=True,
            padding=ft.padding.all(0)
        )
        self.page.update()

    def _load_transactions(self):
        """Charge la page Transactions (placeholder)"""
        self._load_placeholder_page("transactions", "📋", "Transactions")

    def _load_categories(self):
        """Charge la page Catégories (placeholder)"""
        self._load_placeholder_page("categories", "🏷️", "Catégories")

    def _load_analytics(self):
        """Charge la page Analytics (placeholder)"""
        self._load_placeholder_page("analytics", "📊", "Analytics")

    def _load_recurring(self):
        """Charge la page Récurrence (placeholder)"""
        self._load_placeholder_page("recurring", "🔄", "Récurrence")

    def _load_settings(self):
        """Charge la page Paramètres (placeholder)"""
        self._load_placeholder_page("settings", "⚙️", "Paramètres")

    def _load_placeholder_page(self, page_name: str, icon: str, title: str):
        """Charge une page placeholder"""
        self.main_content.content = ft.Container(
            content=ft.Column([
                ft.Text(
                    f"{icon} {title}",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS.TEXTE_PRINCIPAL
                ),
                ft.Container(height=20),
                ft.Text(
                    "Page en cours de développement...",
                    size=16,
                    color=COLORS.TEXTE_SECONDAIRE
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Retour au Dashboard",
                    on_click=lambda _: self._navigate_to("dashboard"),
                    style=ft.ButtonStyle(
                        bgcolor=COLORS.ACCENT_PRINCIPAL,
                        color=COLORS.BACKGROUND_PRINCIPAL
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),
            expand=True
        )
        self.page.update()

    def _navigate_to(self, page_name: str):
        """Navigue vers une page spécifique"""
        pages = ["dashboard", "transactions", "categories", "analytics", "recurring", "settings"]

        if page_name in pages:
            index = pages.index(page_name)
            self.navigation_rail.selected_index = index
            self.current_page = page_name
            self._load_page(page_name)
            self.page.update()

    def _show_add_transaction_dialog(self):
        """Affiche le dialogue d'ajout de transaction"""
        # Placeholder pour le dialogue d'ajout de transaction
        dialog = ft.AlertDialog(
            title=ft.Text("Nouvelle Transaction"),
            content=ft.Text("Fonctionnalité en cours de développement..."),
            actions=[
                ft.TextButton("Fermer", on_click=lambda _: self._close_dialog())
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _close_dialog(self):
        """Ferme le dialogue ouvert"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def get_current_page(self) -> str:
        """Retourne la page actuellement active"""
        return self.current_page

    def refresh_current_page(self):
        """Rafraîchit la page actuelle"""
        self._load_page(self.current_page)


