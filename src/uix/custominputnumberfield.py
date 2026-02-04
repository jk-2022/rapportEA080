import flet as ft

PRIMARY = "teal"

@ft.control
class CustomInputNumberField(ft.TextField):
    border_color="#bbbbbb"
    expand:int=1
    border_width: float =0.6
    cursor_height : int =12
    cursor_width: int =1
    content_padding=ft.Padding.only(left=5, right=5)
    keyboard_type=ft.KeyboardType.NUMBER

    def did_mount(self):
        self.on_focus=self.focus_shadow
        self.on_blur=self.blur_shadow

    def focus_shadow(self, e):
        self.border_color = PRIMARY
        self.update()

    def blur_shadow(self, e):
        self.border_color = "#bbbbbb"
        self.update()


