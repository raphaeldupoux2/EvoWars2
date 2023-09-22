import pygame


class AfficheCampFire:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.image_path = "picture/feu_de_camp.png"
        self.largeur, self.hauteur = 75, 75
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.hauteur/2, self.y - self.largeur*3/4))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.hauteur/2, self.y - self.largeur*3/4, 100, 100))

    def affiche(self):
        self.affiche_zone_png()
        self.affiche_png()
