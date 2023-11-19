import pygame

from anew.player import Player, Spectre, PierreTombale
from pygame_setup import PygameSetUp


class World:
    dimension_humain = (27, 60)
    dimension_pt = (20, 20)

    def __init__(self, conf):
        self.conf = conf

        self.player = []
        self.ennemi = []
        self.pierre_tombale = []
        self.tree = []

        Player(self, (100, 400), 3, True, self.dimension_humain)

        pt = PierreTombale(self, (500, 200), self.dimension_pt)
        # pt2 = PierreTombale(self, (600, 300), self.dimension_pt)
        # pt3 = PierreTombale(self, (450, 250), self.dimension_pt)

        e = Spectre(self, (500, 200), 1, self.dimension_humain)
        # e2 = Spectre(self, (600, 300), 1, self.dimension_humain)
        # e3 = Spectre(self, (450, 250), 1, self.dimension_humain)

        e.pierre_tombale = pt
        # e2.pierre_tombale = pt2
        # e3.pierre_tombale = pt3

    @property
    def all_objects(self):
        return self.player + self.ennemi + self.tree

    @property
    def all_objects_sorted(self):
        return sorted(self.all_objects, key=lambda objet: objet.y)

    @property
    def vivant(self):
        return list(filter(lambda personne: personne.vivant, self.all_objects))

    def run(self, window):
        for o in self.all_objects_sorted:
            o.behavior(window)

    def affiche_stat(self, w):
        police = pygame.font.Font(None, 36)

        player_vitesse = police.render(f"Vitesse : {self.player[0].vitesse:.1f}", True, (0, 0, 0))
        player_possesseur = police.render(f"Hanté : {self.player[0].effet['possession']['possesseur']}", True, (0, 0, 0))
        player_possede = police.render(f"Possession : {self.player[0].effet['possession']['possede']}", True, (0, 0, 0))
        player_is_contoled = police.render(f"Possédé : {self.player[0].effet['possession']['is_controled']}", True, (0, 0, 0))
        spectre_cible = police.render(f"cible des spectres : {[s.cible for s in self.ennemi]}", True, (0, 0, 0))

        w.window.blit(player_vitesse, (10, 10))
        w.window.blit(player_possesseur, (10, 40))
        w.window.blit(player_possede, (10, 70))
        w.window.blit(player_is_contoled, (10, 100))
        w.window.blit(spectre_cible, (300, 10))

    def button(self, event):
        for p in self.player:
            p.button(event)


class GameInstance:
    def __init__(self):
        self.running = True
        self.conf = PygameSetUp("FullStratFightTactic", 1000, 720, 60)
        self.world = World(self.conf)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.world.button(event)

    def game(self):
        f1 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (10, 10), 980, 520, "campagne")
        f2 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (10, 540), 980, 170, "monde parallèle")

        while self.running:
            self.event()

            f1.window.fill((190, 200, 90))
            f2.window.fill((180, 180, 180))

            self.world.run(f1)
            self.world.affiche_stat(f2)

            for f in self.conf.fenetres.all:
                f.comportement()

            self.conf.curseur.refresh_curseur()
            self.conf.main_window.window_refresh()
            self.conf.horloge.fps_control()


g = GameInstance()
g.game()
