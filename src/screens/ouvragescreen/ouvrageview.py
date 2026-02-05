import flet as ft
import asyncio
from .ouvragecard import OuvrageCard

class OuvrageView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.state=state
        self.route = "/projet/list-ouvrage"
        self.projet=self.state.selected_projet
        self.ouvrage_list = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        )
        self.searsh_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click= self.go_filter_page
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click=self.go_create_page
            )
        self.nbre_ouvrage_cnt=ft.Row(
                                    [
                                    ],alignment=ft.MainAxisAlignment.CENTER
                                )
        # self.stat_button = Button("Stast.",icon=Icons.AUTO_GRAPH_OUTLINED, on_click=self.go_static_page)

        self.controls.append(ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(title=ft.Text("Tous ouvrages confondus")),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.searsh_button,
                                self.nbre_ouvrage_cnt,
                                self.add_button,
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.Padding.only(left=10, right=10)
                    ),
                    self.ouvrage_list
                        ],
                        # expand=True,scroll=ScrollMode.ALWAYS
                    ),expand=True
                )
            )
        
        self.load_ouvrages()

    def load_ouvrages(self):
        ouvrages=self.state.load_ouvrages()
        nbre_ouvrage=len(ouvrages)
        self.nbre_ouvrage_cnt.controls.append(ft.Text(f"Total : {nbre_ouvrage}", size=12))
        self.ouvrage_list.controls.clear()
        if ouvrages:
            for ouvrage in ouvrages:
                self.ouvrage_list.controls.append(
                OuvrageCard(state=self.state, ouvrage=ouvrage, formcontrol=self)
            )
    
    async def go_create_page(self,e):
        await self.page.push_route("/projet/list-ouvrage/create-ouvrage")

    async def go_filter_page(self,e):
        await self.page.push_route("/projet/list-ouvrage/filtrer-ouvrage")
        
    def close_dlg(self):
        self.page.pop_dialog()
