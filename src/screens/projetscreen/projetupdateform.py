import flet as ft
from uix.custominputfield import CustomInputField
from myaction.myaction_projet import update_projet, Projet

# @ft.control
class ProjetUpdateForm(ft.Container):
    def __init__(self, projet:Projet, formcontrol):
        super().__init__()
        self.padding = 0
        self.projet=projet
        self.width=450
        self.formcontrol=formcontrol
        self.name = CustomInputField(
            label="Nom projet",
            value=projet.name)
        self.title = CustomInputField(
            label="Titre", 
            multiline=True, 
            max_lines=3,
            value=projet.title
            )
        self.secteurs=CustomInputField(
            label="Secteurs",
            multiline=True, 
            max_lines=2,
            value=projet.secteurs,
            )

        self.content = ft.Container(
            # elevation=20,
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


    def SaveData(self):
        self.projet.name=self.name.value
        self.projet.title=self.title.value
        self.projet.secteurs=self.secteurs.value
        # print(self.projet)
        update_projet(self.projet)
        self.formcontrol.formcontrol.load_projects()
        self.page.pop_dialog()


