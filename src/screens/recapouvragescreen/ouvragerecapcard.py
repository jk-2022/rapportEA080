
import flet as ft
from uix.customtitlelabel import CustomTitleLabel

class OuvrageRecapCard(ft.Card):
    def __init__(self, state, donnees):
        super().__init__()
        self.state=state
        self.donnees=donnees
        self.elevation=5
        self.cont=ft.Column( spacing=0)
        self.cont.controls.clear()
        if donnees:
            list_item=['id','projet_id','localisation_id','created_at']
            for key, val in donnees.items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val))
        else:
            self.cont.controls.append(ft.Row(
                [
                    ft.Text("Pas de données de Localisation enrégistré")
                ],alignment=ft.MainAxisAlignment.CENTER))
        try:
            self.cont.update()
        except:
            pass

        self.content=ft.Container(
            border_radius=10,
            border=ft.Border.all(1,ft.Colors.YELLOW_500),
            expand=True,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Localisation",text_align=ft.TextAlign.CENTER,color=ft.Colors.YELLOW_500)
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.cont,
                    ft.Row(
                        [
                            ft.Button('Maps',icon=ft.Icons.MAP,icon_color=ft.Colors.GREEN_500,on_click=""),
                        ]
                        # ,alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
                ]
            )
        )


 


    