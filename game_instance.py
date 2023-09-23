import pygame

from EvoWars2.picture.tools import Tools
from EvoWars2.sprite.feu_de_camp import AfficheCampFire
from EvoWars2.sprite.fond import Fond, EtaleHerbe, Herbe, EtaleTerre
from sprite.arbre import AfficheArbre
from EvoWars2.logique.player import Player
from sprite.stone import AfficheStone
from sprite.terrain_tennis import AfficheTerrainTennis
from pygamesetup import PygameSetUp
from sprite.projectile import AfficheProjectile


class GameInstance:
    FPS = 60  # Définition du nombre de FPS souhaité
    FRAME_DURATION = 1 / FPS  # Calcul de la durée en secondes entre chaque frame

    def __init__(self):
        self.running = True
        self.w = PygameSetUp(1000, 720, "FullStratFightTactic")
        self.fond = Fond(self.w)
        self.terrain: list = [AfficheTerrainTennis(self.w, 300, 100)]
        self.arbre: list = [AfficheArbre(self.w, 200, 500), AfficheArbre(self.w, 80, 600), AfficheArbre(self.w, 90, 400), AfficheArbre(self.w, 850, 150)]#, Arbre(self.window, 110, 550), Arbre(self.window, 250, 520), Arbre(self.window, 150, 420), Arbre(self.window, 90, 620), Arbre(self.window, 800, 60)]
        self.stone: list = [AfficheStone(self.w, 800, 600), AfficheStone(self.w, 830, 570), AfficheStone(self.w, 860, 600)]
        self.feu_de_camp = [AfficheCampFire(self.w, 433, 100), AfficheCampFire(self.w, 566, 100)]
        self.arme: list = []
        self.player = Player(self.w, self.arbre)
        self.balle: list = [AfficheProjectile(self.w, self.w.width / 2, self.w.height / 2, self.player.physique[0])]
        self.etale_herbe = EtaleHerbe(self.w)
        self.etale_terre = EtaleTerre(self.w)

        # h = Herbe(self.w)
        # Tools.changer_couleur_image_and_save_it(h.image)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def bouton_player(self, event):
        for spirit in self.player.spirit:
            spirit.bouton(event)
        for physique in self.player.physique:
            physique.bouton(event)

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.bouton_player(event)

    def ordre_affiche(self):
        self.fond.changement_de_fond()
        self.etale_herbe.comportement()
        # for spirit in self.player.spirit:
        #     spirit.color = self.fond.couleur_fond
        for terrain in self.terrain:
            terrain.affiche_terrain()
        self.etale_terre.comportement()
        for feu in self.feu_de_camp:
            feu.affiche_png()
        # for spirit in self.player.spirit:
        #     spirit.comportement()
        for physique in self.player.physique:
            physique.comportement()
        for stone in self.stone:
            stone.affiche()
        for arbre in self.arbre:
            arbre.affiche()
        for balle in self.balle:
            balle.comportement()

    def game(self):
        while self.running:
            self.event()
            self.ordre_affiche()
            self.w.window_refresh()
            self.w.fps_control()
