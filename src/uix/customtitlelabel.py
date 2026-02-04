from flet import *

@control
class CustomTitleLabel(Container):
    title:str=""
    value:str=""
    def build(self):
        self.padding=5
        self.content=Row(
            [
                Container(
                    content=Text(self.title,height=20),
                    width=150,
                    align=Alignment.CENTER_LEFT,
                    adaptive=True
                ),
                Container(
                    content=Text(':'),
                    width=20,
                    align=Alignment.CENTER_LEFT,
                    adaptive=True,
                    height=20
                ),
                Container(
                    content=Row(
                        [
                            Text(self.value,weight=FontWeight.W_300)
                        ],alignment=MainAxisAlignment.CENTER
                    ),
                    # expand=True,
                    adaptive=True,
                )
            ],spacing=0
        )
        return self

# class CustomTitleLabel(Container):
#     def __init__(self,title,value,**kwargs):
#         super().__init__()
#         self.padding=5
#         self.content=Row(
#             [
#                 Container(
#                     content=Text(title,height=20),
#                     width=150,
#                     align=Alignment.CENTER_LEFT,
#                     adaptive=True
#                 ),
#                 Container(
#                     content=Text(':'),
#                     width=20,
#                     align=Alignment.CENTER_LEFT,
#                     adaptive=True,
#                     height=20
#                 ),
#                 Container(
#                     content=Row(
#                         [
#                             Text(value,weight=FontWeight.W_300)
#                         ],alignment=MainAxisAlignment.CENTER
#                     ),
#                     # expand=True,
#                     adaptive=True,
#                 )
#             ],spacing=0
#         )