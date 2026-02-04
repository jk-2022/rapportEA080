import flet as ft

from myaction.myaction_ouvrage import load_one_ouvrage
from uix.customtitlelabel import CustomTitleLabel

# @control
class OuvrageControl(ft.Card):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.cont=ft.Column( spacing=0)

        self.content=ft.Container(
            border_radius=10,
            border=ft.Border.all(1,ft.Colors.GREEN_500),
            content=ft.Column(
                [
                    self.cont,
                    ft.Row(
                        [
                            ft.Button('Modifier',icon=ft.Icons.UPDATE,icon_color=ft.Colors.GREEN_500,on_click=lambda e: self.showUpdateData()),
                            ft.Button('Partager',icon=ft.Icons.SHARE,icon_color=ft.Colors.RED,on_click=lambda e: self.shareData),
                        ],alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
                ],alignment=ft.MainAxisAlignment.CENTER
            )
        )

        self.updateData()
    
    def updateData(self):
        ouvrage_id=self.state.selected_ouvrage.id
        donnees=load_one_ouvrage(ouvrage_id)
        self.cont.controls.clear()
        if donnees:
            list_item=['id','projet_id','ouvrage_id','created_at']
            for key, val in donnees[0].items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val)
                    )
    
    def showUpdateData(self):
        self.page.on_route_change("/edit-ouvrage")
        

    def shareData(self,e):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmation"),
            content=ft.Row(
                [
                    ft.Text(f"Voulez-vous Partager ?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Non", on_click=self.close_dlg),
                ft.TextButton("Oui", on_click=self.del_ouvrage, icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        self.page.update()
        
    def del_ouvrage(self,e):
        print("partage effectuer")
        self.page.pop_dialog()
        self.updateData()


    def close_dlg(self, e):
        self.page.pop_dialog()
        # self.page.update()

