import flet as ft
import os
import csv

from myaction.myaction_main import get_all_localites, get_filtered_ouvrages, recuperer_one_local, recuperer_one_projet

from mystorage import *



from .datatable import Mytable, tb

class FiltreOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.route = "/projet/list-ouvrage/filtrer-ouvrage"
        self.liste_ouvrage_filtrer=[]
        self.dropdown_type = ft.Dropdown(
        label="Type",
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
            expand=True,
            text_size=12,
            options=[
                ft.dropdown.Option("Bon état"), 
                ft.dropdown.Option("En panne"), 
                ft.dropdown.Option("Abandonné")],
            on_text_change=lambda e: self.update_list()
        )
        self.dropdown_localite_cnt=ft.Container(
            expand=True
        )
        self.numero_irh = ft.TextField(
            label="N° IRH", on_change=lambda e: self.update_list(),
            expand=True,
            text_size=12,
        )
        self.ouvrage_column_list = ft.Column(
            expand=1,
            scroll=ft.ScrollMode.ALWAYS
        )
        self.controls.append(
            ft.SafeArea(
                ft.Column(
                    [
                        # ft.Row(
                        #     [
                        #     ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e :self.page.on_view_pop()),
                        #     ft.Text("Filtrer les ouvrages"),
                        #     ]
                        # ),
                        ft.AppBar(
                            title=ft.Text(f"Recherche par filtrage")
                        ),
                        ft.Row(
                            [
                            self.dropdown_type,
                            self.dropdown_localite_cnt,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        ),
                        ft.Row(
                            [
                            self.numero_irh,
                            self.dropdown_etat,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        ),
                    # Divider(),
                    Mytable,
                    ft.Button("Générer CSV", on_click= lambda e: self.showGenerate_csv()),
                    ],spacing=7
                ), expand=True
            )
        )
        self.update_localite()

    def update_localite(self):
        localites=get_all_localites()
        self.dropdown_localite = ft.Dropdown(
            label="Localite",
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
            projet_id=projet_id
        )

        if ouvrages:
            print(ouvrages)
            tb.rows = []
            self.liste_ouvrage_filtrer=[]
            for ouvrage in ouvrages:
                print(list(ouvrage.values()))
                self.liste_ouvrage_filtrer.append(list(ouvrage.values()))
                tb.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(ouvrage["type_ouvrage"])),
                            ft.DataCell(ft.Text(ouvrage["numero_irh"])),
                            ft.DataCell(ft.Text(ouvrage["etat"])),
                            ft.DataCell(ft.Text(ouvrage["annee"])),
                            ft.DataCell(ft.Text(ouvrage["type_energie"])),
                            ft.DataCell(ft.Text(ouvrage["type_reservoir"])),
                            ft.DataCell(ft.Text(ouvrage["volume_reservoir"])),
                            ft.DataCell(ft.Text(ouvrage["cause_panne"])),
                            ft.DataCell(ft.Text(ouvrage["observation"])),
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
        projet=recuperer_one_projet(ouvrage['projet_id'])
        set_value('projet',projet[0])
        local=recuperer_one_local(ouvrage['localisation_id'])
        set_value('local',local[0])
        self.page.on_route_change("/recap-ouvrage")

    def showGenerate_csv(self):
        titlefield=ft.TextField(expand=True, height=40)
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
        rows=self.liste_ouvrage_filtrer
        if rows:
            with open(f"{filename}.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(["id","type_ouvrage", "prefecture", "commune", "canton", "localite", "numero irh", "coordonnee x", "coordonnee y",
                "lieu implantation","Année", "type energie", "type reservoir", "Vol reservoir",
                "etat", "cause_panne", "observation","created_at"])
                writer.writerows(rows)
            self.page.show_dialog(ft.SnackBar(ft.Text(f"{filename} saved successfuly"),open=True))
            self.close_dlg()
            return True
        self.page.show_dialog(ft.SnackBar(ft.Text(f"Error for vaving {filename}"),open=True))
    
    def close_dlg(self):
        self.page.pop_dialog()
            
