import flet as ft

from .pannes.pannecontrol import PanneControl
from .suivi.suivicontrol import SuiviControl
from .ouvrages.ouvragecontrol import OuvrageControl
from .pompage.pompagecontrol import PompageControl
from .foration.forationcontrol import ForationControl

from myaction.myaction_main import load_all_data


class RecapOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state=state
        self.projet=self.state.selected_projet
        self.ouvrage=self.state.selected_ouvrage

        self.clipboard = ft.Clipboard()
        self.share=ft.Share()

        self.ouvrages_cnt=OuvrageControl(state=self.state,formcontrol=self)
        self.pompage_cnt=PompageControl(state=self.state,formcontrol=self)
        self.foration_cnt=ForationControl(state=self.state,formcontrol=self)
        self.suivi_cont=SuiviControl(state=self.state)
        self.panne_cont=PanneControl(state=self.state)

        self.controls=[
            ft.Container(height=5),
            ft.Row(
                    [
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click= lambda e:self.page.on_view_pop()),
                    ft.Text("RECAP", text_align=ft.TextAlign.CENTER)
                    ]
                    # ,alignment=MainAxisAlignment.CENTER
                ),
                ft.Tabs(
                    length=5,
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(label="Ouvrage"),
                                    ft.Tab(label="pompage"),
                                    ft.Tab(label="foration"),
                                    ft.Tab(label="suivi"),
                                    ft.Tab(label="pannes"),
                                ]
                            ),
                            ft.TabBarView(
                                expand=True,
                                controls=[
                                    self.ouvrages_cnt,
                                    self.pompage_cnt,
                                    self.foration_cnt,
                                    self.suivi_cont,
                                    self.panne_cont,

                                ]
                            )
                        ]
                    )
                ),
            ft.Row(
                [
                    ft.Button("save pdf",icon=ft.Icons.PICTURE_AS_PDF, on_click= lambda e : self.show_no_make()),
                    ft.Button("Copy",icon=ft.Icons.COPY, on_click= self.copy_data),
                    ft.Button("Partager",icon=ft.Icons.SHARE, on_click= self.to_share_text),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
            
        ]

    def covert_data_to_text(self):
        datas=load_all_data(self.ouvrage.id)
        tex_to_shared=""
        key_data_ignored=["projet_id","id","ouvrage_id","localite","created_at","prefecture", 'Bon état', 'cause_panne','created_at',"annee"]
        val_ignored:str|float=["","0",0.0,"0.0",0,None]
        for data in datas.keys():
            if datas[data]:
                title=data.center(30,"*")
                tex_to_shared+=f"{title}\n"
                for key, val in datas[data][0].items():
                    if key in key_data_ignored or val in val_ignored:
                        pass 
                    else:
                        tex_to_shared+=f"{key} : {val}\n"
        return tex_to_shared


    def show_no_make(self):
        return self.page.show_dialog(ft.SnackBar(ft.Text("option non valide pour l'instant")))
    
    async def to_share_text(self):
        text_to_shared=self.covert_data_to_text()
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )
    
    async def copy_data(self):
        text_to_shared=self.covert_data_to_text()
        await self.clipboard.set(text_to_shared)

    def close_dlg(self,e):
        self.page.pop_dialog()
        self.page.update()