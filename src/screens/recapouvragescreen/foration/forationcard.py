import flet as ft
from uix.customtitlelabel import CustomTitleLabel

def ForationCard(foration,showUpdateData,showDelete,shareData):
    foration_cnt=ft.Column(
        expand=True,
        controls=[]
    )
    
    list_item=['id','ouvrage_id','created_at']
    for key, val in foration[0].items():
        if key in list_item or val=="" or val==None:
            pass 
        else:
            foration_cnt.controls.append(
                CustomTitleLabel(title=key,value=val)
            )

    return ft.Card(
        elevation=5,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    border_radius=ft.BorderRadius.only(bottom_right=10),
                    bgcolor=ft.Colors.CYAN_700,
                    padding=ft.Padding.only(left=5,right=5),
                    content=ft.Text("Pompage"),
                ),
                ft.Container(
                    padding=ft.Padding.all(10),
                    border_radius=ft.BorderRadius.only(bottom_right=10, bottom_left=10),
                    border=ft.Border.only(left=ft.BorderSide(width=4, color=ft.Colors.CYAN_700)),
                    content=foration_cnt
                ),
                ft.Row(
                    [
                        ft.IconButton(icon=ft.Icons.UPDATE,
                                        icon_color=ft.Colors.GREEN_500,
                                        on_click= showUpdateData),
                        ft.IconButton(icon=ft.Icons.DELETE,
                                      icon_color=ft.Colors.RED_700,
                                      on_click=showDelete),
                        ft.IconButton(icon=ft.Icons.SHARE,
                                      icon_color=ft.Colors.BLUE_700,
                                      on_click=shareData),
                    ],alignment=ft.MainAxisAlignment.SPACE_EVENLY
                )
            ]
        )
    )
    