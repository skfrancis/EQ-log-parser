import pandas as pd


# noinspection DuplicatedCode
class FightMember:
    def __init__(self, name):
        self.name = name
        self.first_attack = None
        self.last_attack = None
        self.hits = {
            'attack':  [],
            'amount': [],
            'damagemod': []
        }
        self.misses = {
            'attack':  [],
            'amount': [],
            'damagemod': []
        }

    def get_name(self):
        return self.name

    def add_hit(self, hit_data):
        self._update_attack_time(hit_data.pop('timestamp'))
        self.hits['attack'].append(hit_data.pop('attack'))
        self.hits['amount'].append(hit_data.pop('amount'))
        self.hits['damagemod'].append(hit_data.pop('damagemod'))

    def add_miss(self, miss_data):
        self._update_attack_time(miss_data.pop('timestamp'))
        self.misses['attack'].append(miss_data.pop('attack'))
        self.misses['amount'].append(miss_data.pop('amount'))
        self.misses['damagemod'].append(miss_data.pop('damagemod'))

    def _update_attack_time(self, timestamp):
        if not self.first_attack:
            self.first_attack = timestamp
        self.last_attack = timestamp

    def get_fight_data(self):
        return {
            'member': self.name,
            'first_attack': self.first_attack,
            'last_attack': self.last_attack,
            'hits': pd.DataFrame(self.hits),
            'misses': pd.DataFrame(self.misses)
        }

