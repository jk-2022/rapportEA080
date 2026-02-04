import flet as ft

# import json
# from donnees import *
from datetime import datetime
from myaction.myaction_suivi import Suivi, update_suivi
from uix.custominputfield import CustomInputField
from uix.custominputnumberfield import CustomInputNumberField

# @ft.control
class SuiviUpdateForm(ft.Container):
    def __init__(self, state, suivi:Suivi, formcontrol):
        super().__init__()
        self.state=state
        self.width=450
        self.suivi=suivi
        self.formcontrol=formcontrol

        self.type_reception = ft.Dropdown(
            label="État de l'ouvrage", 
            options=[
                    ft.dropdown.Option("Réception provisoir"),
                    ft.dropdown.Option("Réception definitive"),
                    ft.dropdown.Option("Suivis"),
                ],
        expand=True, 
        value=suivi.type_reception)

        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_reception = CustomInputField(
            label="Date de réception", 
            value=suivi.date_reception
            )
        self.date_btn=ft.IconButton(
            icon=ft.Icons.DATE_RANGE, 
            on_click= lambda e: self.openDatePicker()
            )
        self.participants = CustomInputNumberField(
            label="Participants.",
            value=suivi.participants
            )
        self.recommandation = CustomInputNumberField(
            label="Recommandation.", 
            value=suivi.recommandation
            )
        self.observation = CustomInputField(
            label="Observation",height=80, max_lines=4, expand=True, 
            multiline=True,
            value=self.suivi.observation
            )
    
        self.content = ft.Card(
            elevation=10,
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
        pass
    
    def update_total_prof(self,e):
        prof_alter=self.date_reception.value or 0
        recommandation=self.recommandation.value or 0
        rest=float(recommandation) + float(prof_alter)
        self.participants.value=rest 

    def openDatePicker(self):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2030, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def SaveData(self):
        suivi=Suivi(
        id = self.suivi.id,
        ouvrage_id = self.suivi.ouvrage_id,
        type_reception = self.type_reception.value,
        date_reception = self.date_reception.value,
        participants = self.participants.value,
        recommandation = self.recommandation.value,
        observation = self.observation.value,
        created_at = self.suivi.created_at,
        )
        update_suivi(suivi=suivi)
        self.formcontrol.formcontrol.updateData()
        self.page.pop_dialog()

