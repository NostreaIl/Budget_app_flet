import flet as ft

def create_donut_chart_with_center():
    sections = [
        ft.PieChartSection(75, "Terminé", ft.colors.GREEN_500),
        ft.PieChartSection(25,"Restant", ft.colors.GREY_300),
    ]
    color = [
        ft.colors.GREEN_500,
        ft.colors.GREY_300
    ]
    # Texte central
    center_text = ft.Container(
        content=ft.Column([
            ft.Text("75%", size = 24, weight = ft.FontWeight.BOLD),
            ft.Text("25%", size = 24, weight = ft.FontWeight.BOLD),
            ], alignement = ft.MainAxisAlignment.CENTER),
            alignment = ft.alignment.center,
        )
