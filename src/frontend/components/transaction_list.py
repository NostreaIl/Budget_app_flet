# ui/components/transaction_list.py - Liste des transactions
"""
Composant TransactionsList pour afficher les transactions
avec le style DA 2025 et interactions violet lumineux
"""

import flet as ft
from typing import List, Callable, Optional
from datetime import datetime
from ui.theme.colors import COLORS


class TransactionItem:
    """
    Élément de transaction individuel avec style DA 2025
    """

    def __init__(self, transaction, on_click: Callable = None,
                 on_edit: Callable = None, on_delete: Callable = None):
        """
        Initialise un élément de transaction

        Args:
            transaction: Objet transaction à afficher
            on_click: Callback pour le clic sur la transaction
            on_edit: Callback pour l'édition
            on_delete: Callback pour la suppression
        """
        self.transaction = transaction
        self.on_click = on_click
        self.on_edit = on_edit
        self.on_delete = on_delete

        # Couleurs violet lumineux
        self.VIOLET_LUMINEUX = "#9C27B0"
        self.VIOLET_GLOW = "#E1BEE7"

        self.container = self._build_item()

    def _build_item(self) -> ft.Container:
        """Construit l'élément de transaction"""
        # Déterminer la couleur selon le type
        if self.transaction.montant > 0:
            color = COLORS.SUCCESS_REVENUS
            sign = "+"
            icon_bg_color = f"{COLORS.SUCCESS_REVENUS}20"
        else:
            color = COLORS.ERREUR_DEPENSES
            sign = ""
            icon_bg_color = f"{COLORS.ERREUR_DEPENSES}20"

        # Obtenir l'icône
        icon = getattr(self.transaction, 'icone', '💰')

        return ft.Container(
            content=ft.Row([
                # Icône de la transaction
                ft.Container(
                    content=ft.Text(
                        icon,
                        size=20
                    ),
                    width=40,
                    height=40,
                    bgcolor=icon_bg_color,
                    border_radius=20,
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Container(width=16),  # Espacement

                # Informations principales
                ft.Column([
                    # Description
                    ft.Text(
                        self.transaction.description,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=COLORS.TEXTE_PRINCIPAL
                    ),
                    # Détails (catégorie et date)
                    ft.Row([
                        ft.Text(
                            self.transaction.categorie,
                            size=12,
                            color=COLORS.TEXTE_SECONDAIRE
                        ),
                        ft.Text("•", size=12, color=COLORS.TEXTE_SECONDAIRE),
                        ft.Text(
                            self.transaction.date.strftime("%d/%m/%Y"),
                            size=12,
                            color=COLORS.TEXTE_SECONDAIRE
                        )
                    ], spacing=6)
                ], spacing=4, expand=True),

                # Montant
                ft.Text(
                    f"{sign}{abs(self.transaction.montant):,.2f} €",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=color
                ),

                # Boutons d'action (visibles au survol)
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.icons.EDIT_OUTLINED,
                            icon_color=self.VIOLET_LUMINEUX,
                            icon_size=16,
                            tooltip="Modifier",
                            on_click=lambda e: self.on_edit(self.transaction) if self.on_edit else None
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color=COLORS.ERREUR_DEPENSES,
                            icon_size=16,
                            tooltip="Supprimer",
                            on_click=lambda e: self.on_delete(self.transaction) if self.on_delete else None
                        )
                    ], spacing=4),
                    width=80,
                    visible=False,  # Masqué par défaut
                    ref=ft.Ref[ft.Container]()
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(16),
            bgcolor="transparent",
            border_radius=12,
            border=ft.border.all(1, "transparent"),
            ink=True,
            on_click=lambda e: self.on_click(self.transaction) if self.on_click else None,
            on_hover=self._on_hover,
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
        )

    def _on_hover(self, e):
        """Gère l'effet de survol"""
        actions_container = e.control.content.controls[-1]  # Dernier élément (actions)

        if e.data == "true":  # Souris sur l'élément
            e.control.bgcolor = f"{COLORS.CARTES_COMPOSANTS}80"
            e.control.border = ft.border.all(1, f"{self.VIOLET_GLOW}40")
            actions_container.visible = True
        else:  # Souris hors de l'élément
            e.control.bgcolor = "transparent"
            e.control.border = ft.border.all(1, "transparent")
            actions_container.visible = False

        e.control.update()


class TransactionsList:
    """
    Liste complète des transactions avec filtres et recherche
    Style DA 2025 avec touches violet lumineux
    """

    def __init__(self, transactions: List = None,
                 on_transaction_click: Callable = None,
                 on_transaction_edit: Callable = None,
                 on_transaction_delete: Callable = None,
                 max_items: int = None):
        """
        Initialise la liste des transactions

        Args:
            transactions: Liste des transactions à afficher
            on_transaction_click: Callback pour le clic sur une transaction
            on_transaction_edit: Callback pour l'édition d'une transaction
            on_transaction_delete: Callback pour la suppression d'une transaction
            max_items: Nombre maximum d'éléments à afficher (None = tous)
        """
        self.transactions = transactions or []
        self.on_transaction_click = on_transaction_click
        self.on_transaction_edit = on_transaction_edit
        self.on_transaction_delete = on_transaction_delete
        self.max_items = max_items

        # Couleurs violet lumineux
        self.VIOLET_LUMINEUX = "#9C27B0"

        # État des filtres
        self.search_query = ""
        self.selected_category = None
        self.date_filter = None

        self.container = self._build_list()

    def _build_list(self) -> ft.Container:
        """Construit la liste complète avec filtres"""
        return ft.Container(
            content=ft.Column([
                self._build_filters(),
                ft.Container(height=16),  # Espacement
                self._build_transactions_container()
            ]),
            padding=ft.padding.all(0)
        )

    def _build_filters(self) -> ft.Container:
        """Construit la barre de filtres et recherche"""
        return ft.Container(
            content=ft.Row([
                # Barre de recherche
                ft.Container(
                    content=ft.TextField(
                        hint_text="🔍 Rechercher une transaction...",
                        border_color=COLORS.BORDURES,
                        focused_border_color=self.VIOLET_LUMINEUX,
                        text_style=ft.TextStyle(color=COLORS.TEXTE_PRINCIPAL),
                        hint_style=ft.TextStyle(color=COLORS.TEXTE_SECONDAIRE),
                        cursor_color=self.VIOLET_LUMINEUX,
                        on_change=self._on_search_change
                    ),
                    expand=True
                ),
                ft.Container(width=12),  # Espacement

                # Filtre par catégorie
                ft.Container(
                    content=ft.Dropdown(
                        hint_text="Catégorie",
                        options=[
                            ft.dropdown.Option("Toutes", ""),
                            ft.dropdown.Option("Alimentation", "Alimentation"),
                            ft.dropdown.Option("Transport", "Transport"),
                            ft.dropdown.Option("Loisirs", "Loisirs"),
                            ft.dropdown.Option("Salaire", "Salaire"),
                        ],
                        border_color=COLORS.BORDURES,
                        focused_border_color=self.VIOLET_LUMINEUX,
                        text_style=ft.TextStyle(color=COLORS.TEXTE_PRINCIPAL),
                        on_change=self._on_category_filter_change
                    ),
                    width=150
                ),
                ft.Container(width=12),  # Espacement

                # Bouton tri
                ft.IconButton(
                    icon=ft.icons.SORT,
                    icon_color=COLORS.TEXTE_SECONDAIRE,
                    tooltip="Trier les transactions",
                    on_click=self._on_sort_click
                )
            ]),
            padding=ft.padding.all(16),
            bgcolor=COLORS.CARTES_COMPOSANTS,
            border_radius=8,
            border=ft.border.all(1, COLORS.BORDURES)
        )

    def _build_transactions_container(self) -> ft.Container:
        """Construit le container des transactions"""
        filtered_transactions = self._filter_transactions()

        if not filtered_transactions:
            return self._build_empty_state()

        # Limiter le nombre d'éléments si nécessaire
        if self.max_items:
            filtered_transactions = filtered_transactions[:self.max_items]

        transaction_items = []
        for transaction in filtered_transactions:
            item = TransactionItem(
                transaction=transaction,
                on_click=self.on_transaction_click,
                on_edit=self.on_transaction_edit,
                on_delete=self.on_transaction_delete
            )
            transaction_items.append(item.container)

        return ft.Container(
            content=ft.Column(
                transaction_items,
                spacing=8
            ),
            bgcolor=COLORS.CARTES_COMPOSANTS,
            border_radius=12,
            border=ft.border.all(1, COLORS.BORDURES),
            padding=ft.padding.all(16)
        )

    def _build_empty_state(self) -> ft.Container:
        """Construit l'état vide"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(
                    ft.icons.RECEIPT_LONG_OUTLINED,
                    size=64,
                    color=COLORS.TEXTE_SECONDAIRE
                ),
                ft.Container(height=16),
                ft.Text(
                    "Aucune transaction trouvée",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=COLORS.TEXTE_SECONDAIRE
                ),
                ft.Text(
                    "Essayez de modifier vos filtres de recherche",
                    size=14,
                    color=COLORS.TEXTE_SECONDAIRE
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            height=200,
            alignment=ft.Alignment(0, 0),
            bgcolor=COLORS.CARTES_COMPOSANTS,
            border_radius=12,
            border=ft.border.all(1, COLORS.BORDURES)
        )

    def _filter_transactions(self) -> List:
        """Filtre les transactions selon les critères"""
        filtered = self.transactions.copy()

        # Filtre par recherche
        if self.search_query:
            filtered = [t for t in filtered
                        if self.search_query.lower() in t.description.lower()]

        # Filtre par catégorie
        if self.selected_category:
            filtered = [t for t in filtered
                        if t.categorie == self.selected_category]

        # Tri par date (plus récent en premier)
        filtered.sort(key=lambda t: t.date, reverse=True)

        return filtered

    def _on_search_change(self, e):
        """Gère le changement de recherche"""
        self.search_query = e.control.value or ""
        self._refresh_list()

    def _on_category_filter_change(self, e):
        """Gère le changement de filtre de catégorie"""
        self.selected_category = e.control.value if e.control.value else None
        self._refresh_list()

    def _on_sort_click(self, e):
        """Gère le clic sur le tri"""
        # Ici vous pouvez implémenter différents modes de tri
        print("Tri des transactions...")

    def _refresh_list(self):
        """Rafraîchit la liste des transactions"""
        # Reconstruire le container des transactions
        new_container = self._build_transactions_container()

        # Remplacer le container existant
        self.container.content.controls[2] = new_container  # Index 2 = transactions container
        self.container.update()

    def update_transactions(self, new_transactions: List):
        """Met à jour la liste des transactions"""
        self.transactions = new_transactions
        self._refresh_list()

    def get_container(self) -> ft.Container:
        """Retourne le container principal"""
        return self.container


class CompactTransactionsList:
    """
    Version compacte de la liste des transactions
    Pour l'affichage dans le dashboard
    """

    def __init__(self, transactions: List = None, max_items: int = 5,
                 on_transaction_click: Callable = None):
        """
        Initialise la liste compacte

        Args:
            transactions: Liste des transactions
            max_items: Nombre maximum d'éléments à afficher
            on_transaction_click: Callback pour le clic
        """
        self.transactions = transactions or []
        self.max_items = max_items
        self.on_transaction_click = on_transaction_click

        self.container = self._build_compact_list()

    def _build_compact_list(self) -> ft.Container:
        """Construit la liste compacte"""
        if not self.transactions:
            return ft.Container(
                content=ft.Text(
                    "Aucune transaction récente",
                    color=COLORS.TEXTE_SECONDAIRE,
                    size=14
                ),
                height=100,
                alignment=ft.Alignment(0, 0)
            )

        # Prendre les dernières transactions
        recent_transactions = list(reversed(self.transactions[-self.max_items:]))

        items = []
        for transaction in recent_transactions:
            items.append(self._build_compact_item(transaction))

        return ft.Container(
            content=ft.Column(items, spacing=4),
            padding=ft.padding.all(0)
        )

    def _build_compact_item(self, transaction) -> ft.Container:
        """Construit un élément compact"""
        # Couleur selon le type
        color = COLORS.SUCCESS_REVENUS if transaction.montant > 0 else COLORS.ERREUR_DEPENSES
        sign = "+" if transaction.montant > 0 else ""

        return ft.Container(
            content=ft.Row([
                ft.Text(
                    getattr(transaction, 'icone', '💰'),
                    size=16
                ),
                ft.Container(width=8),
                ft.Column([
                    ft.Text(
                        transaction.description,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=COLORS.TEXTE_PRINCIPAL
                    ),
                    ft.Text(
                        f"{transaction.categorie} • {transaction.date.strftime('%d/%m')}",
                        size=11,
                        color=COLORS.TEXTE_SECONDAIRE
                    )
                ], spacing=2, expand=True),
                ft.Text(
                    f"{sign}{abs(transaction.montant):,.0f} €",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=color
                )
            ]),
            padding=ft.padding.all(8),
            border_radius=6,
            ink=True,
            on_click=lambda e, t=transaction: self.on_transaction_click(t) if self.on_transaction_click else None
        )

    def get_container(self) -> ft.Container:
        """Retourne le container principal"""
        return self.container