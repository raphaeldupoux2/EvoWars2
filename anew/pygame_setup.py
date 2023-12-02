import pygame


class FenetrePrincipale:
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.window = self.window_dimension(width, height)
        self.window_title(title)

    @staticmethod
    def window_title(title):
        return pygame.display.set_caption(title)

    @staticmethod
    def window_dimension(width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    @staticmethod
    def window_refresh():
        return pygame.display.flip()


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
            self.pos_relative = (self.pos_globale[0] - self.fenetre_control.position[0],
                                 self.pos_globale[1] - self.fenetre_control.position[1])

    def refresh_curseur(self):
        self.pos_globale = pygame.mouse.get_pos()
        self.curseur_detecte_fenetre()
        self.curseur_in_fenetre()


class Horloge:
    def __init__(self, fps):
        self.clock = pygame.time.Clock()
        self.fps = fps

    def fps_control(self):
        self.clock.tick(self.fps)


class PygameSetUp:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, title='', width=1000, height=720, fps=60):
        if cls._instance is None:
            cls._instance = super(PygameSetUp, cls).__new__(cls)
            pygame.init()
            cls._instance.main_window = FenetrePrincipale(title, width, height)
            cls._instance.fenetres = SousFenetreManager()
            cls._instance.curseur = Curseur(cls._instance.fenetres)
            cls._instance.horloge = Horloge(fps)
        return cls._instance
