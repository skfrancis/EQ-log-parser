import pandas as pd


class FightMember:
    def __init__(self, name, char_class='', level=0):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.totals = {
            'total_hits': 0,
            'total_dmg': 0,
            'total_misses': 0,
            'total_heals': 0,
            'total_healing': 0,
            'total_over_healing': 0,
            'total_deaths': 0
        }
        self.outbound_dmg = []
        self.outbound_misses = []
        self.outbound_heals = []
        self.inbound_dmg = []
        self.inbound_heals = []
        self.duration = {
            'first_attack': None,
            'final_attack': None
        }

    def get_member_name(self):
        return self.name

    def add_hit(self, hit_data):
        self._update_attack_time(hit_data.get('Timestamp'))
        self.totals['total_hits'] += 1
        self.totals['total_dmg'] += int(hit_data.get('Amount'))
        if hit_data.get('Ability')[0].isupper():
            ability = hit_data.get('Ability')
        else:
            ability = hit_data.get('Ability').capitalize()
        mod = hit_data.get('Mod')
        if any(hit['Ability'] for hit in self.outbound_dmg if ability == hit['Ability']):
            index = [i for i, hit in enumerate(self.outbound_dmg) if ability == hit['Ability']]
            hit = self.outbound_dmg[index[0]]
            if int(hit_data.get('Amount')) > hit['Max']:
                hit['Max'] = int(hit_data.get('Amount'))
            hit['Damage'] += int(hit_data.get('Amount'))
            hit['Count'] += 1
            if mod:
                mod = mod.capitalize()
                hit[mod] = hit.setdefault(mod, 0) + 1
        else:
            data = {
                'Ability': ability,
                'Max': int(hit_data.get('Amount')),
                'Damage': int(hit_data.get('Amount')),
                'Count': 1
            }
            if mod:
                mod = mod.capitalize()
                data[mod] = 1
            self.outbound_dmg.append(data)

    def add_miss(self, miss_data):
        self._update_attack_time(miss_data.get('Timestamp'))
        self.totals['total_misses'] += 1
        if miss_data.get('Ability')[0].isupper():
            ability = miss_data.get('Ability')
        else:
            ability = miss_data.get('Ability').capitalize()
        mod = miss_data.get('Mod')
        if any(miss['Ability'] for miss in self.outbound_misses if ability == miss['Ability']):
            index = [i for i, miss in enumerate(self.outbound_misses) if ability == miss['Ability']]
            miss = self.outbound_misses[index[0]]
            if mod:
                mod = mod.capitalize()
                miss[mod] = miss.setdefault(mod, 0) + 1
            else:
                mod = miss_data.get('Amount').capitalize()
                miss[mod] = miss.setdefault(mod, 0) + 1
        else:
            if mod:
                mod = mod.capitalize()
            else:
                mod = miss_data.get('Amount').capitalize()
            self.outbound_misses.append({
                'Ability': ability,
                mod: 1
            })

    def add_heal(self, heal_data):
        self._update_attack_time(heal_data.get('Timestamp'))
        self.totals['total_heals'] += 1
        self.totals['total_healing'] += int(heal_data.get('Amount')[0])
        self.totals['total_over_healing'] += int(heal_data.get('Amount')[1])
        if heal_data.get('Ability')[0].isupper():
            ability = heal_data.get('Ability')
        else:
            ability = heal_data.get('Ability').capitalize()
        mod = heal_data.get('mod')
        if any(heal['Ability'] for heal in self.outbound_heals if ability == heal['Ability']):
            index = [i for i, heal in enumerate(self.outbound_heals) if ability == heal['Ability']]
            heal = self.outbound_heals[index[0]]
            actual_heal = heal_data.get('Amount')[0]
            max_heal = heal_data.get('Amount')[1]
            if int(actual_heal) > heal['Max']:
                heal['Max'] = int(actual_heal)
            heal['Actual'] += int(actual_heal)
            heal['Overage'] += int(max_heal)
            heal['Count'] += 1
            if mod:
                mod = mod.capitalize()
                heal[mod] = heal.setdefault(mod, 0) + 1
        else:
            actual_heal = heal_data.get('Amount')[0]
            max_heal = heal_data.get('Amount')[1]
            data = {
                'Ability': ability,
                'Max': int(actual_heal),
                'Actual': int(actual_heal),
                'Overage': int(max_heal),
                'Count': 1
            }
            if mod:
                mod = mod.capitalize()
                data[mod] = 1
            self.outbound_heals.append(data)

    def add_death(self, death_data):
        self._update_attack_time(death_data.get('Timestamp'))
        self.totals['total_deaths'] += 1

    def get_fight_data(self):
        index = ['Name', 'Class', 'Level', 'Duration', 'Death Count',
                 'Total Damage', 'Total Hits', 'Total Misses', 'Total Heals',
                 'Total Actual Healing', 'Total Over Healing']
        data = [
            self.name,
            self.char_class,
            self.level,
            int(self._get_duration()),
            self.totals.get('total_deaths'),
            self.totals.get('total_dmg'),
            self.totals.get('total_hits'),
            self.totals.get('total_misses'),
            self.totals.get('total_heals'),
            self.totals.get('total_healing'),
            self.totals.get('total_over_healing')
        ]
        return {
            'data': pd.DataFrame(data, index=index).fillna(0, downcast='infer'),
            'hits': pd.DataFrame(self.outbound_dmg).fillna(0, downcast='infer'),
            'misses': pd.DataFrame(self.outbound_misses).fillna(0, downcast='infer'),
            'heals': pd.DataFrame(self.outbound_heals).fillna(0, downcast='infer')
        }

    def _update_attack_time(self, timestamp):
        if not self.duration.get('first_attack'):
            self.duration['first_attack'] = timestamp
        self.duration['final_attack'] = timestamp

    def _get_duration(self):
        if self.duration.get('final_attack') and self.duration.get('first_attack'):
            duration = self.duration.get('final_attack') - self.duration.get('first_attack')
            duration = duration.total_seconds()
            return duration if int(duration) > 0 else 1
        else:
            return 1
