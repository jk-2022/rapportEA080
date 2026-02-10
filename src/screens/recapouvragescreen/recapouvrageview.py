import flet as ft

from screens.recapouvragescreen.ouvrages.editouvragecontrol import EditOuvrageControl
from screens.recapouvragescreen.recapcontrol import RecapControl

class RecapOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.padding=0
        self.state=state
        self.route = "/projet/list-ouvrage/recap-ouvrage"
        
        self.control_content=RecapControl(state=self.state,formcontrol=self)

        self.controls=[
            ft.AppBar(
                    title=ft.Text("RECAP"), bgcolor=ft.Colors.SURFACE_BRIGHT,
                    actions=[
                        ft.IconButton(icon=ft.Icons.ARCHIVE,
                                      on_click=self.page_go_archive)
                    ]
                ),
            self.control_content
            
        ]
        
    def change_content(self,content):
        self.control_content.controls.clear()
        if content=="edit-ouvrage-content":
            self.control_content.controls.append(
                EditOuvrageControl(state=self.state, formcontrol=self)
            )
        if content=="recap-ouvrage-content":
            self.control_content.controls.append(
                RecapControl(state=self.state, formcontrol=self)
            )
            
    async def page_go_archive(self):
        await self.page.push_route('/archive')
