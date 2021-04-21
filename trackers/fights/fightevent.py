from uuid import uuid4

from trackers.fights.fightmember import FightMember


class FightEvent:
    def __init__(self, target, start_time):
        self.start_time = start_time
        self.end_time = start_time
        self.uuid = str(uuid4())
        self.target = FightMember(target)
        self.members = [self.target]

    def get_target(self):
        return self.target

    def parse_event(self, event_data):
        self.end_time = event_data.get('Timestamp')
        source = self.get_fight_member(event_data.get('Source'))
        target = self.get_fight_member(event_data.get('Target'))

        if event_data.get('Type') == 'nonspell hit' or event_data.get('Type') == 'spell hit':
            source.add_hit(event_data)
            target.add_damage(event_data)
        elif event_data.get('Type') == 'nonspell miss' or event_data.get('Type') == 'spell miss':
            source.add_miss(event_data)
            target.add_avoidance(event_data)
        elif event_data.get('Type') == 'heal':
            source.add_heal(event_data)
            target.add_healing(event_data)
        elif event_data.get('Type') == 'death':
            if target.get_name() == self.target.get_name():
                target.add_death(event_data)
                return self.complete_fight()
            else:
                target.add_death(event_data)
        return None

    def get_fight_member(self, fight_member):
        if any(member.get_name() for member in self.members if fight_member == member.get_name()):
            index = [i for i, member in enumerate(self.members) if fight_member == member.get_name()]
            return self.members[index[0]]
        else:
            new_member = FightMember(fight_member)
            self.members.append(new_member)
            return new_member

    def get_duration(self):
        duration = 1
        if self.start_time and self.end_time:
            actual_duration = self.end_time - self.start_time
            actual_duration = actual_duration.total_seconds()
            duration = actual_duration if int(actual_duration) > duration else duration
        return duration

    def complete_fight(self):
        fight_event = {
            'event_id': self.uuid,
            'target': self.target.get_name(),
            'duration': self.get_duration(),
            'members': self.members
        }
        return fight_event
