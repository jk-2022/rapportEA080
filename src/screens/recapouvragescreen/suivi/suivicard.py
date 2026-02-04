import flet as ft

from myaction.myaction_suivi import Suivi, delete_suivi
from screens.recapouvragescreen.suivi.suiviupdateform import SuiviUpdateForm


@ft.control
class SuiviCard(ft.Card):
    def __init__(self, state, suivi: Suivi, formcontrol):
        super().__init__()
        # self.expand=True
        self.elevation=2
        self.state=state
        self.suivi=suivi
        self.formcontrol=formcontrol
        
        self.content=ft.Container(
            # on_click= lambda e: self.selectsuivi(),
            padding= ft.Padding.all(10),
            data=suivi,
            ink=True,
            expand=True,
            content=ft.Column(
                            [
                                
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                [
                                    
                                    ft.Column(
                                        [
                                        ft.Text(
                                            f"{suivi.type_reception} du {suivi.date_reception}", 
                                            size=13, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text(f"Participants : {suivi.participants}\nRecommandations :   {suivi.recommandation} \nObservations : {suivi.observation}", 
                                            size=12, width=400, expand=True),
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e: self.show_edit_suivi()),
                                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e=self.suivi: self.show_delete_suivi()),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                    )
                                ],spacing=0
                            )
                            ),
                    ],spacing=0
                )
            )
        
        
    def show_edit_suivi(self):
        self.state.selected_suivi=self.suivi
        cont=SuiviUpdateForm(state=self.state, suivi=self.suivi, formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier projet"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e :self.close_dlg()),
                ft.TextButton("Modifier", on_click=lambda e :cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)


    def show_delete_suivi(self):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Suppression"),
            content=ft.Row(
                [
                    ft.Text(f"⚠️ Voulez-vous supprimer ?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Annuler", on_click=lambda e:self.close_dlg()),
                ft.TextButton("Supprimer", 
                              icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700,
                              on_click=lambda e, s=self.suivi.id:self.del_suivi(s)
                              ),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    def del_suivi(self,s):
        delete_suivi(s)
        self.formcontrol.updateData()
        self.page.pop_dialog()
        
    