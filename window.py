import pygame


class Window:

    def __init__(self):
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 720
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    @classmethod
    def set_up(cls):
        pygame.display.set_caption('Evowars')

    def refresh_window_dimension(self):
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
