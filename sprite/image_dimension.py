import pygame


class Image:
    def __init__(self, window, position: tuple, dimension: tuple, pos_decal: tuple, path: str):
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
        self.w.window.blit(self.image, (self.x - self.width * self.x_decal, self.y - self.height * self.y_decal))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.x_decal, self.y - self.y_decal, self.width, self.height))

    def affiche_position(self):
        pygame.draw.circle(self.w.window, (0, 0, 0), [self.x, self.y], 1, 1)

    def affiche_all(self):
        self.affiche_zone_png()
        self.affiche_png()
        self.affiche_position()

    def comportement(self):
        """ On pourra surcharger cette méthode """
        self.affiche_png()


class ImageElementaire(Image):
    dim = (35, 60)

    def __init__(self, window, position: tuple, dimension: tuple = dim):
        super().__init__(window, position, dimension, (1/2, 2/3), "picture/png_hd/elementaire.png")


class AfficheArbre(Image):
    dim = (250, 250)

    def __init__(self, window, position: tuple, dimension: tuple = dim):
        super().__init__(window, position, dimension, (23/44, 7/8), "./picture/arbre/grand_arbre.png")
