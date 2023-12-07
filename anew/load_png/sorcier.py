import pygame


class ImageSorcier:
    W_DECAL = 1/2
    H_DECAL = 50/125

    def __init__(self, dimension: tuple, png_path):
        self.width, self.height = dimension
        self.png_path = png_path
        self.png = self.load_png()
        self.posture = 'face'
        self.cropped_png = self.load_cropped_png()
        self.angle = 0  # en degré

    @property
    def _w_png(self):
        return self.width * 250/55

    @property
    def _h_png(self):
        return self.height

    @property
    def _postures(self):
        return {
            'face': pygame.Rect(self._w_png / 25, 0, self._w_png * 55 / 250, self._h_png),
            'face-cote_droit': pygame.Rect(self._w_png * 70 / 250, 0, self._w_png * 55 / 250, self._h_png),
            'face-cote_gauche': pygame.Rect(self._w_png * 70 / 250, 0, self._w_png * 55 / 250, self._h_png),
            'cote_droit': pygame.Rect(self._w_png / 2, 0, self._w_png * 55 / 250, self._h_png),
            'cote_gauche': pygame.Rect(self._w_png / 2, 0, self._w_png * 55 / 250, self._h_png),
            'dos': pygame.Rect(self._w_png * 183 / 250, 0, self._w_png * 55 / 250, self._h_png)
        }

    def load_png(self):
        image_origin = pygame.image.load(self.png_path).convert_alpha()
        # Tools.changer_couleur_image_and_save_it(image_origin, r=-90, g=50, b=120)
        image = pygame.transform.scale(image_origin, (self._w_png, self._h_png))
        return image

    def reload_png(self):
        self.png = self.load_png()

    def detecte_posture(self):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        angle = - self.angle
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
        cropped_rect = self._postures[self.posture]
        self.reload_png()
        cropped_png = self.png.subsurface(cropped_rect)
        if self.posture == 'cote_gauche' or self.posture == 'face-cote_gauche':
            cropped_png = pygame.transform.flip(cropped_png, True, False)
        return cropped_png

    def refresh_cropped_png(self):
        self.posture = self.detecte_posture()
        self.cropped_png = self.load_cropped_png()
