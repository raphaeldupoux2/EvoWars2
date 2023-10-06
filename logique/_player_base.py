import math
import pygame

from EvoWars2.sprite.personnage import AffichePlayer
from EvoWars2.utils import Utils
from EvoWars2.sprite.epee import ImageEpee
from EvoWars2.logique.maitrise import MaitriseEpee, MaitriseCharge
from EvoWars2.sprite.couronne import AfficheCouronne


class PlayerBase:
    def __init__(self, window, position, liste_obstacle, color=(50, 50, 90)):
        self.window = window.window
        self.x, self.y = position
        self.radius = 20
        self.color = color
        self.player = AffichePlayer(window)
        self.item = {"arme": {"épée": ImageEpee(window, position)},
                     "couronne": AfficheCouronne(window, position)}
        self.maitrise = {"épée": MaitriseEpee(window, self.item["arme"]["épée"].image),
                         "charge": MaitriseCharge()}
        self.vit_modif = 0
        self.solide = True
        self.liste_obstacle = liste_obstacle
        # self.projectile = [Projectile(500, 500)]

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
        self.x, self.y = Utils.move_to((self.x, self.y), self.direction, self.vel())
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

    def vel(self):
        vel = Utils.distance_between((self.x, self.y), Utils.curseur()) / 20
        if vel > 4:
            return 4 + self.vit_modif
        return vel

    def affiche_pied(self):
        return pygame.draw.circle(self.window, self.color, [self.x, self.y+50], self.radius, 0)

    def affiche_skin(self):
        return pygame.draw.circle(self.window, self.color, [self.x, self.y], self.radius, 0), \
            # pygame.draw.circle(self.window, (0, 30, 55), [self.x, self.y], 100, 1), \
        # pygame.draw.circle(self.window, (0, 30, 55), [self.x, self.y], 110, 1)

    # def ligne_vision(self, degree):
    #     angle = -Utils.angle_degree_entre(self.position, Utils.curseur()) * 180 / math.pi - degree
    #     Utils.blit_rotate(self.window, self.ligne, (self.x, self.y), (0, 0.5), angle)

    def angle_mort(self, window):
        # Calculer les angles des deux bords du cône
        angle_g = Utils.angle_radian_entre(self.position, Utils.curseur()) - math.pi / 3
        angle_d = Utils.angle_radian_entre(self.position, Utils.curseur()) + math.pi / 3

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

    @property
    def direction(self):
        if self.maitrise["charge"].anim_charge:
            return self.maitrise["charge"].direction_charge
        elif self.maitrise["épée"].etat_attaque == "coup":
            return self.maitrise["épée"].direction_attaque
        elif Utils.curseur() == (0, 0):
            return self.x, self.y
        else:
            return Utils.curseur()
