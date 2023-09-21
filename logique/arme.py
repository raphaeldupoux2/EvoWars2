
class Arme:
    def __init__(self, nom: str, position: dict, largeur: int, hauteur: int, image, renvoie: bool):
        self.nom = nom
        self.position = position
        self.largeur, self.hauteur = largeur, hauteur
        self.image = image
        self.renvoie = renvoie


class Epee(Arme):
    def __init__(self, position, image):
        super().__init__("épée", position, 30, 100, image, True)

