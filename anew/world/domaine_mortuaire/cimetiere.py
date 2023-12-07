from anew.world.domaine_mortuaire.pierre_tombale import PierreTombale
from anew.world.domaine_mortuaire.spectre import Spectre


class Cimetiere:
    def __init__(self, monde):
        pt = PierreTombale(monde, (500, 200), monde.dimension_pt)
        pt2 = PierreTombale(monde, (600, 200), monde.dimension_pt)
        pt3 = PierreTombale(monde, (700, 200), monde.dimension_pt)

        e = Spectre(monde, (500, 200), 1, monde.dimension_humain)
        e2 = Spectre(monde, (600, 200), 1, monde.dimension_humain)
        e3 = Spectre(monde, (700, 200), 1, monde.dimension_humain)

        e.pierre_tombale = pt
        e2.pierre_tombale = pt2
        e3.pierre_tombale = pt3

        pt4 = PierreTombale(monde, (500, 300), monde.dimension_pt)
        pt5 = PierreTombale(monde, (600, 300), monde.dimension_pt)
        pt6 = PierreTombale(monde, (700, 300), monde.dimension_pt)

        e4 = Spectre(monde, (500, 300), 1, monde.dimension_humain)
        e5 = Spectre(monde, (600, 300), 1, monde.dimension_humain)
        e6 = Spectre(monde, (700, 300), 1, monde.dimension_humain)

        e4.pierre_tombale = pt4
        e5.pierre_tombale = pt5
        e6.pierre_tombale = pt6
