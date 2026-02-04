
import flet as ft
from donnees import donnees
from myaction.myaction_village import update_village, Village
from uix.custominputfield import CustomInputField


# @control
class VillageUpdateForm(ft.Container):
    def __init__(self,village:Village, formcontrol):
        super().__init__()
        self.padding = 0
        self.width=500
        self.village=village
        self.formcontrol=formcontrol
        
        self.prefecture = ft.Dropdown(
            label="Préfecture",
            value=village.prefecture,
            options=[ft.dropdown.Option(val) for val in donnees.keys()],
            expand=True,
            on_text_change=lambda e :self.update_commune(e))

        self.commune = ft.Dropdown(
            label="Commune",
            value=village.commune,
            expand=True)
                
        self.canton = CustomInputField(
            label="Canton",
            value=village.canton)
        self.localite = CustomInputField(
            label="Village",
            value=village.localite)
        self.coordonnee_x = CustomInputField(
            label="Coordonnee X",
            value=village.coordonnee_x)
        self.coordonnee_y = CustomInputField(
            label="Coordonnee Y",
        value=village.coordonnee_y)
        
        self.ressource = ft.Dropdown(
            label="Ressource utiliée", 
            value=village.ressource,
            options=[ft.dropdown.Option("Rivières"), 
                     ft.dropdown.Option("Barrage"), 
                     ft.dropdown.Option("Fleuves"), 
                     ft.dropdown.Option("Sous-sol"), 
                    ],
            expand=True)
        
        self.status = ft.Dropdown(
            label="Status projet", 
            value=village.status,
            options=[
                    ft.dropdown.Option("Aucun Projet encours"), 
                    ft.dropdown.Option("Projet en cours"), 
                    ft.dropdown.Option("Projet suspendu"),
                    ],
            expand=True)
        
        self.observation = CustomInputField(label="Observation",
                                            max_lines=4, multiline=True,
                                            expand=True,
                                            value=village.observation
                                            )

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
                                    self.prefecture,
                                    self.commune,
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.canton, self.localite
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.coordonnee_x,self.coordonnee_y,
                                    # ft.IconButton(icon=ft.Icons.ADD_LOCATION_ALT_OUTLINED,
                                                #   on_click=self.handle_location_service_enabled)
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.ressource,
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.status
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.observation
                                ]
                            ),
                    ]
                )
            )
        )
        
    def show_snackbar(self, message):
        self.page.show_dialog(ft.SnackBar(ft.Text(message)))
        
    def update_commune(self,e):
        self.commune.options.clear()
        for key in donnees.keys():
            if self.prefecture.value==key:
                for value in donnees[key]:
                    self.commune.options.append(ft.dropdown.Option(value))
        self.commune.update()

    def SaveData(self):
        self.village.prefecture = self.prefecture.value
        self.village.commune = self.commune.value
        self.village.canton = self.canton.value.capitalize()
        self.village.localite = self.localite.value.capitalize()
        self.village.coordonnee_x = self.coordonnee_x.value or 0
        self.village.coordonnee_y = self.coordonnee_y.value or 0
        self.village.ressource = self.ressource.value
        self.village.status = self.status.value
        self.village.observation = self.observation.value
        update_village(village=self.village)
        self.formcontrol.load_village()
        self.page.pop_dialog() 


