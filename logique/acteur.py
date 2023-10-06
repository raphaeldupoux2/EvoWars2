
class Acteur:
    w = None

    def __init__(self, w, position, image):
        self.window = w.window
        self.x, self.y = position
        self.skin = image
