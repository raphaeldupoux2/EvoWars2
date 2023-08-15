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
        self.w = Window()
        self.couleur_fond = GameInstance.couleur_sable
        self.terrain: list = [TerrainTennis(self.w, 300, 100)]
        self.arbre: list = [Arbre(self.w, 200, 500), Arbre(self.w, 80, 600), Arbre(self.w, 90, 400), Arbre(self.w, 850, 150)]#, Arbre(self.window, 110, 550), Arbre(self.window, 250, 520), Arbre(self.window, 150, 420), Arbre(self.window, 90, 620), Arbre(self.window, 800, 60)]
        self.stone: list = [Stone(self.w, 800, 600), Stone(self.w, 830, 570), Stone(self.w, 860, 600)]
        self.player = Player(self.w, self.arbre)
        self.projectile = Projectile(self.w, self.w.WINDOW_WIDTH/2, self.w.WINDOW_HEIGHT/2)
        self.controle = Controle()
        self.assombrir = [False, False, False]
