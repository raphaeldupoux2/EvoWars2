import pygame
import math

from anew.load_png.boule_de_feu import ImageBouleDeFeu
from anew.world.acteur import Acteur


class BouleDeFeu(Acteur):
    def __init__(self, monde, coords, vitesse, direction):
        super().__init__(monde, "projectile", coords, zone=None, vitesse=vitesse)
        self.image = ImageBouleDeFeu(dimension=(33, 200))
        self.direction = direction
        self.monde.fireball.append(self)

    def frottement(self):
        self.vitesse -= 0.08
        if self.vitesse <= 0:
            self.vitesse = 0

    def consumation(self):
        if self.vitesse <= 3:
            self.monde.fireball.remove(self)

    def print_image(self, w):
        rotated_image = pygame.transform.rotate(self.image.png, - self.direction * 180 / math.pi - 90)
        rect = rotated_image.get_rect()
        w.window.blit(rotated_image, (self.x - rect.width / 2, self.y - rect.height / 2))

    def behavior(self, w):
        self.frottement()
        self.consumation()
        self.move_in_direction(self.direction)
        self.print_image(w)

