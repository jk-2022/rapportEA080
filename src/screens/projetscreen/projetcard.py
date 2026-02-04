import flet as ft

from mystorage import *
from screens.projetscreen.projetupdateform import ProjetUpdateForm
from myaction.myaction_projet import delete_projet, Projet

class ProjetCard(ft.Card):
    def __init__(self, state, projet: Projet, formcontrol):
        super().__init__()
        self.state=state
        self.elevation=2
        self.projet=projet
        self.formcontrol=formcontrol

        self.content=ft.Container(
            on_click=lambda e: self.selectprojet(),
            padding=ft.Padding.all(10),
            data=projet,
            ink=True,
            # expand=True,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"{projet.name}", size=13,
                                    weight=ft.FontWeight.BOLD),
                            ],alignment=ft.MainAxisAlignment.CENTER
                        )
                        ),
                    ft.VerticalDivider(color=ft.Colors.RED,width=5),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text(
                                                f"{projet.title}\nSecteurs: {projet.secteurs}", 
                                                size=13,width=300)
                                        ],expand=True
                                    )
                                    ),
                            ],alignment=ft.MainAxisAlignment.CENTER
                        )
                        ,expand=True
                        ),
                    ft.Column(
                            [
                                ft.IconButton(icon=ft.Icons.EDIT, on_click= lambda e :self.show_edit_projet()),
                                ft.IconButton(icon=ft.Icons.DELETE, on_click= lambda e :self.show_delete_projet()),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            expand_loose=True
                        )
                    ]
                ))
        
        
    def selectprojet(self):
        self.state.selected_projet=self.projet
        self.page.on_route_change("/list-ouvrage")

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