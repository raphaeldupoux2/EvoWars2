import pygame

from EvoWars2.pygamesetup import pygame_params


class Image:
    def __init__(self, position: tuple, pos_decal: tuple, dimension: tuple, path: str):
        """
        Pour les png qui n'ont pas besoin d'être rogné
        :param window:
        :param position: (x, y)
        :param pos_decal: (x_decal, y_decal)
        :param dimension: (width, height)
        :param path: "picture/arbre/arbre.png"
        """
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
        pygame_params.window.blit(self.image, (self.x - self.x_decal, self.y - self.y_decal))

    def affiche_zone_png(self):
        pygame.draw.rect(pygame_params.window, (0, 150, 0), (self.x - self.x_decal, self.y - self.y_decal, self.width, self.height))

    def affiche_all(self):
        self.affiche_zone_png()
        self.affiche_png()
