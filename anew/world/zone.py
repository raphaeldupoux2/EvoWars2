import pygame

from anew.world.acteur import Acteur


class Zone(Acteur):
    l_tapis = 50
    r_tapis = 50

    def __init__(self, monde, coords, radius):
        super().__init__(monde, 'lieu', coords)
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, radius, radius)  # (x, y, largeur, hauteur)

        self.tapis_top = None
        self.tapis_bot = None
        self.tapis_left = None
        self.tapis_right = None

        self.monde.zone.append(self)

    @property
    def tapis(self):
        return [self.tapis_top, self.tapis_bot, self.tapis_left, self.tapis_right]

    def is_point_inside(self, coords):
        return self.rect.collidepoint(coords)

    def is_point_on_any_carpet(self, coords):
        for t in self.tapis:
            if t:
                if t.collidepoint(coords):
                    print(t.x, t.y)
                    return True
        return False

    def affiche(self, w):
        for t in self.tapis:
            if t:
                pygame.draw.rect(w.window, (255, 150, 0), t)
                pygame.draw.rect(w.window, (0, 0, 0), t, 1)  # Contour
        pygame.draw.rect(w.window, (0, 0, 0), self.rect, 10)

    def update_zone(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.rect.width, self.rect.height = self.radius, self.radius

    def update_tapis(self):
        if self.tapis_top is not None:
            self.tapis_top.midtop = self.rect.midtop
        if self.tapis_bot is not None:
            self.tapis_bot.midbottom = self.rect.midbottom
        if self.tapis_left is not None:
            self.tapis_left.midleft = self.rect.midleft
        if self.tapis_right is not None:
            self.tapis_right.midright = self.rect.midright

    def placement_tapis(self):
        for z in self.monde.zone:
            if self.rect.midright == z.rect.midleft:  # z est sur la droite
                self.tapis_right = pygame.Rect(self.rect.midright[0], self.rect.midright[1], Zone.l_tapis, Zone.r_tapis)

            if self.rect.midleft == z.rect.midright:  # z est sur la gauche
                self.tapis_left = pygame.Rect(self.rect.midleft[0], self.rect.midleft[1], Zone.l_tapis, Zone.r_tapis)

            if self.rect.midtop == z.rect.midbottom:  # z est en haut
                self.tapis_top = pygame.Rect(self.rect.midtop[0], self.rect.midtop[1], Zone.l_tapis, Zone.r_tapis)

            if self.rect.midbottom == z.rect.midtop:  # z est en bas
                self.tapis_bot = pygame.Rect(self.rect.midbottom[0], self.rect.midbottom[1], Zone.l_tapis, Zone.r_tapis)

    def behavior(self, w):
        self.update_zone()
        self.update_tapis()
        self.affiche(w)
