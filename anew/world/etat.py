class Etat:
    def __init__(self, slow_max=300, possession_max=500):
        self.slow = 0
        self.slow_max = slow_max
        self.possession = {'intensity': 0,
                           'possesseur': None,
                           'is_controled': False}
        self.possession_max = possession_max
        self.is_being_possessed = False
        self.is_being_slow = False

    def slow_accumulation(self, add):
        self.slow = min(self.slow + add, self.slow_max)

    def possession_accumulation(self, add):
        self.possession['intensity'] = min(self.possession['intensity'] + add, self.possession_max)
