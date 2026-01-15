import flet as ft

def create_donut_chart_with_center():
    """
    Crée un graphique en donut avec texte central
    Compatible avec Flet 0.80.1
    """
    # Bordures pour les sections (transparente)
    normal_border = ft.BorderSide(width=0, color="#FFFFFF00")

    # Sections du graphique
    sections = [
        ft.PieChartSection(
            value=75,
            color=ft.colors.GREEN_500,
            radius=100,
            border_side=normal_border,
        ),
        ft.PieChartSection(
            value=25,
            color=ft.colors.GREY_300,
            radius=100,
            border_side=normal_border,
        ),
    ]

    # Texte central
    center_text = ft.Container(
        content=ft.Column([
            ft.Text("75%", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_500),
            ft.Text("Terminé", size=12, color=ft.colors.GREY_400),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
    )

    # Graphique pie chart
    chart = ft.PieChart(
        sections=sections,
        sections_space=2,
        center_space_radius=60,  # Espace au centre pour le texte
        expand=True,
    )

    # Stack pour superposer le texte sur le graphique
    return ft.Container(
        content=ft.Stack([
            chart,
            center_text,
        ]),
        width=200,
        height=200,
        alignment=ft.alignment.center,
    )
