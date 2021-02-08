import re


class SpellHitsFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+?) hit (.+?) for (\d+) points? of (.+?) damage by (.+?)\.(?:\s\(([^\(\)]+)\))?$"),
            re.compile(r"^(.+?) has taken (\d+) damage from your (.+?)\.(?:\s\(([^\(\)]+)\))?$"),
            re.compile(r"^(.+?) (?:has|have) taken (\d+) damage from (.+?) by (.+?)\.(?:\s\(([^\(\)]+)\))?$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            damage_mod = None
            source = None
            target = None
            amount = None
            damage_type = None
            spell = None

            if 'damage by' in result_data.string:
                source = result_data.group(1)
                target = result_data.group(2)
                amount = result_data.group(3)
                spell = result_data.group(5)
                damage_type = result_data.group(4)
                if len(result_data.groups()) > 5:
                    damage_mod = result_data.group(6)
            elif 'damage from your' in result_data.string:
                source = 'You'
                target = result_data.group(1).replace('\'s corpse', '')
                amount = result_data.group(2)
                spell = result_data.group(3)
                if len(result_data.groups()) > 3:
                    damage_type = result_data.group(4)
            elif 'damage from' in result_data.string:
                source = result_data.group(4).replace('\'s corpse', '')
                target = result_data.group(1)
                amount = result_data.group(2)
                spell = result_data.group(3)
                if len(result_data.groups()) > 4:
                    damage_type = result_data.group(5)

            return {
                'timestamp': timestamp,
                'source': source,
                'target': target,
                'amount': amount,
                'damagetype': damage_type,
                'spell': spell,
                'damagemod': damage_mod,
                'type': 'spell',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
