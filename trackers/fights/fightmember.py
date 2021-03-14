import pandas as pd


class FightMember:
    def __init__(self, name, char_class=None, level=None):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.death_count = 0
        self.total_dmg = 0
        self.total_hits = 0
        self.total_misses = 0
        self.hits = []
        self.misses = []
        self.duration = {
            'first_attack': None,
            'final_attack': None
        }

    def get_member_name(self):
        return self.name

    def add_hit(self, hit_data):
        self._update_attack_time(hit_data.get('Timestamp'))
        self.total_hits += 1
        self.total_dmg += int(hit_data.get('Amount'))
        attack = hit_data.get('Attack')
        if any(hit['attack'] for hit in self.hits if attack == hit['attack']):
            index = [i for i, hit in enumerate(self.hits) if attack == hit['attack']]
            hit = self.hits[index[0]]
            if int(hit_data.get('Amount')) > hit['max']:
                hit['max'] = int(hit_data.get('Amount'))
            hit['damage'] += int(hit_data.get('Amount'))
            hit['count'] += 1
        else:
            self.hits.append({
               'attack': attack,
               'max': int(hit_data.get('Amount')),
               'damage': int(hit_data.get('Amount')),
               'count': 1
            })

    def add_miss(self, miss_data):
        self._update_attack_time(miss_data.get('Timestamp'))
        self.total_misses += 1
        attack = miss_data.get('Attack')
        if any(miss['miss'] for miss in self.misses if attack == miss['miss']):
            index = [i for i, miss in enumerate(self.misses) if attack == miss['miss']]
            miss = self.misses[index[0]]
            miss['count'] += 1
        else:
            self.misses.append({
                'miss': attack,
                'count': 1
            })

    def add_heal(self, heal_data):
        pass

    def add_death(self, death_data):
        self._set_fight_target(death_data.get('Source'))
        self._update_attack_time(death_data.get('Timestamp'))
        self.death_count += 1

    def get_fight_data(self):
        index = ['name', 'class', 'level', 'duration', 'death count', 'total damage', 'total hits', 'total misses']
        data = [
            self.name,
            self.char_class,
            self.level,
            int(self._get_duration()),
            self.death_count,
            self.total_dmg,
            self.total_hits,
            self.total_misses
        ]
        return {
            'data': pd.DataFrame(data, index=index),
            'hits': pd.DataFrame(self.hits),
            'misses': pd.DataFrame(self.misses)
        }

    def _update_attack_time(self, timestamp):
        if not self.duration.get('first_attack'):
            self.duration['first_attack'] = timestamp
        self.duration['final_attack'] = timestamp

    def _get_duration(self):
        duration = self.duration.get('final_attack') - self.duration.get('first_attack')
        duration = duration.total_seconds()
        return duration if int(duration) > 0 else 1
