import pygame


class AfficheCouronne:
    def __init__(self, position):
        self.x, self.y = position
        self.image_path = "picture/crown.png"
        self.largeur, self.hauteur = 50, 50
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.hauteur/2, self.y - self.largeur/2 - 50))

    def affiche(self):
        self.affiche_png()
