import pygame

from sprite.image_dimension import Image


class ImageElementaire(Image):
    def __init__(self, window, position: tuple):
        super().__init__(window, position, (17.5, 40), (35, 60), "picture/png_hd/elementaire.png")

    def comportement(self):
        self.affiche_png()
