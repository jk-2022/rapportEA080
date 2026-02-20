import asyncio
import flet as ft

# FLET 0.80.5 RESPONSIVE PORTFOLIO WEBSITE

ARTICLES = [
    {
        "id": 1,
        "title": "Projet Immobilier",
        "image": "https://picsum.photos/900/500?1",
        "description": "Plateforme de gestion immobilière développée avec Django et Flet."
    },
    {
        "id": 2,
        "title": "Application Chat Temps Réel",
        "image": "https://picsum.photos/900/500?2",
        "description": "Messagerie temps réel utilisant Django Channels et WebSocket."
    },
    {
        "id": 3,
        "title": "Système de Rapport PDF",
        "image": "https://picsum.photos/900/500?3",
        "description": "Application de génération PDF/DOCX multiplateforme."
    },
    {
        "id": 4,
        "title": "Système de Rapport PDF",
        "image": "https://picsum.photos/900/500?4",
        "description": "Application de génération PDF/DOCX multiplateforme."
    },
    {
        "id": 5,
        "title": "Système de Rapport PDF",
        "image": "https://picsum.photos/900/500?5",
        "description": "Application de génération PDF/DOCX multiplateforme."
    },
]

banner_index = 0

def main(page: ft.Page):
    page.title = "Portfolio Moderne"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.window.width = 500
    page.scroll = ft.ScrollMode.AUTO

    # ---------------- BANNER AUTO SLIDER ----------------
    banner_images = [
        "https://picsum.photos/1600/600?10",
        "https://picsum.photos/1600/600?11",
        "https://picsum.photos/1600/600?12",
    ]


    banner_image = ft.Image(
        src=banner_images[0],
        fit=ft.BoxFit.COVER,
        width=float("inf"),
    )

    banner = ft.Container(
        height=250,
        content=banner_image,
    )

    
    async def auto_slider():
        global banner_index
        while True:
            await asyncio.sleep(3)
            banner_index = (banner_index + 1) % len(banner_images)
            banner_image.src = banner_images[banner_index]
            banner.update()

    page.run_task(auto_slider)


    # ---------------- NAVBAR RESPONSIVE ----------------

    def navbar():
        is_mobile = page.width < 768

        if is_mobile:
            menu = ft.PopupMenuButton(
                icon_color="white",
                items=[
                    ft.PopupMenuItem(content=ft.Text("Accueil"), on_click=lambda e: page.go("/")),
                    ft.PopupMenuItem(content=ft.Text("À propos"), on_click=lambda e: page.go("/about")),
                    ft.PopupMenuItem(content=ft.Text("Contact"), on_click=lambda e: page.go("/contact")),
                ]
            )

            right_content = menu
        else:
            right_content = ft.Row(
                spacing=20,
                controls=[
                    ft.Button("Accueil", on_click=lambda e: page.go("/")),
                    ft.Button("À propos", on_click=lambda e: page.go("/about")),
                    ft.Button("Contact", on_click=lambda e: page.go("/contact")),
                ],
            )

        return ft.Container(
            bgcolor="#0f172a",
            padding=20,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("MON PORTFOLIO", size=20, weight=ft.FontWeight.BOLD, color="white"),
                    right_content,
                ],
            ),
        )

    # ---------------- FOOTER ----------------
    def footer():
        return ft.Container(
            bgcolor="#f1f5f9",
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("© 2026 Jean Kolou - Tous droits réservés"),
                    ft.Text("Développé avec Flet 0.80.5"),
                ],
            ),
        )

    # ---------------- PORTFOLIO CARDS ----------------
    def article_card(article):
        return ft.Container(
            col={"xs": 12, "sm": 6, "md": 4},
            padding=10,
            content=ft.Container(
                bgcolor="white",
                border_radius=15,
                animate_scale=200,
                # on_hover=lambda e: e.control.scale(1.03 if e.data == "true" else 1),
                content=ft.Column(
                    controls=[
                        ft.Image(src=article["image"], height=200, fit=ft.BoxFit.COVER),
                        ft.Container(
                            padding=15,
                            content=ft.Column(
                                controls=[
                                    ft.Text(article["title"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Button(
                                        "Voir détails",
                                        on_click=lambda e, a=article: page.go(f"/detail/{a['id']}")
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        )

    # ---------------- PAGES ----------------
    def home_view():
        return ft.View(
            route="/",
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            padding=0,
            spacing=0,
            controls=[
                navbar(),
                banner,
                ft.Container(
                    padding=40,
                    expand=True,
                    content=ft.ResponsiveRow(
                        controls=[article_card(a) for a in ARTICLES]
                    ),
                ),
                footer(),
            ],
        )

    def detail_view(article_id):
        article = next((a for a in ARTICLES if a["id"] == article_id), None)
        if not article:
            return home_view()

        return ft.View(
            route=f"/detail/{article_id}",
            controls=[
                navbar(),
                ft.Container(
                    padding=50,
                    content=ft.Column(
                        controls=[
                            ft.Text(article["title"], size=32, weight=ft.FontWeight.BOLD),
                            ft.Image(src=article["image"], height=350, fit=ft.BoxFit.COVER),
                            ft.Text(article["description"], size=18),
                            ft.Button("Retour", on_click=lambda e: page.go("/")),
                        ]
                    ),
                ),
                footer(),
            ],
        )

    def about_view():
        return ft.View(
            route="/about",
            padding=0,
            spacing=0,
            controls=[
                navbar(),
                ft.Container(
                    padding=50,
                    expand=True,
                    content=ft.Text(
                        "Développeur Python spécialisé Django & Flet.\n"
                        "Création d'applications web modernes, mobiles et systèmes métier.",
                        size=20,
                    ),
                ),
                footer(),
            ],
        )

    def contact_view():
        return ft.View(
            route="/contact",
            padding=0,
            spacing=0,
            controls=[
                navbar(),
                ft.Container(
                    padding=50,
                    content=ft.Column(
                        width=500,
                        controls=[
                            ft.Text("Contact", size=28, weight=ft.FontWeight.BOLD),
                            ft.TextField(label="Nom"),
                            ft.TextField(label="Email"),
                            ft.TextField(label="Message", multiline=True, min_lines=4),
                            ft.Button("Envoyer"),
                        ],
                    ),
                ),
                footer(),
            ],
        )

    # ---------------- ROUTING ----------------
    def route_change():
        page.views.clear()

        if page.route == "/":
            page.views.append(home_view())

        elif page.route.startswith("/detail/"):
            article_id = int(page.route.split("/")[-1])
            page.views.append(detail_view(article_id))

        elif page.route == "/about":
            page.views.append(about_view())

        elif page.route == "/contact":
            page.views.append(contact_view())

        page.update()
        
    page.views.append(home_view())
    page.on_route_change = route_change
    # page.go("/")


ft.run(main)
