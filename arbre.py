import pygame


class Arbre:
    image_path = "picture/arbre.png"
    image_origin = pygame.image.load(image_path)  # .convert_alpha()
    largeur, hauteur = 190, 150
    image = pygame.transform.scale(image_origin, (largeur, hauteur))

    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.tronc_radius = (self.largeur + self.hauteur)/34
        self.feuille_radius = 50

    def affiche_skin_feuille(self):
        return pygame.draw.circle(self.w.window, (50, 200, 90), [self.x, self.y], self.feuille_radius, 0)

    def affiche_skin_tronc(self):
        return pygame.draw.circle(self.w.window, (88, 41, 0), [self.x, self.y], self.tronc_radius, 0)

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.largeur * 6/11, self.y - 7/8 * self.hauteur))#(self.x - self.longueur/2, self.y - self.largeur))

    def comportement(self):
        # self.affiche_skin_feuille()
        # self.affiche_skin_tronc()
        self.affiche_png()
