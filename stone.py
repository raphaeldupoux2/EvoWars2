import pygame


class Stone:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.image_path = "picture/stones.png"
        self.image_origin = pygame.image.load(self.image_path).convert_alpha()
        self.largeur, self.longueur = 50, 50
        self.image = pygame.transform.scale(self.image_origin, (self.largeur, self.longueur))

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x, self.y))

    def comportement(self):
        self.affiche_png()
