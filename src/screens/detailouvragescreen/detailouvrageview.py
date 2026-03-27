"""
pages/detailouvrageview.py
Vue détail d'un ouvrage avec édition, pannes, suivis et export PV
"""

import asyncio

import flet as ft
from appstate import Projet
from appstate import Foration
from appstate import Pompage
from appstate import Panne 
from myaction.myaction_pompage import delete_pompage, load_one_pompage
from myaction.myaction_main import Ouvrage, delete_ouvrage
from myaction.myaction_foration import load_one_foration, delete_foration
from myaction.myaction_panne import  load_all_pannes, delete_panne
from myaction.myaction_suivi import Suivi, load_all_suivis, delete_suivi

from .convert_to_text import convert_data_all_to_text, convert_data_foration_to_text, convert_data_pompage_to_text
from .sections import _section_forage, _section_localisation, _section_observations, _section_pannes, _section_pompage, _section_suivis
from .suiviform import SuiviForm
from .forationform import ForationForm
from .forationupdateform import ForationUpdateForm
from .pompageform import PompageForm
from .pompageupdateform import PompageUpdateForm
from .panneform import PanneForm
from .panneupdateform import PanneUpdateForm

from utils.constants import (
    PRIMARY, PRIMARY_LIGHT, ACCENT, SURFACE, TEXT_DARK, TEXT_GREY, BG_CARD,
    SUCCESS, WARNING, DANGER, SHADOW,
    ROUTES, app_bar, etat_badge, categorie_chip, divider,
)


CATEGORIES = ["PMH", "PEA", "AEP", "PMH_AEP"]
ETATS = ["Bon", "En panne", "Abandonnée"]


class DetailOuvrageView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.route=f"/projet/list-ouvrage/detail-ouvrage"
        self.state = state
        self.bgcolor = SURFACE
        self.scroll=ft.ScrollMode.AUTO
        self.padding = ft.Padding(0, 0, 0, 0)
        
        self.share=ft.Share()
        self.copy_text=ft.Clipboard()
        
        self.projet: Projet= self.state.selected_projet
        self.ouvrage: Ouvrage = self.state.selected_ouvrage
        self.foration= load_one_foration(self.ouvrage.id)
        self.pompage= load_one_pompage(self.ouvrage.id)
        self.state.pannes= load_all_pannes(self.ouvrage.id)
        # self.suivis= load_all_suivis(self.ouvrage.id)
        

        self.appbar = self._build_appbar()
        self.controls = self._build()

    def _build_appbar(self):
        lieu = self.ouvrage.lieu if self.ouvrage else "Ouvrage"
        return ft.AppBar(
            title=ft.Text(lieu, color="#FFFFFF", weight=ft.FontWeight.BOLD, size=18),
            bgcolor=PRIMARY,
            color=ft.Colors.WHITE,
            actions=[
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    icon_color="#FFFFFF",
                    items=[
                        ft.PopupMenuItem(ft.Text("Exporter PV xlsx"), icon=ft.Icons.TABLE_CHART,
                                         on_click=lambda _: self._export("pv_xlsx")),
                        ft.PopupMenuItem(ft.Text("Exporter PV PDF"), icon=ft.Icons.PICTURE_AS_PDF,
                                         on_click=lambda _: self._export("pv_pdf")),
                        ft.PopupMenuItem(),  # séparateur
                        ft.PopupMenuItem(ft.Text("Rapport détaillé PDF"),
                                         icon=ft.Icons.SUMMARIZE,
                                         on_click=lambda _: self._export("rapport_pdf")),
                        ft.PopupMenuItem(),  # séparateur
                        ft.PopupMenuItem(ft.Text("Supprimer ouvrage"),
                                         icon=ft.Icons.DELETE,
                                         on_click=lambda _: self._delete_ouvrage()),
                    ],
                ),
            ],
        )

    def _build(self):
        if not self.ouvrage:
            return ft.Text("Aucun ouvrage sélectionné.")
        return [
            # ── Résumé ──────────────────────────────────────
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(self.ouvrage.lieu, size=20, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        etat_badge(self.ouvrage.etat),
                        categorie_chip(self.ouvrage.type_ouvrage),
                    ], spacing=8, expand=True),
                    ft.Text(f"Projet : {self.projet.name or '—'}",
                            color=ft.Colors.with_opacity(0.85, "#FFFFFF"), size=13),
                    ft.Text(f"Entreprise : {self.ouvrage.entreprise or '—'}",
                            color=ft.Colors.with_opacity(0.85, "#FFFFFF"), size=13),
                    ft.Row(
                        [
                            ft.Text(f"Village : {self.ouvrage.lieu or '—'}  •  {self.ouvrage.canton or ''}",
                            color=ft.Colors.with_opacity(0.85, "#FFFFFF"), size=13),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.SHARE, 
                                        on_click=self.share_all_data,
                                        icon_color="#1E88E5"
                                    ),
                                    ft.IconButton(icon=ft.Icons.EDIT, 
                                          icon_color=ft.Colors.WHITE,
                                          on_click=self.go_editouvrage_view
                                          )
                                ]
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ], spacing=6),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1),
                    colors=[PRIMARY, "#0D47A1"],
                ),
                padding=ft.Padding(20, 20, 20, 20),
                border_radius=ft.BorderRadius(0, 0, 16, 16),
            ),

            # ft.Container(height=4),

            # ── Sections ─────────────────────────────────────
            ft.Container(
                content=ft.Column([
                    _section_localisation(self.ouvrage,copy_coords=self.copyCoords),
                    divider(),
                    _section_forage(foration=self.foration, sho_edit=lambda e: self.showForationForm(),share_foration=self.share_foration),
                    divider(),
                    _section_pompage(self.pompage, show_edit_pompage=lambda e: self.showPompage(), share_pompage=self.share_pompage),
                    divider(),
                    # _section_reception(self.ouvrage),
                    # divider(),
                    _section_observations(self.ouvrage),
                    divider(),
                    _section_pannes(state=self.state, _open_add_panne=self._open_add_panne, _on_delete_panne=self._on_delete_panne),
                    divider(),
                    _section_suivis(state=self.state,_open_add_suivi=self._open_add_suivi, _on_delete_suivi=self._on_delete_suivi),
                ], spacing=16),
                padding=ft.Padding(16, 16, 16, 32),
            ),
        ]
        
    def _refresh(self):
        self.foration= load_one_foration(self.ouvrage.id)
        self.pompage= load_one_pompage(self.ouvrage.id)
        self.state.pannes= load_all_pannes(self.ouvrage.id)
        self.state.suivis= load_all_suivis(self.ouvrage.id)
        self.controls = self._build()
        # self.page.update()

    # Foration données =============================================
    def showForationForm(self):
        if self.foration=={}:
            cont=ForationForm(state=self.state,formcontrol=self)
        else:
            cont=ForationUpdateForm(state=self.state, donnees=self.foration , formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Info Foration"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Sauvegarder", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

    async def share_foration(self,e):
        text_to_shared=convert_data_foration_to_text(self.ouvrage.to_dict(),self.foration)
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        ) 

    async def share_all(self,e):
        text_to_shared=convert_data_all_to_text(self.ouvrage.to_dict(),self.foration, self.pompage)
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )

    async def share_pompage(self,e):
        text_to_shared=convert_data_pompage_to_text(self.ouvrage.to_dict(),self.pompage)
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )

    async def share_all_data(self,e):
        text_to_shared=convert_data_all_to_text(self.ouvrage.to_dict(), self.foration, self.pompage)
        result = await self.share.share_text(
            text_to_shared,
            subject="Greeting",
            title="Share greeting",
        )
    
    async def copyCoords(self):
        datas=self.ouvrage.to_dict()
        await self.copy_text.set(f"{datas['coordonnee_x'],datas['coordonnee_y']}")
        return self.page.show_dialog(ft.SnackBar(ft.Text("Coordonnées copiés avec succès")))
        
        
    # Pompage données =============================================
    def showPompage(self):
        if self.pompage=={}:
            cont=PompageForm(state=self.state,formcontrol=self)
        else:
            cont=PompageUpdateForm(state=self.state, donnees=self.pompage , formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Info Pompage"),
            content=cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Sauvegarder", on_click=lambda e: cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)
        
    # ── Formulaire panne ─────────────────────────────────────────────────────

    def _open_add_panne(self, _=None):
        panne_cont = PanneForm(state=self.state, formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nouvel panne"),
            content=panne_cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Enregistrer", on_click=lambda e: panne_cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

    # ── Formulaire suivi ─────────────────────────────────────────────────────

    def _open_add_suivi(self, _=None):
        panne_cont = SuiviForm(state=self.state, formcontrol=self)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nouveau Suivi"),
            content=panne_cont,
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Enregistrer", on_click=lambda e: panne_cont.SaveData()),
            ],
            actions_alignment= ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.show_dialog(self.dlg_modal)

    # ── Export ───────────────────────────────────────────────────────────────

    def _export(self, mode: str):
        from services.export_service import export_pv_xlsx, export_pv_pdf, export_rapport_detaille_pdf
        ouvrage = self.ouvrage
        proj = self.projet
        foration=Foration(**self.foration) if self.foration else []
        pompage=Pompage(**self.pompage) if self.pompage else []

        try:
            if mode == "pv_xlsx":
                path = export_pv_xlsx(
                    ouvrage,foration,pompage,
                    proj.name,
                )
                label = "PV xlsx"
            elif mode == "pv_pdf":
                path = export_pv_pdf(
                    ouvrage,foration,pompage,
                    proj.name,
                )
                label = "PV PDF"
            else:  # rapport_pdf
                path = export_rapport_detaille_pdf(
                    ouvrage=ouvrage,foration=foration,pompage=pompage,
                    projet_nom=proj.name,
                )
                label = "Rapport Détaillé PDF"

            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text(f"{label} — Export réussi ✅"),
                content=ft.Column([
                    ft.Text(f"Fichier généré :", size=12),
                    ft.Text(path, size=10, color="#607D8B", selectable=True),
                ], spacing=4, tight=True),
                actions=[
                    ft.TextButton("Voir les archives",
                                  on_click=lambda _: (
                                      self.page.pop_dialog(),
                                      self.page.go(ROUTES["archives"])
                                  )),
                    ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog()),
                ],
            ))
        except Exception as ex:
            self.page.show_dialog(ft.AlertDialog(
                title=ft.Text("Erreur d'export"),
                content=ft.Text(str(ex)),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.pop_dialog())],
            ))
            
    def _on_delete_panne(self,panne_id):
        delete_panne(panne_id)
        self._refresh()     
           
    def _on_delete_suivi(self,suivi_id):
        delete_suivi(suivi_id)
        self._refresh()    
           
    def _delete_ouvrage(self):
        delete_ouvrage(self.ouvrage.id)
        try:
            delete_foration(self.ouvrage.id)
        except:
            pass 
        try:
            delete_pompage(self.ouvrage.id)
        except:
            pass 
        self.page.views.pop()
        self.page.views.pop()
        asyncio.create_task(self.page.push_route("/projet/list-ouvrage"))
        

    # ── Rebuild ──────────────────────────────────────────────────────────────

    def _rebuild(self):
        self.appbar = self._build_appbar()
        self.controls = self._build()
        self.update()

    def did_mount(self):
        self.state.load_suivis()
        self.state.load_pannes()
        self._rebuild()
    
    async def go_editouvrage_view(self):
        await self.page.push_route("/projet/list-ouvrage/detail-ouvrage/edit-ouvrage")
