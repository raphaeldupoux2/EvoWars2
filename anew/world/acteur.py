import math
import pygame
from abc import ABC, abstractmethod


class Famille:
    def __init__(self, type_objet, vivant):
        self.type_objet: str = type_objet  # "creature" / "objet" / "lieu" / "abstrait" / "marqueur", "projectile"
        self.vivant: bool = vivant


class Acteur(ABC):
    def __init__(self, monde, type_objet, coords: tuple, zone=None, vitesse: float = 0, vivant=None):
        self.monde = monde
        self.famille = Famille(type_objet, vivant)
        self.x_abs, self.y_abs = coords
        self.zone = zone
        self.vitesse = vitesse
        self.vitesse_ref = vitesse

    @abstractmethod
    def behavior(self, w):
        pass

    @property
    def x_rel(self):
        return self.x_abs - self.monde.camera.x_abs

    @property
    def y_rel(self):
        return self.y_abs - self.monde.camera.y_abs

    @property
    def x(self):
        return self.x_rel

    @property
    def y(self):
        return self.y_rel

    def move_in_direction(self, direction):
        """
        direction doit être en radian
        """
        self.x_abs += math.cos(direction) * self.vitesse
        self.y_abs += math.sin(direction) * self.vitesse

    def move_to_position(self, position: tuple):
        if not (
                (position[0] - self.vitesse * 2 <= self.x <= position[0] + self.vitesse * 2) and
                (position[1] - self.vitesse * 2 <= self.y <= position[1] + self.vitesse * 2)
        ):
            self.move_in_direction(self.direction_radian_vers(position))
        else:
            return True

    def direction_radian_vers(self, position: tuple):
        return math.atan2(position[1] - self.y, position[0] - self.x)

    def direction_degree_vers(self, position: tuple):
        return self.direction_radian_vers(position) * 180 / math.pi

    def distance_avec(self, position):
        return math.sqrt((self.x - position[0]) ** 2 + (self.y - position[1]) ** 2)


def normalize_angle(angle):
    """
    Convertit un angle en un angle compris entre -180 et 180 degrés.

    Args:
        angle : L'angle en degrés.

    Returns:
        L'angle normalisé en degrés.
    """

    normalized_angle = angle % 360  # Calcul de l'angle modulo 360
    if normalized_angle > 180:  # Si l'angle est supérieur à 180 degrés
        normalized_angle -= 360  # Soustraire 360 degrés pour obtenir un angle négatif

    if normalized_angle < -180:  # Si l'angle est inférieur à -180 degrés
        normalized_angle += 360  # Ajouter 360 degrés pour obtenir un angle positif dans la plage -180 à 180 degrés

    return normalized_angle


def affiche_radius(w, position, rayon):
    pygame.draw.circle(w.window, (0, 0, 0), position, rayon, 1)

# def affiche_zone_png(self, position: dict):
#     pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.hauteur / 2, self.y - self.largeur / 2 - 50, 30, 100))
