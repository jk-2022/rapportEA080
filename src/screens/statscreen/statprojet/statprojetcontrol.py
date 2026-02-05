import flet as ft 
from myaction.myaction_main import  get_all_projets, get_stats_par_projets

from .statanneeprojetcard import StatAnneeProjetCard
from .statprojetcard import StatProjetCard

class StatProjetControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        
        self.projet = ft.Dropdown(
            label="Voir stat par projet", 
            # expand=1,
            width=400,
            on_text_change=lambda e: self.show_tab_stat_by_projet(e)
            )
        
        list_projet = get_all_projets()
        if list_projet:
            self.projet.options=[ft.dropdown.Option(projet['name']) for projet in list_projet]
        
        self.projet_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        self.controls=[
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques par Projet"),
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                          on_click=lambda e: self.formcontrol.change_content("stat-button-content"))
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding.only(left=10,right=10),
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        [
                                            self.projet
                                        ],alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                    self.projet_res_cont
                                ]
                            )
                        )
                    
                    ]
        
    def show_tab_stat_by_projet(self,e):
        projet=e.control.value
        stats=get_stats_par_projets(projet)
        cont_projet=StatProjetCard(par_projet=projet, stat_general=stats)
        cont_projet_annee=StatAnneeProjetCard(stat_general=stats)
        self.projet_res_cont.controls.clear()
        self.projet_res_cont.controls.append(cont_projet)
        self.projet_res_cont.controls.append(cont_projet_annee)
        
