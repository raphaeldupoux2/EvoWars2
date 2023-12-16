import pygame

from anew.world.camera import Camera
from anew.world.domaine_mortuaire.cimetiere import Cimetiere
from anew.world.player import Player


class World:
    dimension_humain = (27, 60)
    dimension_pt = (20, 20)

    def __init__(self, conf):
        self.conf = conf

        self.player = []
        self.spectre = []
        self.pierre_tombale = []
        self.marqueur = []

        player1 = Player(self, (100, 400), 3, self.dimension_humain, 300, 500)
        player2 = Player(self, (100, 200), 3, self.dimension_humain, 300, 500)

        Cimetiere(self)

        self.camera = Camera(self, (100, 100), player1)

    @property
    def all_objects(self):
        return self.player + self.spectre + self.pierre_tombale + [self.camera] + self.marqueur

    @property
    def all_objects_sorted(self):
        return sorted(self.all_objects, key=lambda objet: objet.y)

    @property
    def vivant(self):
        return list(filter(lambda personne: personne.famille.type_objet == "creature" and personne.famille.vivant, self.all_objects))

    def run(self, window):
        for o in self.all_objects_sorted:
            o.behavior(window)

    def affiche_stat(self, w):
        police = pygame.font.Font(None, 36)

        player_vitesse = police.render(f"Vitesse : {self.player[0].vitesse:.1f}", True, (0, 0, 0))
        player_possesseur = police.render(f"Hanté : {self.player[0].etat.possession['possesseur']}", True, (0, 0, 0))
        player_possede = police.render(f"Possession : {self.player[0].etat.possession['intensity']}", True, (0, 0, 0))
        player_is_contoled = police.render(f"Possédé : {self.player[0].etat.possession['is_controled']}", True, (0, 0, 0))
        spectre_cible = police.render(f"cible des spectres : {[s.cible for s in self.spectre]}", True, (0, 0, 0))

        w.window.blit(player_vitesse, (10, 10))
        w.window.blit(player_possesseur, (10, 40))
        w.window.blit(player_possede, (10, 70))
        w.window.blit(player_is_contoled, (10, 100))
        w.window.blit(spectre_cible, (300, 10))
