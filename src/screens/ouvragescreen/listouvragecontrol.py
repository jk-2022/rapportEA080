import flet as ft

from myaction.myaction_main import load_all_data_for_csv
from screens.ouvragescreen.excelfilterouvrage import OuvrageExcelExporter
from screens.ouvragescreen.filtreouvragecontrol import FiltreOuvrageControl
from .ouvragecard import OuvrageCard

from mystorage import *

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

class ListOuvrageControl(ft.Column):
    def __init__(self,state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        self.projet=self.state.selected_projet
        
        self.check_box=ft.Checkbox(on_change=self.selected_bool_all_ouvrage)
        self.nbre_select=ft.Text("selectionnés:")
        self.ouvrage_list_selected=[]
        self.ouvrage_object_list_selected=[]
        
        self.ouvrage_list = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
            )
        self.searsh_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click= lambda e :self.go_filter_content()
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click= lambda e : self.formcontrol.change_content("create-ouvrage-content")
            )
        self.nbre_ouvrage_cnt=ft.Row(
                                    [
                                    ],alignment=ft.MainAxisAlignment.CENTER
                                )

        self.controls= [
                    ft.AppBar(title=ft.Text("Tous ouvrages confondus")),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.check_box,
                                self.nbre_ouvrage_cnt,
                                self.searsh_button,
                                self.add_button,
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.Padding.only(left=10, right=10)
                    ),
                    self.ouvrage_list,
                    ft.Container(
                        padding=5,
                        content=ft.Row(
                            [
                                self.nbre_select,
                                ft.Button("Exporter XlsX",on_click= lambda e :self.showGenerate_csv())
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                        ]
            
        
        self.load_ouvrages()

    def load_ouvrages(self):
        self.ouvrages=self.state.load_ouvrages()
        nbre_ouvrage=len(self.ouvrages)
        self.nbre_ouvrage_cnt.controls.append(ft.Text(f"Total : {nbre_ouvrage}", size=12))
        self.ouvrage_list.controls.clear()
        if self.ouvrages:
            for ouvrage in self.ouvrages:
                ouv=OuvrageCard(state=self.state, ouvrage=ouvrage, selected_bool_ouvrage=self.selected_bool_ouvrage, formcontrol=self)
                self.ouvrage_list.controls.append(ouv)
                self.ouvrage_object_list_selected.append(ouv)
                
    def selected_bool_ouvrage(self,ouvrage):
        nbre_select=0
        for check in self.ouvrage_object_list_selected:
            if check.ouvrage==ouvrage:
                if check.check_box.value==True:
                    check.check_box.value=True 
                else:
                    check.check_box.value=False
                    self.check_box.value=False
            else:
                pass
        for check in self.ouvrage_object_list_selected:
            if check.check_box.value==True:
                nbre_select+=1
                self.nbre_select.value=f"selectionnés: {nbre_select}/{len(self.ouvrage_object_list_selected)}"

    
    def selected_bool_all_ouvrage(self,e):
        for check in self.ouvrage_object_list_selected:
            check.check_box.value=e.control.value
        if e.control.value==False:
            self.nbre_select.value=f"selectionnés: 0"
        else:
            self.nbre_select.value=f"selectionnés: {len(self.ouvrage_object_list_selected)}/{len(self.ouvrage_object_list_selected)}"
            
    def get_selected_ouvrage_id(self):
        list_id_get=[]
        for check in self.ouvrage_object_list_selected:
            if check.check_box.value==True:
                list_id_get.append(check.ouvrage.id)
        # print(list_id_get)
        return list_id_get
    
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
        file_path = os.path.join(get_archive_path(), filename)
        idx= self.get_selected_ouvrage_id()
        rows=[]
        for id in idx:
            data=load_all_data_for_csv(id)
            rows.append(data)
        projet_name=self.state.selected_projet.name
        out=OuvrageExcelExporter(datas=rows, output_path=file_path,projet_name=projet_name)
        if out.export():
            self.page.pop_dialog()
            self.page.show_dialog(ft.SnackBar(ft.Text(f"{file_path} saved successfuly")))
            return True
        self.page.show_dialog(ft.SnackBar(ft.Text(f"Error for vaving {filename}")))

    def go_filter_content(self):
        self.formcontrol.change_content("filtre-content")
