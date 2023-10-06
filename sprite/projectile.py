import math
import pygame

from utils import Utils

from EvoWars2.sprite.image_dimension import Image


class BouleDeFeu(Image):
    def __init__(self, window, position):
        super().__init__(window, position, (17, 18), (33, 200), 'picture/png_hd/fireball.png')


class AfficheProjectile:
    def __init__(self, window, position: tuple, player, liste_obstacle=None):
        self.w = window
        self.x, self.y = position
        self.skin = BouleDeFeu(window, (self.x, self.y))
        self.player_affect = player
        self.color = (200, 200, 0)
        self.vel = 10
        self.radius = 10
        self._direction = 180
        self.projectile_move = False

    @property
    def direction(self):
        return Utils.normalize_angle(self._direction)

    def affiche_balle(self):
        pygame.draw.circle(self.w.window, self.color, [self.x, self.y], self.radius, 0)
        pygame.draw.circle(self.w.window, (0, 0, 0), [self.x, self.y], self.radius, 1)

    def move_to(self):
        if self.projectile_move:
            self.x += math.cos(self._direction * math.pi / 180) * self.vel
            self.y += -math.sin(self._direction * math.pi / 180) * self.vel
            if self.x <= 300 or self.x >= 700:
                self._direction = 180 - self._direction
            elif self.y <= 100 or self.y >= 600:
                self._direction *= -1

    def contact_arme_player(self):
        if Utils.point_dans_rectangle_incline(self.x, self.y, self.player_affect.maitrise["épée"].rotated_rect.centerx,
                                              self.player_affect.maitrise["épée"].rotated_rect.centery, 30, 100,
                                              -self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x, self.player_affect.y), Utils.curseur()) + 90):
            self.player_affect.color = (255, 0, 0)
            self.projectile_move = True
            if self.player_affect.maitrise["épée"].coup == "coup droit":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x, self.player_affect.y), Utils.curseur()) + 90
            elif self.player_affect.maitrise["épée"].coup == "revert":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x, self.player_affect.y), Utils.curseur()) - 90
            else:
                direction = 0
            self._direction = direction

        else:
            self.player_affect.color = (50, 50, 90)

    def comportement(self):
        rotated_image = pygame.transform.rotate(self.skin.image, self.direction - 90)
        rect = rotated_image.get_rect()
        self.w.window.blit(rotated_image, (self.x - rect.width/2, self.y - rect.height/2))

        # self.skin.affiche_png()

        # self.affiche_balle()

        # self.skin.rotated_image(self.x, self.y)
        self.contact_arme_player()
        self.move_to()
