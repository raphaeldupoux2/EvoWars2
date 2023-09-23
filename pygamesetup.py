import pygame


class PygameSetUp:
    def __init__(self, width, height, title):
        pygame.init()
        self.window = self.window_dimension(width, height)
        self.window_title(title)
        self.window_refresh()
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.width = width
        self.height = height
        self.title = title

    def window_title(self, title):
        return pygame.display.set_caption(title)

    def window_dimension(self, width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def window_refresh(self):
        return pygame.display.flip()

    def fps_control(self):
        self.clock.tick(self.fps)
