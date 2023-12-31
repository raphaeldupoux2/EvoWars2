from anew.world.acteur import Acteur
from anew.world.domaine_mortuaire.pierre_tombale import PierreTombale
from anew.world.domaine_mortuaire.spectre import Spectre


class Cimetiere(Acteur):
    ecart_entre_pierre = 100

    def __init__(self, monde, coords, zone):
        super().__init__(monde, "lieu", coords, zone)
        for j in range(3):
            for i in range(3):
                pt = PierreTombale(monde, (self.x_abs + self.ecart_entre_pierre*i, self.y_abs + self.ecart_entre_pierre*j), monde.dimension_pt)
                e = Spectre(monde, (self.x_abs + self.ecart_entre_pierre*i, self.y_abs + self.ecart_entre_pierre*j), 1, monde.dimension_humain, zone)
                e.pierre_tombale = pt

    def behavior(self, w):
        pass
