import math
import random

import pygame

from anew.acteur import Acteur, normalize_angle


class Player(Acteur):
    vitesse_naturelle = 3

    def __init__(self, monde, coords: tuple, vitesse, vivant, dimension):
        super().__init__(monde, coords, vitesse, vivant)
        self.image = ImageSorcier(dimension, 'picture/sorcier_rouge.png')
        self.clic_gauche = (self.x, self.y)
        self.clic_droit = (self.x, self.y)
        self.monde.player.append(self)

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * 1/2, self.y - self.image.height * 50/125))
        self.image.refresh_cropped_png()

    def behavior(self, w):
        self.resolve_effect()
        self.print_image(w)
        if self.effet['possession']['is_controled'] is False:
            self.move_to_position(self.clic_droit)
            self.image.angle = self.direction_degree_vers(self.clic_droit)
        else:
            self.move_to_position((self.effet['possession']['possesseur'].x, self.effet['possession']['possesseur'].y))
            self.image.angle = self.direction_degree_vers((self.effet['possession']['possesseur'].x, self.effet['possession']['possesseur'].y))

    def button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.clic_gauche = event.pos
            elif event.button == 3:
                self.clic_droit = event.pos


class Spectre(Acteur):
    vitesse_naturelle = 1

    def __init__(self, monde, coords: tuple, vitesse, dimension):
        super().__init__(monde, coords, vitesse)
        self.image = ImageSorcier(dimension, 'picture/sorcier_fantome.png')
        self._cible_potentiel = self.monde.player[0]
        self.cible = None
        self.direction = 0  # en radian
        self.pierre_tombale = None
        self.radius = 50
        self.monde.ennemi.append(self)

    def print_image(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.width * 1/2, self.y - self.image.height * 50/125))
        self.image.refresh_cropped_png()

    def pierre_tombale_relation(self):
        # si il s'éloigne trop de la pierre tombale alors il revient
        if self.distance_avec((self.pierre_tombale.x, self.pierre_tombale.y)) > self.pierre_tombale.radius:
            self.direction = self.direction_radian_vers((self.pierre_tombale.x, self.pierre_tombale.y))
            self.cible = None
        # si quelqu'un s'approche trop près de la pierre tombale alors il le prend pour cible
        if self.pierre_tombale.distance_avec((self._cible_potentiel.x, self._cible_potentiel.y)) <= self.pierre_tombale.radius:
            if self._cible_potentiel.effet['possession']['is_controled'] is False:
                self.cible = self._cible_potentiel

    def direction_calcul(self):
        if self.pierre_tombale is not None:
            self.pierre_tombale_relation()
        # il va vers sa cible
        if self.cible is not None:
            self.direction = self.direction_radian_vers((self.cible.x, self.cible.y))

        self.direction += random.uniform(-math.pi/20, math.pi/20)

    def slow_power(self):
        for v in self.monde.vivant:
            if self.distance_avec((v.x, v.y)) < self.radius:
                v.slow_accumulation()

    def possession_power(self):
        if self.distance_avec((self.cible.x, self.cible.y)) < 3:
            if self.cible.effet['possession']['possesseur'] is None:
                self.cible.effet['possession']['possesseur'] = self
            self.cible.possession_accumulation()
        if self.cible.effet['possession']['possede'] > 300:
            self.cible.effet['possession']['is_controled'] = True
            self.cible = None

    def power(self):
        self.slow_power()
        if self.cible is not None:
            self.possession_power()

    def behavior(self, w):
        self.resolve_effect()
        self.direction_calcul()
        self.image.angle = normalize_angle(math.degrees(self.direction))
        self.move_in_direction(self.direction)
        self.print_image(w)
        self.pierre_tombale.print_image(w)
        self.power()
        # self.pierre_tombale.affiche_radius(w)
        # affiche_radius(w, (self.x, self.y), self.radius)


class ImageSorcier:
    def __init__(self, dimension: tuple, png_path):
        self.width, self.height = dimension
        self.png_path = png_path
        self.png = self.load_png()
        self.posture = 'face'
        self.cropped_png = self.load_cropped_png()
        self.angle = 0  # en degré

    @property
    def _w_png(self):
        return self.width * 250/55

    @property
    def _h_png(self):
        return self.height

    @property
    def _postures(self):
        return {
            'face': pygame.Rect(self._w_png / 25, 0, self._w_png * 55 / 250, self._h_png),
            'face-cote_droit': pygame.Rect(self._w_png * 70 / 250, 0, self._w_png * 55 / 250, self._h_png),
            'face-cote_gauche': pygame.Rect(self._w_png * 70 / 250, 0, self._w_png * 55 / 250, self._h_png),
            'cote_droit': pygame.Rect(self._w_png / 2, 0, self._w_png * 55 / 250, self._h_png),
            'cote_gauche': pygame.Rect(self._w_png / 2, 0, self._w_png * 55 / 250, self._h_png),
            'dos': pygame.Rect(self._w_png * 183 / 250, 0, self._w_png * 55 / 250, self._h_png)
        }

    def load_png(self):
        image_origin = pygame.image.load(self.png_path).convert_alpha()
        # Tools.changer_couleur_image_and_save_it(image_origin, r=-90, g=50, b=120)
        image = pygame.transform.scale(image_origin, (self._w_png, self._h_png))
        return image

    def reload_png(self):
        self.png = self.load_png()

    def detecte_posture(self):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        angle = - self.angle
        if -10 < angle <= 40:
            return 'cote_droit'
        elif 140 <= angle <= 180 or -180 <= angle < -170:
            return 'cote_gauche'
        elif 40 < angle < 140:
            return 'dos'
        elif -60 < angle <= -10:
            return 'face-cote_droit'
        elif -170 <= angle < -120:
            return 'face-cote_gauche'
        elif -120 <= angle <= -60:
            return 'face'
        else:
            return 'face'

    def load_cropped_png(self):
        cropped_rect = self._postures[self.posture]
        self.reload_png()
        cropped_png = self.png.subsurface(cropped_rect)
        if self.posture == 'cote_gauche' or self.posture == 'face-cote_gauche':
            cropped_png = pygame.transform.flip(cropped_png, True, False)
        return cropped_png

    def refresh_cropped_png(self):
        self.posture = self.detecte_posture()
        self.cropped_png = self.load_cropped_png()


class PierreTombale(Acteur):
    def __init__(self, monde, coords, dimension):
        super().__init__(monde, coords)
        self.image = ImageStone(dimension)
        self.radius = 200
        self.monde.pierre_tombale.append(self)

    def affiche_radius(self, w):
        pygame.draw.circle(w.window, (0, 0, 0), [self.x, self.y], self.radius, 1)

    def print_image(self, w):
        w.window.blit(self.image.png, (self.x - self.image.width * 1/2, self.y - self.image.height * 50/125))


class ImageStone:
    def __init__(self, dimension):
        self.width, self.height = dimension
        self.liste_png_path = ["picture/pierre/pierre.png",
                               "picture/pierre/pierre2.png",
                               "picture/pierre/pierre3.png"]
        self.png = self.load_png()

    def load_png(self):
        image_path = random.choice(self.liste_png_path)
        image_origin = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.width, self.height))
        flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return image

    def reload_png(self):
        self.png = self.load_png()
