from dataclasses import dataclass, field 
import flet as ft

from myaction.myaction_main import get_stats
from myaction.myaction_panne import Panne, load_all_pannes
from myaction.myaction_projet import *
from myaction.myaction_ouvrage import *
from myaction.myaction_entreprise import *
from myaction.myaction_foration import *
from myaction.myaction_pompage import *
from myaction.myaction_suivi import Suivi, load_all_suivis
from myaction.myaction_village import Village, load_all_villages

@ft.observable
@dataclass
class AppState:
    route:str="/"
    projets:list[Projet]=field(default_factory=list)
    ouvrages:list[Ouvrage]=field(default_factory=list)
    entreprises:list[Entreprise]=field(default_factory=list)
    villages:list[Village]=field(default_factory=list)
    suivis:list[Suivi]=field(default_factory=list)
    pannes:list[Panne]=field(default_factory=list)
    forations: list[Foration] = field(default_factory=list)
    pompages: list[Pompage] = field(default_factory=list)
    all_ouvrages: list[Ouvrage] = field(default_factory=list)
    villages_sans_forage: list[Village] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    
    selected_projet:Projet|None=None
    selected_ouvrage:Ouvrage|None=None
    selected_entreprise:Entreprise|None=None
    selected_suivi:Suivi|None=None
    selected_panne:Panne|None=None

    def load_projets(self):
        self.projets=load_all_projets()
        return self.projets

    def load_ouvrages(self):
        self.ouvrages=load_all_ouvrages(self.selected_projet.id)
        return self.ouvrages

    def load_entreprises(self):
        self.entreprises=load_all_entreprises()
        return self.entreprises
    
    def load_villages(self):
        self.villages=load_all_villages()
        return self.villages

    def load_suivis(self):
        self.suivis=load_all_suivis(self.selected_ouvrage.id)
        return self.suivis

    def load_pannes(self):
        self.pannes=load_all_pannes(self.selected_ouvrage.id)
        return self.pannes
    
    def load_forations(self):
        self.foration=load_all_forations()
        return self.foration
        
    def load_pompages(self):
        self.pompages=load_all_pompages()
        return self.foration
    
    def load_all_ouvrages_flat(self):
        self.all_ouvrages=load_all_ouvrages()
        return self.all_ouvrages
        
    # ── Stats ─────────────────────────────────────────────────────────────────
    def load_stats(self):
        self.stats = get_stats(); return self.stats
