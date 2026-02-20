import flet as ft
import asyncio

# ================= ENTREPRISE EAU POTABLE - FLET 0.80.5 =================

PRODUCTS = [
    {"id": 1, "title": "Bidon 0.5L", "image": "https://picsum.photos/800/600?water1", "desc": "Format pratique pour usage individuel."},
    {"id": 2, "title": "Bidon 1.5L", "image": "https://picsum.photos/800/600?water2", "desc": "Idéal pour la famille et le bureau."},
    {"id": 3, "title": "Bidon 5L", "image": "https://picsum.photos/800/600?water3", "desc": "Solution économique pour la maison."},
    {"id": 4, "title": "Bonbonne 18L", "image": "https://picsum.photos/800/600?water4", "desc": "Adaptée aux distributeurs d'eau."},
]


def main(page: ft.Page):
    page.title = "AquaPure - Eau Potable"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # ================= HERO SLIDER =================

    slider_images = [
        "https://picsum.photos/1600/700?water10",
        "https://picsum.photos/1600/700?water11",
        "https://picsum.photos/1600/700?water12",
    ]

    slider_index = 0

    hero_image = ft.Image(
        src=slider_images[0],
        fit=ft.BoxFit.COVER,
        width=float("inf"),
        height=500,
        opacity=1,
    )

    hero = ft.Stack(
        controls=[
            hero_image,
            ft.Container(bgcolor="#00000066", width=float("inf"), height=500),
            ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("AquaPure",
                                size=45,
                                weight=ft.FontWeight.BOLD,
                                color="white"),
                        ft.Text("Une eau pure, saine et accessible à tous",
                                size=20,
                                color="white"),
                        ft.Button("Voir nos produits", on_click=lambda e: page.go("/products")),
                    ],
                ),
            ),
        ]
    )

    async def auto_slider():
        nonlocal slider_index
        while True:
            await asyncio.sleep(4)
            slider_index = (slider_index + 1) % len(slider_images)
            hero_image.opacity = 0
            hero_image.update()
            await asyncio.sleep(0.4)
            hero_image.src = slider_images[slider_index]
            hero_image.opacity = 1
            hero_image.update()

    page.run_task(auto_slider)

    # ================= NAVBAR =================

    def navbar():
        is_mobile = page.width < 768

        if is_mobile:
            menu = ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Accueil", on_click=lambda e: page.go("/")),
                    ft.PopupMenuItem(text="Produits", on_click=lambda e: page.go("/products")),
                    ft.PopupMenuItem(text="À propos", on_click=lambda e: page.go("/about")),
                    ft.PopupMenuItem(text="Contact", on_click=lambda e: page.go("/contact")),
                ]
            )
            right = menu
        else:
            right = ft.Row(
                spacing=20,
                controls=[
                    ft.Button("Accueil", on_click=lambda e: page.go("/")),
                    ft.Button("Produits", on_click=lambda e: page.go("/products")),
                    ft.Button("À propos", on_click=lambda e: page.go("/about")),
                    ft.Button("Contact", on_click=lambda e: page.go("/contact")),
                ],
            )

        return ft.Container(
            bgcolor="#0ea5e9",
            padding=20,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("AquaPure", size=22, weight=ft.FontWeight.BOLD, color="white"),
                    right,
                ],
            ),
        )

    # ================= FOOTER =================

    def footer():
        return ft.Container(
            bgcolor="#e0f2fe",
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("© 2026 AquaPure - Production d'eau potable"),
                    ft.Text("Qualité • Hygiène • Confiance"),
                ],
            ),
        )

    # ================= PRODUCT CARD =================

    def product_card(product):
        card = ft.Container(
            col={"xs": 12, "sm": 6, "md": 3},
            padding=15,
            content=ft.Container(
                bgcolor="white",
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=15),
                content=ft.Column(
                    controls=[
                        ft.Image(src=product["image"], height=200, fit=ft.BoxFit.COVER),
                        ft.Container(
                            padding=15,
                            content=ft.Column(
                                controls=[
                                    ft.Text(product["title"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(product["desc"]),
                                    ft.Button("Détails",
                                              on_click=lambda e, p=product: page.go(f"/detail/{p['id']}")),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        )

        def hover(e):
            card.content.scale = 1.05 if e.data == "true" else 1
            card.update()

        card.on_hover = hover
        return card

    # ================= VIEWS =================

    def home_view():
        return ft.View(
            route="/",
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                navbar(),
                hero,
                ft.Container(
                    padding=50,
                    content=ft.Column(
                        controls=[
                            ft.Text("Nos Formats Disponibles", size=30, weight=ft.FontWeight.BOLD),
                            ft.ResponsiveRow(
                                controls=[product_card(p) for p in PRODUCTS]
                            ),
                        ]
                    ),
                ),
                footer(),
            ],
        )

    def products_view():
        return ft.View(
            route="/products",
            controls=[
                navbar(),
                ft.Container(
                    padding=50,
                    content=ft.ResponsiveRow(
                        controls=[product_card(p) for p in PRODUCTS]
                    ),
                ),
                footer(),
            ],
        )

    def detail_view(pid):
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            return home_view()

        return ft.View(
            route=f"/detail/{pid}",
            controls=[
                navbar(),
                ft.Container(
                    padding=60,
                    content=ft.Column(
                        controls=[
                            ft.Text(product["title"], size=32, weight=ft.FontWeight.BOLD),
                            ft.Image(src=product["image"], height=400, fit=ft.BoxFit.COVER),
                            ft.Text(product["desc"], size=18),
                            ft.Button("Retour", on_click=lambda e: page.go("/products")),
                        ]
                    ),
                ),
                footer(),
            ],
        )

    def about_view():
        return ft.View(
            route="/about",
            controls=[
                navbar(),
                ft.Container(
                    padding=60,
                    content=ft.Text(
                        "AquaPure est une entreprise spécialisée dans la production et la distribution d'eau potable certifiée.\n"
                        "Nous garantissons qualité, hygiène et respect des normes sanitaires.",
                        size=20,
                    ),
                ),
                footer(),
            ],
        )

    def contact_view():
        return ft.View(
            route="/contact",
            controls=[
                navbar(),
                ft.Container(
                    padding=60,
                    content=ft.Column(
                        width=500,
                        controls=[
                            ft.Text("Contactez-nous", size=28, weight=ft.FontWeight.BOLD),
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

    # ================= ROUTING =================

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_view())
        elif page.route == "/products":
            page.views.append(products_view())
        elif page.route.startswith("/detail/"):
            pid = int(page.route.split("/")[-1])
            page.views.append(detail_view(pid))
        elif page.route == "/about":
            page.views.append(about_view())
        elif page.route == "/contact":
            page.views.append(contact_view())

        # page.update()
    page.views.append(home_view())
    page.on_route_change = route_change
    page.go("/")


ft.run(main)