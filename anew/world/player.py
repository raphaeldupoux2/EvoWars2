import pygame

from anew.load_png.sorcier import ImageSorcier
from anew.world.acteur import Acteur
from anew.world.boule_de_feu import BouleDeFeu
from anew.world.effet import Effet
from anew.world.etat import Etat


class Player(Acteur):
    vitesse_naturelle = 3

    def __init__(self, monde, coords: tuple, vitesse, dimension, slow_max: int, possession_max: int, zone, numero):
        super().__init__(monde, "creature", coords, zone=zone, vitesse=vitesse, vivant=True)
        self.image = ImageSorcier(dimension, 'picture/sorcier_rouge.png')
        self.etat = Etat(slow_max, possession_max)
        self.effet_subis = Effet(self.monde, self, self.etat)
        self.position_affectee = None
        self.zone = zone
        self.numero = numero
        self.monde.player.append(self)

    def __repr__(self):
        return f"Player{self.numero}"

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * self.image.W_DECAL, self.y - self.image.height * self.image.H_DECAL))
        self.image.refresh_cropped_png()

    def move_to_position(self, position):
        self.image.angle = self.direction_degree_vers(position)
        return super().move_to_position(position)

    def move_respecte_zone(self):  # si il s'éloigne trop de la zone alors il est stoppé
        if not self.zone.is_point_inside((self.x, self.y)):
            self.move_to_position(self.zone.rect.center)
            self.position_affectee = None
            self.monde.marqueur = []
        else:
            if self.etat.possession['is_controled'] is False:
                if self.position_affectee is not None:
                    self.move_to_position((self.position_affectee.x, self.position_affectee.y))

    def fireball_power(self, coords):
        direction = self.direction_radian_vers(coords)
        BouleDeFeu(self.monde, (self.x_abs, self.y_abs), 10, direction)

    def passage_entre_zone(self):
        for z in self.monde.zone:
            if self.zone.rect.midright == z.rect.midleft:  # z est sur la droite
                if self.zone.tapis_right.collidepoint((self.x, self.y)):
                    self.zone = z
                    break
            elif self.zone.rect.midleft == z.rect.midright:  # z est sur la gauche
                if self.zone.tapis_left.collidepoint((self.x, self.y)):
                    self.zone = z
                    break
            elif self.zone.rect.midtop == z.rect.midbottom:  # z est en haut
                if self.zone.tapis_top.collidepoint((self.x, self.y)):
                    self.zone = z
                    break
            elif self.zone.rect.midbottom == z.rect.midtop:  # z est en bas
                if self.zone.tapis_bot.collidepoint((self.x, self.y)):
                    self.zone = z
                    break

    def behavior(self, w):
        self.print_image(w)
        self.move_respecte_zone()
        self.effet_subis.apply()


class Marqueur(Acteur):
    def __init__(self, monde, position):
        super().__init__(monde, "marqueur", position)
        self.monde.marqueur.append(self)

    def __repr__(self):
        return f"{self.x_abs, self.y_abs}"

    def behavior(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), [self.x, self.y], 3, 1)
