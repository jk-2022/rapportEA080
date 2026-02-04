import flet as ft
from myaction.myaction_main import get_all_communes, get_stats_commune
from .statanneecommunecontrol import StatAnneeCommuneControl
from .statcommunecontrol import StatCommuneControl


class StatCommuneView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        
        self.commune = ft.Dropdown(
            label="Voir stat par commune",
            expand=True,
            on_text_change=lambda e :self.show_tab_stat_by_commune(e))
        list_commune = get_all_communes() 
        
        for key in list_commune:
            self.commune.options.append(ft.dropdown.Option(key))
        
        self.commune_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e: self.page.on_view_pop()
                                ),
                            ft.Text(f"📁 Stastistiques par Communes")
                            ]
                        ),
                        self.commune,
                        self.commune_res_cont
                    
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
    def show_tab_stat_by_commune(self,e):
        commune=e.control.value
        stats=get_stats_commune(commune)
        cont_commune=StatCommuneControl(commune=commune, stat_general=stats)
        cont_commune_annee=StatAnneeCommuneControl(stat_general=stats)

        self.commune_res_cont.controls.clear()
        self.commune_res_cont.controls.append(cont_commune)
        self.commune_res_cont.controls.append(cont_commune_annee)
        # self.commune_res_cont.update()
        
