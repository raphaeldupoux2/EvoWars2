import pygame


class FenetrePrincipale:
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.window = self.window_dimension(width, height)
        self.window_title(title)

    def window_title(self, title):
        return pygame.display.set_caption(title)

    def window_dimension(self, width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def window_refresh(self):
        return pygame.display.flip()


class SousFenetre:
    def __init__(self, main_window, position, width, height):
        self.main_window = main_window
        self.position = position
        self.width = width
        self.height = height
        self.window = pygame.Surface((width, height))

    def comportement(self):
        self.main_window.window.blit(self.window, self.position)


class SousFenetreManager:
    def __init__(self, main_window):
        self.all = []
        self.f1 = self._add_sous_fenetre(main_window, (0, 0), 1000, 720)
        self.f2 = self._add_sous_fenetre(main_window, (1000, 0), 1000, 720)

    def _add_sous_fenetre(self, main_window, position, largeur, hauteur):
        sous_fenetre = SousFenetre(main_window, position, largeur, hauteur)
        self.all.append(sous_fenetre)
        return sous_fenetre


class PygameSetUp:
    def __init__(self):
        pygame.init()
        self.main_window = FenetrePrincipale("FullStratFightTactic", 1000, 720)
        self.fenetres = SousFenetreManager(self.main_window)
        self._clock = pygame.time.Clock()
        self._fps = 60

    def fps_control(self):
        self._clock.tick(self._fps)
