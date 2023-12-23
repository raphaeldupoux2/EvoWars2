import pygame

from anew.world.camera import Camera
from anew.world.domaine_mortuaire.cimetiere import Cimetiere
from anew.world.player import Player
from anew.world.zone import Zone


class World:
    dimension_humain = (27, 60)
    dimension_pt = (20, 20)

    def __init__(self, conf):
        self.conf = conf

        self.player = []
        self.spectre = []
        self.pierre_tombale = []
        self.marqueur = []
        self.zone = []

        zone = Zone(self, (0, 0), 800)

        player1 = Player(self, (100, 400), 3, self.dimension_humain, 300, 500, zone, numero=1)
        player2 = Player(self, (100, 200), 3, self.dimension_humain, 300, 500, zone, numero=2)

        Cimetiere(self, (350, 250))

        self.camera = Camera(self, (100, 100), player2)

        self.indice_personnage_control = 0
        self.liste_personnage_control = []
        self.liste_personnage_control.extend(self.player)

    @property
    def all_objects(self):
        return self.player + self.spectre + self.pierre_tombale + [self.camera] + self.marqueur + self.zone

    @property
    def all_objects_sorted(self):
        return sorted(self.all_objects, key=lambda objet: objet.y)

    @property
    def vivant(self):
        return list(filter(lambda personne: personne.famille.type_objet == "creature" and personne.famille.vivant, self.all_objects))

    @property
    def personnage_control(self):
        return self.liste_personnage_control[self.indice_personnage_control]

    def run(self, window):
        for o in self.all_objects_sorted:
            o.behavior(window)
        self.camera.cible = self.personnage_control

    def affiche_stat(self, w):
        police = pygame.font.Font(None, 36)

        player_vitesse = police.render(f"Vitesse : {self.personnage_control.vitesse:.1f}", True, (0, 0, 0))
        player_possesseur = police.render(f"Hanté : {self.personnage_control.etat.possession['possesseur']}", True, (0, 0, 0))
        player_possede = police.render(f"Possession : {self.personnage_control.etat.possession['intensity']:.0f}", True, (0, 0, 0))
        player_is_contoled = police.render(f"Possédé : {self.personnage_control.etat.possession['is_controled']}", True, (0, 0, 0))
        player_position = police.render(f"Position : {self.personnage_control.x_abs:.0f}, {self.personnage_control.y_abs:.0f}", True, (0, 0, 0))
        spectre_cible = police.render(f"cible des spectres : {[s.cible for s in self.spectre]}", True, (0, 0, 0))

        w.window.blit(player_vitesse, (10, 10))
        w.window.blit(player_position, (10, 40))
        w.window.blit(player_possesseur, (300, 10))
        w.window.blit(player_possede, (300, 40))
        w.window.blit(player_is_contoled, (300, 70))
        w.window.blit(spectre_cible, (700, 10))
