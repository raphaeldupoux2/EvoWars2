from EvoWars2.sprite.image_dimension import Image
from EvoWars2.utils import Utils


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
    def __init__(self, window, position, dimension):
        super().__init__(window, position, (0, 0), dimension, 'picture/herbe.png')


class EtaleHerbe:
    def __init__(self, window):
        self.window = window
        self.liste_herbe = []
        self.cote_carre = 150
        self.create_carre_herbe()

    def create_carre_herbe(self):
        for j in range(8):
            for i in range(10):
                self.liste_herbe.append(Herbe(self.window, (i * self.cote_carre, j * self.cote_carre), (self.cote_carre, self.cote_carre)))

    def comportement(self):
        for elem in self.liste_herbe:
            elem.affiche_png()
