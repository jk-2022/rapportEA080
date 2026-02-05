import flet as ft 

from donnees import *
from myaction.myaction_ouvrage import update_ouvrage
from uix.custominputfield import CustomInputField
from myaction.myaction_entreprise import create_entreprise

class EditOuvrageView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.page.route = "/edit-ouvrage"
        self.ouvrage=self.state.selected_ouvrage
        self.prefecture = ft.Dropdown(
            label="Préfecture",
            value=self.ouvrage.prefecture,
            options=[ft.dropdown.Option(val) for val in donnees.keys()],
            expand=True,
            on_text_change=lambda e :self.update_commune(e))

        self.commune = ft.Dropdown(
            label="Commune",
            value=self.ouvrage.commune,
            options=[ft.dropdown.Option(val) for val in donnees[self.ouvrage.prefecture]],
            expand=True)
        
        self.choix_entreprise = ft.Dropdown(
            label="Entreprise",
            value=self.ouvrage.entreprise,
            expand=True,
            )
        liste_entreprise=self.state.load_entreprises()
        if liste_entreprise:
            self.choix_entreprise.options=[]
            for entreprise in liste_entreprise:
                self.choix_entreprise.options.append(ft.dropdown.Option(entreprise.name))

        self.add_bnt_entr=ft.IconButton(icon=ft.Icons.ADD, 
                                        on_click=lambda e: self.showNameEntrepriseField())
        self.nom_entreprise = CustomInputField(label="Nom entreprise",
                                               value=self.ouvrage.entreprise)
        self.save_btn=ft.IconButton(icon=ft.Icons.SAVE, 
                                    on_click=lambda e:self.saveContact())

        self.canton = CustomInputField(
            label="Canton",
            value=self.ouvrage.canton)
        self.localite = CustomInputField(
            label="Village",
            value=self.ouvrage.localite)
        self.lieu = CustomInputField(
            label="Lieu d'implantation",
            value=self.ouvrage.lieu)
        self.coordonnee_x = CustomInputField(
            label="Coordonnee X",
            value=self.ouvrage.coordonnee_x)
        self.coordonnee_y = CustomInputField(
            label="Coordonnee Y",
            value=self.ouvrage.coordonnee_y)

        self.type_ouvrage = ft.Dropdown(
            label="Type d'ouvrage", 
            value=self.ouvrage.type_ouvrage,
            options=[ft.dropdown.Option("PMH"), 
                     ft.dropdown.Option("PEA"), 
                     ft.dropdown.Option("PMH en PEA"), 
                     ft.dropdown.Option("AEP"), 
                     ft.dropdown.Option("Mini AEP")
                    ],
            on_text_change=lambda e :self.update_fields(e),
            expand=True,)
        # self.type_ouvrage.visible=False

        self.type_reservoir = ft.Dropdown(
            label="Type réservoir", 
            value=self.ouvrage.type_reservoir,
            options=[ft.dropdown.Option(val) for val in reservoirs],
            expand=True
            )
        self.type_reservoir.visible=False

        self.etat = ft.Dropdown(
            label="État de l'ouvrage",
            value=self.ouvrage.etat,
            options=[
                    ft.dropdown.Option("Bon état"),
                    ft.dropdown.Option("En panne"),
                    ft.dropdown.Option("Abandonné")
                ],
            on_text_change = lambda e :self.update_field_cause(e),
            expand=True 
            )

        self.numero_irh = CustomInputField(
            label="N° IRH",
            value=self.ouvrage.numero_irh)
        
        self.type_energie = CustomInputField(
            label="Type énergie",
            value=self.ouvrage.type_energie)
        self.type_energie.visible=False
        self.annee = CustomInputField(
            label="Année d'impl.",
            value=self.ouvrage.annee)
        self.volume_reservoir = CustomInputField(
            label="Vol. réservoir",
            value=self.ouvrage.volume_reservoir)
        self.volume_reservoir.visible = False
        self.cause_panne = CustomInputField(
            label="Cause de la panne (si applicable)",
            max_lines=4, multiline=True,
            value=self.ouvrage.cause_panne)
        self.cause_panne.visible=False
        self.observation = CustomInputField(
            label="Observation",
            max_lines=4, multiline=True,expand=True,
            value=self.ouvrage.observation)

        self.choix_entreprise_cnt=ft.Row(
                            controls=[
                                self.choix_entreprise,self.add_bnt_entr
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
                    ft.Container(
                        content=ft.Row(
                                [
                                ft.IconButton(icon=ft.Icons.ARROW_BACK, 
                                              on_click= lambda e:self.page.on_view_pop()),
                                ft.Text("Créer un nouveau Ouvrage ", 
                                        text_align=ft.TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                                    )
                            ),
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
                                    self.coordonnee_x,self.coordonnee_y
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
                                    ft.Button("Modifier l'ouvrage",
                                            on_click=lambda e:self.UpdadeData()
                                              )
                                ]
                            ),
                        ]
                    )
                ]
        

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
        # self.page.update()

    def update_field_cause(self,e):
        ouvrage=e.control.value
        if ouvrage=="En panne" or ouvrage=="Abandonné":
            self.cause_panne.visible=True
        else:
            self.cause_panne.visible=False
        # self.page.update()
    
    def updateEntrepriseChoice(self):
        self.choix_entreprise.options.clear()
        liste_entreprise=self.state.load_entreprises()
        if liste_entreprise:
            for entreprixe in liste_entreprise:
                self.choix_entreprise.options.append(ft.dropdown.Option(entreprixe.name))
        # self.choix_entreprise.update()

    def showNameEntrepriseField(self):
        self.entreprise_cnt.visible=True
        self.choix_entreprise_cnt.visible=False
    
    def saveContact(self):
        nom_entreprise = self.nom_entreprise.value
        if nom_entreprise:
            create_entreprise(name=nom_entreprise, contact="")
            self.updateEntrepriseChoice(e=None)
            self.entreprise_cnt.visible=False
            self.choix_entreprise_cnt.visible=True

    def UpdadeData(self):
        self.ouvrage.prefecture = self.prefecture.value
        self.ouvrage.commune = self.commune.value
        self.ouvrage.canton = self.canton.value.capitalize()
        self.ouvrage.localite = self.localite.value.capitalize()
        self.ouvrage.lieu = self.lieu.value.capitalize()
        # if lieu=="" or lieu==None:
        #     return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Inserer le lieu")))
        self.ouvrage.coordonnee_x = self.coordonnee_x.value or 0
        self.ouvrage.coordonnee_y = self.coordonnee_y.value or 0
        self.ouvrage.entreprise = self.choix_entreprise.value
        self.ouvrage.type_ouvrage = self.type_ouvrage.value
        # if type_ouvrage=="" or type_ouvrage==None:
        #     return self.page.show_dialog(ft.SnackBar(ft.Text(f"⚠️ Choisissez le type_ouvrage")))
        self.ouvrage.numero_irh = self.numero_irh.value
        self.ouvrage.type_reservoir = self.type_reservoir.value
        self.ouvrage.type_energie = self.type_energie.value
        self.ouvrage.annee = self.annee.value
        self.ouvrage.volume_reservoir = self.volume_reservoir.value or 0
        self.ouvrage.etat = self.etat.value
        self.ouvrage.cause_panne=self.cause_panne.value
        self.ouvrage.observation = self.observation.value
        update_ouvrage(ouvrage=self.ouvrage)
        self.state.selected_ouvrage=self.ouvrage
        self.state.load_ouvrages()
        # self.page.on_view_pop()
        self.page.views.pop()
        self.page.views.pop()
        self.page.on_route_change("/list-ouvrage")     
