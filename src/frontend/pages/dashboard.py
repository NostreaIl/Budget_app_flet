# ui/pages/dashboard.py - Dashboard corrigé avec Plotly
"""
Page Dashboard corrigée pour BudgetApp DA 2025
Utilise les graphiques Plotly corrigés qui fonctionnent avec Flet
"""

import flet as ft
from typing import Optional, Callable, List
from src.frontend.theme.colors import COLORS
from src.frontend.components.stat_card import StatCard

# Import de la version corrigée des graphiques
try:
    from src.frontend.components.charts.pie_chart import create_donut_chart_with_center
    CHARTS_AVAILABLE = True
except ImportError:
    print("⚠️ Graphiques Plotly non disponibles, utilisation de placeholders")
    CHARTS_AVAILABLE = False


class DashboardPage:
    """
    Page Dashboard avec graphiques Plotly corrigés
    """

    def __init__(self, budget_manager, on_add_transaction: Callable = None,
                 on_view_transactions: Callable = None, on_view_categories: Callable = None,
                 on_view_analytics: Callable = None, on_view_settings: Callable = None):
        """
        Initialise la page Dashboard

        Args:
            budget_manager: Gestionnaire de budget
            on_add_transaction: Callback pour ajouter une transaction
            on_view_transactions: Callback pour voir toutes les transactions
            on_view_categories: Callback pour voir les catégories
            on_view_analytics: Callback pour voir les analytics
            on_view_settings: Callback pour voir les paramètres
        """
        self.budget_manager = budget_manager
        self.on_add_transaction = on_add_transaction
        self.on_view_transactions = on_view_transactions
        self.on_view_categories = on_view_categories
        self.on_view_analytics = on_view_analytics
        self.on_view_settings = on_view_settings

        # Couleurs violet lumineux
        self.VIOLET_LUMINEUX = "#9C27B0"
        self.VIOLET_GLOW = "#E1BEE7"

    def build(self) -> ft.Container:
        """Construit la page Dashboard complète"""
        try:
            content = ft.Column([
                self._build_header(),
                ft.Container(height=24),
                self._build_stats_row(),
                ft.Container(height=32),
                self._build_charts_section(),
                ft.Container(height=32),
                self._build_recent_activity(),
            ])

            return ft.Container(
                content=content,
                padding=ft.padding.all(24),
                bgcolor=COLORS.BACKGROUND_PRINCIPAL,
                expand=True
            )

        except Exception as e:
            print(f"❌ Erreur construction dashboard: {e}")
            return self._build_error_dashboard(str(e))

    def _build_header(self) -> ft.Container:
        """Construit l'en-tête du dashboard"""
        return ft.Container(
            content=ft.Row([
                ft.Text(
                    "📊 Dashboard",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS.TEXTE_PRINCIPAL,
                    font_family="Segoe UI Variable"
                ),
                ft.Container(expand=True),
                self._build_quick_actions_header()
            ]),
            padding=ft.padding.only(bottom=16)
        )

    def _build_quick_actions_header(self) -> ft.Row:
        """Construit les actions rapides dans l'en-tête"""
        return ft.Row([
            self._build_header_button(ft.icons.RECEIPT_LONG, COLORS.ACCENT_PRINCIPAL,
                                    "Transactions", self.on_view_transactions),
            ft.Container(width=12),
            self._build_header_button(ft.icons.CATEGORY, self.VIOLET_LUMINEUX,
                                    "Catégories", self.on_view_categories),
            ft.Container(width=12),
            self._build_header_button(ft.icons.ANALYTICS, COLORS.AVERTISSEMENT,
                                    "Analytics", self.on_view_analytics),
        ])

    def _build_header_button(self, icon, color, tooltip, callback):
        """Construit un bouton d'en-tête"""
        return ft.Container(
            content=ft.IconButton(
                icon=icon,
                icon_color=color,
                tooltip=tooltip,
                on_click=lambda _: callback() if callback else None
            ),
            width=40,
            height=40,
            border=ft.border.all(2, color),
            border_radius=20,
            bgcolor="transparent"
        )

    def _build_stats_row(self) -> ft.Row:
        """Construit la ligne des statistiques principales"""
        try:
            # Calcul sécurisé des statistiques
            transactions = getattr(self.budget_manager, 'transactions', [])
            revenus = sum(t.montant for t in transactions if hasattr(t, 'montant') and t.montant > 0)
            depenses = sum(abs(t.montant) for t in transactions if hasattr(t, 'montant') and t.montant < 0)
            solde = revenus - depenses

            return ft.Row([
                # Carte Solde Total
                ft.Container(
                    content=StatCard(
                        title="Solde Total",
                        value=f"{solde:,.2f} €",
                        color=COLORS.SUCCESS_REVENUS if solde >= 0 else COLORS.ERREUR_DEPENSES,
                        icon="💰",
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, -1),
                            end=ft.Alignment(0, 1),
                            colors=["#2A2A3E", "#312A3A"]
                        ),
                    ).build(),
                    expand=True,
                    height=140,
                ),
                ft.Container(width=15),

                # Carte Revenus
                ft.Container(
                    content=StatCard(
                        title="Revenus (mois)",
                        value=f"+{revenus:,.2f} €",
                        color=COLORS.SUCCESS_REVENUS,
                        icon="📈",
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, -1),
                            end=ft.Alignment(0, 1),
                            colors=["#2A2A3E", "#2F3544", "#35404A"]
                        )
                    ).build(),
                    expand=True,
                    height=140,
                ),
                ft.Container(width=15),

                # Carte Dépenses
                ft.Container(
                    content=StatCard(
                        title="Dépenses (mois)",
                        value=f"-{depenses:,.2f} €",
                        color=COLORS.ERREUR_DEPENSES,
                        icon="📉",
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, -1),
                            end=ft.Alignment(0, 1),
                            colors=["#2A2A3E", "#312A3A", "#382A36"]
                        )
                    ).build(),
                    expand=True,
                    height=140,
                )
            ], alignment=ft.MainAxisAlignment.CENTER, wrap=False)

        except Exception as e:
            print(f"❌ Erreur construction stats: {e}")
            return ft.Row([
                ft.Container(
                    content=ft.Text("Erreur chargement statistiques", color=COLORS.ERREUR_DEPENSES),
                    expand=True
                )
            ])

    def _build_charts_section(self) -> ft.Container:
        """Construit la section des graphiques"""
        if CHARTS_AVAILABLE:
            return create_donut_chart_with_center()

        if not CHARTS_AVAILABLE:
            return self._build_charts_placeholder()

    def _build_charts_placeholder(self) -> ft.Container:
        """Placeholder quand les graphiques ne sont pas disponibles"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "📈 Graphiques (en cours de développement)",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS.TEXTE_PRINCIPAL
                ),
                ft.Container(height=16),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.SHOW_CHART, size=64, color=COLORS.TEXTE_SECONDAIRE),
                        ft.Text(
                            "Graphiques Plotly en cours d'installation",
                            size=16,
                            color=COLORS.TEXTE_SECONDAIRE
                        ),
                        ft.Text(
                            "pip install plotly",
                            size=12,
                            color=COLORS.ACCENT_PRINCIPAL
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    height=200,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=COLORS.CARTES_COMPOSANTS,
                    border_radius=12,
                    border=ft.border.all(1, COLORS.BORDURES)
                )
            ]),
            padding=ft.padding.all(20)
        )

    def _build_recent_activity(self) -> ft.Container:
        """Construit la section d'activité récente"""
        try:
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            "🕒 Activité Récente",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS.TEXTE_PRINCIPAL
                        ),
                        ft.Container(expand=True),
                        ft.TextButton(
                            "Voir tout",
                            style=ft.ButtonStyle(color=self.VIOLET_LUMINEUX),
                            on_click=lambda _: self.on_view_transactions() if self.on_view_transactions else None
                        )
                    ]),
                    ft.Container(height=16),
                    self._build_recent_transactions_list()
                ]),
                padding=ft.padding.all(20),
                bgcolor=COLORS.CARTES_COMPOSANTS,
                border_radius=12,
                border=ft.border.all(1, COLORS.BORDURES)
            )

        except Exception as e:
            print(f"❌ Erreur activité récente: {e}")
            return ft.Container(
                content=ft.Text("Erreur chargement activité", color=COLORS.ERREUR_DEPENSES),
                height=200
            )

    def _build_recent_transactions_list(self) -> ft.Container:
        """Construit la liste des transactions récentes"""
        try:
            transactions = getattr(self.budget_manager, 'transactions', [])
            recent_transactions = transactions[-5:] if transactions else []

            if not recent_transactions:
                return ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.RECEIPT_LONG_OUTLINED, size=48, color=COLORS.TEXTE_SECONDAIRE),
                        ft.Text("Aucune transaction récente", color=COLORS.TEXTE_SECONDAIRE, size=16)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    height=200,
                    alignment=ft.Alignment(0, 0)
                )

            transaction_items = []
            for transaction in reversed(recent_transactions):
                transaction_items.append(self._build_transaction_item(transaction))

            return ft.Container(
                content=ft.Column(transaction_items, spacing=8),
                height=min(len(recent_transactions) * 60, 300)
            )

        except Exception as e:
            print(f"❌ Erreur liste transactions: {e}")
            return ft.Container(
                content=ft.Text("Erreur chargement transactions", color=COLORS.ERREUR_DEPENSES),
                height=200
            )

    def _build_transaction_item(self, transaction) -> ft.Container:
        """Construit un élément de transaction"""
        try:
            # Vérifications sécurisées
            montant = getattr(transaction, 'montant', 0)
            description = getattr(transaction, 'description', 'Transaction')
            categorie = getattr(transaction, 'categorie', 'Divers')
            date_transaction = getattr(transaction, 'date', None)
            icone = getattr(transaction, 'icone', '💰')

            # Déterminer la couleur selon le type
            if montant > 0:
                color = COLORS.SUCCESS_REVENUS
                sign = "+"
            else:
                color = COLORS.ERREUR_DEPENSES
                sign = ""

            # Formater la date
            date_str = date_transaction.strftime("%d/%m") if date_transaction else "N/A"

            return ft.Container(
                content=ft.Row([
                    # Icône de la transaction
                    ft.Container(
                        content=ft.Text(icone, size=20),
                        width=24,
                        alignment=ft.Alignment(0, 0)
                    ),
                    ft.Container(width=12),

                    # Informations de la transaction
                    ft.Column([
                        ft.Text(
                            description,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=COLORS.TEXTE_PRINCIPAL
                        ),
                        ft.Row([
                            ft.Text(categorie, size=12, color=COLORS.TEXTE_SECONDAIRE),
                            ft.Text("•", size=12, color=COLORS.TEXTE_SECONDAIRE),
                            ft.Text(date_str, size=12, color=COLORS.TEXTE_SECONDAIRE)
                        ], spacing=4)
                    ], spacing=2, expand=True),

                    # Montant
                    ft.Text(
                        f"{sign}{abs(montant):,.2f} €",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=color
                    )
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.all(12),
                bgcolor="transparent",
                border_radius=8,
                ink=True,
                tooltip="Cliquer pour plus de détails"
            )

        except Exception as e:
            print(f"❌ Erreur élément transaction: {e}")
            return ft.Container(
                content=ft.Text("Erreur transaction", color=COLORS.ERREUR_DEPENSES),
                height=50
            )

    def _build_error_dashboard(self, error_msg: str) -> ft.Container:
        """Construit un dashboard d'erreur"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.ERROR_OUTLINE, size=64, color=COLORS.ERREUR_DEPENSES),
                ft.Text(
                    "❌ Erreur Dashboard",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS.ERREUR_DEPENSES
                ),
                ft.Text(
                    error_msg,
                    size=16,
                    color=COLORS.TEXTE_SECONDAIRE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Recharger",
                    icon=ft.icons.REFRESH,
                    on_click=lambda _: self.refresh()
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),
            expand=True,
            bgcolor=COLORS.BACKGROUND_PRINCIPAL,
            padding=ft.padding.all(50)
        )

    def refresh(self):
        """Rafraîchit les données de la page"""
        try:
            print("🔄 Rafraîchissement du dashboard...")
            # Ici vous pouvez ajouter la logique de rafraîchissement
            # Par exemple, recharger les données du budget_manager
        except Exception as e:
            print(f"❌ Erreur rafraîchissement: {e}")


# Fonction utilitaire pour tester le dashboard
def test_dashboard(budget_manager):
    """Teste la création du dashboard"""
    try:
        print("🧪 Test création dashboard...")
        dashboard = DashboardPage(budget_manager)
        dashboard_container = dashboard.build()
        print("✅ Dashboard créé avec succès")
        return dashboard_container

    except Exception as e:
        print(f"❌ Erreur test dashboard: {e}")
        return None