import pygame

from logique.acteur import Acteur
from pygamesetup import SousFenetre
from sprite.image_dimension import Image


class Elementaire(Acteur):
    def __init__(self, window: SousFenetre, position):
        super().__init__(window, position, Image((35, 60), (1/2, 2/3), "picture/png_hd/elementaire.png"))
        self.radius_attaque = 15

    def affiche_radius_attaque(self):
        pygame.draw.circle(self.w.window, (0, 255, 0), [self.x, self.y], self.radius_attaque, 1)

    def comportement(self):
        super().comportement()
