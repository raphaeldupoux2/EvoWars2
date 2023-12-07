import pygame


class Horloge:
    def __init__(self, fps):
        self.clock = pygame.time.Clock()
        self.fps = fps

    def fps_control(self):
        self.clock.tick(self.fps)
