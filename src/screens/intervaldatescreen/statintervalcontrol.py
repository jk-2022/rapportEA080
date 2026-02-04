import flet as ft

from uix.customtitlelabel import CustomTitleLabel
from .datatablestat import Mytable_ouvrage, tb_ouvrage


# @ft.control
class StatIntervalControl(ft.Card):
    def __init__(self, stats_data):
        super().__init__()
        self.elevation=5
        self.stats_data=stats_data

        self.tab_cnt_general=ft.Column(
            expand=True, 
            scroll=ft.ScrollMode.ALWAYS)

        self.content=ft.Container(
            padding=ft.padding.all(10),
            expand=True,
            content=ft.Column(
                        [   ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            f"Statsistiques par intervalle de date", 
                                            size=11, 
                                            italic=True),
                                            alignment=ft.Alignment.CENTER
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER
                            ),
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        stats=stats_data['par_type_global']['par_type']
        stats_commune=stats_data['par_commune']
        texte_commune=''
        for commune in stats_commune.keys():
            texte_commune+=f"{commune}/"
        texte_commune=texte_commune[:-1]
    
        stats_canton=stats_data['par_canton']
        texte_canton=''
        for canton in stats_canton.keys():
            texte_canton+=f"{canton}/"
        texte_canton=texte_canton[:-1]
        
        tb_ouvrage.rows=[]
        for types in stats.keys():
            tb_ouvrage.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(types)),
                                ft.DataCell(ft.Text(stats[types]['Bon état'])),
                                ft.DataCell(ft.Text(stats[types]['En panne'])),
                                ft.DataCell(ft.Text(stats[types]['Abandonné'])),
                                ft.DataCell(ft.Text(stats[types]['Total'])),
                            ]
                        )
                    )
            cont=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(f"les dates")
                            )
                        ],alignment=ft.MainAxisAlignment.CENTER,
                    
                    ),
                    ft.Column(
                        [
                            CustomTitleLabel(title="Total Ouvrages",value=stats_data['total_ouvrages']),
                            CustomTitleLabel(title="Total Communes",value=stats_data['total_communes']),
                            CustomTitleLabel(title="Total Cantons",value=stats_data['total_cantons']),
                            CustomTitleLabel(title="Liste Communes",value=texte_commune),
                            CustomTitleLabel(title="Liste Cantons",value=texte_canton),
                        ],spacing=0
                    ),
                    Mytable_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
