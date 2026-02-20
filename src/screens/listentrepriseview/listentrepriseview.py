import flet as ft

class ListEntrepriseView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.route = "/list-entreprise"
        self.padding = 0
        self.searsh_button = ft.Button(
            "Filter",icon=ft.Icons.SEARCH, 
            on_click=lambda e : self.show_maintenance()
            )
        self.add_button = ft.Button(
            "Ajouter",icon=ft.Icons.ADD, 
            on_click=lambda e :self.show_maintenance()
            )
        self.entreprise_list_cont = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        )
        self.nbre_entreprise_cnt=ft.Row(
                                    [
                                    ],alignment=ft.MainAxisAlignment.CENTER
                                )

        self.controls.append(ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(
                            title=ft.Text(f"Liste des Entreprises")
                        ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.searsh_button,
                                self.nbre_entreprise_cnt,
                                self.add_button
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.Padding.only(left=10, right=10)
                    ),
                    self.entreprise_list_cont
                        ],
                        # expand=True,scroll=ScrollMode.ALWAYS
                    ),expand=True
                )
            )
        
        self.load_entreprise()

    def load_entreprise(self):
        entreprises=self.state.load_entreprises()
        nbre_ouvrage=len(entreprises)
        self.nbre_entreprise_cnt.controls.append(ft.Text(f"Total : {nbre_ouvrage}", size=12))
        self.entreprise_list_cont.controls.clear()
        if entreprises:
            for entreprise in entreprises:
                self.entreprise_list_cont.controls.append(
                ft.ListTile(title=entreprise.name, 
                            subtitle=entreprise.contact, 
                            on_click="",
                            leading=ft.Icons.PERSON_2_SHARP,
                            trailing=ft.IconButton(icon=ft.Icons.CALL, on_click=self.show_maintenance)
                            )
            )
    
    def show_maintenance(self):
        return self.page.show_dialog(ft.SnackBar(ft.Text("Option en maintenance")))
    
    def close_dlg(self):
        self.page.pop_dialog()