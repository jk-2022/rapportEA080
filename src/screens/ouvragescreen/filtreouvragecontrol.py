import asyncio
import flet as ft
import os
import csv

from myaction.myaction_main import get_all_localites, get_filtered_ouvrages, get_one_ouvrages, load_all_data_for_csv
from screens.ouvragescreen.excelfilterouvrage import OuvrageExcelExporter
from .datatable import Mytable, tb

from mystorage import *

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

class FiltreOuvrageControl(ft.Column):
    def __init__(self,state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.liste_ouvrage_filtrer=[]
        
        self.dropdown_type = ft.Dropdown(
            label="Type",
            height=40,
            expand=True,
            text_size=13,
            options=[ft.dropdown.Option("PMH"), 
                    ft.dropdown.Option("PEA"), 
                    ft.dropdown.Option("AEP"), 
                    ft.dropdown.Option("PMH en PEA"), 
                    ft.dropdown.Option("Mini AEP")],
            on_text_change=lambda e: self.update_list()
            )

        self.dropdown_etat = ft.Dropdown(
            label="État",
            height=40,
            expand=True,
            text_size=12,
            options=[
                ft.dropdown.Option("Bon état"), 
                ft.dropdown.Option("En cours"), 
                ft.dropdown.Option("En panne"), 
                ft.dropdown.Option("Abandonné")],
            on_text_change=lambda e: self.update_list()
            )
        
        self.suivi = ft.Dropdown(
            label="Suivi",
            height=40,
            expand=True,
            text_size=12,
            options=[
                ft.dropdown.Option("moi"), 
                ft.dropdown.Option("autre")
                ],
            on_text_change=lambda e: self.update_list()
            )
        
        self.dropdown_localite_cnt=ft.Container(
            expand=True
            )
        
        self.numero_irh = ft.TextField(
            label="N° IRH", on_change=lambda e: self.update_list(),
            expand=True,
            text_size=12,
            height=40
            )
        
        self.ouvrage_column_list = ft.Column(
            expand=1,
            scroll=ft.ScrollMode.ALWAYS
            )
        
        self.controls= [
                        ft.AppBar(title=ft.Text("Créer un nouveau Ouvrage "),
                                  leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, 
                                              on_click= lambda e: self.go_list_ouvrage_cont())
                                  ),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding.only(left=10, right=10),
                            content=ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.ADAPTIVE,
                                spacing=5,
                                controls=[
                                    ft.Row(
                                        [
                                        self.dropdown_type,
                                        self.dropdown_localite_cnt,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    ft.Row(
                                        [
                                        self.suivi,
                                        self.dropdown_etat,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    ft.Row(
                                        [
                                        self.numero_irh
                                        ],
                                        # alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    Mytable,
                                    ft.Row(
                                        [
                                            ft.Button("Générer CSV", on_click= lambda e: self.showGenerate_csv())
                                        ], alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ]
                            )
                        )
                    ]
        
        self.update_localite()

    def update_localite(self):
        localites=get_all_localites(self.state.selected_projet.id)
        self.dropdown_localite = ft.Dropdown(
            label="Localite",
            height=40,
            expand=True,
            text_size=12,
            on_text_change=lambda e: self.update_list()
        )
        if localites:
            for localite in localites:
                self.dropdown_localite.options.append(ft.dropdown.Option(localite[0]))
            self.dropdown_localite_cnt.content=self.dropdown_localite
    
    
    def update_list(self):
        self.ouvrage_column_list.controls.clear()
        projet=self.state.selected_projet
        projet_id=projet.id
        ouvrages = get_filtered_ouvrages(
            type_ouvrage=self.dropdown_type.value,
            localite=self.dropdown_localite.value,
            etat=self.dropdown_etat.value,
            numero_irh=self.numero_irh.value,
            suivi=self.suivi.value,
            projet_id=projet_id
        )

        if ouvrages:
            tb.rows = []
            self.liste_ouvrage_filtrer=[]
            for ouvrage in ouvrages:
                data=load_all_data_for_csv(ouvrage["id"])
                self.liste_ouvrage_filtrer.append(data)
                tb.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(ouvrage["type_ouvrage"])),
                            ft.DataCell(ft.Text(ouvrage["lieu"])),
                            ft.DataCell(ft.Text(ouvrage["canton"])),
                            ft.DataCell(ft.Text(ouvrage["commune"])),
                            ft.DataCell(ft.Text(ouvrage["numero_irh"])),
                            ft.DataCell(ft.Text(ouvrage["etat"])),
                            ft.DataCell(ft.Text(ouvrage["annee"])),
                            ft.DataCell(ft.Text(ouvrage["coordonnee_x"])),
                            ft.DataCell(ft.Text(ouvrage["coordonnee_y"])),
                            ft.DataCell(ft.Text(ouvrage["type_energie"])),
                            ft.DataCell(ft.Text(ouvrage["type_reservoir"])),
                            ft.DataCell(ft.Text(ouvrage["volume_reservoir"])),
                        ],
                        data=ouvrage,
                        selected=True,
                        on_select_change=lambda e, data=ouvrage: self.open_ouvrage_detail(data)
                    )
                )
            tb.update()
        else:
            tb.rows=[]
        self.page.update()

    def open_ouvrage_detail(self,ouvrage):
        ouvrage=get_one_ouvrages(ouvrage['id'])
        self.state.selected_ouvrage=ouvrage[0]
        asyncio.create_task(self.page.push_route("/projet/list-ouvrage/recap-ouvrage"))

    def showGenerate_csv(self):
        titlefield=ft.TextField(expand=True, height=40, value=f"liste ouvrage projet {self.state.selected_projet.name}")
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nom du fichier"),
            content=titlefield,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e:self.close_dlg()),
                ft.TextButton("Exporter", on_click = lambda e : self.generate_csv(titlefield.value)),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.show_dialog(self.dlg_modal)

    def generate_csv(self, filename):
        if filename=="":
            filename="Liste ouvrages"
        # print(filename)
        file_path = os.path.join(get_archive_path(), filename)
        rows=self.liste_ouvrage_filtrer
        projet_name=self.state.selected_projet.name
        out=OuvrageExcelExporter(datas=rows, output_path=file_path,projet_name=projet_name)
        if out.export():
            self.close_dlg()
            self.page.show_dialog(ft.SnackBar(ft.Text(f"{file_path} saved successfuly")))
            return True
        self.page.show_dialog(ft.SnackBar(ft.Text(f"Error for vaving {filename}")))
    
    
    def go_list_ouvrage_cont(self):
        self.formcontrol.change_content("list-ouvrage-content")
        
    def close_dlg(self):
        self.page.pop_dialog()
            
