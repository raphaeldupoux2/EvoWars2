import pygame

from anew.player import Player, Spectre, PierreTombale
from pygame_setup import PygameSetUp


class Cimetiere:
    def __init__(self, monde):
        pt = PierreTombale(monde, (500, 200), monde.dimension_pt)
        pt2 = PierreTombale(monde, (600, 200), monde.dimension_pt)
        pt3 = PierreTombale(monde, (700, 200), monde.dimension_pt)

        e = Spectre(monde, (500, 200), 1, monde.dimension_humain)
        e2 = Spectre(monde, (600, 200), 1, monde.dimension_humain)
        e3 = Spectre(monde, (700, 200), 1, monde.dimension_humain)

        e.pierre_tombale = pt
        e2.pierre_tombale = pt2
        e3.pierre_tombale = pt3

        pt4 = PierreTombale(monde, (500, 300), monde.dimension_pt)
        pt5 = PierreTombale(monde, (600, 300), monde.dimension_pt)
        pt6 = PierreTombale(monde, (700, 300), monde.dimension_pt)

        e4 = Spectre(monde, (500, 300), 1, monde.dimension_humain)
        e5 = Spectre(monde, (600, 300), 1, monde.dimension_humain)
        e6 = Spectre(monde, (700, 300), 1, monde.dimension_humain)

        e4.pierre_tombale = pt4
        e5.pierre_tombale = pt5
        e6.pierre_tombale = pt6


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
        Cimetiere(self)

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
        f2 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (10, 540), 980, 170, "stats")

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
