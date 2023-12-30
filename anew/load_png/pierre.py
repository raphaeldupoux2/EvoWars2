import random
import pygame


class ImageStone:
    W_DECAL = 1/2
    H_DECAL = 50/125

    def __init__(self, dimension):
        self.width, self.height = dimension
        self.liste_png_path = ["picture/pierre/pierre.png",
                               "picture/pierre/pierre2.png",
                               "picture/pierre/pierre3.png"]
        self.png = self.load_png()

    def load_png(self):
        image_path = random.choice(self.liste_png_path)
        image_origin = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.width, self.height))
        flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return image

    def reload_png(self):
        self.png = self.load_png()
