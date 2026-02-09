import flet as ft
from uix.customtitlelabel import CustomTitleLabel

def OuvrageRecapCard(ouvrage):
    type_ouvrage=ft.Row(
                        [
                            CustomTitleLabel(title="Type ouvrage",value=f"{ouvrage['type_ouvrage']}"),
                        ]
                    )
    numero_irh=ft.Row(
                        [
                            CustomTitleLabel(title="Numero irh",value=f"{ouvrage['numero_irh']}"),
                        ]
                    )
    annee=ft.Row(
                        [
                            CustomTitleLabel(title="Année",value=f"{ouvrage['annee']}"),
                        ]
                    )
    type_reservoir=ft.Row(
                        [
                            CustomTitleLabel(title="Type reservoir",value=f"{ouvrage['type_reservoir']}"),
                        ]
                    )
    type_energie=ft.Row(
                        [
                            CustomTitleLabel(title="Type énergie",value=f"{ouvrage['type_energie']}"),
                        ]
                    )
    etat=ft.Row(
                    [
                        CustomTitleLabel(title="Etat",value=f"{ouvrage['etat']}"),
                    ]
                )
    cause_panne=ft.Row(
                        [
                            CustomTitleLabel(title="Cause panne",value=f"{ouvrage['cause_panne']}"),
                        ]
                    )
    observation=ft.Row(
                        [
                            CustomTitleLabel(title="observation",value=f"{ouvrage['observation']}"),
                        ]
                    )
    if ouvrage['type_ouvrage']=="PMH":
        type_reservoir.visible=False 
        type_energie.visible=False 
        
    if ouvrage['etat']=="Bon état":
        cause_panne.visible=False
        
    if ouvrage['observation']=="":
        observation.visible=False
        
    return ft.Card(
        elevation=5,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    border_radius=ft.BorderRadius.only(bottom_right=10),
                    bgcolor="#143a6e",
                    padding=ft.Padding.only(left=5,right=5),
                    content=ft.Text("Ouvrage",color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ),
                ft.Container(
                    padding=ft.Padding.all(10),
                    border_radius=ft.BorderRadius.only(bottom_right=10, bottom_left=10),
                    border=ft.Border.only(left=ft.BorderSide(width=4, color="#0a1d37")),
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            type_ouvrage,
                            numero_irh,
                            annee,
                            type_reservoir,
                            type_energie,
                            etat,
                            cause_panne,
                            observation,
                        ]
                    )
                )
            ]
        )
    )
    