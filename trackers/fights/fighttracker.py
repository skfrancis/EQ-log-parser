from trackers.fights.events.fightevent import FightFilter
from trackers.fights.fightmember import FightMember


class FightTracker:
    def __init__(self):
        self.fight_event = FightFilter()
        self.members = []

    def parse(self, log_line):
        current_member = None
        result = self.fight_event.parse(log_line)
        if result:
            source = result.get('source')
            for member in self.members:
                if source in member.get_name():
                    current_member = member
                    break
            if not current_member:
                current_member = FightMember(source)
                self.members.append(current_member)

            amount = result.get('amount')
            if amount == 'death':
                return self._complete_fight()
            elif amount == 'miss' or amount == 'resist':
                current_member.add_miss(result)
            else:
                current_member.add_hit(result)

    def _complete_fight(self):
        fight = []
        for member in self.members:
            fight.append(member.get_fight_data())
        return fight
