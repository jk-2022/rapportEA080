import flet as ft
from datetime import datetime
from donnees import *

from myaction.myaction_foration import create_foration
from uix.custominputnumberfield import CustomInputNumberField

from uix.custominputfield import CustomInputField

# @ft.control
class ForationForm(ft.Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.ouvrage_id=self.state.selected_ouvrage.id
        self.width=460
        self.formcontrol=formcontrol

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_foration = CustomInputField(
            label="Date Foration",
            value=dateTime)
        self.date_btn=ft.IconButton(
            icon=ft.Icons.DATE_RANGE, 
            on_click= lambda e: self.openDatePicker()
            )
        self.prof_alteration = CustomInputNumberField(
            label="Prof Alteration",
            on_change= lambda e:self.update_total_prof()
            )
        self.prof_socle = CustomInputNumberField(
            label="Prof Socle",on_change= lambda e:self.update_total_prof()
            )
        self.prof_total = CustomInputNumberField(
            label="Prof Total", 
            read_only=True)
        self.debit_soufflage = CustomInputNumberField(
            label="Débit soufflage")
        self.prof_tube_plein = CustomInputNumberField(
            label="Prof. Tube plein")
        self.prof_tube_crepine = CustomInputNumberField(
            label="Prof. Tube crepine")
        self.observation = CustomInputField(
            label="Observation", max_lines=4, 
            multiline=True,
            expand=True)
    

        self.content=ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        ft.Row(
                            controls=[
                                self.date_foration,self.date_btn
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.prof_alteration, self.prof_socle
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.prof_tube_crepine,self.prof_tube_plein
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.debit_soufflage, self.prof_total
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
        
    def handle_change(self,e):
        self.date_foration.value=e.control.value.strftime('%d/%m/%Y')

    def handle_dismissal(self,e):
        ""
    
    def update_total_prof(self):
        prof_alter=self.prof_alteration.value or 0
        prof_socle=self.prof_socle.value or 0
        rest=float(prof_socle) + float(prof_alter)
        self.prof_total.value=rest 
        self.prof_total.update()

    def openDatePicker(self,e):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2030, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def recupererDonnees(self):
        date_foration = self.date_foration.value
        prof_alteration = self.prof_alteration.value
        prof_socle = self.prof_socle.value
        prof_total = self.prof_total.value
        debit_soufflage = self.debit_soufflage.value
        prof_tube_plein = self.prof_tube_plein.value
        prof_tube_crepine = self.prof_tube_crepine.value
        observation = self.observation.value
        return {"ouvrage_id": self.ouvrage_id, 
                "date_foration": date_foration, 
                "prof_alteration": prof_alteration,
                "prof_socle": prof_socle,
                "prof_total": prof_total, 
                "prof_tube_crepine": prof_tube_crepine, 
                "prof_tube_plein": prof_tube_plein, 
                "debit_soufflage": debit_soufflage, 
                "observation": observation
                }

    def SaveData(self):
        donnees = self.recupererDonnees()
        create_foration(**donnees)
        self.formcontrol.updateData()
        self.page.pop_dialog()

