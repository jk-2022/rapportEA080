import flet as ft

def main(page: ft.Page):
    page.window.width = 400
    page.window.height = 720
    page.padding = 0
    page.spacing = 0

    # Section 1: Illustration (Haut)
    upper_section = ft.Container(
        expand=2,
        bgcolor=ft.Colors.WHITE,
        image=ft.DecorationImage(
            src="assets/icon.png", # Remplacez par votre image
            fit=ft.BoxFit.COVER),
        # content=,
        alignment=ft.Alignment.CENTER
    )
    

    # Section 2: Contenu Bleu (Bas)
    # L'astuce : le fond du container parent est BLANC, mais le container lui-même est BLEU
    # avec un arrondi uniquement en haut à gauche pour créer l'effet de l'image.
    lower_section = ft.Container(
        expand=3,
        bgcolor=ft.Colors.WHITE, # Couleur de "fond" pour l'arrondi
        content=ft.Container(
            bgcolor="#0a1d37", # Bleu très foncé comme sur l'image
            padding=ft.padding.all(40),
            border_radius=ft.border_radius.only(top_left=80),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Let's connect\nwith each other",
                        size=35,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "A message is a discrete communication intended by the source transmitter.",
                        color=ft.Colors.GREY_400,
                        size=16,
                    ),
                    ft.Container(expand=True), # Espace vide pour pousser le bouton vers le bas
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Text("Let's Start", color=ft.Colors.WHITE, size=18),
                                ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#ff4081", # Rose/Rose vif
                        height=60,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15),
                        ),
                        on_click=lambda _: print("C'est parti !"),
                    ),
                ],
                spacing=20,
            ),
        ),
    )

    page.add(
        ft.Column(
            [upper_section, lower_section],
            expand=True,
            spacing=0,
        )
    )

ft.run(main)