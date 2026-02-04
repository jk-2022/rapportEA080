import flet as ft
from myaction.myaction_main import export_sqlite_to_json, import_json_to_sqlite
from mystorage import *

class SettingView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.state=state

        # self.titlefield=ft.TextField(expand=True, height=40, value="basedb")

        self.controls.append(ft.SafeArea(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                                [
                                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e:self.page.on_view_pop()),
                                ft.Text("Paramètres ", text_align=ft.TextAlign.CENTER)
                                ]
                            )
                    ),
                    ft.Container(
                        padding=ft.Padding.only(right=10),
                        content=ft.Row([
                        ft.Text("Gestions des données", italic=True,size=11)
                        ],alignment=ft.MainAxisAlignment.END
                        ),
                    ),
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column(
                                [
                                    
                                    ft.ListTile(title=ft.Text("Sauvegardez toutes vos données"),leading=ft.Icon(ft.Icons.UPLOAD), on_click=lambda e: self.showExport()),
                                    ft.ListTile(title=ft.Text("Importez toutes vos données"),leading=ft.Icon(ft.Icons.DOWNLOAD), on_click= self.handle_pick_files)
                                ]
                            )
                        )
                    ),
                    ft.Container(
                        padding=ft.Padding.only(right=10,top=20),
                        content=ft.Row([
                        ft.Text("thème", italic=True,size=11)
                        ],alignment=ft.MainAxisAlignment.END
                        ),
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text("Changer le mode de thème"),
                                    ft.Switch(label='',label_position=ft.LabelPosition.LEFT,on_change=self.togle_theme)
                                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=ft.Padding.only(left=10,right=20)
                        )
                    )
                ],expand=True,spacing=0
            ),expand=True
        )
    )
            
    async def handle_save_file(self, e: ft.Event[ft.Button]):
        init_path=get_value("archive_path")
        file_path=await ft.FilePicker().save_file(dialog_title="sauvegarde file",
                                                  initial_directory=init_path
                                                  )
        self.export_base(file_path)

    
    def showExport(self):
        titlefield=ft.TextField(expand=True, height=40,value="basedb")
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nom du fichier"),
            content=titlefield,
            actions=[
                ft.TextButton("Annuler", on_click=self.close_dlg),
                ft.TextButton("Exporter", on_click = lambda e : self.export_base(titlefield.value)),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.show_dialog(self.dlg_modal)

    async def handle_pick_files(self, e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(allowed_extensions=["json"])
        file_path = (
            ", ".join(map(lambda f: f.path, files)) if files else "Cancelled!"
        )
        import_json_to_sqlite(file_path)
        self.page.show_dialog(ft.SnackBar(ft.Text(f"Importation avec succès")))
        
    def export_base(self,title):
        export_sqlite_to_json(title)
        self.page.pop_dialog()
        self.page.show_dialog(ft.SnackBar(ft.Text(f"La sauvegarde {title} est exporter avec succès")))


    def togle_theme(self,e):
        if self.page.theme_mode == ft.ThemeMode.DARK : 
            self.page.theme_mode=ft.ThemeMode.LIGHT
            set_value('theme','ThemeMode.LIGHT')
        else:
            self.page.theme_mode=ft.ThemeMode.DARK
            set_value('theme','ThemeMode.DARK')
        self.page.update()

    def close_dlg(self):
        self.page.pop_dialog()
