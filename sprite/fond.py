from sprite.image_dimension import Image
from utils import Utils


class Fond:
    couleur_sable = (255, 240, 190)

    def __init__(self, window):
        self.w = window
        self.assombrir = [False, False, False]
        self.couleur_fond = self.couleur_sable

    def fond(self):
        self.couleur_fond, self.assombrir = Utils.luminosite_tournante(couleur_fond=self.couleur_fond,
                                                                       vitesse_changement=0.1, assombrir=self.assombrir)

    def changement_de_fond(self):
        self.fond()
        self.w.window.fill(self.couleur_fond)


class Herbe(Image):
    def __init__(self, window, position=(0, 0), dimension=(150, 150)):
        super().__init__(window, position, (0, 0), dimension, 'picture/surface/herbe.png')


class EtaleHerbe:
    def __init__(self, window):
        self.window = window
        self.liste_herbe = []
        self.cote_carre = 200
        self.create_carre_herbe()

    def create_carre_herbe(self):
        for j in range(8):
            for i in range(13):
                self.liste_herbe.append(Herbe(self.window, (i * self.cote_carre, j * self.cote_carre), (self.cote_carre, self.cote_carre)))

    def comportement(self):
        for elem in self.liste_herbe:
            elem.affiche_png()


class TerreCorail(Image):
    def __init__(self, window, position=(0, 0), dimension=(150, 150)):
        super().__init__(window, position, (0, 0), dimension, 'picture/surface/terre_corail.png')


class EtaleTerre:
    def __init__(self, window):
        self.window = window
        self.liste_herbe = []
        self.largeur_rect = 190
        self.longueur_rect = 160
        self.create_carre_herbe()

    def create_carre_herbe(self):
        for j in range(3):
            for i in range(2):
                self.liste_herbe.append(TerreCorail(self.window, (i * self.largeur_rect + 310, j * self.longueur_rect + 110), (self.largeur_rect, self.longueur_rect)))

    def comportement(self):
        for elem in self.liste_herbe:
            elem.affiche_png()
