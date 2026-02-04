import asyncio
import flet as ft
from mystorage import *
from .drawer import page_drawer

class AcceuilView(ft.Column):
    def __init__(self,state):
        super().__init__()
        self.padding=0
        self.state=state
        self.expand=True
        page_height=get_value("win_height")
        bar_cnt=ft.Container(height=60,
                         content=ft.Row(
                             [
                                ft.IconButton(icon=ft.Icons.MENU,
                                              on_click=self.open_drawer
                                              ),
                                ft.Text("ACTIVITE ET RAPPORT ", text_align=ft.TextAlign.CENTER,
                                     size=24, weight=ft.FontWeight.BOLD),
                                ft.IconButton(icon=ft.Icons.LIGHT_MODE, on_click=self.togle_theme)
                             ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                         )
        
        self.controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    expand=True,
                    # bgcolor="orange",
                    height=page_height-40,
                    image=ft.DecorationImage(
                        src="eau2.png",
                        fit=ft.BoxFit.COVER
                        ),
                    content=ft.Column(
                        expand=True,
                        controls=[
                            bar_cnt,
                            
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Button(" 📋  Projets ", 
                                                on_click=lambda e : self.page.on_route_change("/projet"), 
                                                elevation=10),
                                        ],alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Button(" Listes Entreprises ", 
                                                on_click=lambda e: self.state.on_route_change("/list-entreprise"), 
                                                elevation=10),
                                        ],alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Button(" Listes Village sans forage ", 
                                                on_click=lambda e: self.state.on_route_change("/list-village"), 
                                                elevation=10),
                                        ],alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=40
                                )
                            
                        ]
                        # scroll=ft.ScrollMode.ADAPTIVE
                    )
                )
            )
        ]
        
        # self.controls=[
        #     ft.SafeArea(
        #         ft.Stack(
        #             expand=True,
        #             controls=[
        #                 ft.Container(
        #                     content=ft.Image(
        #                         src="eau2.png",
        #                         expand=True
        #                             ),
        #                     expand=True
        #                     ),
        #                 ft.Container(
        #                     content=ft.Column(
        #                             [
        #                                 ft.Button(" 📋  Projets ", 
        #                                           on_click=lambda e : self.page.on_route_change("/projet"), 
        #                                           elevation=10),
        #                                 ft.Button(" Listes Entreprises ", 
        #                                           on_click="", 
        #                                           elevation=10),
        #                             ],
        #                             expand=True,
        #                             alignment=ft.MainAxisAlignment.CENTER,
        #                             # spacing=40
        #                             # rtl=True
        #                         ),
        #                     align=ft.Alignment.CENTER,
        #                     expand=True,
        #                     top=0,bottom=0,left=0,right=0,
        #                     bgcolor="orange"
        #                     ),
        #                 bar_cnt
        #                 ]
        #             )
        #             ,expand=True
        #         )
        # ]

    async def open_drawer(self):
        await self.page.show_drawer()

    def page_go_project(self,e):
       self.page.on_route_change('/project')
       
    def page_go_list_ouvrage(self,e):
        self.page.on_route_change('/list-ouvrage')
        
    def togle_theme(self,e):
        if self.page.theme_mode == ft.ThemeMode.DARK : 
            self.page.theme_mode=ft.ThemeMode.LIGHT
            set_value('theme','ThemeMode.LIGHT')
        else:
            self.page.theme_mode=ft.ThemeMode.DARK
            set_value('theme','ThemeMode.DARK')
        self.page.update()
