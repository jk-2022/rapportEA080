import flet as ft
from datetime import datetime
from myaction.myaction_panne import Panne, update_panne
from uix.custominputfield import CustomInputField

# @ft.control
class PanneUpdateForm(ft.Container):
    def __init__(self, state, panne: Panne, formcontrol):
        super().__init__()
        self.state=state
        self.width=450
        self.panne=panne
        self.formcontrol=formcontrol

        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_signaler = CustomInputField(
            label="Date signaler", value=panne.date_signaler)
        self.date_btn=ft.IconButton(icon=ft.Icons.DATE_RANGE, on_click=lambda e: self.openDatePicker())
        self.description = CustomInputField(
            label="Descriptions", 
            max_lines=4,expand=True, multiline=True,value=self.panne.description)
        self.solution = CustomInputField(
            label="Solutions", 
            max_lines=4,expand=True, multiline=True,value=self.panne.solution)
        self.observation = CustomInputField(
            label="Observation", 
            max_lines=4,expand=True, multiline=True,value=self.panne.observation)
    
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
        self.date_signaler.update()

    def handle_dismissal(self,e):
        pass
    
    def update_total_prof(self,e):
        prof_alter=self.date_signaler.value or 0
        solution=self.solution.value or 0
        rest=float(solution) + float(prof_alter)
        self.description.value=rest 
        self.description.update()

    def openDatePicker(self,e):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2026, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        panne=Panne(
        id = self.panne.id,
        ouvrage_id = self.panne.ouvrage_id,
        date_signaler = self.date_signaler.value,
        description = self.description.value,
        solution = self.solution.value,
        observation = self.observation.value,
        created_at = self.panne.created_at
        )
        update_panne(panne)
        self.formcontrol.formcontrol.updateData()
        self.page.pop_dialog()

