import pygame

from logique.acteur import Acteur
from sprite.image_dimension import AfficheArbre


class Arbre(Acteur):
    couleur_tronc = (112, 93, 72)

    def __init__(self, window, position: tuple):
        super().__init__(position, AfficheArbre(window, position))
        self.w = window
        self.tronc_radius = (self.skin.width + self.skin.height) / 34

    def affiche_tronc(self):
        pygame.draw.circle(self.w.window, self.couleur_tronc, [self.x, self.y], self.tronc_radius, 0)

    def comportement(self):
        self.affiche_skin()
        self.affiche_tronc()
