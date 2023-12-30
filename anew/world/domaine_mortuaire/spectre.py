import math
import random

import pygame

from anew.load_png.sorcier import ImageSorcier
from anew.world.acteur import Acteur, normalize_angle


class Spectre(Acteur):
    vitesse_naturelle = 1

    def __init__(self, monde, coords: tuple, vitesse, dimension, zone):
        super().__init__(monde, "creature", coords, zone=zone, vitesse=vitesse, vivant=False)
        self.image = ImageSorcier(dimension, 'picture/sorcier_fantome.png')
        self._cible_potentiel = self.monde.player
        self.cible = None
        self.direction = 0  # en radian
        self.pierre_tombale = None
        self.slow_radius = 50
        self.possession_radius = 3
        self.monde.spectre.append(self)

    def __repr__(self):
        return f"Spectre_PT: {self.pierre_tombale.x_abs:.0f},{self.pierre_tombale.y_abs:.0f}"

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * self.image.W_DECAL, self.y - self.image.height * self.image.H_DECAL))
        self.image.refresh_cropped_png()

    def respecte_pierre_tombale_limite(self):  # si il s'éloigne trop de la pierre tombale alors il revient
        if self.distance_avec((self.pierre_tombale.x, self.pierre_tombale.y)) > self.pierre_tombale.radius:
            self.direction = self.direction_radian_vers((self.pierre_tombale.x, self.pierre_tombale.y))
            self.cible = None

    def move_respecte_zone(self):  # si il s'éloigne trop de la zone alors il est stoppé
        if not self.zone.is_point_inside((self.x, self.y)):
            self.direction = self.direction_radian_vers(self.zone.rect.center)

    def chasse_cible_potentiel_dans_aire_pierre_tombale(self):  # si quelqu'un s'approche trop près de la pierre tombale alors il le prend pour cible
        for c in self._cible_potentiel:
            if self.pierre_tombale.distance_avec((c.x, c.y)) <= self.pierre_tombale.radius:
                if c.etat.possession['is_controled'] is False:
                    self.cible = c

    def direction_calcul(self):
        self.move_respecte_zone()
        if self.pierre_tombale is not None:
            self.respecte_pierre_tombale_limite()
            self.chasse_cible_potentiel_dans_aire_pierre_tombale()
        # il va vers sa cible
        if self.cible is not None:
            self.direction = self.direction_radian_vers((self.cible.x, self.cible.y))

        self.direction += random.uniform(-math.pi/20, math.pi/20)

    def move_in_direction(self, direction):
        self.image.angle = normalize_angle(math.degrees(direction))
        super().move_in_direction(direction)

    def move(self):
        self.direction_calcul()
        self.move_in_direction(self.direction)

    def slow_power(self):
        for v in self.monde.vivant:
            if self.distance_avec((v.x, v.y)) < self.slow_radius:
                v.etat.is_being_slow = True
                v.etat.slow_accumulation(1)

    def possession_power(self):
        if self.distance_avec((self.cible.x, self.cible.y)) < self.possession_radius:
            self.cible.etat.is_being_possessed = True
            self.cible.etat.possession['possesseur'] = self
            self.cible.etat.possession_accumulation(1)
        if self.cible.etat.possession['intensity'] > 300:
            self.cible.etat.possession['is_controled'] = True
            self.cible = None

    def power(self):
        self.slow_power()
        if self.cible is not None:
            self.possession_power()

    def affiche_radius(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), (self.x, self.y), self.slow_radius, 1)

    def behavior(self, w):
        self.move()
        self.print_image(w)
        self.power()
        # self.affiche_radius(w)
