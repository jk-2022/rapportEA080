import flet as ft

from myaction.myaction_panne import Panne, delete_panne
from screens.recapouvragescreen.pannes.panneupdateform import PanneUpdateForm


@ft.control
class PanneCard(ft.Card):
    def __init__(self, state, panne: Panne, formcontrol):
        super().__init__()
        # self.expand=True
        self.elevation=2
        self.state=state
        self.panne=panne
        self.formcontrol=formcontrol
        
        self.content=ft.Container(
            # on_click= lambda e: self.selectpanne(),
            padding= ft.Padding.all(10),
            data=panne,
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
                                            f"{panne.date_signaler}", 
                                            size=13, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text(f"Causes : {panne.description}\nSolutions :   {panne.solution} \nObservations : {panne.observation}", 
                                            size=12, width=400, expand=True),
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e: self.show_edit_panne()),
                                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e=self.panne: self.show_delete_panne()),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                    )
                                ],spacing=0
                            )
                            ),
                    ],spacing=0
                )
            )
        
        
    def show_edit_panne(self):
        self.state.selected_panne=self.panne
        cont=PanneUpdateForm(state=self.state, panne=self.panne, formcontrol=self)
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


    def show_delete_panne(self):
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
                              on_click=lambda e, s=self.panne.id:self.del_panne(s)
                              ),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def close_dlg(self):
        self.page.pop_dialog()
        
    def del_panne(self,s):
        delete_panne(s)
        self.formcontrol.updateData()
        self.page.pop_dialog()
        
    