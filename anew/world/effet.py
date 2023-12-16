from anew.world.acteur import Acteur
from anew.world.etat import Etat


class Effet:
    def __init__(self, monde, acteur: Acteur, etat: Etat):
        self.monde = monde
        self.acteur = acteur
        self.etat = etat

    def slow_effect(self):
        if self.etat.slow > 0:
            self.acteur.vitesse = max(3 / 4 * self.acteur.vitesse_ref - self.etat.slow / 100, 0) + self.acteur.vitesse_ref / 4

    def possession_effect(self):
        if self.etat.possession['is_controled'] is True:
            self.acteur.move_to_position((self.etat.possession['possesseur'].x, self.etat.possession['possesseur'].y))

    def retablissement(self):
        if not self.etat.is_being_slow:
            self.etat.slow = max(self.etat.slow - 1/2, 0)
        if not self.etat.is_being_possessed:
            self.etat.possession['intensity'] = max(self.etat.possession['intensity'] - 1/5, 0)
        if self.etat.possession['intensity'] <= 200:
            self.etat.possession['is_controled'] = False
        if self.etat.possession['intensity'] <= 0:
            self.etat.possession['possesseur'] = None
        if self.etat.is_being_slow:
            compte_slow_instance = 0
            for s in self.monde.spectre:
                if self.acteur.distance_avec((s.x, s.y)) < s.slow_radius:
                    compte_slow_instance += 1
                    break
            if compte_slow_instance == 0:
                self.etat.is_being_slow = False
        if self.etat.is_being_possessed:
            compte_possession_instance = 0
            for s in self.monde.spectre:
                if self.acteur.distance_avec((s.x, s.y)) < s.possession_radius:
                    compte_possession_instance += 1
                    break
            if compte_possession_instance == 0:
                self.etat.is_being_possessed = False

    def apply(self):
        self.slow_effect()
        self.possession_effect()
        self.retablissement()
