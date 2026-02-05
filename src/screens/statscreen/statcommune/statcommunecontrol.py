import flet as ft
from myaction.myaction_main import get_all_communes, get_stats_commune
from .statanneecommunecard import StatAnneeCommuneCard
from .statcommunecard import StatCommuneCard


class StatCommuneControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol 
        self.expand=True
        
        self.commune = ft.Dropdown(
            label="Voir stat par commune",
            width=400,
            on_text_change=lambda e :self.show_tab_stat_by_commune(e)
            )
        
        list_commune = get_all_communes() 
        if list_commune:
            self.commune.options=[ft.dropdown.Option(key) for key in list_commune]
        
        self.commune_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        self.controls=[
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques par Commune"),
                            leading=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e: self.formcontrol.change_content("stat-button-content")
                                )
                        ),
                        ft.Container(
                            expand=True ,
                            padding=ft.Padding.only(left=10,right=10),
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                            [
                                                self.commune
                                            ],alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                    self.commune_res_cont
                                ]
                            )
                        )           
                    ]
        
    def show_tab_stat_by_commune(self,e):
        commune=e.control.value
        stats=get_stats_commune(commune)
        cont_commune=StatCommuneCard(commune=commune, stat_general=stats)
        cont_commune_annee=StatAnneeCommuneCard(stat_general=stats)

        self.commune_res_cont.controls.clear()
        self.commune_res_cont.controls.append(cont_commune)
        self.commune_res_cont.controls.append(cont_commune_annee)
        
