import flet as ft

from .pompagecard import PompageCard

from .pompageform import PompageForm
from .pompageupdateform import PompageUpdateForm

from myaction.myaction_pompage import delete_pompage, load_one_pompage


@ft.control
class PompageControl(ft.Container):
    def __init__(self, state,  formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        self.cont=ft.Column(
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
            )

        self.content=ft.Column(
                controls=[
                    self.cont,
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            )
        

        self.updateData()

    def updateData(self):
        ouvrage=self.state.selected_ouvrage
        self.donnees=load_one_pompage(ouvrage.id)
        #Important pour stocker les self.donnees en cas d'update
        # print('self.donnees',self.donnees)
        self.cont.controls.clear()
        if self.donnees:
            self.cont.controls.append(PompageCard(self.donnees,self.showUpdateData, self.showDelete, self.shareData))
        else:
            self.cont.controls.append(ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Text("Pas de données de POMPAGE enrégistré")
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            ft.Button("Inserer les données", on_click=lambda e: self.show_create_pompage())
                        ],alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
                )
            )
        
    def showUpdateData(self):
        if self.donnees==[]:
            cont=PompageForm(state=self.state,formcontrol=self)
        else:
            cont=PompageUpdateForm(state=self.state, donnees=self.donnees[0], formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier Pompage"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=self.close_dlg),
                ft.TextButton("Sauvegarder", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def show_create_pompage(self):
        suivi_cont = PompageForm(state=self.state, formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Pompage"),
            content=suivi_cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Enregistrer", on_click=lambda e: suivi_cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

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
                ft.TextButton("Non", on_click=self.close_dlg),
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
        delete_pompage(rid)
        self.updateData()
        self.page.pop_dialog()
    
    def convert_data_to_text(self):
        datas=self.state.selected_ouvrage.to_dict_other()
        # print(datas)
        title="Localisation".center(20,"*")
        text_to_shared=""
        text_to_shared+=f"{title}\n"
        
        for key, val in datas.items():
            text_to_shared+=f"{key} : {val}\n"
        title2="Pompage".center(20,"*")
        text_to_shared+=f"{title2}\n"
        key_data_ignored=["id","ouvrage_id",'created_at']
        val_ignored:str|float=["","0",0.0,"0.0",0,None]
        # print("self.donnees",self.donnees)
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

