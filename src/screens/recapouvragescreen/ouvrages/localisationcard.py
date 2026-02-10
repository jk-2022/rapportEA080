import flet as ft
from uix.customtitlelabel import CustomTitleLabel

def LocalisationCard(ouvrage,copyCoords):
    return ft.Card(
        elevation=5,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    border_radius=ft.BorderRadius.only(bottom_right=10),
                    bgcolor="#143a6e",
                    padding=ft.Padding.only(left=5,right=5),
                    content=ft.Text("Localistation",color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ),
                ft.Container(
                    padding=ft.Padding.all(10),
                    border_radius=ft.BorderRadius.only(bottom_right=10, bottom_left=10),
                    border=ft.Border.only(left=ft.BorderSide(width=4, color="#0a1d37")),
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            ft.Row(
                                [
                                    CustomTitleLabel(title="Lieu d'ouvrage",value=f"{ouvrage['lieu']}"),
                                ]
                            ),
                            ft.Row(
                                [
                                    CustomTitleLabel(title="Canton",value=f"{ouvrage['canton']}"),
                                ]
                            ),
                            ft.Row(
                                [
                                    CustomTitleLabel(title="Commune",value=f"{ouvrage['commune']}"),
                                ]
                            ),
                            ft.Row(
                                [
                                    CustomTitleLabel(title="Entreprise",value=f"{ouvrage['entreprise']}"),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        padding=ft.Padding.only(left=5),
                                        expand=True,
                                        content=ft.Row(
                                                    expand=True,
                                                    controls=[
                                                        ft.Text(f"Latitude : {ouvrage['coordonnee_x']} , Longitude : {ouvrage['coordonnee_y']}"),
                                                        ft.IconButton(icon=ft.Icons.COPY, on_click=copyCoords)
                                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                                )
                                    )
                                ]
                            ),
                        ]
                    )
                )
            ]
        )
    )
    