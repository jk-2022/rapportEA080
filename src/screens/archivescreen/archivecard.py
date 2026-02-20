import os
import flet as ft

from mystorage import get_value 

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

def ArchiveCard(file,delete_file,open_file,formcontrol):

    file_path = os.path.join(get_archive_path(), file["name"])
    async def share_handler(e):
        print(file_path)
        if not os.path.exists(file_path):
            print("Fichier introuvable")
            return

        result = await formcontrol.share.share_files(
            [ft.ShareFile.from_path(file_path)],
            subject="Greeting",
            title="Share greeting",
        )

        # print("Share status:", result.status)
    return ft.ListTile(
                    leading=ft.IconButton(icon=ft.Icons.DELETE, 
                                          tooltip="Supprimer", 
                                          icon_color=ft.Colors.RED_700,
                                          on_click=lambda e, f=file: delete_file(f["name"])
                                          ),
                    trailing=ft.IconButton(icon=ft.Icons.SHARE, 
                                           tooltip="Partager",
                                            icon_color=ft.Colors.BLUE_700, 
                                           on_click=share_handler),
                    title=ft.Text(f"{file['name']}"),
                    subtitle=ft.Text(f"{file['date']}"),
                    on_click=lambda e, f=file: open_file(f),
                    data=file,
                    )
