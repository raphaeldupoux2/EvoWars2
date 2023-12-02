import pygame

from logique.acteur import Acteur
from sprite.image_dimension import Image


class Arbre(Acteur):
    couleur_tronc = (112, 93, 72)

    def __init__(self, window, position: tuple):
        super().__init__(window, position, Image((250, 250), (23/44, 7/8), "./picture/arbre/grand_arbre.png"))
        self.tronc_radius = (self.skin.width + self.skin.height) / 34

    def affiche_tronc(self):
        pygame.draw.circle(self.w.window, self.couleur_tronc, [self.x, self.y], self.tronc_radius, 0)

    def comportement(self):
        super().comportement()
        self.affiche_tronc()
