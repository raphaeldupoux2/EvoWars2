import pygame

from utils import Utils

from EvoWars2.pygamesetup import pygame_params


class MaitriseEpee:
    def __init__(self, image_arme):
        self.image_arme = image_arme
        self.arme_degainee = True
        self.coup = ""
        self.vit_coup = 12
        self.etat_attaque = "repos"
        self.vit_repos = 1
        self.arme_degree = 0
        self.direction_attaque = (0, 0)
        self.rotated_rect = None
        self.affiche_arme((0, 0))

    def normalize_arme_degree(self):
        if Utils.normalize_angle(self.arme_degree) != self.arme_degree:
            self.arme_degree = Utils.normalize_angle(self.arme_degree)

    def arme_degree_relatif(self, position: tuple, curseur: tuple):
        """
        :param position: position du joueur
        :param curseur: position du curseur
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
            self.arme_degree += self.vit_coup
        if self.coup == "revert":
            self.arme_degree -= self.vit_coup

    # Coup
    def bouton_coup_epee(self, event):
        if self.arme_degree == -120 or self.arme_degree == 120:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.etat_attaque = "coup"
                self.direction_attaque = Utils.curseur()

    def coup_epee(self):
        if self.coup == "coup droit":
            self.arme_degree += self.vit_coup
            if self.arme_degree >= 120:
                self.etat_attaque = "repos"

        elif self.coup == "revert":
            self.arme_degree -= self.vit_coup
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
            self.arme_degree += self.vit_repos
        elif -120 < self.arme_degree <= 0:
            self.arme_degree -= self.vit_repos
        elif -180 < self.arme_degree < -125:
            self.arme_degree += self.vit_repos
        elif 180 >= self.arme_degree > 125:
            self.arme_degree -= self.vit_repos
        elif 125 >= self.arme_degree >= 120:
            self.arme_degree = 120
        elif -125 <= self.arme_degree <= -120:
            self.arme_degree = -120

    def affiche_arme(self, position: tuple):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (-5, 0), self.arme_degree + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (35, 0), self.arme_degree + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (15, 0), self.arme_degree + 90)
        else:
            if self.coup == "coup droit":
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (-5, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)
            elif self.coup == "revert":
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (35, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)
            else:
                self.rotated_rect = Utils.blit_rotate(pygame_params.window, self.image_arme, (position[0], position[1]), (15, 0), self.arme_degree_relatif(position, self.direction_attaque) + 90)

    def bouton(self, event):
        if self.etat_attaque == "repos":
            self.bouton_change_hand(event)
            self.bouton_coup_epee(event)

        self.bouton_fanatique(event)
        self.bouton_degainage(event)

    def comportement(self, position):
        self.normalize_arme_degree()
        if self.etat_attaque == "repos":
            self.repositionnement()
            self.direction_attaque = Utils.curseur()
            self.change_hand()

        elif self.etat_attaque == "coup":
            self.coup_epee()

        elif self.etat_attaque == "fanatique":
            self.fanatique()

        if self.arme_degainee:
            self.affiche_arme(position)


class MaitriseCharge:
    def __init__(self):
        self.direction_charge = (0, 0)
        self.anim_charge = False

    def bouton_charge(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.anim_charge = True
                self.direction_charge = Utils.curseur()
                # self.vit_modif += 8

    def charge(self, position):
        if abs(position[0] - self.direction_charge[0]) < 20 and abs(position[1] - self.direction_charge[1]) < 20:
            self.anim_charge = False
            # self.vit_modif -= 8

    def bouton(self, event):
        if self.anim_charge is False:
            self.bouton_charge(event)

    def comportement(self, position):
        if self.anim_charge:
            self.charge(position)
