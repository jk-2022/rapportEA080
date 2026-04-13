import flet as ft
from myaction.myaction_main import export_sqlite_to_json, import_json_to_sqlite, reset_my_db
from mystorage import *

from myaction.db_actions import init_db
from utils.constants import TEXT_GREY, section_title

class SettingView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.padding = 0
        self.state=state
        self.route = "/settings"
        self._import_mode = "json"
        # self.titlefield=ft.TextField(expand=True, height=40, value="basedb")

        self.controls.append(ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(
                            title=ft.Text("Paramètres")
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
                                    section_title("📥 Importer des données"),
                                    ft.Text(
                                        "Restaurez vos données depuis un fichier de sauvegarde "
                                        "JSON ou XLSX précédemment exporté depuis EaRapport. "
                                        "Les données existantes sont conservées (import additif).",
                                        color=TEXT_GREY, size=13,
                                    ),
                                    ft.Row(
                                        [
                                            
                                            # ft.ListTile(title=ft.Text("Importez toutes vos données"),
                                            #             leading=ft.Icon(ft.Icons.DOWNLOAD), on_click= self.handle_pick_files),
                                            ft.FilledButton(
                                                "Sélectionner JSON",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=self.handle_pick_files,
                                                expand=True
                                            ),
                                            ft.FilledButton(
                                                "Sélectionner EXCEL",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=self._pick_import_file,
                                                expand=True
                                            )
                                            ]),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text(
                                                "📄 JSON — Toutes les données dans un seul fichier.\n"
                                                "📊 XLSX — 4 feuilles : Projets, Entreprises, Villages, Ouvrages.",
                                                size=11, color=TEXT_GREY,
                                            ),
                                        ]),
                                        bgcolor="#FFFDE7",
                                        border_radius=ft.BorderRadius(8, 8, 8, 8),
                                        padding=ft.Padding(10, 8, 10, 8),
                                    ),
                                    section_title("💾 Sauvegarde des données"),
                                    ft.Text(
                                        "Exportez toutes vos données (projets, ouvrages, entreprises, "
                                        "villages) dans un fichier de sauvegarde.",
                                        color=TEXT_GREY, size=13,
                                    ),
                                    ft.FilledButton(
                                            "Exporter en JSON DB",
                                            icon=ft.Icons.CODE, 
                                            expand=True,
                                            on_click=lambda e: self.showExport()),
                                    ft.Row([
                                        ft.FilledButton(
                                            "Exporter JSON state",
                                            icon=ft.Icons.CODE,
                                            on_click=lambda _: self._export_second("json"),
                                            expand=True,
                                        ),
                                        ft.FilledButton(
                                            "Exporter en XLSX",
                                            icon=ft.Icons.TABLE_CHART,
                                            on_click=lambda _: self._export_second("xlsx"),
                                            expand=True,
                                            style=ft.ButtonStyle(bgcolor="#1B5E20"),
                                        ),
                                    ], spacing=8),
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
                    ),
                    ft.ListTile(title=ft.Text("Réinitialiser la base de donnée", color="#0b67e7"),leading=ft.Icon(ft.Icons.RESTORE), on_click=lambda e: self.show_reset())
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
        
    def _export_second(self, fmt: str):
        from services.export_service import export_backup_json, export_backup_xlsx
        try:
            path = export_backup_json(self.state) if fmt == "json" \
                   else export_backup_xlsx(self.state)
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Sauvegarde réussie ✅"),
                content=ft.Column([
                    ft.Text("Fichier enregistré dans les archives :"),
                    ft.Text(path, size=11, color=TEXT_GREY, selectable=True),
                ], spacing=4, tight=True),
                actions=[
                    ft.TextButton("Voir les archives",
                                  on_click= self.page_go_archives
                                  ),
                    ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog()),
                ],
            ))
        except Exception as ex:
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Erreur de sauvegarde"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog())],
            ))
            
        # ── Import — sélection du fichier ────────────────────────────────────────

    async def _pick_import_file(self, e: ft.Event[ft.Button]):
        extensions = ["xlsx", "xls"]

        files = await ft.FilePicker().pick_files(allowed_extensions=extensions)
        path = (
            ", ".join(map(lambda f: f.path, files)) if files else "Cancelled!"
            )
        if path=="Cancelled!":
            return
        fmt  = ""

        # Boîte de confirmation avant import
        self.page.show_dialog(ft.AlertDialog(
            title=ft.Text(f"Importer ce fichier {fmt.upper()} ?"),
            content=ft.Column([
                ft.Text(
                    "Les données du fichier seront ajoutées à la base existante "
                    "(les enregistrements actuels sont conservés).",
                    color=TEXT_GREY, size=13,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{path}", size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#1565C0",
                    ),
                    bgcolor="#E3F2FD",
                    border_radius=ft.BorderRadius(6, 6, 6, 6),
                    padding=ft.Padding(10, 6, 10, 6),
                ),
            ], spacing=10, tight=True),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: self.page.pop_dialog()),
                ft.FilledButton(
                    "Importer",
                    on_click=lambda _: (
                        self.page.pop_dialog(),
                        self._do_import(path, fmt),
                    ),
                ),
            ],
        ))
    
    def _do_import(self, path: str, fmt: str):
        try:
            if fmt == "json":
                from services.export_service import import_backup_json
                import_backup_json(path, self.state)
                errors = []
            else:
                from services.export_service import import_backup_xlsx
                errors = import_backup_xlsx(path, self.state)

            if not errors:
                self.page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Import réussi ✅"),
                    content=ft.Text(
                        "Toutes les données ont été importées avec succès.\n"
                        "La base de données a été mise à jour.",
                    ),
                    actions=[
                        ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog()),
                    ],
                ))
            else:
                dialog=ft.AlertDialog(
                    title=ft.Text("Import terminé avec avertissements ⚠️"),
                    content=ft.Column([
                            ft.Text(
                                f"Import terminé mais {len(errors)} ligne(s) ignorée(s) :",
                                color=TEXT_GREY, size=13,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(f"• {err}", size=11, color="#B71C1C")
                                    for err in errors[:10]  # Max 10 erreurs affichées
                                ] + ([ft.Text(f"… et {len(errors)-10} autre(s)", size=11,
                                              color=TEXT_GREY)]
                                     if len(errors) > 10 else []),
                                    spacing=4,
                                ),
                                bgcolor="#FFEBEE",
                                border_radius=ft.BorderRadius(8, 8, 8, 8),
                                padding=ft.Padding(10, 8, 10, 8),
                            ),
                        ], spacing=8, width=300),
                        actions=[
                            ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog()),
                        ],
                    )
                self.page.show_dialog(dialog)
        except Exception as ex:
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Erreur d'import"),
                content=ft.Column([
                    ft.Text("Une erreur est survenue lors de l'import :", color=TEXT_GREY, size=12),
                    ft.Text(str(ex), size=12, color="#B71C1C"),
                ], spacing=6, tight=True),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog())],
            ))

    
    def show_reset(self):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("reinitialiser", size=12)
                ],alignment=ft.MainAxisAlignment.CENTER
                ),
            content=ft.Row(
                [
                    ft.Text("Voulez-vous réinitialiser votre application")
                ],alignment=ft.MainAxisAlignment.CENTER
                ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_dlg),
                ft.TextButton("Oui", on_click = self.reset_db),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.show_dialog(self.dlg_modal)
        
    async def reset_db(self):
        await reset_my_db()
        await init_db()
        self.page.pop_dialog()
        self.page.show_dialog(ft.SnackBar(ft.Text("Vous avez réinitialiser votre application avec succès")))

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

    async def page_go_archives(self):
        self.page.pop_dialog()
        await self.page.push_route("/archive")
        
        
    def close_dlg(self):
        self.page.pop_dialog()
