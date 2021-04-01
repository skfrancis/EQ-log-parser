import pandas as pd


class FightMember:
    def __init__(self, name, char_class='', level=0):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.totals = {
            'total_outbound_dmg': 0,
            'total_hits': 0,
            'total_misses': 0,
            'total_inbound_dmg': 0,
            'total_heals': 0,
            'total_healing': 0,
            'total_over_healing': 0,
            'total_healed': 0,
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
        self.pet = None

    def get_member_name(self):
        return self.name

    def add_hit(self, hit_data):
        self._update_participation_time(hit_data.get('Timestamp'))
        self.totals['total_hits'] += 1
        self.totals['total_outbound_dmg'] += int(hit_data.get('Amount'))
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

    def add_damage(self, dmg_data):
        self._update_participation_time(dmg_data.get('Timestamp'))
        self.totals['total_inbound_dmg'] += int(dmg_data.get('Amount'))
        if dmg_data.get('Ability')[0].isupper():
            ability = dmg_data.get('Ability')
        else:
            ability = dmg_data.get('Ability').capitalize()
        mod = dmg_data.get('Mod')
        if any(dmg['Ability'] for dmg in self.inbound_dmg if ability == dmg['Ability']):
            index = [i for i, dmg in enumerate(self.inbound_dmg) if ability == dmg['Ability']]
            dmg = self.inbound_dmg[index[0]]
            if int(dmg_data.get('Amount')) > dmg['Max']:
                dmg['Max'] = int(dmg_data.get('Amount'))
            dmg['Damage'] += int(dmg_data.get('Amount'))
            dmg['Count'] += 1
            if mod:
                mod = mod.capitalize()
                dmg[mod] = dmg.setdefault(mod, 0) + 1
        else:
            data = {
                'Ability': ability,
                'Max': int(dmg_data.get('Amount')),
                'Damage': int(dmg_data.get('Amount')),
                'Count': 1
            }
            if mod:
                mod = mod.capitalize()
                data[mod] = 1
            self.inbound_dmg.append(data)

    def add_miss(self, miss_data):
        self._update_participation_time(miss_data.get('Timestamp'))
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
        self._update_participation_time(heal_data.get('Timestamp'))
        self.totals['total_heals'] += 1
        self.totals['total_healing'] += int(heal_data.get('Amount')[0])
        self.totals['total_over_healing'] += (int(heal_data.get('Amount')[1]) - int(heal_data.get('Amount')[0]))
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
            heal['Overage'] += (int(max_heal) - int(actual_heal))
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
                'Overage': (int(max_heal) - int(actual_heal)),
                'Count': 1
            }
            if mod:
                mod = mod.capitalize()
                data[mod] = 1
            self.outbound_heals.append(data)

    def add_healing(self, healed_data):
        self._update_participation_time(healed_data.get('Timestamp'))
        self.totals['total_healed'] += int(healed_data.get('Amount')[0])
        if healed_data.get('Ability')[0].isupper():
            ability = healed_data.get('Ability')
        else:
            ability = healed_data.get('Ability').capitalize()
        mod = healed_data.get('mod')
        if any(heal['Ability'] for heal in self.inbound_heals if ability == heal['Ability']):
            index = [i for i, heal in enumerate(self.inbound_heals) if ability == heal['Ability']]
            heal = self.inbound_heals[index[0]]
            actual_heal = healed_data.get('Amount')[0]
            heal['Actual'] += int(actual_heal)
            heal['Count'] += 1
            if mod:
                mod = mod.capitalize()
                heal[mod] = heal.setdefault(mod, 0) + 1
        else:
            actual_heal = healed_data.get('Amount')[0]
            data = {
                'Ability': ability,
                'Max': int(actual_heal),
                'Actual': int(actual_heal),
                'Count': 1
            }
            if mod:
                mod = mod.capitalize()
                data[mod] = 1
            self.inbound_heals.append(data)

    def add_death(self, death_data):
        self._update_participation_time(death_data.get('Timestamp'))
        self.totals['total_deaths'] += 1

    def get_fight_data(self):
        index = ['Name', 'Class', 'Level', 'Duration',
                 'Total Damage (OB)', 'Total Hits (OB)', 'Total Misses (OB)',
                 'Total Heals (OB)', 'Total Actual Healing (OB)', 'Total Healing Overage (OB)',
                 'Total Damage (IB)', 'Total Healing (IB)', 'Death Count'
        ]
        data = [
            self.name,
            self.char_class,
            self.level,
            int(self._get_duration()),
            self.totals.get('total_outbound_dmg'),
            self.totals.get('total_hits'),
            self.totals.get('total_misses'),
            self.totals.get('total_heals'),
            self.totals.get('total_healing'),
            self.totals.get('total_over_healing'),
            self.totals.get('total_inbound_dmg'),
            self.totals.get('total_healed'),
            self.totals.get('total_deaths'),
        ]
        return {
            'data': pd.DataFrame(data, index=index).fillna(0, downcast='infer'),
            'hits': pd.DataFrame(self.outbound_dmg).fillna(0, downcast='infer'),
            'misses': pd.DataFrame(self.outbound_misses).fillna(0, downcast='infer'),
            'heals': pd.DataFrame(self.outbound_heals).fillna(0, downcast='infer'),
            'damage': pd.DataFrame(self.inbound_dmg).fillna(0, downcast='infer'),
            'healing': pd.DataFrame(self.inbound_heals).fillna(0, downcast='infer')
        }

    def _update_participation_time(self, timestamp):
        if not self.duration.get('first_attack'):
            self.duration['first_attack'] = timestamp
        self.duration['final_attack'] = timestamp

    def _get_duration(self):
        duration = 1
        if self.duration.get('final_attack') and self.duration.get('first_attack'):
            actual_duration = self.duration.get('final_attack') - self.duration.get('first_attack')
            actual_duration = actual_duration.total_seconds()
            duration = actual_duration if int(actual_duration) > duration else duration
        return duration
