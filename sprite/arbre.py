import pygame


class Arbre:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.largeur, self.hauteur = 190, 150
        self.tronc_radius = (self.largeur + self.hauteur) / 34
        self.feuille_radius = 50
        self.image = self.load_image()

    def load_image(self):
        image_path = "picture/arbre/arbre.png"
        image_origin = pygame.image.load(image_path)  # .convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.hauteur))
        return image

    def affiche_feuille(self):
        return pygame.draw.circle(self.w.window, (50, 200, 90), [self.x, self.y], self.feuille_radius, 0)

    def affiche_tronc(self):
        return pygame.draw.circle(self.w.window, (88, 41, 0), [self.x, self.y], self.tronc_radius, 0)

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.largeur * 6 / 11, self.y - 7 / 8 * self.hauteur))

    def comportement(self):
        # self.affiche_feuille()
        # self.affiche_tronc()
        self.affiche_png()


class Arbre1:
    couleur_tronc = (112, 93, 72)
    couleur_feuille = (50, 200, 90)
    coefx_arbre_hautdroit, coefy_arbre_hautdroit = 326 / 500, 103 / 500

    def __init__(self, window, x, y):
        self.w = window
        self.largeur_arbre, self.hauteur_arbre = 140, 140
        self.image = self.load_image()
        self.x = x
        self.y = y
        self.tronc_radius = (self.largeur_arbre + self.hauteur_arbre) / 28
        self.feuille_radius = self.largeur_arbre * 50 / 140

    def load_image(self):
        image_path = "../picture/arbre/arbres.png"
        image_origin = pygame.image.load(image_path)  # .convert_alpha()
        largeur_png, hauteur_png = self.largeur_arbre * 500 / 140, self.hauteur_arbre * 500 / 140
        positionx_png_hautdroit, positiony_png_hautdroit = largeur_png * self.coefx_arbre_hautdroit, hauteur_png * self.coefy_arbre_hautdroit
        image = pygame.transform.scale(image_origin, (largeur_png, hauteur_png))
        cropped_rect = pygame.Rect(positionx_png_hautdroit, positiony_png_hautdroit, self.largeur_arbre,
                                   self.hauteur_arbre)
        cropped_image = image.subsurface(cropped_rect)
        return cropped_image

    def affiche_feuille(self):
        return pygame.draw.circle(self.w.window, self.couleur_feuille, [self.x, self.y], self.feuille_radius, 0)

    def affiche_tronc(self):
        return pygame.draw.circle(self.w.window, self.couleur_tronc, [self.x, self.y], self.tronc_radius, 0)

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x - self.largeur_arbre / 2, self.y - self.hauteur_arbre * 72 / 140))

    def comportement(self):
        # pygame.draw.rect(self.w.window, (0, 255, 0), (self.x - self.largeur_arbre / 2, self.y - self.hauteur_arbre * 72 / 140, self.largeur_arbre, self.hauteur_arbre))
        # self.affiche_feuille()
        self.affiche_tronc()
        self.affiche_png()
