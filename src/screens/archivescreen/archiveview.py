import asyncio
import flet as ft
import os
from datetime import datetime
from mystorage import get_value
from screens.archivescreen.archivecard import ArchiveCard


def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

ARCHIVE_DIR=get_archive_path()

def list_archives() -> list[dict]:
    files = []
    if os.path.exists(ARCHIVE_DIR):
        for f in sorted(os.listdir(ARCHIVE_DIR), reverse=True):
            full = os.path.join(ARCHIVE_DIR, f)
            size = os.path.getsize(full)
            mtime = os.path.getmtime(full)
            files.append({
                "name": f,
                "path": full,
                "size": size,
                "date": datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M"),
                "ext": os.path.splitext(f)[1].lower(),
            })
    return files

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
        for file in list_archives():
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
