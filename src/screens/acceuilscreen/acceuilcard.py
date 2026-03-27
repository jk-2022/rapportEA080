import flet as ft

class AcceuilCard(ft.Card):
    def __init__(self, title, img, change_view):
        super().__init__()
        self.elevation=10
        self.height=120
        self.width=110
        
        self.content=ft.Container(
            on_click=change_view,
            ink=True,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        padding= ft.Padding.all(10),
                        height=70,
                        expand=True,
                        image=ft.DecorationImage(
                            src=img,
                            # fit=ft.BoxFit.COVER
                        )
                    ),
                    ft.Container(
                        height=40,
                        # bgcolor=ft.Colors.RED,
                        content=ft.Row(
                            [
                                ft.Text(f"{title}",width=80,
                                        text_align=ft.TextAlign.CENTER,
                                        weight=ft.FontWeight.BOLD, size=14
                                        )
                            ], alignment=ft.MainAxisAlignment.CENTER
                        )
                    )
                ]
            )
        )
        
    async def selectouvrage(self, e):
        self.state.selected_ouvrage=self.ouvrage
        await self.page.push_route("/projet/list-ouvrage/recap-ouvrage")
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    