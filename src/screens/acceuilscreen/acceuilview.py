import asyncio
import flet as ft
from mystorage import *
from .drawer import page_drawer

class AcceuilView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding=0
        self.route="/"
        self.state=state
        page_height=get_value("win_height")
        bar_cnt=ft.Container(height=60,
                         content=ft.Row(
                             [
                                ft.IconButton(icon=ft.Icons.MENU,
                                              on_click= self.show_open_drawer
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
                content=ft.Column(
                    expand=True,
                    controls=[
                        bar_cnt,
                        ft.Container(
                            expand=1,
                            height=page_height-40,
                            image=ft.DecorationImage(
                                src="eau_home.png",
                                # fit=ft.BoxFit.COVER
                                )
                            ),
                        ft.Container(
                            expand=3,
                            bgcolor="#0a1d37",
                            border_radius=ft.BorderRadius.only(top_left=80),
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Button(" 📋  Projets ", 
                                                        on_click= self.go_projet_view, 
                                                        elevation=10),
                                                ],alignment=ft.MainAxisAlignment.CENTER,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Button("Statistiques", 
                                                            on_click=self.go_static_view, 
                                                            icon=ft.Icons.STACKED_LINE_CHART_OUTLINED,
                                                            elevation=10
                                                            )
                                                ],alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Button(" Listes Entreprises ", 
                                                        on_click=self.go_entreprise_view, 
                                                        elevation=10),
                                                ],alignment=ft.MainAxisAlignment.CENTER,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Button(" Listes Village sans forage ", 
                                                        on_click=self.go_village_view, 
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
                    ]
                )
            )
        ]
        
    
        
    async def go_projet_view(self,e):
        await self.handle_change()
        await self.page.push_route("/projet")
        
        
    async def go_stats(self,e):
        await self.handle_change()
        await self.page.push_route('/stats')
        
    async def go_apropos(self,e):
        await self.handle_change()
        await self.page.push_route("/apropos")
        
    async def handle_change(self):
        await self.page.close_drawer()
    
    async def go_archive(self,e):
        await self.handle_change()
        await self.page.push_route('/archive')
    
    async def go_settings(self,e):
        await self.handle_change()
        await self.page.push_route('/settings')

    async def show_open_drawer(self,e):
        self.page.drawer= page_drawer(handle_change=self.handle_change,
                                    go_apropos=self.go_apropos,
                                    go_archive=self.go_archive,
                                    go_stats=self.go_stats,
                                    go_settings=self.go_settings)
        await self.page.show_drawer()

    async def go_static_view(self,e):
        await self.page.push_route("/stats")
       
    async def go_village_view(self,e):
        await self.page.push_route("/list-village")
        
    async def go_entreprise_view(self,e):
        await self.page.push_route("/list-entreprise")
        
    def togle_theme(self,e):
        if self.page.theme_mode == ft.ThemeMode.DARK : 
            self.page.theme_mode=ft.ThemeMode.LIGHT
            set_value('theme','ThemeMode.LIGHT')
        else:
            self.page.theme_mode=ft.ThemeMode.DARK
            set_value('theme','ThemeMode.DARK')
        self.page.update()
