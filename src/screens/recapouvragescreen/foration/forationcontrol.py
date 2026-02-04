import flet as ft

from myaction.myaction_foration import delete_foration, load_one_foration

from .forationform import ForationForm
from .forationupdateform import ForationUpdateForm
from uix.customtitlelabel import CustomTitleLabel


# @ft.control
class ForationControl(ft.Card):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.elevation=5
        self.cont=ft.Column( spacing=0)

        self.delete_btn=ft.Button('Supprimer',
                                  icon=ft.Icons.DELETE,
                                  icon_color=ft.Colors.RED,
                                  on_click=lambda e: self.showDelete()
                                  )
        self.delete_btn.visible=False

        self.content=ft.Container(
            border_radius=10,
            border=ft.Border.all(1,ft.Colors.BLUE_500),
            expand=True,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Foration",text_align=ft.TextAlign.CENTER,color=ft.Colors.BLUE_500)
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.cont,
                    ft.Row(
                        [
                            ft.Button('Modifier',icon=ft.Icons.UPDATE,icon_color=ft.Colors.GREEN_500,on_click=lambda e : self.showUpdateData()),
                            self.delete_btn,
                        ],alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
                ],alignment=ft.MainAxisAlignment.CENTER
            )
        )

        self.updateData()
    
    def updateData(self):
        donnees=load_one_foration(self.state.selected_ouvrage.id)
        self.donnees=donnees # important pr update
        self.cont.controls.clear()
        if donnees:
            self.delete_btn.visible=True
            list_item=['id','ouvrage_id','created_at']
            for key, val in donnees[0].items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val)
                    )
        else:
            self.delete_btn.visible=False
            self.cont.controls.append(ft.Row(
                [
                    ft.Text("Pas de données de FORATION enrégistré")
                ],alignment=ft.MainAxisAlignment.CENTER))
        

    def showDelete(self):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmation"),
            content=ft.Row(
                [
                    ft.Text(f"Voulez-vous supprimer ?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Non", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Oui", on_click=lambda e: self.del_foration(), icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        self.page.update()
        
    def del_foration(self):
        rid=int(self.donnees[0]['id'])
        delete_foration(rid)
        self.page.pop_dialog()
        self.updateData()
    
    def showUpdateData(self):
        if self.donnees==[]:
            cont=ForationForm(state=self.state,formcontrol=self)
        else:
            cont=ForationUpdateForm(state=self.state, donnees=self.donnees[0] , formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Info Foration"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Sauvegarder", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

    def close_dlg(self):
        self.page.pop_dialog()

