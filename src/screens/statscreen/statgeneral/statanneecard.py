# import os
import flet as ft
from .datatablestat import Mytable_annee, tb_annee

# @ft.control
class StatAnneeCard(ft.Card):
    def __init__(self,stat_general):
        super().__init__()
        self.tab_cnt_annee=ft.Column()
        self.elevation=5
        self.stat_general=stat_general

        self.annee = ft.Dropdown(
            label="Voir stat par Année", 
            expand=True,
            on_text_change=lambda e :self.show_tab_stat_by_annee(e))
        for key in stat_general['par_annee'].keys():
            self.annee.options.append(ft.dropdown.Option(key))

        self.content=ft.Container(
            padding=ft.Padding.all(10),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                        content=ft.Text(f"Statistiques par Année", size=11, italic=True),align=ft.Alignment.CENTER
                        )
                        ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.annee,
                    self.tab_cnt_annee
                    ]
                ))
       
    def show_tab_stat_by_annee(self,e):
        annee=e.control.value
        data_annee=self.stat_general['par_annee'][annee]
        tb_annee.rows=[]
        self.tab_cnt_annee.controls.clear()
        for types in data_annee['par_type'].keys():
            tb_annee.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(types)),
                                ft.DataCell(ft.Text(data_annee['par_type'][types]['Bon état'])),
                                ft.DataCell(ft.Text(data_annee['par_type'][types]['En panne'])),
                                ft.DataCell(ft.Text(data_annee['par_type'][types]['Abandonné'])),
                                ft.DataCell(ft.Text(data_annee['par_type'][types]['total_ouvrage'])),
                            ]
                        )
                    )
        self.tab_cnt_annee.controls.append(Mytable_annee)

