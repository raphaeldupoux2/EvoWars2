import pygame


class SousFenetreManager:
    all = []

    def add_sous_fenetre(self, main_window, position, largeur, hauteur, nom):
        sous_fenetre = SousFenetre(main_window, position, largeur, hauteur, nom)
        self.all.append(sous_fenetre)
        return sous_fenetre


class SousFenetre:
    def __init__(self, main_window, position, width, height, nom):
        self.nom: str = nom
        self.main_window = main_window
        self.position: tuple = position
        self.width: int = width
        self.height: int = height
        self.window = pygame.Surface((width, height))

    def comportement(self):
        self.main_window.window.blit(self.window, self.position)
