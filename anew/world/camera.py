from anew.world.acteur import Acteur


class Camera(Acteur):

    def __init__(self, monde, position, cible=None):
        super().__init__(monde, "abstrait", position)
        self.cible = cible

    def behavior(self, w):
        if self.cible is not None:
            self.x_abs = self.cible.x_abs - w.width / 2
            self.y_abs = self.cible.y_abs - w.height / 2
