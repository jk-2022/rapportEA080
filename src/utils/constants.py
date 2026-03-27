"""
utils/constants.py
Constantes et widgets réutilisables pour EaRapport
"""

import flet as ft

# ── Couleurs ─────────────────────────────────────────────────────────────────
PRIMARY      = "#1565C0"   # Bleu foncé eau
PRIMARY_LIGHT= "#1E88E5"
ACCENT       = "#00ACC1"   # Cyan eau
SURFACE      = "#F5F9FF"
BG_CARD      = "#FFFFFF"
TEXT_DARK    = "#1A237E"
TEXT_LIGHT   = "#FFFFFF"
TEXT_GREY    = "#607D8B"
SUCCESS      = "#2E7D32"
WARNING      = "#F57F17"
DANGER       = "#C62828"
SHADOW       = "#BBDEFB"

ETAT_COLORS = {
    "Bon":        SUCCESS,
    "En panne":   WARNING,
    "Abandonnée": DANGER,
}

CATEGORIE_ICONS = {
    "PMH":     ft.Icons.WATER_DROP,
    "PEA":     ft.Icons.ELECTRICAL_SERVICES,
    "AEP":     ft.Icons.WATER,
    "PMH_AEP": ft.Icons.WATER_DROP_OUTLINED,
}

ROUTES = {
    "accueil":        "/",
    "projets":        "/projets",
    "ouvrages":       "/ouvrages",
    "all_ouvrages":   "/all_ouvrages",
    "detail_ouvrage": "/detail_ouvrage",
    "dashboard":      "/dashboard",
    "archives":       "/archives",
    "parametres":     "/parametres",
    "a_propos":       "/a_propos",
    "entreprises":    "/entreprises",
    "villages_sf":    "/villages_sf",
}


# ── Widgets réutilisables ─────────────────────────────────────────────────────

def app_bar(title: str, show_back: bool = False) -> ft.AppBar:
    """Barre d'application commune."""
    leading = None
    if show_back:
        leading = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=TEXT_LIGHT,
            # on_click=lambda _: self.page.go_back(),
        )
    return ft.AppBar(
        title=ft.Text(title, color=TEXT_LIGHT, weight=ft.FontWeight.BOLD, size=18),
        bgcolor=PRIMARY,
        leading=leading,
        leading_width=48,
        center_title=False,
        color=ft.Colors.WHITE
    )


def search_bar(on_change, hint: str = "Rechercher…") -> ft.TextField:
    """Barre de recherche standard."""
    return ft.TextField(
        hint_text=hint,
        prefix_icon=ft.Icons.SEARCH,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=PRIMARY_LIGHT,
        focused_border_color=PRIMARY,
        on_change=on_change,
        height=48,
        text_size=14,
    )


def etat_badge(etat: str) -> ft.Container:
    """Badge coloré pour l'état d'un ouvrage."""
    color = ETAT_COLORS.get(etat, TEXT_GREY)
    return ft.Container(
        content=ft.Text(etat, color=TEXT_LIGHT, size=11, weight=ft.FontWeight.BOLD),
        bgcolor=color,
        border_radius=ft.BorderRadius(12, 12, 12, 12),
        padding=ft.Padding(8, 3, 8, 3),
    )


def categorie_chip(categorie: str) -> ft.Container:
    """Chip pour la catégorie d'ouvrage."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(CATEGORIE_ICONS.get(categorie, ft.Icons.WATER), size=14, color=PRIMARY),
                ft.Text(categorie, size=11, color=PRIMARY, weight=ft.FontWeight.W_600),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor=SHADOW,
        border_radius=ft.BorderRadius(10, 10, 10, 10),
        padding=ft.Padding(8, 3, 8, 3),
    )
    
def champ_recherche(hint_text:str, on_change):
    # ── Barre de recherche ────────────────────────────────────────────────
    return ft.TextField(
        hint_text="Rechercher un établissement…",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        expand=True,
        filled=True,
        fill_color=SURFACE,
        border_color=ft.Colors.with_opacity(0.1, "black"),
        on_change=on_change,
        height=40,
        cursor_height=16,
        # text_align=ft.TextAlign.CENTER
    )


def card_container(content: ft.Control, on_click=None) -> ft.Container:
    """Carte standard avec ombre."""
    return ft.Container(
        content=content,
        bgcolor=BG_CARD,
        border_radius=ft.BorderRadius(12, 12, 12, 12),
        padding=ft.Padding(16, 12, 16, 12),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.12, "#000000"),
            offset=ft.Offset(0, 2),
        ),
        on_click=on_click,
        ink=on_click is not None,
    )


def stat_card(label: str, value, icon: str, color: str = PRIMARY) -> ft.Container:
    """Carte statistique pour le dashboard."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(icon, color=color, size=28),
                ft.Text(str(value), size=22, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=11, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=BG_CARD,
        border_radius=ft.BorderRadius(12, 12, 12, 12),
        padding=ft.Padding(12, 16, 12, 16),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.10, "#000000"),
            offset=ft.Offset(0, 2),
        ),
        expand=True,
    )


def fab(icon: str, on_click, tooltip: str = "Ajouter") -> ft.FloatingActionButton:
    return ft.FloatingActionButton(
        icon=icon,
        bgcolor=PRIMARY,
        on_click=on_click,
        tooltip=tooltip,
    )


def confirm_dialog(page: ft.Page, title: str, content: str, on_confirm) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[
            ft.TextButton("Annuler", on_click=lambda _: page.close_dialog()),
            ft.TextButton(
                "Confirmer",
                style=ft.ButtonStyle(color=DANGER),
                on_click=lambda _: (page.close_dialog(), on_confirm()),
            ),
        ],
    )
    return dlg


def text_field(label: str, value: str = "", multiline: bool = False,
               keyboard_type=None, **kwargs) -> ft.TextField:
    return ft.TextField(
        label=label,
        value=value,
        multiline=multiline,
        min_lines=3 if multiline else 1,
        max_lines=6 if multiline else 1,
        keyboard_type=keyboard_type,
        border_color=PRIMARY_LIGHT,
        focused_border_color=PRIMARY,
        label_style=ft.TextStyle(color=TEXT_GREY),
        **kwargs,
    )


def dropdown(label: str, options: list[str], value: str = "") -> ft.Dropdown:
    return ft.Dropdown(
        label=label,
        value=value if value in options else (options[0] if options else ""),
        options=[ft.dropdown.Option(o) for o in options],
        border_color=PRIMARY_LIGHT,
        focused_border_color=PRIMARY,
        label_style=ft.TextStyle(color=TEXT_GREY),
    )


def section_title(text: str) -> ft.Text:
    return ft.Text(
        text,
        size=14,
        weight=ft.FontWeight.BOLD,
        color=PRIMARY,
    )


def divider() -> ft.Divider:
    return ft.Divider(height=1, color=SHADOW)


def empty_state(message: str, icon: str = ft.Icons.INBOX) -> ft.Column:
    return ft.Column(
        [
            ft.Icon(icon, size=64, color=ft.Colors.with_opacity(0.3, PRIMARY)),
            ft.Text(message, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
