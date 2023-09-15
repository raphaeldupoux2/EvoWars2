import pygame


class AffichePlayer:

    largeur, longueur = 250, 125
    image_path_origin = "picture/personnage/origin.png"
    image_path = "picture/personnage/personnage.png"
    postures = {
        "face": pygame.Rect(largeur / 25, 0, largeur * 55 / 250, longueur),
        "face-cote_droit": pygame.Rect(largeur * 70 / 250, 0, largeur * 55 / 250, longueur),
        "cote_droit": pygame.Rect(largeur / 2, 0, largeur * 55 / 250, longueur),
        "dos": pygame.Rect(largeur * 183 / 250, 0, largeur * 55 / 250, longueur)
    }

    def __init__(self, window, posture='face'):
        self.w = window
        self.posture = posture
        self.image = self._load_image()

    @staticmethod
    def detecte_posture(angle_direction_mouvement):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        if -10 < angle_direction_mouvement <= 20:
            return "cote_droit"
        elif 160 <= angle_direction_mouvement <= 180 or -180 <= angle_direction_mouvement < -170:
            return "cote_gauche"
        elif 20 < angle_direction_mouvement < 160:
            return "dos"
        elif -50 < angle_direction_mouvement <= -10:
            return "face-cote_droit"
        elif -170 <= angle_direction_mouvement < -130:
            return "face-cote_gauche"
        elif -130 <= angle_direction_mouvement <= -50:
            return "face"
        else:
            return "face"

    def _load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.longueur))
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
        self.w.window.blit(self.image, (position['x'] - 30, position['y'] - 50))

    def affiche_zone_png(self, position: dict):
        pygame.draw.rect(self.w.window, (0, 150, 0), (position['x'] - 30, position['y'] - 50, 55, 125))

    def affiche_all(self, position: dict):
        self.affiche_zone_png(position)
        self.affiche_png(position)

    def comportement(self, position, angle_direction_mouvement):
        self.load_image(angle_direction_mouvement)
        self.affiche_png(position)
