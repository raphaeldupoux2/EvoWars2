import math
import pygame


class Projectile:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.color = (200, 200, 0)
        self.vel = 10
        self.radius = 10
        self.angle = 180

    def affiche_skin(self):
        pygame.draw.circle(self.w.window, self.color, [self.x, self.y], self.radius, 0)
        pygame.draw.circle(self.w.window, (0, 0, 0), [self.x, self.y], self.radius, 1)

    def move_to(self):
        self.x += math.cos(self.angle * math.pi / 180) * self.vel
        self.y += -math.sin(self.angle * math.pi / 180) * self.vel
        if self.x <= 0:
            self.angle -= 180
        elif self.y <= 0:
            self.angle -= 180
        elif self.x >= self.w.WINDOW_WIDTH:
            self.angle -= 180
        elif self.y >= self.w.WINDOW_HEIGHT:
            self.angle -= 180
