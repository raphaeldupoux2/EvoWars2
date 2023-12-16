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
        self.position_affectee = Marqueur(monde, (self.x_abs, self.y_abs))
        self.monde.player.append(self)

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * self.image.W_DECAL, self.y - self.image.height * self.image.H_DECAL))
        self.image.refresh_cropped_png()

    def move_to_position(self, position):
        super().move_to_position(position)
        self.image.angle = self.direction_degree_vers(position)

    def behavior(self, w):
        self.print_image(w)
        if self.etat.possession['is_controled'] is False:
            self.move_to_position((self.position_affectee.x, self.position_affectee.y))
        self.effet_subis.apply()


class Marqueur(Acteur):
    def __init__(self, monde, position):
        super().__init__(monde, "marqueur", position)
        self.monde.marqueur.append(self)

    def behavior(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), [self.x, self.y], 3, 1)
