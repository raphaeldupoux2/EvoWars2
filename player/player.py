from player.player_physique import PlayerPhysique
from player.player_spirit import PlayerSpirit


class Player:
    def __init__(self, window, liste_obstacle):
        self.physique = [PlayerPhysique(window, liste_obstacle)]
        self.spirit = []  # [PlayerSpirit(window)]
