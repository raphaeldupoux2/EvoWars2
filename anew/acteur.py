import pygame


class Acteur:
    def __init__(self, coords: tuple):
        self.x, self.y = coords


class Image:
    def __init__(self, png_path: str, dimension: tuple):
        self.width, self.height = dimension
        self.png_path = png_path
        self.png = self.load_png()

    def load_png(self):
        image_origin = pygame.image.load(self.png_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.width, self.height))
        return image

    def reload_png(self):
        self.png = self.load_png()
