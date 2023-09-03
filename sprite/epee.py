import pygame


class Epee:
    def __init__(self, window, position):
        self.w = window
        self.position = position
        self.image_path = "picture/epee.png"
        self.largeur, self.hauteur = 30, 100
        self.image = self.load_image()
        self.degree = 0

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_png(self):
        self.w.window.blit(self.image,
                           (self.position['x'] - self.hauteur / 2, self.position['y'] - self.largeur / 2 - 50))

    def affiche(self):
        self.affiche_png()
