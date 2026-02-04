
import flet as ft

from datetime import datetime
from myaction.myaction_projet import create_projet
from uix.custominputfield import CustomInputField


# @control
class ProjetForm(ft.Container):
    def __init__(self, formcontrol):
        super().__init__()
        self.padding = 0
        self.width=500
        self.formcontrol=formcontrol
        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date = ft.Text(f"{dateTime}", height=40)
        self.name = CustomInputField(
            label="projet ")
        self.title = CustomInputField(
            label="Titre ", 
            multiline=True, 
            max_lines=3)
        self.secteurs=CustomInputField(
            label="Secteurs", 
            multiline=True, 
            max_lines=2)

        self.content = ft.Container(
            # elevation=10,
            content=ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        ft.Row(
                            controls=[
                                self.name,
                            ]
                        ),
                        self.title,
                        self.secteurs
                    ]
                )
            )
        )

    def recupererDonnees(self):
        name = self.name.value
        if name=="" or name==None:
            return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Inserer le Nom du Projet")))
        name=name.upper()
        title = self.title.value
        secteurs = self.secteurs.value
        return {"name": name, "title": title, "secteurs": secteurs}

    def SaveData(self):
        donnees = self.recupererDonnees()
        if donnees:
            create_projet(**donnees)
            self.formcontrol.load_projects()
            self.page.pop_dialog()
        else:
            return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Inserer le Nom du projet")))
