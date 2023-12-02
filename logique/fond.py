from logique.acteur import Acteur
from sprite.image_dimension import Image, ImageTerreCorail


class Herbe(Acteur):
    def __init__(self, window, position):
        super().__init__(window, position, Image((200, 200), (0, 0), 'picture/surface/herbe.png'))


class TerreCorail(Acteur):
    def __init__(self, window, position, dimension=None):
        super().__init__(window, position, ImageTerreCorail(dimension))

    def comportement(self):
        self.affiche_png()


class EtaleHerbe:
    def __init__(self, window):
        self.window = window
        self.liste_herbe = []
        self.cote_carre = 200
        self.create_carre_herbe()

    def create_carre_herbe(self):
        for j in range(8):
            for i in range(13):
                self.liste_herbe.append(Herbe(self.window, (i * self.cote_carre, j * self.cote_carre)))

    def comportement(self):
        for elem in self.liste_herbe:
            elem.comportement()


class EtaleTerre:
    def __init__(self, window, position):
        self.window = window
        self.x, self.y = position
        self.liste_terre = []
        self.largeur_rect = 190
        self.longueur_rect = 160
        self.create_carre_terre()

    def create_carre_terre(self):
        for j in range(3):
            for i in range(2):
                self.liste_terre.append(TerreCorail(self.window, (i * self.largeur_rect + 310, j * self.longueur_rect + 110), (self.largeur_rect, self.longueur_rect)))

    def comportement(self):
        for elem in self.liste_terre:
            elem.affiche_png()
