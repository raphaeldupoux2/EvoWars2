from player._player_base import PlayerBase
import pygame

from utils import Utils


class Player:
    def __init__(self, window, liste_obstacle):
        self.physique = [PlayerPhysique(window, liste_obstacle)]
        self.spirit = []  # [PlayerSpirit(window)]


class PlayerPhysique(PlayerBase):
    def __init__(self, window, liste_obstacle):
        super().__init__(window, liste_obstacle, color=(50, 50, 90), is_in_control=True)
        self.image_path = "picture/crown.png"
        self.image_origin = pygame.image.load(self.image_path).convert_alpha()
        self.largeur, self.longueur = 50, 50
        self.image = pygame.transform.scale(self.image_origin, (self.largeur, self.longueur))

    def bouton_change_in_controle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.is_in_control = not self.is_in_control

    def bouton(self, event):
        if self.is_in_control:
            if self.etat_attaque == "repos":
                self.bouton_change_hand(event)
                self.bouton_coup_epee(event)

            if self.anim_charge is False:
                self.bouton_charge(event)

            self.bouton_fanatique(event)
            self.bouton_degainage(event)
        self.bouton_change_in_controle(event)

    def comportement(self):
        if self.etat_attaque == "repos":
            self.repositionnement()
            self.change_hand()

        elif self.etat_attaque == "coup":
            self.coup_epee()

        elif self.etat_attaque == "fanatique":
            self.fanatique()

        if self.anim_charge:
            self.charge()

        # if self.is_in_control:
        #     self.angle_mort(self.w.window)
        # self.ligne_vision(60)
        # self.ligne_vision(-60)

        if self.arme_degainee:
            self.affiche_arme_x_y_inverse()

        self.bouge()
        self.affiche_skin()
        Utils.affiche_curseur(self.w.window)
        # self.detection_collision_arme()
        self.w.window.blit(self.image, (self.position['x'] - self.longueur/2, self.position['y'] - self.largeur/2 - 20))


class PlayerSpirit(PlayerBase):
    def __init__(self, window):
        super().__init__(window, liste_obstacle=[], color=(255, 255, 255), is_in_control=True)

    def bouton(self, event):
        if self.is_in_control:
            if self.etat_attaque == "repos":
                self.bouton_change_hand(event)
                self.bouton_coup_epee(event)

            if self.anim_charge is False:
                self.bouton_charge(event)

            self.bouton_fanatique(event)
            self.bouton_degainage(event)

    def comportement(self):
        if self.etat_attaque == "repos":
            self.repositionnement()
            self.change_hand()

        elif self.etat_attaque == "coup":
            self.coup_epee()

        elif self.etat_attaque == "fanatique":
            self.fanatique()

        if self.anim_charge:
            self.charge()

        # if self.is_in_control:
        #     self.angle_mort(self.w.window)
        self.ligne_vision(60)
        self.ligne_vision(-60)

        if self.arme_degainee:
            self.affiche_arme()

        self.bouge()
        self.affiche_skin()
        Utils.affiche_curseur(self.w.window)
        # self.detection_collision_arme()
