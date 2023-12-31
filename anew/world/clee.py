from anew.load_png.clee import ImageClee
from anew.world.acteur import Acteur


class Clee(Acteur):
    def __init__(self, monde, coords, dimension):
        super().__init__(monde, "objet", coords)
        self.image = ImageClee(dimension)
        self.monde.clee.append(self)

    def print_image(self, w):
        w.window.blit(self.image.png, (self.x, self.y))

    def behavior(self, w):
        self.print_image(w)
