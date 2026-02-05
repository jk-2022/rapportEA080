import flet as ft

import datetime
from myaction.myaction_main import found_ouvrage_interval
from uix.custominputfield import CustomInputField
from .statdetailcard import StatDetailCard
from .statintervalcard import StatIntervalCard

class StatIntervalControl(ft.Column):
    def __init__(self, state, formcontrol):
        super().__init__()
        self.state=state
        self.formcontrol=formcontrol
        self.expand=True
        
        self.ouvrages_cont=ft.Column(
            expand=True, 
            scroll=ft.ScrollMode.ALWAYS)
        
        self.date1=CustomInputField(
            label='Date début',
            expand=True, 
            on_click=lambda e: self.show_date1(e))
        
        self.date2=CustomInputField(
            label='Date début',
            expand=True, 
            on_click=lambda e: self.show_date2(e))
        
        self.btn_text=ft.Button(
            'Afficher les resultats', 
            on_click= lambda e: self.show_result(e)
            )
        
        self.detail_btn=ft.TextButton(
            'Voirs la liste des ouvrages',
             on_click=lambda e: self.show_list_ouvrage(e)
             )
        
        self.date_picker1=ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    on_change=self.handle_change1,
                )

        self.date_picker2=ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    on_change=self.handle_change2,
                )
        
        self.controls=[
                        ft.AppBar(
                            title=ft.Text(f"📁 Stastistiques par Intervalle"),
                            leading=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=lambda e: self.formcontrol.change_content("stat-button-content")
                                ),
                        ),
                        ft.Container(
                            expand=True, 
                            padding=ft.Padding(left=10, right=10),
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        [
                                            self.date1,
                                            self.date2,
                                        
                                            ]
                                        ),
                                    self.btn_text,
                                    self.ouvrages_cont
                                ]
                            )
                        )
                    
                    ]
        
    def handle_change1(self, e):
        self.date1.value=e.control.value.strftime('%Y-%m-%d')
        self.date1.update()

    def handle_change2(self, e):
        self.date2.value=e.control.value.strftime('%Y-%m-%d')
        self.date2.update()
        
    def show_date1(self,e):
        self.page.show_dialog(self.date_picker1)
    
    def show_date2(self,e):
        self.page.show_dialog(self.date_picker2)
        
    def show_result(self,e):
        date1=self.date1.value
        date2=self.date2.value
        self.result=found_ouvrage_interval(date1,date2)
        # print(self.result)
        if self.result['total_ouvrages']==0:
            return self.page.show_dialog(ft.SnackBar(ft.Text("Aucun resultat n'a été trouver")))
        cont=StatIntervalCard(stats_data=self.result)
        self.ouvrages_cont.controls.clear()
        self.ouvrages_cont.controls.append(cont)
        self.ouvrages_cont.controls.append(self.detail_btn)
        self.ouvrages_cont.update()
        
    def show_list_ouvrage(self,e):
        stat_details=self.result['details']
        cont=StatDetailCard(stats_data=stat_details)
        self.ouvrages_cont.controls.append(cont)
        # self.detail_btn.visible=False
        # self.detail_btn.update()
        self.ouvrages_cont.update()
