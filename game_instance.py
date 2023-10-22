import pygame

from EvoWars2.logique.elementaire import Elementaire
from EvoWars2.picture.tools import Tools
from EvoWars2.sprite.elementaire import ImageElementaire
from EvoWars2.sprite.feu_de_camp import AfficheCampFire
from EvoWars2.sprite.fond import Fond, EtaleHerbe, EtaleTerre
from sprite.arbre import AfficheArbre
from EvoWars2.logique.player import Player
from sprite.stone import AfficheStone
from sprite.terrain_tennis import AfficheTerrainTennis
from pygamesetup import PygameSetUp, SousFenetre
from sprite.projectile import AfficheProjectile


class Map:
    def __init__(self, f, curseur):
        self.curseur = curseur
        self.fond = Fond(f.f1)
        self.fond2 = Fond(f.f2)
        self.terrain: list = [AfficheTerrainTennis(f.f1, 300, 100)]
        self.arbre: list = [AfficheArbre(f.f1, (200, 500)), AfficheArbre(f.f1, (80, 600)), AfficheArbre(f.f1, (90, 400)), AfficheArbre(f.f1, (850, 150))]  # , Arbre(f.f1indow, 110, 550), Arbre(f.f1indow, 250, 520), Arbre(f.f1indow, 150, 420), Arbre(f.f1indow, 90, 620), Arbre(f.f1indow, 800, 60)]
        self.stone: list = [AfficheStone(f.f1, (800, 600)), AfficheStone(f.f1, (830, 570)), AfficheStone(f.f1, (860, 600))]
        self.feu_de_camp = [AfficheCampFire(f.f1, (433, 100)), AfficheCampFire(f.f1, (566, 100))]
        self.arme: list = []
        self.player = [Player(f.f1, self.curseur, (f.f1.width / 2, f.f1.height * 2 / 3), self.arbre), Player(f.f2, self.curseur, (f.f1.width / 2, f.f1.height * 2 / 3), self.arbre)]
        self.balle: list = [AfficheProjectile(f.f1, curseur, (f.f1.width / 2, f.f1.height / 2), self.player[0])]
        self.etale_herbe = EtaleHerbe(f.f1)
        self.etale_terre = EtaleTerre(f.f1)
        self.elementaire = [Elementaire(f.f1, (f.f2.width / 2, f.f2.height * 2 / 3))]

        self._liste_objets = self.arbre + self.stone + self.feu_de_camp + self.player + self.balle + self.elementaire
        self.liste_objets_tries = []

        # h = Herbe(self.conf.fenetre1)
        # Tools.changer_couleur_image_and_save_it(h.image)

    def bouton_player(self, event):
        for p in self.player:
            p.bouton(event)

    def bouton(self, event):
        self.bouton_player(event)

    def refresh_liste_affiche(self):
        self.liste_objets_tries = sorted(self._liste_objets, key=lambda objet: objet.y)

    def affiche_fond(self):
        self.fond.changement_de_fond()
        self.fond2.changement_de_fond()
        self.etale_herbe.comportement()
        for terrain in self.terrain:
            terrain.affiche_terrain()
        self.etale_terre.comportement()

    def affiche(self):
        self.affiche_fond()
        self.refresh_liste_affiche()
        for elem in self.liste_objets_tries:
            elem.comportement()


class GameInstance:
    def __init__(self):
        self.running = True
        self.conf = PygameSetUp()
        self.map = Map(self.conf.fenetres, self.conf.curseur)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.map.bouton(event)

    def game(self):
        while self.running:
            self.event()
            self.map.affiche()

            for f in self.conf.fenetres.all:
                f.comportement()

            self.conf.curseur.refresh_curseur()
            self.conf.main_window.window_refresh()
            self.conf.fps_control()
