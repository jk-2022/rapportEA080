import flet as ft

class ListEntrepriseView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.route = "/list-entreprise"
        self.padding = 0
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
                    # ft.Container(
                    #     content=ft.Row(
                    #             [
                    #             ft.IconButton(
                    #                 icon=ft.Icons.ARROW_BACK, 
                    #                 on_click= lambda e:self.page.on_view_pop()),
                    #             ft.Text(
                    #                 "Liste des entreprises ", 
                    #                 text_align=ft.TextAlign.CENTER)
                    #             ]
                    #             # ,alignment=MainAxisAlignment.CENTER
                    #         )
                    # ),
                    ft.AppBar(
                            title=ft.Text(f"Liste des Entreprises")
                        ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.nbre_entreprise_cnt,
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
                ft.ListTile(title=entreprise.name, subtitle=entreprise.contact, on_click="",leading=ft.Icons.PERSON_2_SHARP)
            )
        
    def close_dlg(self):
        self.page.pop_dialog()