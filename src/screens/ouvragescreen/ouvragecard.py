import asyncio
import flet as ft

from myaction.myaction_ouvrage import Ouvrage, delete_ouvrage

class OuvrageCard(ft.Card):
    def __init__(self, state, ouvrage:Ouvrage, formcontrol):
        super().__init__()
        self.elevation=10
        self.state=state
        self.ouvrage=ouvrage
        self.formcontrol=formcontrol
        
        self.content=ft.Container(
            on_click=self.selectouvrage,
            padding= ft.Padding.all(10),
            data=ouvrage,
            ink=True,
            expand=True,
            content=ft.Row(
                    [      
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                [
                                    
                                    ft.Column(
                                        [
                                        ft.Text(f"Type : {ouvrage.type_ouvrage} / {ouvrage.etat} / {ouvrage.annee}", size=13, weight=ft.FontWeight.W_500),
                                        ft.Container(
                                            content=ft.Text(f"Lieu : {ouvrage.lieu} / localité : {ouvrage.localite} / canton : {ouvrage.canton} / Commune : {ouvrage.commune}", size=12, width=340,expand=True),
                                            ),
                                        ],
                                    ),
                                ],spacing=0
                            )
                            ),
                        
                    ],spacing=0
                )
            )
        
    async def selectouvrage(self, e):
        self.state.selected_ouvrage=self.ouvrage
        await self.page.push_route("/projet/list-ouvrage/recap-ouvrage")
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    