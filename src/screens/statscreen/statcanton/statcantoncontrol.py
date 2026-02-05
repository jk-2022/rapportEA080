import flet as ft

from myaction.myaction_main import get_all_cantons, get_stats_canton
from .statanneecantoncard import StatAnneeCantonCard
from .statcantoncard import StatCantonCard

class StatCantonControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True 
        
        self.canton = ft.Dropdown(
            label="Voir stat par canton",
            width=400,
            on_text_change=lambda e :self.show_tab_stat_by_canton(e)
            )
        
        list_cantons = get_all_cantons()
        if list_cantons:
            self.canton.options=[ft.dropdown.Option(key) for key in list_cantons]
            
        self.canton_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        self.controls=[
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques par Canton"),
                            leading=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e :self.formcontrol.change_content("stat-button-content")),
                        ),
                        ft.Container(
                            expand=True, 
                            padding=ft.Padding(left=10,right=10),
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            self.canton
                                        ], alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    self.canton_res_cont
                                ]
                            )
                        )
                    ]
    def show_tab_stat_by_canton(self,e):
        canton=e.control.value
        stats=get_stats_canton(canton)
        cont_canton=StatCantonCard(canton=canton, stat_general=stats)
        cont_canton_annee=StatAnneeCantonCard(stat_general=stats)

        self.canton_res_cont.controls.clear()
        self.canton_res_cont.controls.append(cont_canton)
        self.canton_res_cont.controls.append(cont_canton_annee)
        self.canton_res_cont.update()
        
