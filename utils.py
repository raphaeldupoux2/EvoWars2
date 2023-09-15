import math

import pygame


class Utils:

    @staticmethod
    def curseur():
        return {'x': pygame.mouse.get_pos()[0],
                'y': pygame.mouse.get_pos()[1]}

    @staticmethod
    def angle_radian_entre(position1: dict, position2: dict):
        """
        :return: angle en radian
        """
        return math.atan2(position2['y'] - position1['y'], position2['x'] - position1['x'])

    @staticmethod
    def angle_degree_entre(position1: dict, position2: dict):
        """
        :return: angle en radian
        """
        return math.atan2(position2['y'] - position1['y'], position2['x'] - position1['x']) * 180 / math.pi

    @staticmethod
    def distance_between(objet1: dict, objet2: dict):
        return math.sqrt((objet1['y'] - objet2['y']) ** 2 + (objet1['x'] - objet2['x']) ** 2)

    @staticmethod
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

    @classmethod
    def move_to(cls, position1: dict, position2: dict, vitesse):
        if position1 != position2:
            position1['x'] += math.cos(cls.angle_entre(position1, position2)) * vitesse
            position1['y'] += math.sin(cls.angle_entre(position1, position2)) * vitesse

    @staticmethod
    def blit_rotate(window, image, pos, origin_pos, angle):
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
        window.blit(rotated_image, origin)

        # à changer en simplement : return rotated_image
        rotated_rect = rotated_image.get_rect()
        rotated_rect.x, rotated_rect.y = origin
        return rotated_rect

    @classmethod
    def affiche_curseur(cls, window):
        return pygame.draw.circle(window, (255, 0, 0), (cls.curseur()['x'], cls.curseur()['y']), 1)

    @staticmethod
    def luminosite_tournante(couleur_fond, vitesse_changement, assombrir):
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
