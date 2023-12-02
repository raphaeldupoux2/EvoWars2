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

