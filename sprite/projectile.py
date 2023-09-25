import math
import pygame

from utils import Utils

from EvoWars2.sprite.image_dimension import Image


class FireBall(Image):
    def __init__(self, window, position):
        super().__init__(window, position, (17, 18), (200, 200), 'picture/png_hd/flamme.png')
        self.posx_fb = self.width/2
        self.posy_fb = 0  # self.height*2/5
        self.width_fb = self.width/6
        self.height_fb = self.height  # *3/5
        self.cropped_image = self.crop_image()

    def crop_image(self):
        image = pygame.transform.scale(self.image, (self.width, self.height))
        cropped_rect = pygame.Rect(self.posx_fb, self.posy_fb, self.width_fb, self.height_fb)
        cropped_image = image.subsurface(cropped_rect)
        return cropped_image

    def affiche_cropped_png(self, x, y):
        self.w.window.blit(self.cropped_image, (x - self.x_decal, y - self.y_decal))

    def affiche_zone_cropped_png(self, x, y):
        pygame.draw.rect(self.w.window, (0, 150, 0), (x - self.x_decal, y - self.y_decal, self.width_fb, self.height_fb))

    def affiche_cropped_all(self, x, y):
        self.affiche_zone_cropped_png(x, y)
        self.affiche_cropped_png(x, y)


class BouleDeFeu(Image):
    def __init__(self, window, position):
        super().__init__(window, position, (17, 18), (33, 200), 'picture/png_hd/fireball.png')


class AfficheProjectile:
    def __init__(self, window, x, y, player, liste_obstacle=None):
        self.w = window
        self.x = x
        self.y = y
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
                                              -self.player_affect.maitrise["épée"].arme_degree_relatif(self.player_affect.position, Utils.curseur()) + 90):
            self.player_affect.color = (255, 0, 0)
            self.projectile_move = True
            if self.player_affect.maitrise["épée"].coup == "coup droit":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif(self.player_affect.position, Utils.curseur()) + 90
            elif self.player_affect.maitrise["épée"].coup == "revert":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif(self.player_affect.position, Utils.curseur()) - 90
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
