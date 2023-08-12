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
