import pygame

from anew.acteur import Acteur, Image


class Player(Acteur):
    def __init__(self, coords: tuple, dimension):
        super().__init__(coords)
        self.image = ImagePlayer(dimension)

    def comportement(self, w):
        w.window.blit(self.image.cropped_png, (self.x - self.image.l_perso * 1/2, self.y - self.image.h_perso * 50/125))


class ImagePlayerPostures(Image):
    def __init__(self, dimension: tuple):
        super().__init__('../picture/personnage/origin_redimension.png', (250, 125))
        self.l_perso, self.h_perso = dimension
        self.postures = None
        self.reload(dimension)

    def reload(self, dimension):
        self.l_perso, self.h_perso = dimension
        self.width, self.height = self.l_perso * 250 / 55, self.h_perso
        self.postures = {
            'face': pygame.Rect(self.width / 25, 0, self.width * 55 / 250, self.height),
            'face-cote_droit': pygame.Rect(self.width * 70 / 250, 0, self.width * 55 / 250, self.height),
            'face-cote_gauche': pygame.Rect(self.width * 70 / 250, 0, self.width * 55 / 250, self.height),
            'cote_droit': pygame.Rect(self.width / 2, 0, self.width * 55 / 250, self.height),
            'cote_gauche': pygame.Rect(self.width / 2, 0, self.width * 55 / 250, self.height),
            'dos': pygame.Rect(self.width * 183 / 250, 0, self.width * 55 / 250, self.height)
        }


class ImagePlayer(ImagePlayerPostures):
    def __init__(self, dimension: tuple):
        super().__init__(dimension)
        self.posture = 'face'
        self.cropped_png = self.load_cropped_png()

    @staticmethod
    def detecte_posture(angle_direction_mouvement):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        angle = - angle_direction_mouvement
        if -10 < angle <= 40:
            return 'cote_droit'
        elif 140 <= angle <= 180 or -180 <= angle < -170:
            return 'cote_gauche'
        elif 40 < angle < 140:
            return 'dos'
        elif -60 < angle <= -10:
            return 'face-cote_droit'
        elif -170 <= angle < -120:
            return 'face-cote_gauche'
        elif -120 <= angle <= -60:
            return 'face'
        else:
            return 'face'

    def load_cropped_png(self):
        cropped_rect = self.postures[self.posture]
        cropped_png = self.png.subsurface(cropped_rect)
        if self.posture == 'cote_gauche' or self.posture == 'face-cote_gauche':
            cropped_png = pygame.transform.flip(cropped_png, True, False)
        return cropped_png

    def reload_cropped_png(self, angle_direction_mouvement):
        posture = self.detecte_posture(angle_direction_mouvement)
        if self.posture != posture:
            self.posture = posture
            self.cropped_png = self.load_cropped_png()
