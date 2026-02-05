import flet as ft
from mystorage import *
from .statanneecard import StatAnneeCard
from .statgeneralcard import StatGeneralCard

class StatGeneralControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        
        stats_gen= get_value('stats_gen')
        self.general_cnt=ft.Column(
            expand=True, 
            scroll=ft.ScrollMode.ALWAYS
            )
        
        cont_gen=StatGeneralCard(stat_general=stats_gen)
        cont_ann=StatAnneeCard(stat_general=stats_gen)
        
        self.general_cnt.controls.append(cont_gen)
        self.general_cnt.controls.append(cont_ann)
        
        self.controls=[
            ft.AppBar(
                title=ft.Text(f"📁 Stastistiques Générals"),
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,on_click= lambda e: self.formcontrol.change_content("stat-button-content"))
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding.only(left=10, right=10),
                content=self.general_cnt
            )
        
        ]
        
