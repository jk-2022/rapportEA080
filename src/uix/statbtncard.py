import flet as ft

@ft.control
class StatBtnCard(ft.Container):
    title:str=""
    # ink=True
    def build(self):
        self.content=ft.Card(
            content=ft.Row(
                [
                    ft.Text(f"{self.title}", size=13)
                ],alignment=ft.MainAxisAlignment.CENTER
            ),
            height=60,
            # bgcolor=ft.Colors.RED_300
        )
        return self

