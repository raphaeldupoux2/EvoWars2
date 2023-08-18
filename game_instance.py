from sprite.arbre import Arbre
from player.player import Player
from sprite.stone import Stone
from sprite.terrain_tennis import TerrainTennis
from utils import Utils
from window import Window
from sprite.projectile import Projectile


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
        self.balle = [Projectile(self.w, self.w.WINDOW_WIDTH/2, self.w.WINDOW_HEIGHT/2, self.player.physique[0])]
        self.assombrir = [False, False, False]

    def fond(self):
        self.couleur_fond, self.assombrir = Utils.luminosite_tournante(couleur_fond=self.couleur_fond, vitesse_changement=0.1, assombrir=self.assombrir)

    def comportement(self):
        self.fond()
        self.w.window.fill(self.couleur_fond)

