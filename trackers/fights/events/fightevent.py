import datetime
from uuid import uuid4
from trackers.fights.fightmember import FightMember


class FightEvent:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.uuid = str(uuid4())
        self.target = None
        self.members = []

    def parse_event(self, event_data):
        self.updated_time = datetime.datetime.now()
        source = event_data.get('Source')
        target = event_data.get('Target')

        if event_data.get('Type') == 'hit':
            fight_member = self.get_fight_member(source)
            fight_member.add_hit(event_data)
        elif event_data.get('Type') == 'miss':
            fight_member = self.get_fight_member(source)
            fight_member.add_miss(event_data)
        elif event_data.get('Type') == 'death':
            return self.complete_fight()
        return None

    def get_fight_member(self, source):
        fight_member = None
        for member in self.members:
            if source == member.get_member_name():
                fight_member = member
                break
        if not fight_member:
            fight_member = FightMember(source)
            self.members.append(fight_member)
        return fight_member

    def complete_fight(self):
        fight_data = []
        for member in self.members:
            fight_data.append(member.get_fight_data())
        return fight_data
