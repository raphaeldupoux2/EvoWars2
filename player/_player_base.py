import math
import pygame


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


class Outil:
    def __init__(self):
        self.ligne = pygame.Surface([1000, 1])
        self.ligne.set_colorkey((0, 0, 0))
        self.ligne.fill((80, 80, 150))

        self.epee = pygame.Surface([30, 100])
        self.epee.set_colorkey((0, 0, 0))
        self.epee.fill((186, 196, 200))

        self.epee_image_path = "picture/epee.png"
        self.epee_image_origin = pygame.image.load(self.epee_image_path).convert_alpha()
        self.epee_largeur, self.epee_longueur = 30, 100
        self.epee = pygame.transform.scale(self.epee_image_origin, (self.epee_largeur, self.epee_longueur))

        self.gun = pygame.Surface([80, 10])
        self.gun.set_colorkey((0, 0, 0))
        self.gun.fill((47, 79, 79))


class PlayerBase:
    def __init__(self, window, liste_obstacle, color=(50, 50, 90), is_in_control=True):
        self.is_in_control = is_in_control
        self.w = window
        self.x = self.w.WINDOW_WIDTH / 2
        self.y = self.w.WINDOW_HEIGHT / 2
        self.outil = Outil()
        self.radius = 20
        self.color = color
        self.ligne = self.outil.ligne
        self.arme = self.outil.epee
        self.arme_degree = 0
        self.arme_degainee = True
        self.gun = self.outil.gun
        self.gun_degree = 0
        self.gun_degainee = True
        self.coup = ""
        self.anim_charge = False
        self.etat_attaque = "repos"
        self.direction_charge = {'x': 0, 'y': 0}
        self.direction_attaque = {'x': 0, 'y': 0}
        self.vit_modif = 0
        self.solide = True
        self.liste_obstacle = liste_obstacle
        # self.projectile = [Projectile(500, 500)]

        self.rotated_rect = None

    @property
    def curseur(self):
        if self.is_in_control is False:
            return {'x': self.x,
                    'y': self.y}
        return {'x': pygame.mouse.get_pos()[0],
                'y': pygame.mouse.get_pos()[1]}

    def angle_vers(self, cible: dict):
        return math.atan2(cible['y'] - self.y, cible['x'] - self.x)

    def arme_degree_r(self, curseur):
        """
        :param curseur:
        :return: angle de l'arme + angle de la direction du curseur
        """
        return -self.angle_vers(curseur) * 180 / math.pi + self.arme_degree

    def move_to(self, cible: dict):
        self.x += math.cos(self.angle_vers(cible)) * self.vel(cible)
        self.y += math.sin(self.angle_vers(cible)) * self.vel(cible)

    def touche(self, objet):
        distance = math.sqrt((objet.x - self.x) ** 2 + (objet.y - self.y) ** 2)
        if distance <= self.radius + objet.tronc_radius:
            # self.color = (255, 0, 0)
            return True
        else:
            # self.color = (50, 50, 90)
            return False

    def bouge(self):
        old_x, old_y = self.x, self.y
        self.move_to(self.direction)
        if not self.solide:
            return

        for obstacle in self.liste_obstacle:
            if self.touche(obstacle):
                new_x = self.x
                self.x = old_x
                if self.touche(obstacle):
                    self.x = new_x
                    self.y = old_y

                if self.touche(obstacle):
                    self.x = old_x

    def inside_circle(self, objet: list):
        if (objet[0] - self.x) ** 2 + (objet[1] - self.y) ** 2 <= 20 ** 2:
            return True
        return False

    def distance_to(self, objet: dict):
        return math.sqrt((objet['y'] - self.y) ** 2 + (objet['x'] - self.x) ** 2)

    def vel(self, curseur):
        vel = self.distance_to(curseur) / 20
        if vel > 2:
            return 2 + self.vit_modif
        return vel

    def affiche_skin(self):
        return pygame.draw.circle(self.w.window, self.color, [self.x, self.y], self.radius, 0), \
               pygame.draw.circle(self.w.window, (0, 30, 55), [self.x, self.y], 100, 1), \
               pygame.draw.circle(self.w.window, (0, 30, 55), [self.x, self.y], 110, 1)

    def affiche_curseur(self):
        return pygame.draw.circle(self.w.window, (255, 0, 0), (self.curseur['x'], self.curseur['y']), 1)

    # def rotate(self):
    #     rotated_surface, origin = blit_rotate(rotated_surface, (x_rectangle, y_rectangle), (200, 0), -angle_inclinaison)
    #
    #     rotated_rect = rotated_surface.get_rect()
    #     rotated_rect.x, rotated_rect.y = origin
    #
    #     screen.blit(rotated_surface, origin)
    #
    #     if point_dans_rectangle_incline(curseur()['x'], curseur()['y'],
    #                                     rotated_rect.centerx, rotated_rect.centery,
    #                                     largeur_rectangle, hauteur_rectangle,
    #                                     angle_inclinaison):
    #         pygame.draw.rect(screen, BLUE, rotated_rect, 2)

    def blit_rotate(self, surf, image, pos, origin_pos, angle):
        """
        :param surf: pygame.display(), c'est la fenêtre
        :param image: pygame.Surface(), une surface
        :param pos: la position du coin supérieur gauche de la surface qui est le centre de la rotation
        :param origin_pos: permet de décaler le centre de rotation
        :param angle: angle de rotation
        :return: affiche la surface et met à jour les données de position de l'objet surface
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
        self.rotated_rect = rotated_image.get_rect()
        self.rotated_rect.x, self.rotated_rect.y = origin
        surf.blit(rotated_image, origin)

        # return rotated_image, origin

    # def rotate(self, surf, image, pos, origin_pos, angle):
    #     rotated_image, origin = self.rotate(image, pos, origin_pos, angle)
    #     self.rotated_rect = rotated_image.get_rect()
    #     self.rotated_rect.x, self.rotated_rect.y = origin
    #     surf.blit(rotated_image, origin)

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

    # Fanatique
    def bouton_fanatique(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_focused() and pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.etat_attaque != "fanatique":
                    self.etat_attaque = "fanatique"
                else:
                    self.etat_attaque = "repos"

    def fanatique(self):
        if self.coup == "coup droit":
            self.arme_degree += 12
        if self.coup == "revert":
            self.arme_degree -= 12

    # Coup
    def bouton_coup_epee(self, event):
        if self.arme_degree == -120 or self.arme_degree == 120:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.etat_attaque = "coup"
                self.direction_attaque = self.curseur

    def coup_epee(self):
        if self.coup == "coup droit":
            self.arme_degree += 12
            if normalize_angle(self.arme_degree) >= 120:
                self.etat_attaque = "repos"

        elif self.coup == "revert":
            self.arme_degree -= 12
            if normalize_angle(self.arme_degree) <= -120:
                self.etat_attaque = "repos"

    def bouton_charge(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.anim_charge = True
                self.direction_charge = self.curseur
                # self.vit_modif += 8

    def charge(self):
        if abs(self.x - self.direction_charge['x']) < 20 and abs(
                self.y - self.direction_charge['y'] < 20):
            self.anim_charge = False
            # self.vit_modif -= 8

    def ligne_vision(self, degree):
        angle = -self.angle_vers(self.curseur) * 180 / math.pi - degree
        self.blit_rotate(self.w.window, self.ligne, (self.x, self.y), (0, 0.5), angle)

    def angle_mort(self, window, curseur):
        # Calculer les angles des deux bords du cône
        angle_g = self.angle_vers(curseur) - math.pi / 3
        angle_d = self.angle_vers(curseur) + math.pi / 3

        # Calculer les coordonnées des coins du rectangle gauche
        x1_g = self.x - 1000 * math.cos(angle_g)
        y1_g = self.y - 1000 * math.sin(angle_g)
        x2_g = self.x + 1000 * math.cos(angle_g)
        y2_g = self.y + 1000 * math.sin(angle_g)
        x3_g = x2_g + 1000 * math.sin(angle_g)
        y3_g = y2_g - 1000 * math.cos(angle_g)
        x4_g = x1_g + 1000 * math.sin(angle_g)
        y4_g = y1_g - 1000 * math.cos(angle_g)

        # Calculer les co0données des coins du rectangle droit
        x1_d = self.x - 1000 * math.cos(angle_d)
        y1_d = self.y - 1000 * math.sin(angle_d)
        x2_d = self.x + 1000 * math.cos(angle_d)
        y2_d = self.y + 1000 * math.sin(angle_d)
        x3_d = x2_d - 1000 * math.sin(angle_d)
        y3_d = y2_d + 1000 * math.cos(angle_d)
        x4_d = x1_d - 1000 * math.sin(angle_d)
        y4_d = y1_d + 1000 * math.cos(angle_d)

        # Dessiner les rectangles
        pygame.draw.polygon(window, (0, 0, 0), [(x1_g, y1_g), (x2_g, y2_g), (x3_g, y3_g), (x4_g, y4_g)])
        pygame.draw.polygon(window, (0, 0, 0), [(x1_d, y1_d), (x2_d, y2_d), (x3_d, y3_d), (x4_d, y4_d)])

    # Repos
    def repositionnement(self):
        if 120 > normalize_angle(self.arme_degree) > 0:
            self.arme_degree += 3
        elif -120 < normalize_angle(self.arme_degree) <= 0:
            self.arme_degree -= 3
        elif -180 < normalize_angle(self.arme_degree) < -125:
            self.arme_degree += 3
        elif 180 >= normalize_angle(self.arme_degree) > 125:
            self.arme_degree -= 3
        elif 125 >= normalize_angle(self.arme_degree) >= 120:
            self.arme_degree = 120
        elif -125 <= normalize_angle(self.arme_degree) <= -120:
            self.arme_degree = -120

    def change_hand(self):
        if self.arme_degree == -120:
            self.coup = "coup droit"
        elif self.arme_degree == 120:
            self.coup = "revert"

    def bouton_change_hand(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.arme_degree == -120:
                    self.arme_degree = 120
            if event.key == pygame.K_e:
                if self.arme_degree == 120:
                    self.arme_degree = -120

    @property
    def direction(self):
        if self.anim_charge:
            return self.direction_charge
        elif self.etat_attaque == "coup":
            return self.direction_attaque
        else:
            return self.curseur

    def affiche_arme(self):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, 20), self.arme_degree)
            elif self.coup == "revert":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, -10), self.arme_degree)
            else:
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, 5), self.arme_degree)
        else:
            if self.coup == "coup droit":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, 20), self.arme_degree_r(self.direction))
            elif self.coup == "revert":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, -10), self.arme_degree_r(self.direction))
            else:
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (0, 5), self.arme_degree_r(self.direction))

    def affiche_arme_x_y_inverse(self):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (-5, 0), self.arme_degree + 90)
            elif self.coup == "revert":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (35, 0), self.arme_degree + 90)
            else:
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (-15, 0), self.arme_degree + 90)
        else:
            if self.coup == "coup droit":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (-5, 0),
                                 self.arme_degree_r(self.direction) + 90)
            elif self.coup == "revert":
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (35, 0),
                                 self.arme_degree_r(self.direction) + 90)
            else:
                self.blit_rotate(self.w.window, self.arme, (self.x, self.y), (-5, 0), self.arme_degree_r(self.direction) + 90)

    # def detect_ball(self):
    #     arme
    #     if arme.collidepoint(self.projectile[0].x, self.projectile[0].y)

    def detection_collision_arme(self):
        # print(self.check_collision(self.arme.get_rect(), self.projectile[0]), [self.x, self.y], end=' ')
        pass

    def check_collision(self, rect, circle):
        rect_center_x = rect.x + rect.width / 2
        rect_center_y = rect.y + rect.height / 2

        circle_distance_x = abs(circle.x - rect_center_x)
        circle_distance_y = abs(circle.y - rect_center_y)
        print(circle_distance_x, circle_distance_y, rect.width / 2 + circle.radius)

        if circle_distance_x > (rect.width / 2 + circle.radius):
            return False
        if circle_distance_y > (rect.height / 2 + circle.radius):
            return False

        if circle_distance_x <= (rect.width / 2):
            return True
        if circle_distance_y <= (rect.height / 2):
            return True

        corner_distance_sq = (circle_distance_x - rect.width / 2) ** 2 + (circle_distance_y - rect.height / 2) ** 2

        return corner_distance_sq <= (circle.radius ** 2)

    def bouton_degainage(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if self.arme_degainee:
                    self.arme_degainee = False
                elif self.arme_degainee is False:
                    self.arme_degainee = True
