import flet as ft
import flet_charts as fch

def create_donut_chart_with_center():
    """
    Crée un graphique en donut avec texte central
    Compatible avec Flet 0.80.2
    """
    # Bordures pour les sections (transparente)
    normal_border = ft.BorderSide(width=0, color="#FFFFFF00")

    # Sections du graphique
    sections = [
        fch.PieChartSection(
            value=75,
            color=ft.Colors.GREEN_500,
            radius=100,
            border_side=normal_border,
        ),
        fch.PieChartSection(
            value=25,
            color=ft.Colors.GREY_300,
            radius=100,
            border_side=normal_border,
        ),
    ]

    # Création du graphique (variable manquante)
    pie_chart = fch.PieChart(
        sections=sections,
        sections_space=0,
        center_space_radius=40,  # Trou au centre pour effet donut
        expand=True,
    )

    # Texte central (variable manquante)
    center_text = ft.Container(
        content=ft.Text(
            "75%",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        alignment=ft.Alignment(0,0),
    )

    # Stack pour superposer le texte sur le graphique
    return ft.Container(
        content=ft.Stack([
            pie_chart,      # ← Corrigé (était 'chart')
            center_text,    # ← Maintenant défini
        ]),
        width=200,
        height=200,
        alignment=ft.alignment.Alignment(0,0),  # ← Corrigé syntaxe
    )
