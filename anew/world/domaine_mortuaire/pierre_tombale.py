import pygame

from anew.load_png.pierre import ImageStone
from anew.world.acteur import Acteur


class PierreTombale(Acteur):
    def __init__(self, monde, coords, dimension):
        super().__init__(monde, "objet", coords)
        self.image = ImageStone(dimension)
        self.radius = 200
        self.monde.pierre_tombale.append(self)

    def affiche_radius(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), [self.x, self.y], self.radius, 1)

    def print_image(self, w):
        w.window.blit(self.image.png, (self.x - self.image.width * 1/2, self.y - self.image.height * 50/125))

    def behavior(self, w):
        self.print_image(w)
        # self.affiche_radius(w)

