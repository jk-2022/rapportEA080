import flet as ft
from mystorage import *

from .statinterval.statintervalcontrol import StatIntervalControl
from .statcanton.statcantoncontrol import StatCantonControl
from .statcommune.statcommunecontrol import StatCommuneControl
from .statbuttoncontrol import StatButtonControl
from .statgeneral.statgeneralcontrol import StatGeneralControl
from .statprojet.statprojetcontrol import StatProjetControl

class StatView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.padding=0
        self.state=state
        self.route = "/stats"
        
        self.controls.append(
            StatButtonControl(state=self.state, formcontrol=self),
            
        )
        
    def change_content(self, content):
        self.controls.clear()
        # print(content)
        if content=="stat-button-content":
            self.controls.append(StatButtonControl(state=self.state,formcontrol=self))
        if content=="stat-general-content":
            self.controls.append(StatGeneralControl(state=self.state, formcontrol=self))
        if content=="stat-projet-content":
            self.controls.append(StatProjetControl(state=self.state, formcontrol=self))
        if content=="stat-commune-content":
            self.controls.append(StatCommuneControl(state=self.state, formcontrol=self))
        if content=="stat-canton-content":
            self.controls.append(StatCantonControl(state=self.state, formcontrol=self))
        if content=="stat-interval-content":
            self.controls.append(StatIntervalControl(state=self.state, formcontrol=self))
        

        
