from dataclasses import dataclass, field 
import flet as ft

from myaction.myaction_panne import Panne, load_all_pannes
from myaction.myaction_projet import *
from myaction.myaction_ouvrage import *
from myaction.myaction_entreprise import *
from myaction.myaction_suivi import Suivi, load_all_suivis

@ft.observable
@dataclass
class AppState:
    route:str="/"
    projets:list[Projet]=field(default_factory=list)
    ouvrages:list[Ouvrage]=field(default_factory=list)
    entreprises:list[Entreprise]=field(default_factory=list)
    suivis:list[Suivi]=field(default_factory=list)
    pannes:list[Panne]=field(default_factory=list)
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

    def load_suivis(self):
        self.suivis=load_all_suivis(self.selected_ouvrage.id)
        return self.suivis

    def load_pannes(self):
        self.suivis=load_all_pannes(self.selected_ouvrage.id)
        return self.suivis
