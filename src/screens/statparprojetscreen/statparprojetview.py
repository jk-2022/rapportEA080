import flet as ft 
from myaction.myaction_main import  get_all_projets, get_stats_par_projets
from .statanneeparprojetcontrol import StatAnneeParProjetControl
from .statparprojetcontrol import StatParProjetControl


class StatParProjetView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        
        self.projet = ft.Dropdown(
            label="Voir stat par projet", 
            expand=True,
            on_text_change=lambda e: self.show_tab_stat_by_projet(e)
            )
        list_projet = get_all_projets() 
        if list_projet:
            for projet in list_projet:
                self.projet.options.append(ft.dropdown.Option(projet['name']))
        
        self.projet_res_cont=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
        
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                            ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                          on_click=lambda e: self.page.on_view_pop()),
                            ft.Text(f"📁 Stastistiques par projets")
                            ]
                        ),
                        self.projet,
                        self.projet_res_cont
                    
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
    def show_tab_stat_by_projet(self,e):
        projet=e.control.value
        stats=get_stats_par_projets(projet)
        cont_projet=StatParProjetControl(par_projet=projet, stat_general=stats)
        cont_projet_annee=StatAnneeParProjetControl(stat_general=stats)

        self.projet_res_cont.controls.clear()
        self.projet_res_cont.controls.append(cont_projet)
        self.projet_res_cont.controls.append(cont_projet_annee)
        # self.projet_res_cont.update()
        
