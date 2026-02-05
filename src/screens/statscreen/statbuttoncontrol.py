import flet as ft
from mystorage import *

from myaction.myaction_main import get_statistiques
from uix.statbtncard import StatBtnCard

class StatButtonControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        
        self.controls=[
            ft.AppBar(
                title=ft.Text(f"📁 Stastistiques"),
            ),
            
            ft.Container(
                expand=True,
                align=ft.Alignment.CENTER,
                content=ft.Column(
                        controls=[
                            StatBtnCard(
                                title='Stats générals', 
                                on_click=lambda e :self.change_content_form("stat-general-content")),
                            StatBtnCard(
                                title='Stats par projet', 
                                on_click=lambda e :self.change_content_form("stat-projet-content")),
                            StatBtnCard(
                                title='Stats communes', 
                                on_click=lambda e :self.change_content_form("stat-commune-content")),
                            StatBtnCard(
                                title='Stats cantons', 
                                on_click=lambda e :self.change_content_form("stat-canton-content")),
                            StatBtnCard(
                                title='Stats intervalle dates', 
                                on_click=lambda e :self.change_content_form("stat-interval-content")),
                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
                )
                        
            ]
        
        
    def change_content_form(self,content):
        if content=="stat-general-content":
            stats_gen = get_statistiques()
            set_value('stats_gen', stats_gen)
        self.formcontrol.change_content(content)
        
