import flet as ft

from uix.customtitlelabel import CustomTitleLabel
from .datatablestat import Mytable_ouvrage, tb_ouvrage


class StatGeneralCard(ft.Card):
    def __init__(self, stat_general):
        super().__init__()
        self.elevation=5
        self.expand=True
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
                                content=ft.Text(f"Statistiques générale", size=11, italic=True),align=ft.Alignment.CENTER
                        )
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Column(
                        [
                            CustomTitleLabel(title="Nombre de Projet",value=stat_general['nombre_projet']),
                            CustomTitleLabel(title="Nombre de commune",value=stat_general['nombre_commune']),
                            CustomTitleLabel(title="Nombre de canton",value=stat_general['nombre_canton']),
                            CustomTitleLabel(title="Nombre en état",value=stat_general['total_bon_etat']),
                            CustomTitleLabel(title="Nombre en panne",value=stat_general['total_panne']),
                            CustomTitleLabel(title="Nombre Abandonné",value=stat_general['total_abandonne']),
                            CustomTitleLabel(title="Nombre d'ouvrages",value=stat_general['total_ouvrages']),
                        ],spacing=0
                    ),
                    self.tab_cnt_general,
                    ],scroll=ft.ScrollMode.ALWAYS, expand=True
                ))
        tb_ouvrage.rows=[]
        self.tab_cnt_general.controls.clear()
        for types in stat_general['par_type'].keys():
            tb_ouvrage.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(types)),
                                ft.DataCell(ft.Text(stat_general['par_type'][types]['Bon état'])),
                                ft.DataCell(ft.Text(stat_general['par_type'][types]['En panne'])),
                                ft.DataCell(ft.Text(stat_general['par_type'][types]['Abandonné'])),
                                ft.DataCell(ft.Text(stat_general['par_type'][types]['total_ouvrage'])),
                            ]
                        )
                    )
        self.tab_cnt_general.controls.append(Mytable_ouvrage)
    
   

