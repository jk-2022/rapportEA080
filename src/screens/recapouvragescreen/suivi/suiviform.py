import flet as ft

from datetime import datetime
# import json
from donnees import *
from myaction.myaction_suivi import create_suivi
from uix.custominputfield import CustomInputField

# @ft.control
class SuiviForm(ft.Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.width=450
        self.formcontrol=formcontrol

        self.type_reception = ft.Dropdown(
            label="État de l'ouvrage", 
            options=[
                    ft.dropdown.Option("Réception provisoir"),
                    ft.dropdown.Option("Réception definitive"),
                    ft.dropdown.Option("Suivis"),
                ],
        expand=True)

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_reception = CustomInputField(
            label="Date reception.", 
            value=dateTime
            )
        self.date_btn=ft.IconButton(
            icon=ft.Icons.DATE_RANGE, 
            on_click= lambda e :self.openDatePicker()
            )
        self.recommandation = CustomInputField(
            label="Recommandations", max_lines=4, 
            multiline=True,expand=True
            )
        self.participants = CustomInputField(
            label="Participants",
            value="DREA, CVD",
            max_lines=4, 
            multiline=True,expand=True
            )
        self.observation = CustomInputField(
            label="Observations", max_lines=4, 
            multiline=True,expand=True
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
                                self.type_reception
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.date_reception
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.participants
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.recommandation
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

    def handle_change(self,e):
        self.date_reception.value=e.control.value.strftime('%d/%m/%Y')

    def handle_dismissal(self,e):
        ""

    def openDatePicker(self,e):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2030, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def recupererDonnees(self):
        type_reception = self.type_reception.value
        date_reception = self.date_reception.value
        participants = self.participants.value
        recommandation = self.recommandation.value
        observation = self.observation.value
        return {
            "ouvrage_id": self.state.selected_ouvrage.id, 
            "type_reception": type_reception, 
            "date_reception": date_reception,
            "participants": participants,
            "recommandation": recommandation, 
            "observation": observation
            }

    def SaveData(self):
        donnees = self.recupererDonnees()
        create_suivi(**donnees)
        self.formcontrol.updateData()
        self.formcontrol.close_dlg()

