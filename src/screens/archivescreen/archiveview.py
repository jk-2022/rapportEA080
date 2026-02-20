import asyncio
import flet as ft
import os
from datetime import datetime
from mystorage import get_value
from screens.archivescreen.archivecard import ArchiveCard

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
            expand=1,
            scroll=ft.ScrollMode.ADAPTIVE
        )

        self.controls=[ft.SafeArea(
            ft.Column(
                controls=[
                    ft.AppBar(title=ft.Text("ARCHIVES")),
                    # ft.Divider(),
                    self.archive_list
                        ]
                    ),expand=1
                )]
            
        self.load_archives()
        
    def load_archives(self):
        self.archive_list.controls.clear()
        for file in get_exported_files():
            row = ArchiveCard(file,self.delete_file,self.open_file,self)                 
            self.archive_list.controls.append(row)

    def open_file(self, path):
        file=os.path.join(get_archive_path(), path["name"])
        if self.page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
            self.page.launch_url(f"file://{file}")
        else:
            os.startfile(file)

    
    async def handle_share_click(self, e, filename):
        await self.share_the_file(filename)
   
    async def share_the_file(self, file):
        self.file=os.path.join(get_archive_path(), file)
        result = await self.share.share_files(
            [ft.ShareFile.from_path(self.file)],
            subject="Greeting",
            title="Share greeting",
        )
        
    def delete_file(self,file_name):
        os.remove(os.path.join(get_archive_path(), file_name))
        self.load_archives()
        self.page.update()
