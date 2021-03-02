import datetime
from uuid import uuid4
from trackers.fights.fightmember import FightMember


class FightEvent:
    def __init__(self, target):
        self.start_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.uuid = str(uuid4())
        self.target = FightMember(target)
        self.members = []

    def parse_event(self, event_data):
        source = event_data.get('Source')
        fight_member = self.get_fight_member(source)
        if event_data.get('Type') == 'hit':
            fight_member.add_hit(event_data)
        elif event_data.get('Type') == 'miss':
            fight_member.add_miss(event_data)
        elif event_data.get('Type') == 'heal':
            fight_member.add_heal(event_data)
        elif event_data.get('Type') == 'death':
            fight_member.add_death(event_data)

    def get_fight_member(self, source):
        fight_member = None
        if source == self.target.get_member_name():
            return self.target
        for member in self.members:
            if source == member.get_member_name():
                fight_member = member
                break
        if not fight_member:
            fight_member = FightMember(source)
            self.members.append(fight_member)
        return fight_member

    def complete_fight(self):
        pass
