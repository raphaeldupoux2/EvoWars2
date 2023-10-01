import random

import pygame

from EvoWars2.pygamesetup import pygame_params


class AfficheStone:
    def __init__(self, position: tuple):
        self.x, self.y = position
        self.largeur, self.longueur = 61, 44
        self.image = self.load_image()

    def load_image(self):
        liste_image_path = ["picture/pierre/pierre.png",
                            "picture/pierre/pierre2.png",
                            "picture/pierre/pierre3.png"]
        image_path = random.choice(liste_image_path)
        image_origin = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.longueur))
        flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return image

    def affiche_png(self):
        pygame_params.window.blit(self.image, (self.x, self.y))

    def comportement(self):
        self.affiche_png()
