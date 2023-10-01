import pygame

from EvoWars2.pygamesetup import pygame_params


class AfficheTerrainTennis:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (222, 144, 144)
        self.largeur = 400
        self.longueur = 500
        self.largeur_bande = 10
        self.color_bande = (255, 255, 255)
        self.color_cage = (255, 128, 0)

    def affiche_terrain(self):
        pygame.draw.rect(pygame_params.window, self.color, (self.x, self.y, self.largeur, self.longueur))
        pygame.draw.rect(pygame_params.window, self.color_bande, (self.x, self.y, self.largeur_bande, 500))
        pygame.draw.rect(pygame_params.window, self.color_bande, (self.x + self.largeur - self.largeur_bande, self.y, self.largeur_bande, 500))
        pygame.draw.rect(pygame_params.window, self.color_bande, (self.x, self.y, 400, self.largeur_bande))
        # pygame.draw.rect(pygame_params.window, self.color_cage, (self.x + 166, self.y, 70, self.largeur_bande))
        pygame.draw.rect(pygame_params.window, self.color_bande, (self.x, self.y + self.longueur - self.largeur_bande, 400, self.largeur_bande))
        # pygame.draw.rect(pygame_params.window, self.color_bande, (self.x, self.y + self.longueur/2 - self.largeur_bande/2, 400, self.largeur_bande))

    def affiche(self):
        self.affiche_terrain()
