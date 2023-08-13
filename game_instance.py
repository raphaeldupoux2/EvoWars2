import math

import pygame

from arbre import Arbre
from controle import Controle
from player.player import Player
from stone import Stone
from terrain_tennis import TerrainTennis
from window import Window
from projectile import Projectile


class GameInstance:
    couleur_sable = (255, 240, 190)
    FPS = 60  # Définition du nombre de FPS souhaité
    FRAME_DURATION = 1 / FPS  # Calcul de la durée en secondes entre chaque frame

    def __init__(self):
        super().__init__()
        self.w = Window()
        self.couleur_fond = GameInstance.couleur_sable
        self.terrain: list = [TerrainTennis(self.w, 300, 100)]
        self.arbre: list = [Arbre(self.w, 200, 500), Arbre(self.w, 80, 600), Arbre(self.w, 90, 400), Arbre(self.w, 800, 60)]
        self.stone: list = [Stone(self.w, 800, 600), Stone(self.w, 850, 555)]
        self.player = Player(self.w, self.arbre)
        self.projectile = Projectile(self.w, self.w.WINDOW_WIDTH / 2, self.w.WINDOW_HEIGHT / 2)
        self.controle = Controle()
        self.assombrir = [False, False, False]

    @property
    def curseur(self):
        return {'x': pygame.mouse.get_pos()[0],
                'y': pygame.mouse.get_pos()[1]}

    @staticmethod
    def angle_entre(position1: dict, position2: dict):
        return math.atan2(position2['y'] - position1['y'], position2['x'] - position1['x'])

    @staticmethod
    def distance_between(objet1: dict, objet2: dict):
        return math.sqrt((objet1['y'] - objet2['y']) ** 2 + (objet1['x'] - objet2['x']) ** 2)

    @staticmethod
    def normalize_angle(angle):
        """
        Convertit un angle en un angle compris entre -180 et 180 degrés.

        Arguments :
        angle -- L'angle en degrés.

        Retourne :
        L'angle normalisé en degrés.
        """

        normalized_angle = angle % 360  # Calcul de l'angle modulo 360
        if normalized_angle > 180:  # Si l'angle est supérieur à 180 degrés
            normalized_angle -= 360  # Soustraire 360 degrés pour obtenir un angle négatif
        return normalized_angle

    @staticmethod
    def point_dans_rectangle_incline(a, b, x, y, l, h, alpha):
        """
        Vérifie si un point donné (a, b) se trouve à l'intérieur d'un rectangle incliné.

        Args:
            a (float): Coordonnée x du point.
            b (float): Coordonnée y du point.
            x (float): Coordonnée x du centre du rectangle.
            y (float): Coordonnée y du centre du rectangle.
            l (float): Largeur du rectangle.
            h (float): Hauteur du rectangle.
            alpha (float): Angle d'inclinaison du rectangle en degrés.

        Returns:
            bool: True si le point (a, b) est à l'intérieur du rectangle incliné, False sinon.
        """
        # Déplacer le point pour que le centre du rectangle soit à l'origine du repère.
        a -= x
        b -= y

        # Appliquer une rotation inverse autour de l'origine par l'angle d'inclinaison négatif (-alpha).
        rad_alpha = math.radians(-alpha)
        rotated_a = a * math.cos(rad_alpha) - b * math.sin(rad_alpha)
        rotated_b = a * math.sin(rad_alpha) + b * math.cos(rad_alpha)

        # Vérifier si le point après rotation inverse est à l'intérieur d'un rectangle non incliné.
        return abs(rotated_a) <= l / 2 and abs(rotated_b) <= h / 2

    def move_to(self, position1: dict, position2: dict, vitesse):
        position1['x'] += math.cos(self.angle_entre(position1, position2)) * vitesse
        position1['y'] += math.sin(self.angle_entre(position1, position2)) * vitesse

    def blit_rotate(self, image, pos, origin_pos, angle):
        """
        :param image: pygame.Surface() ou Sprite
        :param pos: la position du coin supérieur gauche de la surface qui est le centre de la rotation
        :param origin_pos: permet de décaler le centre de rotation
        :param angle: angle de rotation
        :return: affiche image rotaté et met à jour les données de position de l'objet surface
        """
        # calculate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle))
        min_x, min_y = min([0, sin_a * h, cos_a * w, sin_a * h + cos_a * w]), max(
            [0, sin_a * w, -cos_a * h, sin_a * w - cos_a * h])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - origin_pos[0] + min_x - pivot_move[0], pos[1] - origin_pos[1] - min_y + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        self.w.window.blit(rotated_image, origin)

        # à changer en simplement : return rotated_image
        rotated_rect = rotated_image.get_rect()
        rotated_rect.x, rotated_rect.y = origin
        return rotated_rect

    def affiche_curseur(self):
        return pygame.draw.circle(self.w.window, (255, 0, 0), (self.curseur['x'], self.curseur['y']), 1)

    def luminosite_tournante(self, couleur_fond, vitesse_changement, assombrir):
        if couleur_fond[0] >= 255:
            assombrir[0] = True
        if couleur_fond[1] >= 255:
            assombrir[1] = True
        if couleur_fond[2] >= 255:
            assombrir[2] = True

        if couleur_fond[0] <= 0:
            assombrir[0] = False
        if couleur_fond[1] <= 0:
            assombrir[1] = False
        if couleur_fond[2] <= 0:
            assombrir[2] = False

        if assombrir[0] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (-vitesse_changement, 0, 0)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (vitesse_changement, 0, 0)))

        if assombrir[1] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, -vitesse_changement, 0)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, vitesse_changement, 0)))

        if assombrir[2] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, 0, -vitesse_changement)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, 0, vitesse_changement)))

        return couleur_fond, assombrir
