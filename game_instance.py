from arbre import Arbre
from controle import Controle
from player.player import Player
from stone import Stone
from terrain_tennis import TerrainTennis
from window import Window
from projectile import Projectile


class GameInstance:
    couleur_sable = (255, 240, 190)
    FPS = 60  # Définition du nombre de FPS souhaité
    FRAME_DURATION = 1 / FPS  # Calcul de la durée en secondes entre chaque frame

    def __init__(self):
        super().__init__()
        self.window = Window()
        self.couleur_fond = GameInstance.couleur_sable
        self.terrain: list = [TerrainTennis(self.window, 300, 100)]
        self.arbre: list = [Arbre(self.window, 200, 500), Arbre(self.window, 80, 600), Arbre(self.window, 90, 400), Arbre(self.window, 800, 60)]
        self.stone: list = [Stone(self.window, 800, 600), Stone(self.window, 850, 555)]
        self.player = Player(self.window, self.arbre)
        self.projectile = Projectile(self.window, self.window.WINDOW_WIDTH/2, self.window.WINDOW_HEIGHT/2)
        self.controle = Controle()
        self.assombrir = [False, False, False]

    @staticmethod
    def luminosite_tournante(couleur_fond, vitesse_changement, assombrir):
        if couleur_fond[0] >= 255:
            assombrir[0] = True
        if couleur_fond[1] >= 255:
            assombrir[1] = True
        if couleur_fond[2] >= 255:
            assombrir[2] = True

        if couleur_fond[0] <= 0:
            assombrir[0] = False
        if couleur_fond[1] <= 0:
            assombrir[1] = False
        if couleur_fond[2] <= 0:
            assombrir[2] = False

        if assombrir[0] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (-vitesse_changement, 0, 0)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (vitesse_changement, 0, 0)))

        if assombrir[1] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, -vitesse_changement, 0)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, vitesse_changement, 0)))

        if assombrir[2] is True:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, 0, -vitesse_changement)))
        else:
            couleur_fond = tuple(sum(i) for i in zip(couleur_fond, (0, 0, vitesse_changement)))

        return couleur_fond, assombrir
