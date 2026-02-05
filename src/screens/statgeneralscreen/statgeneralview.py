import flet as ft
from mystorage import *
from .statanneecontrol import StatAnneeControl
from .statgeneralcontrol import StatGeneralControl

class StatGeneralView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.route = "/statgeneral"
        stats_gen= get_value('stats_gen')
        self.general_cnt=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        cont_gen=StatGeneralControl(stat_general=stats_gen)
        cont_ann=StatAnneeControl(stat_general=stats_gen)
        self.general_cnt.controls.append(cont_gen)
        self.general_cnt.controls.append(cont_ann)
        
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    controls=[
                        # ft.Row(
                        #     [
                        #     ft.IconButton(icon=ft.Icons.ARROW_BACK,on_click= lambda e: self.page.on_view_pop()),
                        #     ft.Text(f"📁 Stastistiques Générals")
                        #     ]
                        # ),
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques Générals")
                        ),
                        
                        self.general_cnt
                    
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
