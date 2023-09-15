import pygame

from utils import Utils


class MaitriseEpee:
    def __init__(self, window, image_arme):
        self.w = window
        self.image_arme = image_arme
        self.arme_degainee = True
        self.coup = ""
        self.etat_attaque = "repos"
        self.arme_degree = 0
        self.direction_attaque = {'x': 0, 'y': 0}
        self.rotated_rect = None

    def normalize_arme_degree(self):
        if Utils.normalize_angle(self.arme_degree) != self.arme_degree:
            self.arme_degree = Utils.normalize_angle(self.arme_degree)

    def arme_degree_relatif(self, position, curseur):
        """
        :param position:
        :param curseur:
        :return: angle de l'arme + angle de la direction du curseur
        """
        return -Utils.angle_degree_entre(position, curseur) + self.arme_degree

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
            if self.arme_degree >= 120:
                self.etat_attaque = "repos"

        elif self.coup == "revert":
            self.arme_degree -= 12
            if self.arme_degree <= -120:
                self.etat_attaque = "repos"

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

    def bouton_degainage(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if self.arme_degainee:
                    self.arme_degainee = False
                elif self.arme_degainee is False:
                    self.arme_degainee = True

    # Repos
    def repositionnement(self):
        if 120 > self.arme_degree > 0:
            self.arme_degree += 3
        elif -120 < self.arme_degree <= 0:
            self.arme_degree -= 3
        elif -180 < self.arme_degree < -125:
            self.arme_degree += 3
        elif 180 >= self.arme_degree > 125:
            self.arme_degree -= 3
        elif 125 >= self.arme_degree >= 120:
            self.arme_degree = 120
        elif -125 <= self.arme_degree <= -120:
            self.arme_degree = -120

    def affiche_arme_x_y_inverse(self, position):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (-5, 0), self.arme_degree + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (35, 0), self.arme_degree + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (-15, 0), self.arme_degree + 90)
        else:
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (-5, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (35, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(self.w.window, self.image_arme, (position['x'], position['y']), (-5, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)


class MaitriseCharge:
    def __init__(self):
        self.direction_charge = {'x': 0, 'y': 0}
        self.anim_charge = False

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
