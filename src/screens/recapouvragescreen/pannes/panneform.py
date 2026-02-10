import flet as ft
from datetime import datetime
from myaction.myaction_panne import create_panne
from uix.custominputfield import CustomInputField

class PanneForm(ft.Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.width=460
        self.formcontrol=formcontrol

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_btn=ft.IconButton(icon=ft.Icons.DATE_RANGE, on_click=lambda e: self.openDatePicker())
        self.date_signaler = CustomInputField(label="Date reception.", value=dateTime)
        self.description = CustomInputField(
            label="Description", 
        max_lines=4, multiline=True,expand=True)
        self.solution = CustomInputField(
            label="Solutions", 
        max_lines=4, multiline=True,expand=True)
        self.observation = CustomInputField(
            label="Observation", 
        max_lines=4, multiline=True,expand=True)
    
        self.content=ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        ft.Row(
                            controls=[
                                self.date_signaler,self.date_btn
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.description
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.solution
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
        self.date_signaler.value=e.control.value.strftime('%d/%m/%Y')

    def handle_dismissal(self,e):
        ""

    def openDatePicker(self):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2030, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def recupererDonnees(self):
        date_signaler = self.date_signaler.value
        description = self.description.value
        solution = self.solution.value
        observation = self.observation.value
        return {
            "ouvrage_id": self.state.selected_ouvrage.id,
            "date_signaler": date_signaler,
            "description": description,
            "solution": solution, 
            "observation": observation
                }

    def SaveData(self):
        donnees = self.recupererDonnees()
        create_panne(**donnees)
        self.formcontrol.updateData()
        self.page.pop_dialog()

