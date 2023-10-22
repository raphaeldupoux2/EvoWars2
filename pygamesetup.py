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
    def __init__(self, main_window, position=(0, 0), width=0, height=0, nom=""):
        self.nom: str = nom
        self.main_window = main_window
        self.position: tuple = position
        self.width: int = width
        self.height: int = height
        self.window = pygame.Surface((width, height))

    def comportement(self):
        self.main_window.window.blit(self.window, self.position)


class SousFenetreManager:
    def __init__(self, main_window):
        self.all = []
        self.f1 = self._add_sous_fenetre(main_window, (10, 10), 980, 700, "campagne")
        self.f2 = self._add_sous_fenetre(main_window, (1020, 10), 200, 200, "monde parallèle")

    def _add_sous_fenetre(self, main_window, position, largeur, hauteur, nom):
        sous_fenetre = SousFenetre(main_window, position, largeur, hauteur, nom)
        self.all.append(sous_fenetre)
        return sous_fenetre


class Curseur:
    def __init__(self, fenetres: SousFenetreManager):
        self.fenetres = fenetres
        self.fenetre_control = None
        self.pos_globale = (0, 0)
        self.pos_relative = (0, 0)

    def curseur_detecte_fenetre(self):
        """
        :return: la fenêtre localisée à l'endroit de la position du curseur
        """
        self.fenetre_control = None
        for f in self.fenetres.all:
            if f.position[0] < self.pos_globale[0] < f.position[0] + f.width and f.position[1] < self.pos_globale[1] < f.position[1] + f.height:
                self.fenetre_control = f

    def curseur_in_fenetre(self):
        """
        retourne la position du curseur relative à la fenêtre
        :return: tuple(x, y)
        """
        if self.fenetre_control is not None:
            self.pos_relative = self.pos_globale[0] - self.fenetre_control.position[0], self.pos_globale[1] - self.fenetre_control.position[1]

    def refresh_curseur(self):
        self.pos_globale = pygame.mouse.get_pos()
        self.curseur_detecte_fenetre()
        self.curseur_in_fenetre()

    def comportement(self, f):
        if self.fenetre_control == f:
            # if self.fenetre_control == self.fenetres.f2:
            #     return self.pos_relative[0], self.pos_relative[1]
            return self.pos_relative
        else:
            return None


class PygameSetUp:
    def __init__(self):
        pygame.init()
        self.main_window = FenetrePrincipale("FullStratFightTactic", 1000, 720)
        self.fenetres = SousFenetreManager(self.main_window)
        self.curseur = Curseur(self.fenetres)
        self._clock = pygame.time.Clock()
        self._fps = 60

    def fps_control(self):
        self._clock.tick(self._fps)
