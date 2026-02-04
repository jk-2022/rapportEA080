import flet as ft

from screens.recapouvragescreen.pannes.pannecard import PanneCard

from .panneform import PanneForm
from .panneupdateform import PanneUpdateForm


# @ft.control
class PanneControl(ft.Card):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.elevation=5
        self.cont=ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.ALWAYS,
            )
        
        self.label= ft.Text(f"les Pannes sur l'ouvrage",
                         text_align=ft.TextAlign.CENTER,
                         color=ft.Colors.GREY_500)

        self.content=ft.Container(
            border_radius=10,
            border=ft.Border.all(1,ft.Colors.GREY_500),
            expand=True,
            content=ft.Column(
                [
                    ft.Row(
                        [
                           self.label
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.cont,
                    ft.Row(
                        [
                            ft.TextButton(
                                "Ajouter",icon=ft.Icons.ADD, on_click=lambda e: self.show_panne()
                            )
                        ]
                    )
                ]
            )
        )

        self.updateData()
    
    def updateData(self):
        donnees=self.state.load_pannes()
        self.donnees=donnees
        self.cont.controls.clear()
        if donnees:
            for panne in donnees:
                self.cont.controls.append(
                    PanneCard(state=self.state,panne=panne,formcontrol=self)
                )
        else:
            self.cont.controls.append(ft.Row(
                [
                    ft.Text("Pas de pannes enrégistré pour cet Ouvrage")
                ],alignment=ft.MainAxisAlignment.CENTER))
            
    def show_panne(self):
        suivi_cont = PanneForm(state=self.state, formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nouvel évènement"),
            content=suivi_cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Enregistrer", on_click=lambda e: suivi_cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

    def close_dlg(self):
        self.page.pop_dialog()

