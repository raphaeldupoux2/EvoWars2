import pygame


class FenetrePrincipale:
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.window = self.window_dimension(width, height)
        self.window_title(title)

    @staticmethod
    def window_title(title):
        return pygame.display.set_caption(title)

    @staticmethod
    def window_dimension(width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    @staticmethod
    def window_refresh():
        return pygame.display.flip()
