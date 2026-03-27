import os
import flet as ft

from mystorage import get_value
from utils.constants import BG_CARD, DANGER, PRIMARY, TEXT_DARK, TEXT_GREY 

def get_archive_path():
    ARCHIVES_PATH=get_value("archive_path")
    return ARCHIVES_PATH

def ArchiveCard(file:dict,delete_file,open_file,formcontrol):
    icon = ft.Icons.TABLE_CHART if file["ext"] == ".xlsx" else (
               ft.Icons.PICTURE_AS_PDF if file["ext"] == ".pdf" else ft.Icons.CODE)
    color = "#1B5E20" if file["ext"] == ".xlsx" else (
                "#B71C1C" if file["ext"] == ".pdf" else PRIMARY)
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
    return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color="#FFFFFF", size=22),
                    bgcolor=color,
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(10, 10, 10, 10),
                ),
                ft.Column([
                    ft.Text(file["name"], size=13, weight=ft.FontWeight.W_600,
                            color=TEXT_DARK, max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"{file['date']}  •  {round(file['size']/1024, 1)} Ko",
                            size=11, color=TEXT_GREY),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=DANGER,
                    tooltip="Supprimer",
                    on_click=lambda _, path=file["path"]: delete_file(path),
                ),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(12, 12, 12, 12),
            padding=ft.Padding(12, 10, 12, 10),
            shadow=ft.BoxShadow(blur_radius=5,
                                color=ft.Colors.with_opacity(0.08, "#000000"),
                                offset=ft.Offset(0, 2)),
        )
    
    
def _file_card(self, f: dict) -> ft.Container:
        icon = ft.Icons.TABLE_CHART if f["ext"] == ".xlsx" else (
               ft.Icons.PICTURE_AS_PDF if f["ext"] == ".pdf" else ft.Icons.CODE)
        color = "#1B5E20" if f["ext"] == ".xlsx" else (
                "#B71C1C" if f["ext"] == ".pdf" else PRIMARY)

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color="#FFFFFF", size=22),
                    bgcolor=color,
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    padding=ft.Padding(10, 10, 10, 10),
                ),
                ft.Column([
                    ft.Text(f["name"], size=13, weight=ft.FontWeight.W_600,
                            color=TEXT_DARK, max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"{f['date']}  •  {round(f['size']/1024, 1)} Ko",
                            size=11, color=TEXT_GREY),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=DANGER,
                    tooltip="Supprimer",
                    on_click=lambda _, path=f["path"]: self._delete_file(path),
                ),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(12, 12, 12, 12),
            padding=ft.Padding(12, 10, 12, 10),
            shadow=ft.BoxShadow(blur_radius=5,
                                color=ft.Colors.with_opacity(0.08, "#000000"),
                                offset=ft.Offset(0, 2)),
        )
