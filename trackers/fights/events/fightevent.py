from trackers.fights.filters.meleefilter import MeleeFilter
from trackers.fights.filters.spellfilter import SpellFilter
from trackers.fights.filters.deathfilter import DeathFilter


class FightEvent:
    def __init__(self):
        self.melee_filter = MeleeFilter()
        self.spell_filter = SpellFilter()
        self.death_filter = DeathFilter()

    def parse(self, log_line):
        result = self.melee_filter.parse(log_line)
        if result:
            return result
        result = self.spell_filter.parse(log_line)
        if result:
            return result
        result = self.death_filter.parse(log_line)
        if result:
            return result

        return None


