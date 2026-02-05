
import asyncio
import flet as ft

from screens.projetscreen.projetcard import ProjetCard
from screens.projetscreen.projetform import ProjetForm

class ProjectView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.route="/projet"
        self.state=state
        self.project_list = ft.Column(
            expand=1,
            scroll=ft.ScrollMode.ALWAYS
            )
        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, 
            on_click= lambda e :self.show_projet()
            )

        self.controls=[ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(
                            title=ft.Text("Projets")
                        ),
                    ft.Container(
                        padding=ft.Padding.only(right=20),
                        content=ft.Row(
                        [
                            ft.Button("Statistiques", 
                                      on_click=self.go_to_static, 
                                      icon=ft.Icons.STACKED_LINE_CHART_OUTLINED)
                        ],alignment=ft.MainAxisAlignment.END
                    )
                    ),
                    self.project_list
                        ],expand=True,scroll=ft.ScrollMode.ALWAYS
                    ),expand=True
                )
        ]
        self.load_projects()
    
    def load_projects(self):
        self.project_list.controls.clear()
        projets=self.state.load_projets()
        if projets:
            for projet in projets:
                self.project_list.controls.append(
                ProjetCard(state=self.state, projet=projet,formcontrol=self)
            )
        
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
        
    async def go_to_static(self,e):
        await self.page.push_route("/stats")
        
    def close_dlg(self):
        self.page.pop_dialog()
