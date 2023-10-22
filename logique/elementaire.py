import pygame

from EvoWars2.logique.acteur import Acteur
from EvoWars2.pygamesetup import SousFenetre
from EvoWars2.sprite.elementaire import ImageElementaire
from EvoWars2.utils import Utils


class Elementaire(Acteur):
    def __init__(self, window: SousFenetre, position):
        super().__init__(position, ImageElementaire(window, position))
        self.w = window
        self.radius_attaque = 15

    def affiche_radius_attaque(self):
        pygame.draw.circle(self.w.window, (0, 255, 0), [self.x, self.y], self.radius_attaque, 1)

    def comportement(self):
        self.affiche_skin()
        # self.x, self.y = Utils.move_to((self.x, self.y), (self.x + 10, self.y + 10), 2)
