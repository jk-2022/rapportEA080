import flet as ft
import asyncio
from mystorage import *
from screens.projetscreen.projetupdateform import ProjetUpdateForm
from myaction.db_actions import delete_projet, Projet
from utils.constants import PRIMARY, TEXT_DARK, TEXT_GREY


class ProjetCard(ft.Card):
    def __init__(self, state, projet: Projet, formcontrol):
        super().__init__()
        self.state=state
        self.elevation=2
        self.projet=projet
        self.formcontrol=formcontrol

        self.content=ft.Container(
            on_click=self.selectprojet,
            padding=ft.Padding.all(10),
            data=projet,
            ink=True,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.FOLDER, color="#FFFFFF", size=24),
                        bgcolor=PRIMARY,
                        border_radius=ft.BorderRadius(10, 10, 10, 10),
                        padding=ft.Padding(10, 10, 10, 10),
                    ),
                    ft.Column(
                        [
                            ft.Text(projet.name, weight=ft.FontWeight.BOLD, color=TEXT_DARK, size=14),
                            ft.Text(projet.title or "Aucune description",
                                    color=TEXT_GREY, size=12, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            # ft.Text(f"{p.date_debut} — {p.date_fin}",
                            #         color=TEXT_GREY, size=11),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        icon_color=TEXT_GREY,
                        items=[
                            ft.PopupMenuItem(
                                ft.Text("Ouvrir"),
                                icon=ft.Icons.OPEN_IN_NEW,
                                on_click= self.selectprojet,
                            ),
                            ft.PopupMenuItem(
                                ft.Text("Modifier"),
                                icon=ft.Icons.EDIT,
                                on_click=lambda _: self.show_edit_projet(),
                            ),
                            ft.PopupMenuItem(
                                ft.Text("Supprimer"),
                                icon=ft.Icons.DELETE,
                                on_click=lambda _: self.show_delete_projet(),
                            ),
                        ],
                    ),
                    ]
                ))
        
    
        
    async def selectprojet(self,e):
        self.state.selected_projet=self.projet
        await self.page.push_route("/projet/list-ouvrage")

    def show_delete_projet(self):
        name=self.projet.name
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Suppression"),
            content=ft.Row(
                [
                    ft.Text(f"⚠️ Voulez-vous supprimer {name} ?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Annuler", on_click=lambda e:self.close_dlg()),
                ft.TextButton("Supprimer",
                              icon=ft.Icons.DELETE, 
                              icon_color=ft.Colors.RED_700, 
                              on_click=lambda e:self.del_projet()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def show_edit_projet(self):
        cont=ProjetUpdateForm( projet=self.projet,formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier projet"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Modifier", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    def del_projet(self):
        delete_projet(projet_id=self.projet.id)
        self.page.pop_dialog()
        self.formcontrol.load_projects()