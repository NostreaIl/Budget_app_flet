import flet as ft

def create_donut_chart_with_center():
    """
    Crée un graphique en donut (placeholder temporaire)
    TODO: Implémenter avec une vraie bibliothèque de charts (plotly, matplotlib, etc.)
    """
    # Placeholder temporaire en attendant l'implémentation réelle
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.PIE_CHART_OUTLINE, size=64, color=ft.colors.BLUE_400),
            ft.Container(height=8),
            ft.Text(
                "Graphique en développement",
                size=14,
                color=ft.colors.GREY_500,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=4),
            ft.Text(
                "75% Terminé • 25% Restant",
                size=12,
                color=ft.colors.GREY_400,
                text_align=ft.TextAlign.CENTER
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER),
        width=200,
        height=200,
        border_radius=12,
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
        border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
        alignment=ft.alignment.center
    )
