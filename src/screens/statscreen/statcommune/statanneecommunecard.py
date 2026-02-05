# import os
from flet import *
from .datatablestat import Mytable_annee, tb_annee


class StatAnneeCommuneCard(Card):
    def __init__(self,stat_general):
        super().__init__()
        self.tab_cnt_annee=Column()
        self.elevation=5
        self.stat_general=stat_general

        self.annee = Dropdown(
            label="Voir stat par Année",
            expand=True,
            on_text_change=self.show_tab_stat_by_annee
            )
        for key in stat_general['par_annee'].keys():
            self.annee.options.append(dropdown.Option(key))

        self.content=Container(
            padding=Padding.all(10),
            content=Column(
                [
                    Row(
                        [
                            Container(
                        content=Text(f"Statistiques par Année", 
                                     size=11, italic=True),
                                     alignment=Alignment.CENTER
                        )
                        ],alignment=MainAxisAlignment.CENTER
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
                        DataRow(
                            cells=[
                                DataCell(Text(types)),
                                DataCell(Text(data_annee['par_type'][types]['Bon état'])),
                                DataCell(Text(data_annee['par_type'][types]['En panne'])),
                                DataCell(Text(data_annee['par_type'][types]['Abandonné'])),
                                DataCell(Text(data_annee['par_type'][types]['total_ouvrage'])),
                            ]
                        )
                    )
        self.tab_cnt_annee.controls.append(Mytable_annee)

