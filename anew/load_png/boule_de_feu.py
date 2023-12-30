import random
import pygame


class ImageBouleDeFeu:
    W_DECAL = 1 / 2
    H_DECAL = 1 / 2

    def __init__(self, dimension):
        self.width, self.height = dimension
        self.png_path = "picture/boule_de_feu.png"
        self.png = self.load_png()

    def load_png(self):
        image = pygame.image.load(self.png_path).convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))
        flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return image

    def reload_png(self):
        self.png = self.load_png()
