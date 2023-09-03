import pygame


class AfficheTerrainTennis:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.color = (222, 144, 144)
        self.largeur = 400
        self.longueur = 500
        self.largeur_bande = 10
        self.color_bande = (255, 255, 255)

    def affiche_terrain(self):
        pygame.draw.rect(self.w.window, self.color, (self.x, self.y, self.largeur, self.longueur))
        pygame.draw.rect(self.w.window, self.color_bande, (self.x, self.y, self.largeur_bande, 500))
        pygame.draw.rect(self.w.window, self.color_bande, (self.x + self.largeur - self.largeur_bande, self.y, self.largeur_bande, 500))
        pygame.draw.rect(self.w.window, self.color_bande, (self.x, self.y, 400, self.largeur_bande))
        pygame.draw.rect(self.w.window, self.color_bande, (self.x, self.y + self.longueur - self.largeur_bande, 400, self.largeur_bande))
        pygame.draw.rect(self.w.window, self.color_bande, (self.x, self.y + self.longueur/2 - self.largeur_bande/2, 400, self.largeur_bande))

    def affiche(self):
        self.affiche_terrain()
