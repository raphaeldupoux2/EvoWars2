import pygame


class ImageClee:
    W_DECAL = 1 / 2
    H_DECAL = 1 / 2

    def __init__(self, dimension):
        pygame.init()

        self.width, self.height = dimension
        self.png_path = "picture/clee.png"
        self.png = self.load_png()

    def load_png(self):
        image = pygame.image.load(self.png_path)
        image = pygame.transform.scale(image, (self.width, self.height))
        return image

    def reload_png(self):
        self.png = self.load_png()