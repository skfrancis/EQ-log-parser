import regex


class MeleeHitsFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(?P<source>.+?) (?P<damage>\bhit|shoot|kick|slash|crush|pierce|bash|slam|strike|"
                          r"punch|backstab|bite|claw|smash|slice|gore|maul|rend|burn|sting|frenzy on|frenzies on\b)e?s?"
                          r" (?!by non-melee)(?P<target>.+?) for (?P<amount>\d+) points? of damage"
                          r"\.(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            regex.compile(r"^(?P<target>.+?) is \w+ by (?P<source>.+?) \w+ for (?P<amount>\d+) points? of "
                          r"(?P<damage>non-melee) damage\.$")

        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group('source').replace('YOUR', 'you'),
                'damage': result_data.group('damage'),
                'target': result_data.group('target'),
                'amount': result_data.group('amount'),
                'damagemod': result_data.group('dmgmod'),
                'type': 'melee',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
