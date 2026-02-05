import flet as ft

from .datatablestat import Mytable_detail_ouvrage, tb_detail_ouvrage


# @ft.control
class StatDetailCard(ft.Card):
    def __init__(self, stats_data):
        super().__init__()
        self.elevation=5
        self.stats_data=stats_data

        self.tab_cnt_general=ft.Column(
            expand=True, 
            scroll=ft.ScrollMode.ALWAYS )
        
        self.content=ft.Container(
            padding=ft.Padding.all(10),
            expand=True,
            content=ft.Column(
                        [   
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        tb_detail_ouvrage.rows=[]
        for ouvrage in stats_data:
            tb_detail_ouvrage.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(ouvrage['type_ouvrage'])),
                                ft.DataCell(ft.Text(ouvrage['lieu'])),
                                ft.DataCell(ft.Text(ouvrage['canton'])),
                                ft.DataCell(ft.Text(ouvrage['commune'])),
                                ft.DataCell(ft.Text(ouvrage['etat'])),
                                ft.DataCell(ft.Text(ouvrage['annee'])),
                            ]
                        )
                    )
            cont=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(f"Listes des ouvrages")
                            )
                        ],alignment=ft.MainAxisAlignment.CENTER,
                    
                    ),
                    Mytable_detail_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
