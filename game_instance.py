import pygame

from EvoWars2.logique.acteur import Acteur
from EvoWars2.picture.tools import Tools
from EvoWars2.sprite.feu_de_camp import AfficheCampFire
from EvoWars2.sprite.fond import Fond, EtaleHerbe, EtaleTerre
from sprite.arbre import AfficheArbre
from EvoWars2.logique.player import Player
from sprite.stone import AfficheStone
from sprite.terrain_tennis import AfficheTerrainTennis
from pygamesetup import PygameSetUp, pygame_params
from sprite.projectile import AfficheProjectile


class GameInstance:
    def __init__(self):
        self.running = True
        self.w = PygameSetUp(1000, 720, "FullStratFightTactic")
        self.fond = Fond()
        self.terrain: list = [AfficheTerrainTennis(300, 100)]
        self.arbre: list = [AfficheArbre((200, 500)), AfficheArbre((80, 600)), AfficheArbre((90, 400)), AfficheArbre((850, 150))]#, Arbre(110, 550), Arbre(250, 520), Arbre(150, 420), Arbre(self.window, 90, 620), Arbre(self.window, 800, 60)]
        self.stone: list = [AfficheStone((800, 600)), AfficheStone((830, 570)), AfficheStone((860, 600))]
        self.feu_de_camp = [AfficheCampFire((433, 100)), AfficheCampFire((566, 100))]
        self.arme: list = []
        self.player = [Player(self.arbre)]
        self.balle: list = [AfficheProjectile(self.player[0].physique[0])]
        self.etale_herbe = EtaleHerbe()
        self.etale_terre = EtaleTerre()

        self.liste_objets = self.arbre + self.stone + self.feu_de_camp + self.player[0].physique + self.balle
        self.liste_objets_tries = []

        # h = Herbe(self.w)
        # Tools.changer_couleur_image_and_save_it(h.image)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def bouton_player(self, event):
        for spirit in self.player[0].spirit:
            spirit.bouton(event)
        for physique in self.player[0].physique:
            physique.bouton(event)

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.bouton_player(event)

    def refresh_liste_affiche(self):
        self.liste_objets_tries = sorted(self.liste_objets, key=lambda objet: objet.y)

    def affiche_fond(self):
        self.fond.changement_de_fond()
        self.etale_herbe.comportement()
        # for spirit in self.player.spirit:
        #     spirit.color = self.fond.couleur_fond
        for terrain in self.terrain:
            terrain.affiche_terrain()
        self.etale_terre.comportement()

    def affiche(self):
        self.affiche_fond()
        self.refresh_liste_affiche()
        for elem in self.liste_objets_tries:
            elem.comportement()

    def game(self):
        while self.running:
            self.event()
            self.affiche()
            # self.ordre_affiche()
            pygame_params.window_refresh()
            pygame_params.fps_control()
