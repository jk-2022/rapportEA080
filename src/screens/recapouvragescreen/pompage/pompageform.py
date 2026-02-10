
from flet import *

from datetime import datetime

from donnees import *
from uix.custominputnumberfield import CustomInputNumberField
from uix.custominputfield import CustomInputField
from myaction.myaction_pompage import create_pompage

# @control
class PompageForm(Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.ouvrage_id=self.state.selected_ouvrage.id
        self.width=460
        self.formcontrol=formcontrol
        
        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_pompage = CustomInputField(label="Date Pompage.",value=dateTime)
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click=lambda e: self.openDatePicker())
        self.type_pompe = CustomInputField(label="Type Pompe.")
        self.cote_pompe = CustomInputNumberField(label="Côte pompe.")
        self.temps_pompage = CustomInputNumberField(label="Durée de pompage.")
        self.debit_pompage = CustomInputNumberField(label="Débit pompage.")
        self.niv_dynamique = CustomInputNumberField(label="Niv Statique")
        self.niv_statique = CustomInputNumberField(label="Niv Dynamique.")
        self.observation = CustomInputField(label="Observation",height=80, max_lines=4, multiline=True)
    
        self.content=Container(
                padding=15,
                expand=True,
                content=Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        Row(
                            controls=[
                                self.date_pompage,self.date_btn
                            ]
                        ),
                        Row(
                            controls=[
                                self.type_pompe, self.cote_pompe
                            ]
                        ),
                        Row(
                            controls=[
                                self.temps_pompage, self.debit_pompage
                            ]
                        ),
                        Row(
                            controls=[
                                self.niv_dynamique,self.niv_statique
                            ]
                        ),
                        Row(
                            controls=[
                                self.observation
                            ]
                        ),
                    ]
                )
            )
    

    def handle_change(self,e):
        self.date_pompage.value=e.control.value.strftime('%d/%m/%Y')

    def handle_dismissal(self,e):
        ""

    def openDatePicker(self):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2030, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.show_dialog(date)

    def recupererDonnees(self):
        date_pompage = self.date_pompage.value
        type_pompe = self.type_pompe.value
        cote_pompe = self.cote_pompe.value
        temps_pompage = self.temps_pompage.value
        debit_pompage = self.debit_pompage.value
        niv_dynamique = self.niv_dynamique.value
        niv_statique = self.niv_statique.value
        observation = self.observation.value
        return {"ouvrage_id":self.ouvrage_id, "date_pompage": date_pompage, "type_pompe": type_pompe,
                "cote_pompe": cote_pompe,"temps_pompage": temps_pompage, 
                "debit_pompage": debit_pompage, "niv_dynamique": niv_dynamique, 
                "niv_statique": niv_statique, "observation": observation
                }

    def SaveData(self):
        donnees = self.recupererDonnees()
        create_pompage(**donnees)
        self.formcontrol.updateData()
        self.formcontrol.close_dlg()
        