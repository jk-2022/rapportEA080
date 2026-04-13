import asyncio
import flet as ft

from myaction.db_actions import Ouvrage, load_one_projets
from utils.constants import TEXT_DARK, TEXT_GREY, categorie_chip, etat_badge


class AllOuvrageCard(ft.Card):
    def __init__(self, state, ouvrage:Ouvrage,  formcontrol):
        super().__init__()
        self.elevation=10
        self.state=state
        self.ouvrage=ouvrage
        self.formcontrol=formcontrol
        # self.check_box=ft.Checkbox(on_change= lambda e: selected_bool_ouvrage(ouvrage),value=False)
        
        self.content=ft.Container(
            on_click=self.selectouvrage,
            padding= ft.Padding.all(10),
            data=ouvrage,
            ink=True,
            expand=True,
            content=ft.Row(
                    [      
                        ft.Column(
                            [
                                ft.Row([
                                    ft.Row([
                                            ft.Icon(ft.Icons.LOCATION_ON, size=12, color=TEXT_GREY),
                                            ft.Text(f"{ouvrage.lieu}-{ouvrage.canton}", color=TEXT_GREY, size=12),
                                            categorie_chip(ouvrage.type_ouvrage),
                                            etat_badge(ouvrage.etat),
                                        ], spacing=4),
                                    ft.Text(f"Num° Irh :{ouvrage.numero_irh  or ' -- '}", weight=ft.FontWeight.BOLD, color=TEXT_DARK, size=14),
                                    ft.Text(f"Année : {ouvrage.annee or ' -- '}", color=TEXT_GREY, size=12),
                                ], spacing=6, wrap=True),
                                # ft.Text(f"Débit : {o.debit} m³/h", color=TEXT_GREY, size=12),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        
                    ],spacing=0
                )
            )
        
    async def selectouvrage(self, e):
        self.state.selected_ouvrage=self.ouvrage
        self.state.selected_projet=load_one_projets(self.ouvrage.projet_id)[0]
        await self.page.push_route("/projet/list-ouvrage/detail-ouvrage")
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    