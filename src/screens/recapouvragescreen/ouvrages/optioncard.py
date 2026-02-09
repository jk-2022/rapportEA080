import flet as ft

def OptionCard(showUpdateData,shareData):
    return ft.Card(
        elevation=5,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(10),
                    border_radius=ft.BorderRadius.only(bottom_right=10, bottom_left=10),
                    border=ft.Border.only(left=ft.BorderSide(width=4, color="#0a1d37")),
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.EDIT,
                                                  icon_color=ft.Colors.GREEN_500,
                                                  on_click=showUpdateData),
                                    ft.IconButton(icon=ft.Icons.SHARE,
                                                  on_click=shareData
                                                  ),
                                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
                            ),
                        ]
                    )
                )
            ]
        )
    )
    