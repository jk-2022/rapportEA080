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
                        ft.Container(
                            content=ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.EDIT, 
                                                on_click=lambda e: self.show_edit_ouvrage(),
                                                ),
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE, 
                                                on_click=lambda e: self.show_delete_ouvrage(),
                                                ),
                                        ],
                                    )
                        )
                    ],spacing=0
                )
            )
        
    async def selectouvrage(self, e):
        self.state.selected_ouvrage=self.ouvrage
        await self.page.push_route("/projet/list-ouvrage/recap-ouvrage")
        
    def show_edit_ouvrage(self):
        self.state.selected_ouvrage=self.ouvrage 
        self.formcontrol.formcontrol.change_content("edit-ouvrage-content")

    def show_delete_ouvrage(self):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Suppression"),
            content=ft.Row(
                [
                    ft.Text(f"⚠️ Voulez-vous supprimer ?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_dlg),
                ft.TextButton("Supprimer", on_click=self.del_ouvrage),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    def del_ouvrage(self):
        delete_ouvrage(self.ouvrage.id)
        self.formcontrol.load_ouvrages()
        self.page.pop_dialog()
        
    