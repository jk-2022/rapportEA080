import flet as ft
from mystorage import *

from myaction.myaction_main import get_statistiques
from uix.statbtncard import StatBtnCard

class StatView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.route = "/stats"
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    controls=[
                        # ft.Row(
                        #     [
                        #     ft.IconButton(
                        #         icon=ft.Icons.ARROW_BACK,
                        #         on_click=lambda e :self.page.on_view_pop()
                        #         ),
                        #     ft.Text(f"📁 Stastistiques")
                        #     ]
                        # ),
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques")
                        ),
                        
                        ft.Container(
                            expand=True,
                            align=ft.Alignment.CENTER,
                            content=ft.Column(
                                    [
                                        StatBtnCard(
                                            title='Stats générals', 
                                            on_click=lambda e :self.page_go_general()),
                                        StatBtnCard(
                                            title='Stats par projet', 
                                            on_click=lambda e :self.page_go_par_projet()),
                                        StatBtnCard(
                                            title='Stats communes', 
                                            on_click=lambda e :self.page_go_commune()),
                                        StatBtnCard(
                                            title='Stats cantons', 
                                            on_click=lambda e :self.page_go_canton()),
                                        StatBtnCard(
                                            title='Stats intervalle dates', 
                                            on_click=lambda e :self.page_go_interval()),
                                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                )
                        )
                        
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
        
    def page_go_general(self):
        stats_gen = get_statistiques()
        set_value('stats_gen', stats_gen)
        self.page.on_route_change('/statgeneral')
    def page_go_commune(self):
        self.page.on_route_change('/statcommune') 
    def page_go_par_projet(self):
        self.page.on_route_change('/statparprojet') 
    def page_go_canton(self):
        self.page.on_route_change('/statcanton')
    def page_go_interval(self):
        self.page.on_route_change('/intervaldate')
        
