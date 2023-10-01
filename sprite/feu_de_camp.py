import pygame

from EvoWars2.pygamesetup import pygame_params


class AfficheCampFire:
    def __init__(self, position: tuple):
        self.x, self.y = position
        self.image_path = "picture/feu_de_camp.png"
        self.largeur, self.hauteur = 75, 75
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_png(self):
        pygame_params.window.blit(self.image, (self.x - self.hauteur/2, self.y - self.largeur*3/4))

    def affiche_zone_png(self):
        pygame.draw.rect(pygame_params.window, (0, 150, 0), (self.x - self.hauteur/2, self.y - self.largeur*3/4, 100, 100))

    def affiche(self):
        self.affiche_zone_png()
        self.affiche_png()

    def comportement(self):
        self.affiche_png()
