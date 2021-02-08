import re


class MeleeHitsFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+?) (hit|shoot|kick|slash|crush|pierce|bash|slam|strike|punch|backstab|bite|claw|"
                       r"smash|slice|gore|maul|rend|burn|sting|frenzy on|frenzies on)e?s? "
                       r"(?!by non-melee)(.+?) for (\d+) points? of damage\.(?:\s\(([^\(\)]+)\))?$"),
            re.compile(r"^(.+?) is \w+ by (.+?) \w+ for (\d+) points? of (non-melee) damage\.$")

        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            damage_mod = None
            if len(result_data.groups()) > 4:
                damage_mod = result_data.group(5)
            if result_data.group(4) != 'non-melee':
                source = result_data.group(1)
                damage = result_data.group(2)
                target = result_data.group(3)
                amount = result_data.group(4)
            else:
                source = result_data.group(2).replace('YOUR', 'You')
                damage = result_data.group(4)
                target = result_data.group(1)
                amount = result_data.group(3)
            return {
                'timestamp': timestamp,
                'source': source,
                'damage': damage,
                'target': target,
                'Amount': amount,
                'damagemod': damage_mod,
                'type': 'melee',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
