import math
import pygame


class Acteur:
    def __init__(self, monde, coords: tuple, vitesse: float = 0, vivant=False):
        self.monde = monde
        self.x, self.y = coords
        self.vitesse = vitesse
        self.vitesse_ref = vitesse
        self.effet = {'slow': 0,
                      'possession': {'possede': 0, 'possesseur': None, 'is_controled': False}}  # 0 coorespond au nombre d'occurence de l'effet affecter à l'acteur
        self.vivant = vivant

    def resolve_effect(self):
        # if self.effet['slow'] > 0:
        self.slow_effect()
        self.retablissement()
        # else:
        #     self.vitesse = self.vitesse_ref

    def slow_accumulation(self):
        self.effet['slow'] = min(self.effet['slow'] + 1, 500)

    def possession_accumulation(self):
        self.effet['possession']['possede'] = min(self.effet['possession']['possede'] + 1, 500)

    def slow_effect(self):
        self.vitesse = (3 / 4 * self.vitesse_ref*(1-self.effet['slow']) - self.effet['slow']*3/4) + self.vitesse_ref / 4

    def retablissement(self):
        self.effet['slow'] = max(self.effet['slow'] - 1 / 2, 0)
        self.effet['possession']['possede'] = max(self.effet['possession']['possede'] - 1 / 10, 0)
        if self.effet['possession']['possede'] <= 200:
            self.effet['possession']['is_controled'] = False

    def move_in_direction(self, direction):
        """
        direction doit être en radian
        """
        self.x += math.cos(direction) * max(self.vitesse, 0)
        self.y += math.sin(direction) * max(self.vitesse, 0)

    def move_to_position(self, position: tuple):
        if not (
                (position[0] - max(self.vitesse, 0) * 2 <= self.x <= position[0] + max(self.vitesse, 0) * 2) and
                (position[1] - max(self.vitesse, 0) * 2 <= self.y <= position[1] + max(self.vitesse, 0) * 2)
        ):
            self.move_in_direction(self.direction_radian_vers(position))

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
