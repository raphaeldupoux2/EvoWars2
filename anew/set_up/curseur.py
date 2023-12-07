import pygame

from anew.set_up.sous_fenetre import SousFenetreManager


class Curseur:
    def __init__(self, fenetres: SousFenetreManager):
        self.fenetres = fenetres
        self.fenetre_control = None
        self.pos_globale = (0, 0)
        self.pos_relative = (0, 0)

    def curseur_detecte_fenetre(self):
        """
        :return: la fenêtre localisée à l'endroit de la position du curseur
        """
        self.fenetre_control = None
        for f in self.fenetres.all:
            if f.position[0] < self.pos_globale[0] < f.position[0] + f.width and f.position[1] < self.pos_globale[1] < f.position[1] + f.height:
                self.fenetre_control = f

    def curseur_in_fenetre(self):
        """
        retourne la position du curseur relative à la fenêtre
        :return: tuple(x, y)
        """
        if self.fenetre_control is not None:
            self.pos_relative = (self.pos_globale[0] - self.fenetre_control.position[0],
                                 self.pos_globale[1] - self.fenetre_control.position[1])

    def refresh_curseur(self):
        self.pos_globale = pygame.mouse.get_pos()
        self.curseur_detecte_fenetre()
        self.curseur_in_fenetre()
