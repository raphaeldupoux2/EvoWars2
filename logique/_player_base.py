import math
import pygame

from EvoWars2.sprite.personnage import AffichePlayer
from EvoWars2.utils import Utils
from EvoWars2.sprite.epee import ImageEpee
from EvoWars2.logique.maitrise import MaitriseEpee, MaitriseCharge
from EvoWars2.sprite.couronne import AfficheCouronne


class PlayerBase:
    def __init__(self, window, liste_obstacle, color=(50, 50, 90)):
        self.w = window
        self.position = {'x': self.w.width / 2, 'y': self.w.height *2/3}
        self.radius = 20
        self.color = color
        self.player = AffichePlayer(window)
        self.item = {"arme": {"épée": ImageEpee(window, self.position)},
                     "couronne": AfficheCouronne(window, self.position)}
        self.maitrise = {"épée": MaitriseEpee(window, self.item["arme"]["épée"].image),
                         "charge": MaitriseCharge()}
        self.vit_modif = 0
        self.solide = True
        self.liste_obstacle = liste_obstacle
        # self.projectile = [Projectile(500, 500)]

    def touche(self, objet):
        distance = math.sqrt((objet.x - self.position['x']) ** 2 + (objet.y - self.position['y']) ** 2)
        if distance <= self.radius + objet.tronc_radius:
            # self.color = (255, 0, 0)
            return True
        else:
            # self.color = (50, 50, 90)
            return False

    def bouge(self):
        old_x, old_y = self.position['x'], self.position['y']
        Utils.move_to(self.position, self.direction, self.vel())
        if not self.solide:
            return

        for obstacle in self.liste_obstacle:
            if self.touche(obstacle):
                new_x = self.position['x']
                self.position['x'] = old_x
                if self.touche(obstacle):
                    self.position['x'] = new_x
                    self.position['y'] = old_y

                if self.touche(obstacle):
                    self.position['x'] = old_x

    def vel(self):
        vel = Utils.distance_between(self.position, Utils.curseur()) / 20
        if vel > 4:
            return 4 + self.vit_modif
        return vel

    def affiche_skin(self):
        return pygame.draw.circle(self.w.window, self.color, [self.position['x'], self.position['y']], self.radius, 0), \
            # pygame.draw.circle(self.w.window, (0, 30, 55), [self.position['x'], self.position['y']], 100, 1), \
        # pygame.draw.circle(self.w.window, (0, 30, 55), [self.position['x'], self.position['y']], 110, 1)

    # def ligne_vision(self, degree):
    #     angle = -Utils.angle_degree_entre(self.position, Utils.curseur()) * 180 / math.pi - degree
    #     Utils.blit_rotate(self.w.window, self.ligne, (self.position['x'], self.position['y']), (0, 0.5), angle)

    def angle_mort(self, window):
        # Calculer les angles des deux bords du cône
        angle_g = Utils.angle_radian_entre(self.position, Utils.curseur()) - math.pi / 3
        angle_d = Utils.angle_radian_entre(self.position, Utils.curseur()) + math.pi / 3

        # Calculer les coordonnées des coins du rectangle gauche
        x1_g = self.position['x'] - 1000 * math.cos(angle_g)
        y1_g = self.position['y'] - 1000 * math.sin(angle_g)
        x2_g = self.position['x'] + 1000 * math.cos(angle_g)
        y2_g = self.position['y'] + 1000 * math.sin(angle_g)
        x3_g = x2_g + 1000 * math.sin(angle_g)
        y3_g = y2_g - 1000 * math.cos(angle_g)
        x4_g = x1_g + 1000 * math.sin(angle_g)
        y4_g = y1_g - 1000 * math.cos(angle_g)

        # Calculer les co0données des coins du rectangle droit
        x1_d = self.position['x'] - 1000 * math.cos(angle_d)
        y1_d = self.position['y'] - 1000 * math.sin(angle_d)
        x2_d = self.position['x'] + 1000 * math.cos(angle_d)
        y2_d = self.position['y'] + 1000 * math.sin(angle_d)
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
        elif Utils.curseur() == {'x': 0, 'y': 0}:
            return self.position
        else:
            return Utils.curseur()
