import pygame


class ImageEpee:
    def __init__(self, window, position):
        self.w = window
        self.x, self.y = position
        self.image_path = "picture/epee.png"
        self.largeur, self.hauteur = 30, 100
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_png(self):
        self.w.window.blit(self.image,
                           (self.x - self.hauteur / 2, self.position['y'] - self.largeur / 2 - 50))

    def affiche_zone_png(self, position: dict):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x - self.hauteur / 2, self.y - self.largeur / 2 - 50, 30, 100))

    def affiche_all(self, position: dict):
        self.affiche_zone_png(position)
        self.affiche_png(position)
