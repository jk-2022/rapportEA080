
import flet as ft

from datetime import datetime
from donnees import *

from myaction.myaction_pompage import update_pompage, Pompage
from uix.custominputnumberfield import CustomInputNumberField
from uix.custominputfield import CustomInputField

class PompageUpdateForm(ft.Container):
    def __init__(self, state, donnees, formcontrol):
        super().__init__()
        self.state=state
        self.width=460
        self.donnees=donnees
        self.formcontrol=formcontrol

        self.date_pompage = CustomInputField(
            label="Date Pompage.",
            value=donnees['date_pompage']
            )
        self.date_btn=ft.IconButton(
            icon=ft.Icons.DATE_RANGE, 
            on_click= self.openDatePicker
            )
        self.type_pompe = CustomInputField(
            label="Type de Pompe",
            value=donnees['type_pompe']
            )
        self.cote_pompe = CustomInputNumberField(
            label="Côte Pompe.",
            value=donnees['cote_pompe']
            )
        self.temps_pompage = CustomInputNumberField(
            label="Temps pompage",
            value=donnees['temps_pompage']
            )
        self.debit_pompage = CustomInputNumberField(
            label="Débit Pompage",
            value=donnees['debit_pompage']
            )
        self.niv_dynamique = CustomInputNumberField(
            label="Niv Dynamique",
            value=donnees['niv_dynamique']
            )
        self.niv_statique = CustomInputNumberField(
            label="Niv Statique",
            value=donnees['niv_statique']
            )
        self.observation = CustomInputField(
            label="Observation",
            height=80, 
            max_lines=4, 
            multiline=True,
            expand=True,
            value=self.donnees['observation'])
    
        self.content=ft.Container(
                padding=15,
                expand=True,
                content=ft.Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        ft.Row(
                            controls=[
                                self.date_pompage,self.date_btn
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.type_pompe, self.cote_pompe
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.temps_pompage, self.debit_pompage
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.niv_dynamique, self.niv_statique
                            ]
                        ),
                    ]
                )
            )
        

    def handle_change(self,e):
        self.date_pompage.value=e.control.value.strftime('%d/%m/%Y')
        self.date_pompage.update()

    def handle_dismissal(self,e):
        ""

    def openDatePicker(self,e):
        date=ft.DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def SaveData(self):
        pompage=Pompage(
            id=self.donnees["id"],
            ouvrage_id=self.state.selected_ouvrage.id,
            date_pompage = self.date_pompage.value,
            type_pompe = self.type_pompe.value,
            cote_pompe = self.cote_pompe.value,
            temps_pompage = self.temps_pompage.value,
            debit_pompage = self.debit_pompage.value,
            niv_dynamique = self.niv_dynamique.value,
            niv_statique = self.niv_statique.value,
            observation = self.observation.value,
            created_at=self.donnees["created_at"]
            )
        update_pompage(pompage=pompage)
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

