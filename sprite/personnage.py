import pygame

from EvoWars2.utils import Utils
from EvoWars2.pygamesetup import pygame_params


class AffichePlayer:

    largeur, hauteur = 250, 125
    image_path_origin = "picture/personnage/origin_redimension.png"
    image_path = "picture/personnage/personnage.png"
    postures = {
        "face": pygame.Rect(largeur / 25, 0, largeur * 55 / 250, hauteur),
        "face-cote_droit": pygame.Rect(largeur * 70 / 250, 0, largeur * 55 / 250, hauteur),
        "face-cote_gauche": pygame.Rect(largeur * 70 / 250, 0, largeur * 55 / 250, hauteur),
        "cote_droit": pygame.Rect(largeur / 2, 0, largeur * 55 / 250, hauteur),
        "cote_gauche": pygame.Rect(largeur / 2, 0, largeur * 55 / 250, hauteur),
        "dos": pygame.Rect(largeur * 183 / 250, 0, largeur * 55 / 250, hauteur)
    }
    l_perso, h_perso = 55, 125

    def __init__(self, posture='face'):
        self.posture = posture
        self.image = self._load_image()

    @staticmethod
    def detecte_posture(angle_direction_mouvement):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        angle = - angle_direction_mouvement
        if -10 < angle <= 40:
            return "cote_droit"
        elif 140 <= angle <= 180 or -180 <= angle < -170:
            return "cote_gauche"
        elif 40 < angle < 140:
            return "dos"
        elif -60 < angle <= -10:
            return "face-cote_droit"
        elif -170 <= angle < -120:
            return "face-cote_gauche"
        elif -120 <= angle <= -60:
            return "face"
        else:
            return "face"

    def _load_image(self):
        image_origin = pygame.image.load(self.image_path_origin).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        cropped_rect = self.postures[self.posture]
        cropped_image = image.subsurface(cropped_rect)
        if self.posture == "cote_gauche" or self.posture == "face-cote_gauche":
            cropped_image = pygame.transform.flip(cropped_image, True, False)
        return cropped_image

    def load_image(self, angle_direction_mouvement):
        posture = self.detecte_posture(angle_direction_mouvement)
        if self.posture != posture:
            self.posture = posture
            self.image = self._load_image()

    def affiche_png(self, position: dict):
        pygame_params.window.blit(self.image, (position[0] - self.l_perso/2, position[1] - self.h_perso*50/125))

    def affiche_zone_png(self, position: dict):
        pygame.draw.rect(pygame_params.window, (0, 150, 0), (position[0] - self.l_perso/2, position[1] - 50, self.l_perso, self.h_perso))

    def affiche_all(self, position: dict):
        self.affiche_zone_png(position)
        self.affiche_png(position)

    def comportement(self, position, angle_direction_mouvement):
        self.load_image(angle_direction_mouvement)
        self.affiche_png(position)
