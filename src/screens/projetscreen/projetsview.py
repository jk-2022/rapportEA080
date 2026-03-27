
import asyncio
import flet as ft

from appstate import Projet
from screens.projetscreen.projetcard import ProjetCard
from screens.projetscreen.projetform import ProjetForm
from utils.constants import app_bar, champ_recherche

class ProjectView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.route="/projet"
        self.state=state
        self._query = ""
        
        self.project_list = ft.Column(
            expand=True
            )
        
        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, 
            on_click= lambda e :self.show_projet()
            )
        
        self.barre_recherche=champ_recherche("projet",self._on_search)

        self.controls=[ft.SafeArea(
            ft.Column(
                controls=[
                    app_bar(title=f"Tous vos projets"),
                    ft.Container(
                        padding=ft.Padding.only(left=10,right=10),
                        content=self.barre_recherche
                        ),
                    self.project_list
                        ],expand=True,scroll=ft.ScrollMode.ALWAYS
                    ),expand=True
                )
        ]
        # self._refresh()
 
    def show_projet(self):
        projet_content = ProjetForm(self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nouveau projet"),
            content=projet_content,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e :self.close_dlg()),
                ft.TextButton("Enregistrer", on_click=lambda e :projet_content.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def _filtered(self) -> list[Projet]:
        q = self._query.lower()
        return [p for p in self.state.load_projets() if q in p.name.lower() or q in p.title.lower()]
        
    def _refresh(self):
        self.project_list.controls.clear()
        projets= self._filtered()
        if projets:
            for projet in projets:
                self.project_list.controls.append(
                ProjetCard(state=self.state, projet=projet,formcontrol=self)
            )
        self.update()
        
    def _on_search(self, e):
        self._query = self.barre_recherche.value
        self._refresh()
        
    def did_mount(self):
        self._refresh()
        
    def close_dlg(self):
        self.page.pop_dialog()
