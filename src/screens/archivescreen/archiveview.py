import asyncio
import flet as ft
import os
from datetime import datetime
from mystorage import get_value

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

def get_exported_files():
    files=[]
    for file_name in os.listdir(get_archive_path()):
        file_path = os.path.join(get_archive_path(), file_name)
        if os.path.isfile(file_path):
            ext = file_name.split(".")[-1].upper()
            created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d/%m/%Y %H:%M")
            files.append({"name": file_name, "type": ext, "date": created})
    return files

def get_icon_for_extension(extension: str):
    icons_map = {
        "PDF": ft.Icons.PICTURE_AS_PDF,
        "DOCX": ft.Icons.DESCRIPTION,
        "CSV": ft.Icons.TABLE_CHART,
        # Ajoute d'autres si besoin
    }
    return icons_map.get(extension, ft.Icons.INSERT_DRIVE_FILE)

class ArchiveView(ft.View):
    def __init__(self,state):
        super().__init__()
        self.state=state
        self.route = "/archive"
        self.padding = 0
        self.share = ft.Share()
        
        self.archive_list = ft.Column(
            expand=1
        )

        self.controls=[ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(title=ft.Text("ARCHIVES")),
                    ft.Divider(),
                    self.archive_list
                        ]
                    ),expand=1
                )]
            
        self.load_archives()
        
    def load_archives(self):
        self.archive_list.controls.clear()
        for file in get_exported_files():
            icon = get_icon_for_extension(file["type"])
            row = ft.ListTile(
                    leading=ft.IconButton(icon=ft.Icons.DELETE, 
                                          tooltip="Supprimer", 
                                          icon_color=ft.Colors.RED_700,
                                          on_click=lambda e, f=file: self.delete_file(f["name"])
                                          ),
                    trailing=ft.IconButton(icon=ft.Icons.SHARE, 
                                           tooltip="Partager",
                                            icon_color=ft.Colors.BLUE_700, 
                                           on_click=lambda e, f=file: self.share_the_file(f["name"])),
                    title=ft.Text(f"{file['name']}"),
                    subtitle=ft.Text(f"{file['date']}"),
                    on_click=lambda e, f=file: self.open_file(f),
                    data=file,
                    )
            self.archive_list.controls.append(row)


    def open_file(self, file):
        try:
            os.startfile(os.path.join(get_archive_path(), file["name"]))
        except:
            self.share.share_files(
                [ft.ShareFile.from_path(file)],
                text="Sharing a file from memory",
            )
    def share_the_file(self, file):
        self.file=os.path.join(get_archive_path(), file)
        self.share_file()
        print(self.file)
        # return True
        
    async def share_file(self):
        result = await self.share.share_files(
            [ft.ShareFile.from_path(self.file)],
            subject="Greeting",
            title="Share greeting",
        )
        
    def delete_file(self,file_name):
        os.remove(os.path.join(get_archive_path(), file_name))
        self.load_archives()
        self.page.update()
