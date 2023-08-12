import pygame


class Arbre:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.tronc_radius = 15
        self.feuille_radius = 50
        self.image_path = "picture/arbre.png"
        self.image_origin = pygame.image.load(self.image_path)  # .convert_alpha()
        self.largeur, self.longueur = 190, 200
        self.image = pygame.transform.scale(self.image_origin, (self.largeur, self.longueur))

    def affiche_skin_feuille(self):
        return pygame.draw.circle(self.w.window, (50, 200, 90), [self.x, self.y], self.feuille_radius, 0)

    def affiche_skin_tronc(self):
        return pygame.draw.circle(self.w.window, (88, 41, 0), [self.x, self.y], self.tronc_radius, 0)

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.longueur/2 - 3, self.y - self.largeur + 20))

    def comportement(self):
        # self.affiche_skin_feuille()
        # self.affiche_skin_tronc()
        self.affiche_png()
