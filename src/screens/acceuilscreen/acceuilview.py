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
                                            #   on_click=lambda e: asyncio.create_task(self.open_drawer())
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
                                                on_click= self.go_projet_view, 
                                                elevation=10),
                                        ],alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Button(" Listes Entreprises ", 
                                                on_click=lambda e: asyncio.create_task(self.page.push_route("/list-entreprise")), 
                                                elevation=10),
                                        ],alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Button(" Listes Village sans forage ", 
                                                on_click=lambda e: asyncio.create_task(self.page.push_route("/list-village")), 
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
        
    
        
    async def go_projet_view(self,e):
        # await handle_change()
        await self.page.push_route("/projet")
        
    async def go_apropos(self,e):
        # await handle_change()
        self.page.on_route_change("/apropos")
        
    async def handle_change(self):
        await self.page.close_drawer()
    
    async def go_archive(self,e):
        # await handle_change()
        self.page.on_route_change('/archive')
    
    async def go_settings(self,e):
        # await handle_change()
        self.page.on_route_change('/settings')
    
    async def go_stats(self,e):
        # await handle_change()
        self.page.on_route_change('/stats')
        
    

    async def open_drawer(self):
        self.page.drawer= page_drawer(handle_change=self.handle_change,
                                    go_apropos=self.go_apropos,
                                    go_archive=self.go_archive,
                                    go_stats=self.go_stats,
                                    go_settings=self.go_settings)
        await self.page.show_drawer()

    # async def page_go_project(self,e):
    #     print(e)
    #     await self.page.push_route('/projet')
       
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
