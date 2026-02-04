import os
import flet as ft


class ApropoView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        bac_cnt=ft.Container(height=40,
                          content=ft.Row(
                              controls=[
                                  ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                             on_click= lambda e: self.page.on_view_pop()),
                                  ft.Text(" ")
                                ]
                            )
                          )
        fichier = os.path.join(os.path.dirname(__file__), "apropos.txt")
        with open(fichier,"r",encoding='utf-8') as f:
            text=f.read()

        apropo_cont=ft.ListView(
            expand=True,
            controls=[
                ft.Text(text)
            ]
        )
        self.controls=[
            ft.SafeArea(
                ft.Column(
                    expand=True,
                    controls=[
                        bac_cnt,
                        apropo_cont,
                    ]
                ),
                expand=True
            )]
        
    async def go_back_to_products(self,e):
        self.page.push_route('/acceuil')
