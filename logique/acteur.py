import pygame

from sprite.image_dimension import Image


class Acteur:
    def __init__(self, window, position, skin):
        self.w = window
        self.x, self.y = position
        self.x_decal, self.y_decal = pos_decal
        self.width, self.height = dimension
        self.image_path = path
        self.image = self.load_image()
        # self.skin: Image = skin

    def affiche_png(self):
        self.w.window.blit(self.skin.image, (self.x - self.skin.width * self.skin.x_decal, self.y - self.skin.height * self.skin.y_decal))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.skin.x_decal, self.y - self.skin.y_decal, self.skin.width, self.skin.height))

    def affiche_position(self):
        pygame.draw.circle(self.w.window, (0, 0, 0), [x, y], 1, 1)

    def affiche_all(self):
        self.affiche_zone_png()
        self.affiche_png()
        self.affiche_position()

    def comportement(self):
        self.skin.affiche_png(self.w.window, self.x, self.y)