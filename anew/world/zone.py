import pygame

from anew.world.acteur import Acteur


class Zone(Acteur):
    def __init__(self, monde, coords, radius):
        super().__init__(monde, 'lieu', coords)
        self.radius = radius
        self.monde.zone.append(self)

    def affiche(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), [self.x, self.y], self.radius, 10)

    def behavior(self, w):
        self.affiche(w)
