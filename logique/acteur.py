import pygame

from EvoWars2.pygamesetup import SousFenetre
from EvoWars2.sprite.elementaire import ImageElementaire


class Acteur:
    def __init__(self, position, skin):
        self.x, self.y = position
        self.skin = skin

    def refresh_skin(self):
        self.skin.x, self.skin.y = self.x, self.y

    def affiche_skin(self):
        self.refresh_skin()
        self.skin.comportement()
