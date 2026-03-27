import flet as ft

from appstate import Ouvrage
from myaction.myaction_main import load_all_data_for_csv
from screens.ouvragescreen.excelfilterouvrage import OuvrageExcelExporter
from screens.ouvragescreen.filtreouvragecontrol import FiltreOuvrageControl
from utils.constants import app_bar, champ_recherche
from .ouvragecard import OuvrageCard

from mystorage import *

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

class OuvrageView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding=0
        self.state=state
        self.route=f"/projet/list-ouvrage"
        self.expand=True
        self.projet=self.state.selected_projet
        self._query=""
        
        self.check_box=ft.Checkbox(label=ft.Text("Tous"), on_change=self.selected_bool_all_ouvrage)
        self.nbre_select=ft.Text("selectionnés:")
        self.ouvrage_list_selected=[]
        self.ouvrage_object_list_selected=[]
        
        self.barre_recherche=champ_recherche("projet",self._on_search)
        
        self.ouvrage_list = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
            )
        self.filtre_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click= self.go_filter_view
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click= self.go_create_view
            )

        self.controls= [
                    app_bar(title=f"Tous ouvrages de {self.projet.name}"),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.check_box,
                                self.barre_recherche,
                                self.filtre_button,
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
                                ft.Button("Exporter XlsX",on_click= lambda e :self.showGenerate_csv()),
                                self.add_button,
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                        ]

        self._refresh()
    
    def _filtered(self) -> list[Ouvrage]:
        q = self._query.lower()
        return [o for o in self.state.load_ouvrages() if q in o.lieu.lower() or q in o.localite.lower() or q in o.canton.lower() or q in str(o.numero_irh)]
        
    def _on_search(self, e):
        self._query = self.barre_recherche.value
        self._refresh()

    def _refresh(self):
        self.ouvrage_object_list_selected=[]
        self.ouvrages=self._filtered()
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
        
    async def go_filter_view(self):
        await self.page.push_route("/projet/list-ouvrage/filtre-ouvrage")
        
    async def go_create_view(self):
        await self.page.push_route("/projet/list-ouvrage/create-ouvrage")
