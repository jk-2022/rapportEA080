"""
pages/dashboardview.py
Vue Dashboard avec statistiques complètes
"""

import flet as ft
from utils.constants import (
    PRIMARY, PRIMARY_LIGHT, ACCENT, SURFACE, TEXT_DARK, TEXT_GREY, BG_CARD,
    SUCCESS, WARNING, DANGER, SHADOW,
    ROUTES, app_bar, stat_card, section_title,
)


class DashboardView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.route="/dashboard"
        self.state = state
        self.bgcolor = SURFACE
        self.padding = ft.Padding(0, 0, 0, 0)
        self.appbar = app_bar("Dashboard")
        self.scroll=ft.ScrollMode.AUTO
        self.controls = self._build()

    def _build(self):
        s = self.state.stats

        total      = s.get("total_ouvrages", 0)
        bon        = s.get("ouvrages_bon", 0)
        en_panne   = s.get("ouvrages_en_panne", 0)
        abandonne  = s.get("ouvrages_abandonnee", 0)
        projets    = s.get("total_projets", 0)
        entreprises= s.get("total_entreprises", 0)
        villages   = s.get("total_villages", 0)
        vsf        = s.get("villages_sans_forage", 0)
        pmh        = s.get("ouvrages_pmh", 0)
        pea        = s.get("ouvrages_pea", 0)
        aep        = s.get("ouvrages_aep", 0)
        pmh_aep    = s.get("ouvrages_pmh_aep", 0)
        par_projet = s.get("par_projet", [])

        def _pct(n):
            return f"{round(n/total*100)}%" if total else "0%"

        return [
                    # ── Vue globale ─────────────────────────────────
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.DASHBOARD, color="#FFFFFF", size=20),
                                ft.Text("Vue Globale", color="#FFFFFF",
                                        weight=ft.FontWeight.BOLD, size=15),
                            ], spacing=8),
                            ft.Row([
                                ft.Text(str(total), size=40, weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF"),
                                ft.Column([
                                    ft.Text("ouvrages", color=ft.Colors.with_opacity(0.8, "#FFFFFF"), size=13),
                                    ft.Text("au total", color=ft.Colors.with_opacity(0.8, "#FFFFFF"), size=11),
                                ], spacing=0),
                            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ], spacing=8),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, -1),
                            end=ft.Alignment(1, 1),
                            colors=[PRIMARY, "#0D47A1"],
                        ),
                        padding=ft.Padding(20, 20, 20, 20),
                        border_radius=ft.BorderRadius(0, 0, 16, 16),
                    ),

                    ft.Container(
                        content=ft.Column([

                            # ── Cartes résumé ────────────────────────
                            ft.Row([
                                stat_card("Projets", projets, ft.Icons.FOLDER, PRIMARY),
                                stat_card("Entreprises", entreprises, ft.Icons.BUSINESS, "#2E7D32"),
                            ], spacing=12),
                            ft.Row([
                                stat_card("Villages", villages, ft.Icons.LOCATION_ON, ACCENT),
                                stat_card("Villages s/ forage", vsf, ft.Icons.LOCATION_OFF, DANGER),
                            ], spacing=12),

                            # ── État des ouvrages ─────────────────────
                            section_title("État des Ouvrages"),
                            self._progress_bar("Bon", bon, total, SUCCESS),
                            self._progress_bar("En panne", en_panne, total, WARNING),
                            self._progress_bar("Abandonnée", abandonne, total, DANGER),

                            # ── Par catégorie ────────────────────────
                            section_title("Par Catégorie"),
                            ft.Row([
                                self._cat_card("PMH", pmh, ft.Icons.WATER_DROP, "#1565C0"),
                                self._cat_card("PEA", pea, ft.Icons.ELECTRICAL_SERVICES, "#00897B"),
                                self._cat_card("AEP", aep, ft.Icons.WATER, "#0277BD"),
                                self._cat_card("PMH/AEP", pmh_aep, ft.Icons.WATER_DROP_OUTLINED, "#6A1B9A"),
                            ], spacing=8),

                            # ── Par projet ───────────────────────────
                            section_title("Ouvrages par Projet"),
                            *[self._projet_row(item) for item in par_projet],
                        ], spacing=16),
                        padding=ft.Padding(16, 20, 16, 32),
                    ),
                ]

    def _progress_bar(self, label: str, value: int, total: int, color: str) -> ft.Column:
        pct = value / total if total else 0
        return ft.Column([
            ft.Row([
                ft.Text(label, size=13, color=TEXT_DARK, expand=True),
                ft.Text(f"{value}  ({round(pct*100)}%)", size=12, color=TEXT_GREY),
            ]),
            ft.ProgressBar(value=pct, bgcolor=SHADOW, color=color, height=10,
                           border_radius=ft.BorderRadius(5, 5, 5, 5)),
        ], spacing=4)

    def _cat_card(self, label: str, value: int, icon: str, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=22),
                ft.Text(str(value), size=18, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=10, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(8, 12, 8, 12),
            shadow=ft.BoxShadow(blur_radius=4,
                                color=ft.Colors.with_opacity(0.08, "#000000"),
                                offset=ft.Offset(0, 2)),
            expand=True,
        )

    def _projet_row(self, item: dict) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.FOLDER_OPEN, color=PRIMARY, size=16),
                ft.Text(item["nom"], color=TEXT_DARK, size=13, expand=True),
                ft.Container(
                    content=ft.Text(str(item["nb"]), color="#FFFFFF", size=12,
                                    weight=ft.FontWeight.BOLD),
                    bgcolor=PRIMARY,
                    border_radius=ft.BorderRadius(12, 12, 12, 12),
                    padding=ft.Padding(10, 3, 10, 3),
                ),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(12, 10, 12, 10),
            shadow=ft.BoxShadow(blur_radius=4,
                                color=ft.Colors.with_opacity(0.07, "#000000"),
                                offset=ft.Offset(0, 2)),
        )

    def did_mount(self):
        self.state.load_stats()
        self.controls = self._build()
        self.update()
