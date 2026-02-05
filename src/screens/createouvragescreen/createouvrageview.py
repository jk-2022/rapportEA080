import flet as ft 
from typing import Callable
from donnees import *
from myaction.myaction_ouvrage import create_ouvrage
from uix.custominputfield import CustomInputField
from myaction.myaction_entreprise import create_entreprise

try:
    import flet_geolocator as ftg
except:
    pass

class CreateOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.route = "/projet/list-ouvrage/create-ouvrage" 
        # self.geo = ftg.Geolocator(
        #     configuration=ftg.GeolocatorConfiguration(
        #         accuracy=ftg.GeolocatorPositionAccuracy.LOW
        #         ),
        #     on_position_change=self.handle_position_change,
        #     on_error=lambda e : self.show_snackbar(f"Error: {e.data}"),
        #     )
        # self.location_settings_dlg = self.get_dialog(self.handle_open_location_settings)
        # self.app_settings_dlg = self.get_dialog(self.handle_open_app_settings)
        self.prefecture = ft.Dropdown(
            label="Préfecture",
            value="Oti-Sud",
            options=[ft.dropdown.Option(val) for val in donnees.keys()],
            expand=True,
            on_text_change=lambda e :self.update_commune(e))

        self.commune = ft.Dropdown(
            label="Commune",
            expand=True)
        
        self.choix_entreprise = ft.Dropdown(
            label="Entreprise", options=[],
            expand=True,
            )
        liste_entreprise=self.state.load_entreprises()
        if liste_entreprise:
            for entreprise in liste_entreprise:
                self.choix_entreprise.options.append(ft.dropdown.Option(entreprise.name))

        self.add_bnt_entr=ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e: self.showNameEntrepriseField())
        self.nom_entreprise = CustomInputField(label="Nom entreprise")
        self.save_btn=ft.IconButton(icon=ft.Icons.SAVE, on_click=lambda e: self.saveContact())

        self.canton = CustomInputField(label="Canton")
        self.localite = CustomInputField(label="Village")
        self.lieu = CustomInputField(label="Lieu d'implantation")
        self.coordonnee_x = CustomInputField(label="Coordonnee X")
        self.coordonnee_y = CustomInputField(label="Coordonnee Y")

        self.type_ouvrage = ft.Dropdown(
            label="Type d'ouvrage", 
            value="PMH",
            options=[ft.dropdown.Option("PMH"), 
                     ft.dropdown.Option("PEA"), 
                     ft.dropdown.Option("PMH en PEA"), 
                     ft.dropdown.Option("AEP"), 
                     ft.dropdown.Option("Mini AEP")
                    ],
            on_text_change=lambda e :self.update_fields(e),
            expand=True)

        self.type_reservoir = ft.Dropdown(
            label="Type réservoir", 
            options=[ft.dropdown.Option(val) for val in reservoirs],
            expand=True
            )
        self.type_reservoir.visible=False

        self.etat = ft.Dropdown(
            label="État de l'ouvrage",
            value="Bon état",
            options=[
                    ft.dropdown.Option("Bon état"),
                    ft.dropdown.Option("En panne"),
                    ft.dropdown.Option("Abandonné")
                ],
            on_text_change = lambda e :self.update_field_cause(e),
            expand=True 
            )

        self.numero_irh = CustomInputField(label="N° IRH")
        
        self.type_energie = CustomInputField(
            label="Type énergie"
            )
        self.type_energie.visible=False
        self.annee = CustomInputField(
            label="Année d'impl.", 
            value="0000"
            )
        self.volume_reservoir = CustomInputField(
            label="Vol. réservoir"
            )
        self.volume_reservoir.visible = False
        self.cause_panne = CustomInputField(
            label="Cause de la panne (si applicable)",
            max_lines=4, multiline=True,)
        self.cause_panne.visible=False
        self.observation = CustomInputField(label="Observation",
                                            max_lines=4, multiline=True,
                                            expand=True)

        self.choix_entreprise_cnt=ft.Row(
                            controls=[
                                self.choix_entreprise,
                                self.add_bnt_entr
                            ]
                        )

        self.entreprise_cnt=ft.Container(
            border=ft.Border.all(1, ft.Colors.YELLOW_400),
            padding=5,
            border_radius=5,
            content=ft.Row(
                        [
                            self.nom_entreprise,self.save_btn
                        ]
                    )
        )
        self.entreprise_cnt.visible=False

        self.controls = [
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
                spacing=10,
                controls=[
                    # ft.Container(
                    #     content=ft.Row(
                    #             [
                    #                 ft.IconButton(icon=ft.Icons.ARROW_BACK, 
                    #                             on_click= lambda e:self.page.on_view_pop()),
                    #                 ft.Text("Créer un nouveau Ouvrage ", 
                    #                         text_align=ft.TextAlign.CENTER)
                    #             ]
                    #             # ,alignment=MainAxisAlignment.CENTER
                    #                 )
                    #             )
                    ft.AppBar(title=ft.Text("Créer un nouveau ouvrage"))
                    ,
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
                            self.lieu,
                            ft.Row(
                                controls=[
                                    self.coordonnee_x,self.coordonnee_y,
                                    # ft.IconButton(icon=ft.Icons.ADD_LOCATION_ALT_OUTLINED,
                                                #   on_click=self.handle_location_service_enabled)
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.type_ouvrage, self.annee
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.numero_irh, self.volume_reservoir,
                                ], 
                            ),
                            ft.Row(
                                controls=[
                                    self.type_reservoir, self.type_energie
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.etat
                                ]
                            ),
                            self.choix_entreprise_cnt,
                            self.entreprise_cnt,
                            ft.Row(
                                controls=[
                                    self.cause_panne
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.observation
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Button("Enregistrer l'ouvrage",
                                            on_click=lambda e: self.SaveData()
                                              )
                                ]
                            ),
                        ]
                    )
                ]
    
    # def get_dialog(self,handler: Callable):
    #     return ft.AlertDialog(
    #         adaptive=True,
    #         title="Opening Location Settings...",
    #         content=ft.Text(
    #             "You are about to be redirected to the location/app settings. "
    #             "Please locate this app and grant it location permissions."
    #         ),
    #         actions=[ft.TextButton("rediriger", on_click=handler)],
    #         actions_alignment=ft.MainAxisAlignment.CENTER,
    #     )
        
    # ==================Localisation======================
    # def handle_position_change(self, e: ftg.GeolocatorPositionChangeEvent):
    #     self.coordonnee_x.value=e.position.latitude
    #     self.coordonnee_y.value=e.position.longitude

    # async def handle_get_current_position(self, e: ft.Event[ft.OutlinedButton]):
    #     p = await self.geo.get_current_position()
    #     self.show_snackbar(f"Current position: ({p.latitude}, {p.longitude})")

    # async def handle_location_service_enabled(self, e):
    #     try:
    #         p = await self.geo.is_location_service_enabled()
    #         self.show_snackbar(f"Location service enabled: {p}")
    #         if p==False:
    #             self.page.show_dialog(self.location_settings_dlg)
    #     except:
    #         pass

    # async def handle_open_location_settings(self, e: ft.Event[ft.OutlinedButton]):
    #     p = await self.geo.open_location_settings()
    #     self.page.pop_dialog()
    #     if p is True:
    #         self.show_snackbar("Location settings opened successfully.")
    #     else:
    #         self.show_snackbar("Location settings could not be opened.")

    # async def handle_open_app_settings(self, e: ft.Event[ft.OutlinedButton]):
    #     p = await self.geo.open_app_settings()
    #     self.page.pop_dialog()
    #     if p:
    #         self.show_snackbar("App settings opened successfully.")
    #     else:
    #         self.show_snackbar("App settings could not be opened.")
    
    def show_snackbar(self, message):
        self.page.show_dialog(ft.SnackBar(ft.Text(message)))

    def update_commune(self,e):
        self.commune.options.clear()
        for key in donnees.keys():
            if self.prefecture.value==key:
                for value in donnees[key]:
                    self.commune.options.append(ft.dropdown.Option(value))
        self.commune.update()

    def update_fields(self,e):
        ouvrage=e.control.value
        if ouvrage=="PMH" or ouvrage=="PMH en PEA":
            self.type_energie.visible=False
            self.type_reservoir.visible=False
            self.volume_reservoir.visible=False
        else:
            self.type_energie.visible=True
            self.type_reservoir.visible=True
            self.volume_reservoir.visible=True

    def update_field_cause(self,e):
        ouvrage=e.control.value
        if ouvrage=="En panne" or ouvrage=="Abandonné":
            self.cause_panne.visible=True
        else:
            self.cause_panne.visible=False
    
    def updateEntrepriseChoice(self):
        self.choix_entreprise.options.clear()
        liste_entreprise=self.state.load_entreprises()
        if liste_entreprise:
            for entreprixe in liste_entreprise:
                self.choix_entreprise.options.append(ft.dropdown.Option(entreprixe.name))

    def showNameEntrepriseField(self):
        self.entreprise_cnt.visible=True
        self.choix_entreprise_cnt.visible=False
    
    def saveContact(self):
        nom_entreprise = self.nom_entreprise.value.upper()
        if nom_entreprise:
            create_entreprise(name=nom_entreprise, contact="")
            self.updateEntrepriseChoice()
            self.entreprise_cnt.visible=False
            self.choix_entreprise_cnt.visible=True

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
        lieu = self.lieu.value
        if lieu=="" or lieu==None:
            return self.show_snackbar(f"⚠️ Inserer le lieu")
        coordonnee_x = self.coordonnee_x.value or 0
        coordonnee_y = self.coordonnee_y.value or 0
        choix_entreprise = self.choix_entreprise.value
        if choix_entreprise=="" or choix_entreprise==None:
            return self.show_snackbar(f"⚠️ Donner le nom de l'entreprise ")
        type_ouvrage = self.type_ouvrage.value
        numero_irh = self.numero_irh.value
        type_reservoir = self.type_reservoir.value
        type_energie = self.type_energie.value
        annee = self.annee.value
        if annee=="" or annee==None:
            return self.show_snackbar(f"⚠️ Inserer l'année")
        volume_reservoir = self.volume_reservoir.value or 0
        etat = self.etat.value
        if etat=="" or etat==None:
            return self.show_snackbar(f"⚠️ Choisissez l'état")
        cause_panne=self.cause_panne.value
        observation = self.observation.value
        return {"prefecture": prefecture, "commune": commune, "canton": canton.capitalize(), "localite": localite.capitalize(),"lieu": lieu.capitalize(), "coordonnee_x": coordonnee_x, "coordonnee_y": coordonnee_y, "entreprise": choix_entreprise,"type_ouvrage": type_ouvrage,"numero_irh": numero_irh, "type_reservoir":type_reservoir,"type_energie": type_energie,"annee": annee, "volume_reservoir": volume_reservoir, "etat": etat, "cause_panne":cause_panne, "observation": observation}

    def SaveData(self):
        projet_id=self.state.selected_projet.id
        donnees = self.recupererDonnees()
        if donnees:
            create_ouvrage(projet_id, donnees["prefecture"], donnees["commune"], donnees["canton"], donnees["localite"], donnees["lieu"], donnees["coordonnee_x"], donnees["coordonnee_y"],donnees["entreprise"], donnees["type_ouvrage"], donnees["numero_irh"], donnees["annee"], donnees["type_energie"], donnees["type_reservoir"],donnees["volume_reservoir"], donnees["etat"], donnees["cause_panne"],donnees["observation"])
            self.state.load_ouvrages()
            self.page.views.pop()
            self.page.views.pop()
            self.page.on_route_change("/list-ouvrage")  
        else:
            return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Données manquante")))