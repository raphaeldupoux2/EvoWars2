import pygame

from anew.set_up.curseur import Curseur
from anew.set_up.fenetre import FenetrePrincipale
from anew.set_up.horloge import Horloge
from anew.set_up.sous_fenetre import SousFenetreManager


class PygameSetUp:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, title='', width=1000, height=720, fps=60):
        if cls._instance is None:
            cls._instance = super(PygameSetUp, cls).__new__(cls)
            pygame.init()
            cls._instance.main_window = FenetrePrincipale(title, width, height)
            cls._instance.fenetres = SousFenetreManager()
            cls._instance.curseur = Curseur(cls._instance.fenetres)
            cls._instance.horloge = Horloge(fps)
        return cls._instance
