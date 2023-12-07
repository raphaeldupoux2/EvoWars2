import pygame

from anew.load_png.sorcier import ImageSorcier
from anew.world.acteur import Acteur
from anew.world.effet import Effet
from anew.world.etat import Etat


class Player(Acteur):
    vitesse_naturelle = 3

    def __init__(self, monde, coords: tuple, vitesse, dimension, slow_max: int, possession_max: int):
        super().__init__(monde, "creature", coords, vitesse=vitesse, vivant=True)
        self.image = ImageSorcier(dimension, 'picture/sorcier_rouge.png')
        self.etat = Etat(slow_max, possession_max)
        self.effet_subis = Effet(self.monde, self, self.etat)
        self.clic_gauche = (self.x, self.y)
        self.clic_droit = (self.x, self.y)
        self.monde.player.append(self)

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * self.image.W_DECAL, self.y - self.image.height * self.image.H_DECAL))
        self.image.refresh_cropped_png()

    def move_to_position(self, direction):
        super().move_to_position(direction)
        self.image.angle = self.direction_degree_vers(direction)

    def behavior(self, w):
        self.print_image(w)
        if self.etat.possession['is_controled'] is False:
            self.move_to_position(self.clic_droit)
        self.effet_subis.apply()

    def button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.clic_gauche = event.pos
            elif event.button == 3:
                self.clic_droit = event.pos
