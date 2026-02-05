import flet as ft

from myaction.myaction_main import get_all_cantons, get_stats_canton
from .statanneecantoncontrol import StatAnneeCantonControl
from .statcantoncontrol import StatCantonControl

class StatCantonView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.route = "/statcanton"
        self.canton = ft.Dropdown(
            label="Voir stat par canton",
            expand=True,
            on_text_change=lambda e :self.show_tab_stat_by_canton(e)
            )
        self.list_cantons = get_all_cantons()
       
        for key in self.list_cantons:
            self.canton.options.append(ft.dropdown.Option(key))
            
        self.canton_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    controls=[
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques par Canton")
                        ),
                        # ft.Row(
                        #     [
                        #     ft.IconButton(
                        #         icon=ft.Icons.ARROW_BACK,
                        #         on_click=lambda e :self.page.on_view_pop()),
                        #     ft.Text(f"📁 Stastistiques par Canton")
                        #     ]
                        # ),
                        self.canton,
                         self.canton_res_cont
                    
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
    def show_tab_stat_by_canton(self,e):
        canton=e.control.value
        stats=get_stats_canton(canton)
        # print(stats)
        cont_canton=StatCantonControl(canton=canton, stat_general=stats)
        cont_canton_annee=StatAnneeCantonControl(stat_general=stats)

        self.canton_res_cont.controls.clear()
        self.canton_res_cont.controls.append(cont_canton)
        self.canton_res_cont.controls.append(cont_canton_annee)
        self.canton_res_cont.update()
        
