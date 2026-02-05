import flet as ft

from myaction.myaction_village import delete_village
from screens.villagescreen.villageform import VillageForm
from screens.villagescreen.villageupdateform import VillageUpdateForm

class VillageView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.state=state
        self.route = "/list-village"
        self.searsh_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click=lambda e : self.go_filter_page()
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click=lambda e :self.show_village_form()
            )
        
        self.village_list_cont = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        )
        self.nbre_village_cnt=ft.Row(
                                    [
                                    ],alignment=ft.MainAxisAlignment.CENTER
                                )

        self.controls.append(ft.SafeArea(
            ft.Column(
                controls=[
                    # ft.Container(
                    #     content=ft.Row(
                    #             [
                    #             ft.IconButton(
                    #                 icon=ft.Icons.ARROW_BACK, 
                    #                 on_click= lambda e:self.page.on_view_pop()),
                    #             ft.Text(
                    #                 "Liste des villages ", 
                    #                 text_align=ft.TextAlign.CENTER)
                    #             ]
                    #             # ,alignment=MainAxisAlignment.CENTER
                    #         )
                    # ),
                    ft.AppBar(
                            title=ft.Text(f"Liste des Villages")
                        ),
                    
                    ft.Container(
                        content=ft.Row(
                            [
                                self.searsh_button,
                                self.nbre_village_cnt,
                                self.add_button,
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.Padding.only(left=10, right=10)
                    ),
                    self.village_list_cont
                        ],
                        # expand=True,scroll=ScrollMode.ALWAYS
                    ),expand=True
                )
            )
        
        self.load_village()

    def load_village(self):
        villages=self.state.load_villages()
        nbre_village=len(villages)
        self.nbre_village_cnt.controls.append(ft.Text(f"Total : {nbre_village}", size=12))
        self.village_list_cont.controls.clear()
        if villages:
            for village in villages:
                self.village_list_cont.controls.append(
                ft.ListTile(title=f"villlage : {village.localite}", 
                            subtitle=f"{village.canton}/{village.commune}",
                            data=village,
                            on_click="",
                            leading=ft.IconButton(icon=ft.Icons.DELETE, 
                                                   icon_color=ft.Colors.RED_700,
                                                   on_click= lambda e, data=village.id: self.show_delete_village(data)
                                                   ),
                            trailing=ft.IconButton(icon=ft.Icons.EDIT, 
                                                   icon_color=ft.Colors.GREEN_700,
                                                   on_click= lambda e, data=village: self.show_edit_village(data)
                                                   )
                            )
            )
                
    def show_village_form(self):
        village_cont = VillageForm(self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nouveau Village"),
            content=village_cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e :self.close_dlg()),
                ft.TextButton("Enregistrer", on_click=lambda e :village_cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
        
    def show_delete_village(self, village_id):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Suppression"),
            content=ft.Row(
                [
                    ft.Text(f"⚠️ Voulez-vous supprimer?")
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Annuler", on_click=lambda e:self.close_dlg()),
                ft.TextButton("Supprimer",
                              icon=ft.Icons.DELETE, 
                              icon_color=ft.Colors.RED_700, 
                              on_click=lambda e, id=village_id:self.del_village(id)),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def show_edit_village(self,data):
        cont=VillageUpdateForm( village=data,formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier village"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.close_dlg()),
                ft.TextButton("Modifier", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    def del_village(self,village_id):
        delete_village(village_id=village_id)
        self.page.pop_dialog()
        self.load_village()
        
    def go_filter_page(self):
        return self.page.show_dialog(ft.SnackBar(ft.Text("Option en maintenance")))
        
    def close_dlg(self):
        self.page.pop_dialog()