from sprite.arbre import AfficheArbre
from logique.player import Player
from sprite.stone import AfficheStone
from sprite.terrain_tennis import AfficheTerrainTennis
from utils import Utils
from window import Window
from sprite.projectile import AfficheProjectile


class GameInstance:
    couleur_sable = (255, 240, 190)
    FPS = 60  # Définition du nombre de FPS souhaité
    FRAME_DURATION = 1 / FPS  # Calcul de la durée en secondes entre chaque frame

    def __init__(self):
        super().__init__()
        self.w = Window()
        self.couleur_fond = GameInstance.couleur_sable
        self.terrain: list = [AfficheTerrainTennis(self.w, 300, 100)]
        self.arbre: list = [AfficheArbre(self.w, 200, 500), AfficheArbre(self.w, 80, 600), AfficheArbre(self.w, 90, 400), AfficheArbre(self.w, 850, 150)]#, Arbre(self.window, 110, 550), Arbre(self.window, 250, 520), Arbre(self.window, 150, 420), Arbre(self.window, 90, 620), Arbre(self.window, 800, 60)]
        self.stone: list = [AfficheStone(self.w, 800, 600), AfficheStone(self.w, 830, 570), AfficheStone(self.w, 860, 600)]
        self.player = Player(self.w, self.arbre)

        self.balle = [AfficheProjectile(self.w, self.w.WINDOW_WIDTH / 2, self.w.WINDOW_HEIGHT / 2, self.player.physique[0])]
        self.assombrir = [False, False, False]

    def fond(self):
        self.couleur_fond, self.assombrir = Utils.luminosite_tournante(couleur_fond=self.couleur_fond, vitesse_changement=0.1, assombrir=self.assombrir)

    def ordre_affiche(self):
        for spirit in self.player.spirit:
            spirit.color = self.couleur_fond
        for terrain in self.terrain:
            terrain.affiche_terrain()
        for spirit in self.player.spirit:
            spirit.comportement()
        p.affiche_png()
        for physique in self.player.physique:
            physique.comportement()
        for stone in self.stone:
            stone.comportement()
        for arbre in self.arbre:
            arbre.comportement()
        for balle in self.balle:
            balle.comportement()

    def comportement(self):
        self.fond()
        self.w.window.fill(self.couleur_fond)

