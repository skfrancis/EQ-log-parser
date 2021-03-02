from pprint import pprint
from trackers.fights.filters.meleefilter import MeleeFilter
from trackers.fights.filters.spellfilter import SpellFilter
from trackers.fights.filters.deathfilter import DeathFilter
from trackers.fights.filters.healingfilter import HealingFilter


class FightFilter:
    def __init__(self, display=False):
        self.display = display
        self.filters = [
            MeleeFilter(),
            SpellFilter(),
            HealingFilter(),
            DeathFilter()
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        for fight_filter in self.filters:
            parsed = fight_filter.parse(log_line)
            if parsed:
                if self.display:
                    display_data(parsed)
                return parsed
        return None
