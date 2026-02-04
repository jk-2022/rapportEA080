import flet as ft

from screens.recapouvragescreen.suivi.suivicard import SuiviCard

from .suiviform import SuiviForm
from .suiviupdateform import SuiviUpdateForm
from uix.customtitlelabel import CustomTitleLabel


# @ft.control
class SuiviControl(ft.Card):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.elevation=5
        self.cont=ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.ALWAYS,
            )

        self.label= ft.Text(
            f"les évènements sur l'ouvrage",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_500
            )

        self.content=ft.Container(
            border_radius=10,
            border=ft.Border.all(1,ft.Colors.AMBER_500),
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
                                "Ajouter",icon=ft.Icons.ADD, on_click=lambda e: self.show_suivi()
                            )
                        ]
                    )
                ]
            )
        )

        self.updateData()
    
    def updateData(self):
        donnees=self.state.load_suivis()
        self.donnees=donnees
        self.cont.controls.clear()
        if donnees:
            for suivi in donnees:
                self.cont.controls.append(
                    SuiviCard(state=self.state,suivi=suivi,formcontrol=self)
                )
        else:
            self.cont.controls.append(
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Text("Pas de données suivis enrégistré")
                    ],alignment=ft.MainAxisAlignment.CENTER
                )
                )
            )
        

    def show_suivi(self):
        suivi_cont = SuiviForm(state=self.state, formcontrol=self)
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

