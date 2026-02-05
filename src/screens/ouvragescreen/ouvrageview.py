import flet as ft

from .createouvragecontrol import CreateOuvrageControl
from .editouvragecontrol import EditOuvrageControl
from .filtreouvragecontrol import FiltreOuvrageControl
from .listouvragecontrol import ListOuvrageControl

class OuvrageView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.state=state
        self.route = "/projet/list-ouvrage"
        
        self.controls.append(
            ListOuvrageControl(state=self.state, formcontrol=self)
        )
        
    def change_content(self,content):
        self.controls.clear()
        if content=="filtre-content":
            self.controls.append(FiltreOuvrageControl(state=self.state,formcontrol=self))
        if content=="list-ouvrage-content":
            self.controls.append(ListOuvrageControl(state=self.state,formcontrol=self))
        if content=="create-ouvrage-content":
            self.controls.append(CreateOuvrageControl(state=self.state,formcontrol=self))
        if content=="edit-ouvrage-content":
            self.controls.append(EditOuvrageControl(state=self.state,formcontrol=self))


