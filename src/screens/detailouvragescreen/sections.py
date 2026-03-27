import flet as ft

from appstate import Ouvrage
from myaction.myaction_foration import Foration
from myaction.myaction_pompage import Pompage
from utils.constants import ACCENT, PRIMARY, SUCCESS, TEXT_DARK, TEXT_GREY, WARNING, section_title 

def _info_row(label: str, value: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(label, color=TEXT_GREY, size=12, width=160),
                ft.Text(value or "—", color=TEXT_DARK, size=13, weight=ft.FontWeight.W_500,
                        expand=True),
            ],
            spacing=8,
        )
        
def _section_localisation(o: Ouvrage,copy_coords) -> ft.Column:
    return ft.Column([
        section_title("📍 Localisation"),
        _info_row("Latitude", o.coordonnee_x),
        ft.Row(
            [
                _info_row("Longitude", o.coordonnee_y),
                ft.IconButton(icon=ft.Icons.COPY, 
                                on_click=copy_coords
                                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    ], spacing=8)

def _section_forage(foration: dict, sho_edit, share_foration) -> ft.Column:
    return ft.Column([
        section_title("🔩 Données de Forage"),
        _info_row("Date foration", f"{foration.get('date_foration','-')} m"),
        _info_row("Prof alteration", f"{foration.get('prof_alteration','-')} m"),
        _info_row("Prof socle", f"{foration.get('prof_socle','-')} m"),
        _info_row("Prof total", f"{foration.get('prof_total','-')} m"),
        _info_row("Prof tube_crepine", f"{foration.get('prof_tube_crepine','-')} m"),
        
        ft.Row(
            [
                _info_row("Prof tube_plein", f"{foration.get('prof_tube_plein','-')} m"),
                ft.IconButton(icon=ft.Icons.SHARE, 
                                on_click=share_foration,
                                icon_color="#1E88E5"
                                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Row(
            [
                _info_row("Debit soufflage", f"{foration.get('debit_soufflage','-')} m3/h"),
                ft.IconButton(icon=ft.Icons.EDIT, 
                                          on_click=sho_edit
                                          )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    ], spacing=8)

def _section_pompage(pompage: dict, show_edit_pompage, share_pompage) -> ft.Column:
    return ft.Column([
        section_title("💧 Données de Pompage"),
        _info_row("Date pompage", f"{pompage.get('date_pompage','-')} m"),
        _info_row("Type pompe", f"{pompage.get('type_pompe','-')} m"),
        _info_row("Côte pompe", f"{pompage.get('cote_pompe','-')} m"),
        _info_row("Niv. dynamique", f"{pompage.get('niv_statique','-')} m"),
        _info_row("Niv. Statique", f"{pompage.get('niv_dynamique','-')} m"),
        ft.Row(
            [
                 _info_row("Durée pompage", f"{pompage.get('temps_pompage','-')} h"),
                ft.IconButton(icon=ft.Icons.SHARE, 
                                on_click=share_pompage,
                                icon_color="#1E88E5"
                                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Row(
            [
                _info_row("Débit pompage", f"{pompage.get('debit_pompage','-')} m³/h"),
                ft.IconButton(icon=ft.Icons.EDIT, 
                                          on_click=show_edit_pompage
                                          )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    ], spacing=8)

def _section_reception(ouvrage: Ouvrage) -> ft.Column:
    return ft.Column([
        section_title("📋 Dates de Réception"),
        _info_row("Provisoire", '--'),
        _info_row("Technique", '--'),
        _info_row("Définitive", '--'),
    ], spacing=8)

def _section_observations(ouvrage: Ouvrage) -> ft.Column:
    return ft.Column([
        section_title("📝 Observations"),
        ft.Text(ouvrage.observation or "Aucune observation.", color=TEXT_GREY, size=13),
    ], spacing=8)
    
def _section_pannes(state, _open_add_panne, _on_delete_panne) -> ft.Column:
    pannes = state.pannes
    items = [
        ft.Container(
            content=ft.Column([
                ft.Row(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.WARNING_AMBER, color=WARNING, size=16),
                            ft.Text(p.date_signaler, size=12, color=TEXT_GREY),
                            ft.Container(
                                content=ft.Text("Résolu" if p.solution else "En cours",
                                                size=10, color="#FFFFFF"),
                                bgcolor=SUCCESS if p.solution else WARNING,
                                border_radius=ft.BorderRadius(8, 8, 8, 8),
                                padding=ft.Padding(6, 2, 6, 2),
                                ),
                            ], spacing=6),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700,
                            on_click=lambda e, panne_id=p.id: _on_delete_panne(panne_id)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                ft.Text(p.description, size=13, color=TEXT_DARK),
                ft.Text(f"Solution : {p.solution or '—'}", size=12, color=TEXT_GREY),
            ], spacing=4),
            bgcolor="#FFF8E1",
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            padding=ft.Padding(12, 10, 12, 10),
        )
        for p in pannes
    ] or [ft.Text("Aucune panne signalée.", color=TEXT_GREY, size=13)]
    return ft.Column([
            ft.Row([
                section_title("⚠️ Pannes et Solutions"),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE,
                    icon_color=PRIMARY,
                    tooltip="Ajouter panne",
                    on_click=_open_add_panne,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            *items,
        ], spacing=8)
    

def _section_suivis(state,_open_add_suivi, _on_delete_suivi) -> ft.Column:
        suivis = state.suivis
        items = [
            ft.Container(
                content=ft.Column([
                    ft.Row(
                        [
                            ft.Row([
                                ft.Icon(ft.Icons.CALENDAR_TODAY, color=ACCENT, size=16),
                                ft.Text(s.date_reception, size=12, color=TEXT_GREY),
                                ft.Text(f"Type de suivi : {s.type_reception}", size=12, color=PRIMARY),
                            ], spacing=6),
                                ft.IconButton(
                                icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700,
                                on_click=lambda e, suivi_id=s.id: _on_delete_suivi(suivi_id)
                            )
                        ], alignment= ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ft.Text(s.observation or "—", size=13, color=TEXT_DARK),
                ], spacing=4),
                bgcolor="#E0F7FA",
                border_radius=ft.BorderRadius(8, 8, 8, 8),
                padding=ft.Padding(12, 10, 12, 10),
            )
            for s in suivis
        ] or [ft.Text("Aucun suivi enregistré.", color=TEXT_GREY, size=13)]

        return ft.Column([
            ft.Row([
                section_title("🔍 Suivis"),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE,
                    icon_color=PRIMARY,
                    tooltip="Ajouter suivi",
                    on_click=_open_add_suivi,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            *items,
        ], spacing=8)