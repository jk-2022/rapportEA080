import flet as ft

from uix.customtitlelabel import CustomTitleLabel
from .datatablestat import Mytable_ouvrage, tb_ouvrage

class StatCommuneControl(ft.Card):
    def __init__(self, commune, stat_general):
        super().__init__()
        self.elevation=5
        self.stat_general=stat_general

        self.tab_cnt_general=ft.Column(
            expand=True, 
            scroll=ft.ScrollMode.ALWAYS
            )

        self.content=ft.Container(
            padding=ft.Padding.all(10),
            expand=True,
            content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(f"Statsistiques pour", 
                                                     size=11, italic=True),
                                                     align=ft.Alignment.CENTER
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER
                            ),
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        stat_commune=stat_general['par_type']
        tb_ouvrage.rows=[]
        for types in stat_commune.keys():
            tb_ouvrage.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(types)),
                                ft.DataCell(ft.Text(stat_commune[types]['Bon état'])),
                                ft.DataCell(ft.Text(stat_commune[types]['En panne'])),
                                ft.DataCell(ft.Text(stat_commune[types]['Abandonné'])),
                                ft.DataCell(ft.Text(stat_commune[types]['total_ouvrage'])),
                            ]
                        )
                    )
        cont=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"{commune}")
                        )
                    ],alignment=ft.MainAxisAlignment.CENTER,
                
                ),
                ft.Column(
                    [
                        CustomTitleLabel(title="Nombre en état",value=stat_general['total_bon_etat']),
                        CustomTitleLabel(title="Nombre en panne",value=stat_general['total_panne']),
                        CustomTitleLabel(title="Nombre Abandonné",value=stat_general['total_abandonne']),
                        CustomTitleLabel(title="Nombre d'ouvrages",value=stat_general['total_ouvrages'])
                    ],spacing=0
                ),
                Mytable_ouvrage
            ]
        )
        self.tab_cnt_general.controls.append(cont)
