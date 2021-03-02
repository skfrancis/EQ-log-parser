

class FightMember:
    def __init__(self, name):
        self.name = name
        self.target = None
        self.death_count = 0
        self.duration = {
            'first_attack': None,
            'final_attack': None
        }
        self.hits = {
            'total_dmg': 0,
            'total_hits': 0,
            'attacks': []
        }
        self.misses = {
            'total_misses': 0,
            'misses': []
        }
        self.heals = {
            'attack': [],
            'amount': [],
            'mod': []
        }

    def get_member_name(self):
        return self.name

    def get_duration(self):
        duration = self.duration.get('final_attack') - self.duration.get('first_attack')
        return duration.total_seconds()

    def add_hit(self, hit_data):
        self._set_fight_target(hit_data.get('Target'))
        self._update_attack_time(hit_data.get('Timestamp'))
        self.hits['total_hits'] += 1
        self.hits['total_dmg'] += int(hit_data.get('Amount'))
        attack = hit_data.get('Attack')
        if any(hit for hit in self.hits.get('attacks') if attack in hit):
            index = [i for i, hit in enumerate(self.hits.get('attacks')) if attack in hit]
            hit = self.hits.get('attacks')[index[0]]
            hit[attack] += int(hit_data.get('Amount'))
            hit['count'] += 1
        else:
            self.hits.get('attacks').append({
                attack: int(hit_data.get('Amount')),
                'count': 1
            })

    def add_miss(self, miss_data):
        self._set_fight_target(miss_data.get('Target'))
        self._update_attack_time(miss_data.get('Timestamp'))
        self.misses['total_misses'] += 1
        attack = miss_data.get('Attack')
        if any(miss for miss in self.misses.get('misses') if attack in miss):
            index = [i for i, miss in enumerate(self.misses.get('misses')) if attack in miss]
            miss = self.misses.get('misses')[index[0]]
            miss[attack] += 1
        else:
            self.misses.get('misses').append({attack: 1})

    def add_heal(self, heal_data):
        self._update_attack_time(heal_data.get('Timestamp'))
        self.hits['attack'].append(heal_data.pop('Attack'))
        self.hits['amount'].append(heal_data.pop('Amount'))

    def add_death(self, death_data):
        self._set_fight_target(death_data.get('Source'))
        self._update_attack_time(death_data.get('Timestamp'))
        self.death_count += 1

    def get_fight_data(self):
        return {
            'name': self.name,
            'target': self.target,
            'duration': self.get_duration(),
            'death_count': self.death_count,
            'hits': self.hits,
            'misses': self.misses
        }

    def _set_fight_target(self, target):
        if not self.target:
            self.target = target

    def _update_attack_time(self, timestamp):
        if not self.duration.get('first_attack'):
            self.duration['first_attack'] = timestamp
        self.duration['final_attack'] = timestamp
