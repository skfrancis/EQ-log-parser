

class FightMember:
    def __init__(self, name, target):
        self.name = name
        self.target = target
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

    def get_target(self):
        return self.target

    def add_hit(self, data):
        self.hits['attack'].append(data.pop('attack'))
        self.hits['amount'].append(data.pop('amount'))
        self.hits['damagemod'].append(data.pop('damagemod'))

    def add_miss(self, data):
        self.misses['attack'].append(data.pop('attack'))
        self.misses['amount'].append(data.pop('amount'))
        self.misses['damagemod'].append(data.pop('damagemod'))
