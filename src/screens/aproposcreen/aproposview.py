"""
pages/aproposview.py
Vue À propos de l'application
"""

import flet as ft
from utils.constants import (
    PRIMARY, SURFACE, TEXT_DARK, TEXT_GREY, BG_CARD, TEXT_LIGHT,
    ROUTES, app_bar,
)


class AproposView(ft.View):
    def __init__(self, state):
        super().__init__()
        self.route=ROUTES["a_propos"]
        self.state = state
        self.bgcolor = SURFACE
        self.spacing=0
        self.padding = ft.Padding(0, 0, 0, 0)
        self.appbar = app_bar("À propos", show_back=False)
        self.scroll=ft.ScrollMode.AUTO
        self.controls = [
            # ── Logo / Header ────────────────────────────────────
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WATER_DROP, color=TEXT_LIGHT, size=64),
                    ft.Text("EaRapport", size=28, weight=ft.FontWeight.BOLD, color=TEXT_LIGHT),
                    ft.Text("Version 1.0.0", color=ft.Colors.with_opacity(0.8, TEXT_LIGHT), size=13),
                    ft.Text("Application de recensement et suivi des ouvrages d'eau",
                            color=ft.Colors.with_opacity(0.8, TEXT_LIGHT),
                            size=12, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1),
                    colors=[PRIMARY, "#0D47A1"],
                ),
                padding=ft.Padding(20, 40, 20, 40),
                border_radius=ft.BorderRadius(0, 0, 20, 20),
                width=float("inf"),
            ),

            ft.Container(
                content=ft.Column([
                    # ── Fonctionnalités ───────────────────────────
                    self._info_card("🎯 Objectif", [
                        "Permettre aux agents de suivi des ouvrages de forages de :",
                        "• Consulter et gérer les ouvrages par projet",
                        "• Générer des procès-verbaux en xlsx ou PDF",
                        "• Filtrer et exporter la liste des ouvrages",
                        "• Suivre les pannes et solutions",
                        "• Visualiser les statistiques via un dashboard",
                    ]),

                    # ── Types d'ouvrages ──────────────────────────
                    self._info_card("💧 Types d'Ouvrages", [
                        "PMH  — Pompe à Motricité Humaine",
                        "PEA  — Poste d'Eau Autonome",
                        "AEP  — Adduction en Eau Potable",
                        "PMH/AEP — PMH en adduction",
                    ]),

                    # ── Infos techniques ──────────────────────────
                    self._info_card("⚙️ Informations Techniques", [
                        "Plateforme : Android ≥ 10",
                        "Framework : Flet 0.80.5 (Python)",
                        "Base de données : SQLite",
                        "Export : OpenPyXL (xlsx) + ReportLab (PDF)",
                    ]),

                    # ── Copyright ─────────────────────────────────
                    ft.Container(
                        content=ft.Text(
                            "© 2024 EaRapport — Tous droits réservés",
                            color=TEXT_GREY, size=12,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.Padding(0, 8, 0, 0),
                        width=float("inf"),
                    ),
                ], spacing=16),
                padding=ft.Padding(16, 20, 16, 32),
            ),
        ]

    def _info_card(self, title: str, lines: list[str]) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=PRIMARY),
                ft.Divider(height=1, color="#BBDEFB"),
                *[ft.Text(line, size=13, color=TEXT_DARK) for line in lines],
            ], spacing=8),
            bgcolor=BG_CARD,
            border_radius=ft.BorderRadius(12, 12, 12, 12),
            padding=ft.Padding(16, 14, 16, 14),
            shadow=ft.BoxShadow(blur_radius=5,
                                color=ft.Colors.with_opacity(0.08, "#000000"),
                                offset=ft.Offset(0, 2)),
        )
