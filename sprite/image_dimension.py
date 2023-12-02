import pygame


class Image:
    def __init__(self, dimension: tuple, pos_decal: tuple, path: str):
        """
        Pour les png qui n'ont pas besoin d'être rogné
        :param pos_decal: (x_decal, y_decal) détermine le point de référence du png (les pieds du personnage)
        :param dimension: (width, height)
        :param path: "picture/arbre/arbre.png"
        """
        self.x_decal, self.y_decal = pos_decal
        self.width, self.height = dimension
        self.image_path = path
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.width, self.height))
        return image

    def reload_image(self):
        self.image = self.load_image()


class ImageHerbe(Image):
    def __init__(self, dimension=(200, 200)):
        super().__init__((200, 200), (0, 0), 'picture/surface/herbe.png')


class ImageTerreCorail(Image):
    def __init__(self, dimension=(200, 200)):
        super().__init__(dimension, 'picture/surface/terre_corail.png')
