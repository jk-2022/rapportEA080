
import flet as ft
from donnees import donnees
from myaction.myaction_village import create_village
from uix.custominputfield import CustomInputField


# @control
class VillageForm(ft.Container):
    def __init__(self, formcontrol):
        super().__init__()
        self.padding = 0
        self.width=500
        self.formcontrol=formcontrol
        
        self.prefecture = ft.Dropdown(
            label="Préfecture",
            value="Oti-Sud",
            options=[ft.dropdown.Option(val) for val in donnees.keys()],
            expand=True,
            on_text_change=lambda e :self.update_commune(e))

        self.commune = ft.Dropdown(
            label="Commune",
            expand=True)
                
        self.canton = CustomInputField(label="Canton")
        self.localite = CustomInputField(label="Village")
        self.coordonnee_x = CustomInputField(label="Coordonnee X")
        self.coordonnee_y = CustomInputField(label="Coordonnee Y")
        
        self.ressource = ft.Dropdown(
            label="Resoource utilisée", 
            value="Rivières",
            options=[ft.dropdown.Option("Rivières"), 
                     ft.dropdown.Option("Barrage"), 
                     ft.dropdown.Option("Fleuves"), 
                     ft.dropdown.Option("Sous-sol"), 
                    ],
            expand=True)
        
        self.status = ft.Dropdown(
            label="Status projet", 
            value="Aucun Projet encours",
            options=[
                    ft.dropdown.Option("Aucun Projet encours"), 
                    ft.dropdown.Option("Projet en cours"), 
                    ft.dropdown.Option("Projet suspendu"),
                    ],
            expand=True)
        
        self.observation = CustomInputField(label="Observation",
                                            max_lines=4, multiline=True,
                                            expand=True)

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

    def recupererDonnees(self):
        prefecture = self.prefecture.value
        commune = self.commune.value
        if commune=="" or commune==None:
            return self.show_snackbar(f"⚠️ Inserer la commune")
        canton = self.canton.value
        if canton=="" or canton==None:
            return self.show_snackbar(f"⚠️ Inserer le canton")
        localite = self.localite.value
        if localite=="" or localite==None:
            return self.show_snackbar(f"⚠️ Inserer le localite")
        coordonnee_x = self.coordonnee_x.value or 0
        coordonnee_y = self.coordonnee_y.value or 0
        ressource = self.ressource.value
        status = self.status.value
        observation = self.observation.value
        return {"prefecture": prefecture, "commune": commune, "canton": canton.capitalize(), "localite": localite.capitalize(), "coordonnee_x": coordonnee_x, "coordonnee_y": coordonnee_y, "ressource": ressource,"status": status, "observation": observation}


    def SaveData(self):
        donnees = self.recupererDonnees()
        if donnees:
            create_village(**donnees)
            self.formcontrol.load_village()
            self.page.pop_dialog()
        else:
            return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Inserer le Nom du village")))
