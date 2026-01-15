# ui/components/stat_card.py - Composant carte statistique avec dégradés
"""
Composant StatCard reproduisant les cartes statistiques du dashboard QML
Avec animations, effets visuels DA 2025 et support des dégradés
"""

import flet as ft
from ui.theme.colors import COLORS


class StatCard:
    """
    Composant carte statistique avec style DA 2025
    Reproduit les cartes du dashboard QML avec effets violet lumineux et dégradés
    """

    def __init__(self, title: str, value: str, color: str,
                 background_color: str = None, trend: str = None,
                 trend_subtitle: str = None, icon: str = None, gradient: ft.LinearGradient = None):
        """
        Initialise une carte statistique

        Args:
            title: Titre de la carte (ex: "💰 Solde Total")
            value: Valeur principale (ex: "1,234.56 €")
            subtitle: Sous-titre (ex: "Tous comptes")
            color: Couleur principale de la carte
            background_color: Couleur de fond (optionnel, ignoré si gradient fourni)
            trend: Indicateur de tendance (ex: "+189%")
            trend_subtitle: Sous-titre de tendance (ex: "vs mois dernier")
            icon: Icône supplémentaire (optionnel)
            gradient: Dégradé de fond (optionnel)
        """
        self.title = title
        self.value = value
        # self.subtitle = subtitle
        self.color = color
        self.background_color = background_color or COLORS.CARTES_COMPOSANTS
        self.trend = trend
        self.trend_subtitle = trend_subtitle
        self.icon = icon
        self.gradient = gradient

        # Couleurs violet lumineux pour les effets
        self.VIOLET_LUMINEUX = "#9C27B0"
        self.VIOLET_GLOW = "#E1BEE7"

    def build(self) -> ft.Container:
        """Construit la carte statistique complète"""
        content_items = [
            ft.Container(
                content=ft.Text(
                    self.icon,
                    size=24,  # Grosse icône
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.Alignment(0, 0)
            ),
            ft.Container(height=16),  # Espacement après l'icône
            # Titre
            ft.Text(
                self.title,
                size=14,
                weight=ft.FontWeight.W_500,
                color=COLORS.TEXTE_SECONDAIRE,
                text_align=ft.TextAlign.CENTER

            ),
            ft.Container(height=8),  # Espacement

            # Valeur principale
            ft.Text(
                self.value,
                size=24,
                weight=ft.FontWeight.BOLD,
                color=self.color,
                text_align=ft.TextAlign.CENTER

        )
            # ft.Container(height=4),  # Espacement
            # # Sous-titre
            # ft.Text(
            #     self.subtitle,
            #     size=12,
            #     color=COLORS.TEXTE_SECONDAIRE
            # )
        ]

        # Ajouter la tendance si présente
        if self.trend:
            content_items.extend([
                ft.Container(height=12),  # Espacement
                self._build_trend_indicator()
            ])

        # Utiliser gradient ou bgcolor selon ce qui est fourni
        container_kwargs = {
            "content": ft.Column(
                content_items,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,  # ✅ NOUVEAU - Centre vertical
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # ✅ NOUVEAU - Centre horizontal
            ),
            "padding": ft.padding.all(20),
            "border_radius": 12,
            "border": ft.border.all(1, COLORS.BORDURES),
            "height": 160 if self.icon else 120,  # ✅ NOUVEAU - Hauteur adaptative
            "animate": 300,
            # "on_hover": self._on_hover
        }
        # Toujours définir bgcolor, gradient en priorité si fourni
        container_kwargs["bgcolor"] = self.background_color
        if self.gradient:
            container_kwargs["gradient"] = self.gradient

        return ft.Container(**container_kwargs)

    def _build_trend_indicator(self) -> ft.Container:
        """Construit l'indicateur de tendance"""
        # Déterminer la couleur de la tendance
        if self.trend.startswith('+'):
            trend_color = COLORS.SUCCESS_REVENUS
            trend_icon = "📈"
        elif self.trend.startswith('-'):
            trend_color = COLORS.ERREUR_DEPENSES
            trend_icon = "📉"
        else:
            trend_color = COLORS.TEXTE_SECONDAIRE
            trend_icon = "📊"

        return ft.Container(
            content=ft.Row([
                ft.Text(
                    trend_icon,
                    size=16
                ),
                ft.Container(width=8),  # Espacement
                ft.Column([
                    ft.Text(
                        self.trend,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=trend_color
                    ),
                    ft.Text(
                        self.trend_subtitle or "",
                        size=10,
                        color=COLORS.TEXTE_SECONDAIRE
                    )
                ], spacing=2)
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(8),
            bgcolor=f"{trend_color}15",  # Couleur très transparente
            border_radius=8,
            border=ft.border.all(1, f"{trend_color}30")
        )

    def _on_hover(self, e):
        """Gère l'effet de survol"""
        if e.data == "true":  # Souris sur la carte
            e.control.border = ft.border.all(1, f"{self.VIOLET_GLOW}50")
            # Si gradient, pas de changement de couleur, sinon changement normal
            if not self.gradient:
                e.control.bgcolor = f"{self.background_color}CC"  # Légèrement plus transparent
        else:  # Souris hors de la carte
            e.control.border = ft.border.all(1, COLORS.BORDURES)
            if not self.gradient:
                e.control.bgcolor = self.background_color

        e.control.update()


class MiniStatCard:
    """
    Version compacte de StatCard pour les widgets plus petits
    """

    def __init__(self, icon: str, value: str, label: str, color: str):
        """
        Initialise une mini carte statistique

        Args:
            icon: Icône/émoji de la carte
            value: Valeur à afficher
            label: Libellé de la carte
            color: Couleur principale
        """
        self.icon = icon
        self.value = value
        self.label = label
        self.color = color

    def build(self) -> ft.Container:
        """Construit la mini carte"""
        return ft.Container(
            content=ft.Row([
                # Icône
                ft.Container(
                    content=ft.Text(
                        self.icon,
                        size=20
                    ),
                    width=32,
                    height=32,
                    bgcolor=f"{self.color}20",
                    border_radius=16,
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Container(width=12),  # Espacement

                # Contenu
                ft.Column([
                    ft.Text(
                        self.value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self.color
                    ),
                    ft.Text(
                        self.label,
                        size=12,
                        color=COLORS.TEXTE_SECONDAIRE
                    )
                ], spacing=2, expand=True)
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.all(12),
            bgcolor=COLORS.CARTES_COMPOSANTS,
            border_radius=8,
            border=ft.border.all(1, COLORS.BORDURES),
            height=60
        )


class ProgressStatCard:
    """
    Carte statistique avec barre de progression
    Utilisée pour les budgets et objectifs
    """

    def __init__(self, title: str, current: float, target: float,
                 color: str, unit: str = "€"):
        """
        Initialise une carte avec progression

        Args:
            title: Titre de la carte
            current: Valeur actuelle
            target: Valeur cible
            color: Couleur de la progression
            unit: Unité d'affichage
        """
        self.title = title
        self.current = current
        self.target = target
        self.color = color
        self.unit = unit

    def build(self) -> ft.Container:
        """Construit la carte avec progression"""
        # Calcul du pourcentage
        percentage = min((self.current / self.target) * 100, 100) if self.target > 0 else 0

        # Couleur selon le pourcentage
        if percentage >= 90:
            progress_color = COLORS.ERREUR_DEPENSES  # Rouge si proche de la limite
        elif percentage >= 70:
            progress_color = COLORS.AVERTISSEMENT  # Orange si modéré
        else:
            progress_color = COLORS.SUCCESS_REVENUS  # Vert si bon

        return ft.Container(
            content=ft.Column([
                # En-tête
                ft.Row([
                    ft.Text(
                        self.title,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=COLORS.TEXTE_SECONDAIRE
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        f"{percentage:.0f}%",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=progress_color
                    )
                ]),
                ft.Container(height=8),  # Espacement

                # Barre de progression
                ft.ProgressBar(
                    value=percentage / 100,
                    bgcolor=f"{COLORS.BORDURES}50",
                    color=progress_color,
                    height=6
                ),
                ft.Container(height=8),  # Espacement

                # Valeurs
                ft.Row([
                    ft.Text(
                        f"{self.current:,.2f} {self.unit}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self.color
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        f"/ {self.target:,.2f} {self.unit}",
                        size=12,
                        color=COLORS.TEXTE_SECONDAIRE
                    )
                ])
            ], spacing=0),
            padding=ft.padding.all(16),
            bgcolor=COLORS.CARTES_COMPOSANTS,
            border_radius=8,
            border=ft.border.all(1, COLORS.BORDURES),
            height=100
        )