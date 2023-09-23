import pygame


class Image:
    def __init__(self, window, position: tuple, pos_decal: tuple, dimension: tuple, path: str):
        """
        Pour les png qui n'ont pas besoin d'être rogné
        :param window:
        :param position: (x, y)
        :param pos_decal: (x_decal, y_decal)
        :param dimension: (width, height)
        :param path: "picture/arbre/arbre.png"
        """
        self.w = window
        self.x, self.y = position
        self.x_decal, self.y_decal = pos_decal
        self.width, self.height = dimension
        self.image_path = path
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.width, self.height))
        return image

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.x_decal, self.y - self.y_decal))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.x_decal, self.y - self.y_decal, self.width, self.height))

    def affiche_all(self):
        self.affiche_zone_png()
        self.affiche_png()


class ImageMultiDirection(Image):
    def __init__(self, window, position: tuple, pos_decal: tuple, dimension: tuple, path: str, angle_direction):
        """
        :param window:
        :param position: (x, y)
        :param pos_decal: (x_decal, y_decal)
        :param dimension: (width, height)
        :param path: "picture/arbre/arbre.png"
        :param angle_direction: en degré
        """
        super().__init__(window, position, pos_decal, dimension, path)
        self.angle_direction = angle_direction
        self.posture = "face"

    @staticmethod
    def detecte_posture_6_angle(angle_direction):
        """
        Args:
            angle_direction_mouvement en degré.
        """
        angle = - angle_direction
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

    def comportement(self, angle_direction_mouvement):
        self.load_image(angle_direction_mouvement)
        self.affiche_png()
