import math
import pygame


class Projectile:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.color = (200, 200, 0)
        self.vel = 1
        self.radius = 10

    def affiche_skin(self):
        pygame.draw.circle(self.w.window, self.color, [self.x, self.y], self.radius, 0)
        pygame.draw.circle(self.w.window, (0, 0, 0), [self.x, self.y], self.radius, 1)

    def move_to(self, angle):
        print(angle)
        self.x += math.cos(angle) * self.vel
        self.y += math.sin(angle) * self.vel
