import flet as ft

from myaction.myaction_foration import delete_foration, load_one_foration
from screens.recapouvragescreen.foration.forationcard import ForationCard

from .forationform import ForationForm
from .forationupdateform import ForationUpdateForm
from uix.customtitlelabel import CustomTitleLabel


# @ft.control
class ForationControl(ft.Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        self.share=ft.Share()
        
        self.cont=ft.Column(spacing=0,
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE
                            )

        self.content=ft.Column([
                    self.cont,
                ],alignment=ft.MainAxisAlignment.CENTER
            )

        self.updateData()
    
    def updateData(self):
        self.donnees=load_one_foration(self.state.selected_ouvrage.id) # important pr update
        self.cont.controls.clear()
        if self.donnees:
            self.cont.controls.append(
                        ForationCard(self.donnees,self.showUpdateData,self.showDelete,self.shareData)
                    )
        else:
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
        rid=int(self.self.donnees[0]['id'])
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
        
    def convert_data_to_text(self):
        datas=self.state.selected_ouvrage.to_dict_other()
        # print(datas)
        title="Localisation".center(20,"*")
        text_to_shared=""
        text_to_shared+=f"{title}\n"
        
        for key, val in datas.items():
            text_to_shared+=f"{key} : {val}\n"
        title2="Foration".center(20,"*")
        text_to_shared+=f"{title2}\n"
        key_data_ignored=["id","ouvrage_id",'created_at']
        val_ignored:str|float=["","0",0.0,"0.0",0,None]
        for key, val in self.donnees[0].items():
            if key in key_data_ignored or val in val_ignored:
                pass 
            else:
                text_to_shared+=f"{key} : {val}\n"
        return text_to_shared

    async def shareData(self,e):
        text_to_shared=self.convert_data_to_text()
        # print(text_to_shared)
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )

    def close_dlg(self):
        self.page.pop_dialog()

