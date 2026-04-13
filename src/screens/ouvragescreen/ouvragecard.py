import asyncio
import flet as ft

from myaction.db_actions import Ouvrage
from utils.constants import TEXT_DARK, TEXT_GREY, categorie_chip, etat_badge


class OuvrageCard(ft.Card):
    def __init__(self, state, ouvrage:Ouvrage, selected_bool_ouvrage, formcontrol):
        super().__init__()
        self.elevation=10
        self.state=state
        self.ouvrage=ouvrage
        self.formcontrol=formcontrol
        self.check_box=ft.Checkbox(on_change= lambda e: selected_bool_ouvrage(ouvrage),value=False)
        
        self.content=ft.Container(
            on_click=self.selectouvrage,
            padding= ft.Padding.all(10),
            data=ouvrage,
            ink=True,
            expand=True,
            content=ft.Row(
                    [      
                        self.check_box,
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
                        # ft.PopupMenuButton(
                        #     icon=ft.Icons.MORE_VERT,
                        #     icon_color=TEXT_GREY,
                        #     items=[
                        #         ft.PopupMenuItem(ft.Text("Détails"), icon=ft.Icons.INFO,
                        #                         on_click=lambda _, ouv=o: self._open_detail(ouv)),
                        #         ft.PopupMenuItem(ft.Text("Modifier"), icon=ft.Icons.EDIT,
                        #                         on_click=lambda _, ouv=o: self._open_edit_dialog(ouv)),
                        #         ft.PopupMenuItem(ft.Text("Supprimer"), icon=ft.Icons.DELETE,
                        #                         on_click=lambda _, ouv=o: self._confirm_delete(ouv)),
                        #     ],
                        # ),
                        
                        # ft.Container(
                        #     expand=True,
                        #     content=ft.Column(
                        #         [
                                    
                        #             ft.Column(
                        #                 [
                        #                 ft.Row(
                        #                     [
                        #                         ft.Text(f"{ouvrage.type_ouvrage} / {ouvrage.etat} / {ouvrage.annee}", size=13, weight=ft.FontWeight.W_500),
                        #                         ft.Text(f"{ouvrage.suivi}", color="#005bdb", size=10)
                        #                     ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        #                     ),
                        #                 ft.Container(
                        #                     content=ft.Text(f"Lieu : {ouvrage.lieu} / canton : {ouvrage.canton} / Entrep. : {ouvrage.entreprise}", size=12, width=340,expand=True),
                        #                     ),
                        #                 ],
                        #             ),
                        #         ],spacing=0
                        #     )
                        #     ),
                        
                    ],spacing=0
                )
            )
        
    async def selectouvrage(self, e):
        self.state.selected_ouvrage=self.ouvrage
        await self.page.push_route("/projet/list-ouvrage/detail-ouvrage")
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    