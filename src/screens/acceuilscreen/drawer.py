import flet as ft 


def page_drawer(handle_change,go_apropos,go_archive,go_stats, go_settings):
    return ft.NavigationDrawer(
            on_change=handle_change,
            controls=[
                    ft.Container(
                        height=120,
                        content=ft.CircleAvatar(content=ft.Icon(icon=ft.Icons.PERSON)),
                        padding=10
                    ),
                    ft.Divider(thickness=2),
                    ft.Column(
                    [
                        ft.Container(
                            content=ft.Column([
                                    ft.ListTile(title=ft.Text("A propos"),leading=ft.Icon(icon=ft.Icons.INFO), on_click= go_apropos),
                                    ft.ListTile(title=ft.Text("Archives"),leading=ft.Icon(icon=ft.Icons.ARCHIVE),on_click= go_archive),
                                    ft.ListTile(title=ft.Text("Staistiques"),leading=ft.Icon(icon=ft.Icons.STACKED_LINE_CHART_OUTLINED),on_click= go_stats),
                                    ft.ListTile(title=ft.Text("Paramètres"),leading=ft.Icon(icon=ft.Icons.SETTINGS),on_click= go_settings),
                                        ]
                            ),
                                ),
                        ft.Divider(thickness=2),
                        ft.Row(
                            [
                                ft.Text("jeankolou19@gmail.com\nTel:90007727")
                            ],alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.TextButton('Nous contacter !'),
                        ),
                    ],
                    expand=1,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                )
            ],
        )