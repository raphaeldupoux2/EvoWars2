import math
import pygame

from utils import Utils


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
        self.position = {'x': self.w.WINDOW_WIDTH / 2, 'y': self.w.WINDOW_WIDTH / 2}
        # self.x = self.w.WINDOW_WIDTH / 2
        # self.y = self.w.WINDOW_WIDTH / 2
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

    def arme_degree_relatif(self, curseur):
        """
        :param curseur:
        :return: angle de l'arme + angle de la direction du curseur
        """
        return -Utils.angle_entre(self.position, curseur) * 180 / math.pi + self.arme_degree

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
               pygame.draw.circle(self.w.window, (0, 30, 55), [self.position['x'], self.position['y']], 100, 1), \
               pygame.draw.circle(self.w.window, (0, 30, 55), [self.position['x'], self.position['y']], 110, 1)

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
                self.direction_attaque = Utils.curseur()

    def coup_epee(self):
        if self.coup == "coup droit":
            self.arme_degree += 12
            if Utils.normalize_angle(self.arme_degree) >= 120:
                self.etat_attaque = "repos"

        elif self.coup == "revert":
            self.arme_degree -= 12
            if Utils.normalize_angle(self.arme_degree) <= -120:
                self.etat_attaque = "repos"

    def bouton_charge(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.anim_charge = True
                self.direction_charge = Utils.curseur()
                # self.vit_modif += 8

    def charge(self):
        if abs(self.position['x'] - self.direction_charge['x']) < 20 and abs(
                self.position['y'] - self.direction_charge['y'] < 20):
            self.anim_charge = False
            # self.vit_modif -= 8

    def ligne_vision(self, degree):
        angle = -Utils.angle_entre(self.position, Utils.curseur()) * 180 / math.pi - degree
        Utils.blit_rotate(self.w.window, self.ligne, (self.position['x'], self.position['y']), (0, 0.5), angle)

    def angle_mort(self, window):
        # Calculer les angles des deux bords du cône
        angle_g = Utils.angle_entre(self.position, Utils.curseur()) - math.pi / 3
        angle_d = Utils.angle_entre(self.position, Utils.curseur()) + math.pi / 3

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

    # Repos
    def repositionnement(self):
        if 120 > Utils.normalize_angle(self.arme_degree) > 0:
            self.arme_degree += 3
        elif -120 < Utils.normalize_angle(self.arme_degree) <= 0:
            self.arme_degree -= 3
        elif -180 < Utils.normalize_angle(self.arme_degree) < -125:
            self.arme_degree += 3
        elif 180 >= Utils.normalize_angle(self.arme_degree) > 125:
            self.arme_degree -= 3
        elif 125 >= Utils.normalize_angle(self.arme_degree) >= 120:
            self.arme_degree = 120
        elif -125 <= Utils.normalize_angle(self.arme_degree) <= -120:
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
            return Utils.curseur()

    def affiche_arme(self):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, 20), self.arme_degree)
            elif self.coup == "revert":
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, -10), self.arme_degree)
            else:
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, 5), self.arme_degree)
        else:
            if self.coup == "coup droit":
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, 20), self.arme_degree_relatif(self.direction))
            elif self.coup == "revert":
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, -10), self.arme_degree_relatif(self.direction))
            else:
                Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (0, 5), self.arme_degree_relatif(self.direction))

    def affiche_arme_x_y_inverse(self):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (-5, 0), self.arme_degree + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (35, 0), self.arme_degree + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (-15, 0), self.arme_degree + 90)
        else:
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (-5, 0),
                                                     self.arme_degree_relatif(self.direction) + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (35, 0),
                                                     self.arme_degree_relatif(self.direction) + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.arme, (self.position['x'], self.position['y']), (-5, 0), self.arme_degree_relatif(self.direction) + 90)


    def bouton_degainage(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if self.arme_degainee:
                    self.arme_degainee = False
                elif self.arme_degainee is False:
                    self.arme_degainee = True
