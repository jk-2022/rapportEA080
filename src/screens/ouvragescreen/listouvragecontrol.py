import flet as ft

from screens.ouvragescreen.filtreouvragecontrol import FiltreOuvrageControl
from .ouvragecard import OuvrageCard

class ListOuvrageControl(ft.Column):
    def __init__(self,state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        self.projet=self.state.selected_projet
        self.ouvrage_list = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
            )
        self.searsh_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click= lambda e :self.go_filter_content()
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click= lambda e : self.formcontrol.change_content("create-ouvrage-content")
            )
        self.nbre_ouvrage_cnt=ft.Row(
                                    [
                                    ],alignment=ft.MainAxisAlignment.CENTER
                                )

        self.controls= [
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
                        ]
            
        
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

    def go_filter_content(self):
        self.formcontrol.change_content("filtre-content")
