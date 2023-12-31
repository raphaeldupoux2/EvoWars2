import pygame

from anew.world.camera import Camera
from anew.world.clee import Clee
from anew.world.domaine_mortuaire.cimetiere import Cimetiere
from anew.world.player import Player
from anew.world.zone import Zone


class World:
    dimension_humain = (27, 60)
    dimension_pt = (20, 20)
    cote_zone = 500

    def __init__(self, conf):
        self.conf = conf

        self.player = []
        self.spectre = []
        self.pierre_tombale = []
        self.fireball = []
        self.marqueur = []
        self.zone = []
        self.clee = []

        self.camera = Camera(self, (100, 100))

        # ZONE 1 Cimetière
        zone = Zone(self, (0, 0), self.cote_zone)
        player1 = Player(self, (100, 200), 3, self.dimension_humain, 300, 500, zone, numero=1)
        player2 = Player(self, (-100, 400), 3, self.dimension_humain, 300, 500, zone, numero=2)
        player4 = Player(self, (-100, 400), 3, self.dimension_humain, 300, 500, zone, numero=4)
        zone2 = Zone(self, (-self.cote_zone, 0), self.cote_zone)
        zone3 = Zone(self, (-self.cote_zone, -self.cote_zone), self.cote_zone)
        player3 = Player(self, (-100, 400), 3, self.dimension_humain, 300, 500, zone3, numero=3)
        zone4 = Zone(self, (0, -self.cote_zone), self.cote_zone)
        zone5 = Zone(self, (0, self.cote_zone), self.cote_zone)
        zone6 = Zone(self, (self.cote_zone, 0), self.cote_zone)
        Cimetiere(self, (650, 150), zone6)
        zone7 = Zone(self, (self.cote_zone, self.cote_zone), self.cote_zone)
        Clee(self, (0, 0), (self.cote_zone, self.cote_zone))

        for z in self.zone:
            z.placement_tapis()

        self.camera.cible = player1

        self.indice_personnage_control = 0
        self.liste_personnage_control = []
        self.liste_personnage_control.extend(self.player)

    @property
    def all_objects(self):
        return self.player + self.spectre + self.pierre_tombale + [self.camera] + self.marqueur + self.zone + self.fireball + self.clee

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
