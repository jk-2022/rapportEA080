import asyncio
import flet as ft

from myaction.myaction_ouvrage import load_one_ouvrage
from screens.recapouvragescreen.ouvrages.onvragerecapcard import OuvrageRecapCard
from screens.recapouvragescreen.ouvrages.optioncard import OptionCard
from .localisationcard import LocalisationCard

# @control
class OuvrageControl(ft.Container):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.ouvrage=self.state.selected_ouvrage
        self.share=ft.Share()
        self.copy_text=ft.Clipboard()
        
        self.padding=ft.Padding.only(left=10,right=10)
        self.cont=ft.Column(spacing=10,
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            tight=True
                            )

        self.content=ft.Column(
                [
                    self.cont,
                ],alignment=ft.MainAxisAlignment.CENTER
            )

        self.updateData()
    
    def updateData(self):
        ouvrage_id=self.state.selected_ouvrage.id
        donnees=load_one_ouvrage(ouvrage_id)
        self.cont.controls.clear()
        # print(donnees)
        if donnees:
            self.cont.controls.append(
                LocalisationCard(donnees[0],self.copyCoords)
            )
            self.cont.controls.append(
                OuvrageRecapCard(donnees[0])
            )
            self.cont.controls.append(
                OptionCard(self.showUpdateData,self.shareData)
            )
    
    def showUpdateData(self):
        self.formcontrol.formcontrol.change_content('edit-ouvrage-content')
        
        
    def convert_data_to_text(self):
        datas=self.ouvrage.to_dict()
        text_to_shared=""
        key_data_ignored=["projet_id","id","ouvrage_id","localite","created_at","prefecture", 'Bon état', 'cause_panne','created_at',"annee"]
        val_ignored:str|float=["","0",0.0,"0.0",0,None]
        for key, val in datas.items():
            if key in key_data_ignored or val in val_ignored:
                pass 
            else:
                text_to_shared+=f"{key} : {val}\n"
        return text_to_shared

    async def shareData(self,e):
        text_to_shared=self.convert_data_to_text()
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )
    
    async def copyCoords(self):
        datas=self.ouvrage.to_dict()
        await self.copy_text.set(f"{datas['coordonnee_x'],datas['coordonnee_y']}")
        return self.page.show_dialog(ft.SnackBar(ft.Text("Coordonnées copiés avec succès")))


