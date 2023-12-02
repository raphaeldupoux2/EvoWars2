import math
import pygame

from utils import Utils

from logique.player import Player
from sprite.elementaire import ImageElementaire
from sprite.image_dimension import Image


class BouleDeFeu(Image):
    def __init__(self, window, position):
        super().__init__(window, position, (17, 18), (33, 200), 'picture/png_hd/fireball.png')


class AfficheProjectile:
    def __init__(self, window, curseur, position: tuple, player: Player, liste_obstacle=None):
        self.w = window
        self.curseur = curseur
        self.x, self.y = position
        self.skin = BouleDeFeu(window, (self.x, self.y))
        self.player_affect = player
        self.color = (200, 200, 0)
        self.vel = 0
        self.radius = 10
        self._direction = 180
        self.projectile_move = False
        self.new = True

    def frottement(self):
        self.vel -= 0.08
        if self.vel <= 0:
            self.vel = 0

    def changement_skin(self):
        if self.vel == 0:
            self.skin = ImageElementaire(self.w, (self.x, self.y))
            self.skin.affiche_png()
        else:
            self.skin = BouleDeFeu(self.w, (self.x, self.y))
            rotated_image = pygame.transform.rotate(self.skin.image, self.direction - 90)
            rect = rotated_image.get_rect()
            self.w.window.blit(rotated_image, (self.x - rect.width / 2, self.y - rect.height / 2))

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
            if 290 <= self.x <= 300 or 710 >= self.x >= 700:
                self._direction = 180 - self._direction
            elif 90 <= self.y <= 100 or 610 >= self.y >= 600:
                self._direction *= -1

    def contact_arme_player(self):
        if Utils.point_dans_rectangle_incline(self.x, self.y, self.player_affect.maitrise["épée"].rotated_rect.centerx,
                                              self.player_affect.maitrise["épée"].rotated_rect.centery, 30, 100,
                                              -self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x_arme, self.player_affect.y_arme), self.curseur.pos_relative) + 90):
            self.new = False
            self.vel = 10
            self.player_affect.color = (255, 0, 0)
            self.projectile_move = True
            if self.player_affect.maitrise["épée"].coup == "coup droit":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x_arme, self.player_affect.y_arme), self.curseur.pos_relative) + 90
            elif self.player_affect.maitrise["épée"].coup == "revert":
                direction = self.player_affect.maitrise["épée"].arme_degree_relatif((self.player_affect.x_arme, self.player_affect.y_arme), self.curseur.pos_relative) - 90
            else:
                direction = 0
            self._direction = direction

        elif Utils.distance_between((self.x, self.y), (self.player_affect.x_arme, self.player_affect.y_arme)) < 20:
            print("Touché")

        else:
            if self.new is True:
                self.projectile_move = True
                direction = - Utils.angle_degree_entre((self.x, self.y), (self.player_affect.x_arme, self.player_affect.y_arme))
                self.vel = 5
                self._direction = direction

    def comportement(self):
        self.frottement()
        self.changement_skin()


        # self.skin.affiche_png()

        # self.affiche_balle()

        # self.skin.rotated_image(self.x, self.y)
        self.contact_arme_player()
        self.move_to()
