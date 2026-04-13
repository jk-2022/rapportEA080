"""pages/allouvrageview.py — Tous les ouvrages + filtres avancés + export"""
# import asyncio

import flet as ft
from screens.allouvragescreen.allouvragecard import AllOuvrageCard
from uix.custominputfield import CustomInputField
from utils.constants import (
    PRIMARY, PRIMARY_LIGHT, SURFACE, TEXT_GREY, BG_CARD, DANGER, SHADOW,
    ROUTES, empty_state,
)

class AllOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.route="/allouvrage"
        self.state = state
        
        self.all_ouvrages=self.state.load_all_ouvrages_flat()
        
        self.bgcolor = SURFACE
        self.padding = ft.Padding(0,0,0,0)
        self.appbar = self._build_appbar()
        self._counter_text = ft.Text("", size=12, color=TEXT_GREY)
        self._list_container = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )
        self.expand=True
        self.scroll=ft.ScrollMode.AUTO
        
        self._query="" 
        self._filter_type=""
        self._filter_etat=""
        self._filter_localite=""
        self._annee_debut=""
        self._annee_fin=""
        
        self._code_tf = CustomInputField(
            hint_text="Numéro IRH...",
            prefix_icon=ft.Icons.SEARCH, border_radius=ft.BorderRadius(8,8,8,8),
            filled=True, fill_color=ft.Colors.WHITE,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            on_change=self._on_code_change, height=48, text_size=14
            )
        self._type_dd = ft.Dropdown(hint_text="Type", value="",
            options=[ft.dropdown.Option("","Tous types")]+
                    [ft.dropdown.Option(c) for c in ["PMH","PEA","AEP","PMH_AEP"]],
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            expand=True, height=50, 
            on_text_change=self._on_type_change, 
            text_size=12
            )
        self._etat_dd = ft.Dropdown(hint_text="État", value="",
            options=[ft.dropdown.Option("","Tous états")]+
                    [ft.dropdown.Option(e) for e in ["Bon état","En panne","Abandonnée"]],
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            expand=True, height=50, 
            on_text_change=lambda e: self._on_etat_change(e), 
            text_size=12
            )
        self._loc_tf = CustomInputField(hint_text="Filtrer par localité / préfecture / commune…",
            prefix_icon=ft.Icons.LOCATION_ON, border_radius=ft.BorderRadius(8,8,8,8),
            filled=True, fill_color=ft.Colors.WHITE,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            on_change=self._on_loc_change, height=48, text_size=14
            )
        self._adeb_tf = CustomInputField(hint_text="Année début",
            prefix_icon=ft.Icons.CALENDAR_TODAY, border_radius=ft.BorderRadius(8,8,8,8),
            filled=True, fill_color=ft.Colors.WHITE,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._on_adeb_change, height=48, text_size=14, expand=True, max_length=4
            )
        self._afin_tf = CustomInputField(hint_text="Année fin",
            prefix_icon=ft.Icons.CALENDAR_MONTH, border_radius=ft.BorderRadius(8,8,8,8),
            filled=True, fill_color=ft.Colors.WHITE,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._on_afin_change, height=48, text_size=14, expand=True, max_length=4
            )
        
        filter_panel = ft.Container(
            content=ft.Column([
                self._code_tf,
                ft.Row([self._type_dd, self._etat_dd], spacing=8),
                self._loc_tf,
                ft.Text("Intervalle d'années :", size=12, color=TEXT_GREY, weight=ft.FontWeight.W_500),
                ft.Row([self._adeb_tf, self._afin_tf], spacing=8),
                ft.Row([
                    ft.TextButton("Réinitialiser", icon=ft.Icons.FILTER_ALT_OFF,
                                  on_click=self._reset, style=ft.ButtonStyle(color=DANGER)),
                ], alignment=ft.MainAxisAlignment.END),
            ], spacing=10),
            padding=ft.Padding(16,14,16,10), bgcolor=BG_CARD,
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.07,"#000000"),
                                offset=ft.Offset(0,2)),
        )
        counter_row = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.FILTER_LIST, color=PRIMARY, size=16),
                self._counter_text,
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.TABLE_CHART, icon_color="#1B5E20",
                              tooltip="xlsx", icon_size=20, on_click=lambda _: self._export("xlsx")),
                ft.IconButton(icon=ft.Icons.PICTURE_AS_PDF, icon_color="#B71C1C",
                              tooltip="PDF",  icon_size=20, on_click=lambda _: self._export("pdf")),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(16,4,8,4), bgcolor=SHADOW,
        )
        
        self.controls = [
            filter_panel, 
            counter_row, 
            self._list_container
        ]
        self._refresh_list()

    def _build_appbar(self):
        return ft.AppBar(
            title=ft.Text("Tous les Ouvrages", color="#FFFFFF", 
                          weight=ft.FontWeight.BOLD, size=18,
                          ),
            bgcolor=PRIMARY,
            color="#FFFFFF",
            actions=[
                ft.PopupMenuButton(icon=ft.Icons.DOWNLOAD, icon_color="#FFFFFF",
                    items=[
                        ft.PopupMenuItem(ft.Text("Exporter en xlsx"), icon=ft.Icons.TABLE_CHART,
                                         on_click=lambda _: self._export("xlsx")),
                        ft.PopupMenuItem(ft.Text("Exporter en PDF"),  icon=ft.Icons.PICTURE_AS_PDF,
                                         on_click=lambda _: self._export("pdf")),
                    ]),
            ],
        )

    def _filtered(self):
        q=self._query.lower()
        loc=self._filter_localite.lower()
        result=[]
        for o in self.all_ouvrages:
            if q and q not in str(o.numero_irh): 
                continue
            if self._filter_type and o.type_ouvrage != self._filter_type: 
                continue
            if self._filter_etat and o.etat != self._filter_etat: 
                continue
            if loc and loc not in o.localite.lower() and loc not in o.prefecture.lower() \
               and loc not in o.commune.lower(): 
                   continue
            if self._annee_debut:
                try:
                    if (o.annee or "0") < self._annee_debut: continue
                except: pass
            if self._annee_fin:
                try:
                    if (o.annee or "9999") > self._annee_fin: continue
                except: pass
            result.append(o)
        return result

    # def _ouvrage_list(self):
    #     items = self._filtered()
    #     self._counter_text.value = f"{len(items)} ouvrage(s)"
    #     if not items:
    #         return empty_state("Aucun ouvrage ne correspond aux filtres.", ft.Icons.WATER)
    #     return ft.ListView(
    #         controls=[AllOuvrageCard(state=self.state, ouvrage=o, formcontrol=self) for o in items], 
    #                        spacing=10, expand=True)


    def _on_code_change(self, e): 
        self._query=e.control.value
        self._refresh_list()
        
    def _on_type_change(self, e): 
        self._filter_type=e.control.value 
        self._refresh_list()
    def _on_etat_change(self, e): 
        self._filter_etat=e.control.value 
        self._refresh_list()
    def _on_loc_change(self, e):  
        self._filter_localite=e.control.value
        self._refresh_list()
    def _on_adeb_change(self, e): 
        self._annee_debut=e.control.value 
        self._refresh_list()
    def _on_afin_change(self, e): 
        self._annee_fin=e.control.value 
        self._refresh_list()

    def _reset(self, _=None):
        self._query=self._filter_type=self._filter_etat=self._filter_localite=""
        self._annee_debut=self._annee_fin=""
        self._code_tf.value=self._type_dd.value=self._etat_dd.value=""
        self._loc_tf.value=self._adeb_tf.value=self._afin_tf.value=""
        self._refresh_list()

    def _refresh_list(self):
        items = self._filtered()
        self._counter_text.value = f"{len(items)} ouvrage(s)"
        if not items:
            return empty_state("Aucun ouvrage ne correspond aux filtres.", ft.Icons.WATER)
        self._list_container.controls =[AllOuvrageCard(state=self.state, ouvrage=o, formcontrol=self) for o in items]
        # self._list_container.controls = self._ouvrage_list() 
        # self.update()

    def _export(self, fmt: str):
        from services.export_service import export_ouvrages_xlsx, export_ouvrages_pdf
        ouvrages = self._filtered()
        if not ouvrages:
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Export impossible"),
                content=ft.Text("Aucun ouvrage à exporter."),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog())]))
            return
        projets_map = {p.id: p for p in self.state.projets}
        parts=[]
        if self._filter_type: parts.append(self._filter_type)
        if self._filter_etat: parts.append(self._filter_etat)
        if self._filter_localite: parts.append(self._filter_localite)
        if self._annee_debut or self._annee_fin:
            parts.append(f"{self._annee_debut or '?'}–{self._annee_fin or '?'}")
        titre = "Ouvrages filtrés" + (f" — {', '.join(parts)}" if parts else "")
        try:
            path = (export_ouvrages_xlsx(ouvrages, projets=projets_map)
                    if fmt == "xlsx"
                    else export_ouvrages_pdf(ouvrages, titre=titre, projets=projets_map))
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Export réussi ✅"),
                content=ft.Column([
                    ft.Text(f"{len(ouvrages)} ouvrage(s) exporté(s)."),
                    ft.Text(path, size=10, color=TEXT_GREY, selectable=True),
                ], spacing=4, tight=True),
                actions=[
                    ft.TextButton("Voir les archives",
                                  on_click=lambda _: (self.page.pop_dialog(),
                                                       self.page.go(ROUTES["archives"]))),
                    ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog()),
                ],
            ))
        except Exception as ex:
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Erreur"), content=ft.Text(str(ex)),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog())]))

    def did_mount(self):
        self.state.load_all_ouvrages_flat(); self._refresh_list()
