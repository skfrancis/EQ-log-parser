import re


def return_data(timestamp, result_data):
    return {
        'timestamp': timestamp,
        'source': result_data.group('source').replace('YOUR', 'You'),
        'target': result_data.group('target').replace('YOU', 'You'),
        'amount': result_data.group('amount'),
        'attack': result_data.group('dmgtype'),
        'damagemod': result_data.group('dmgmod'),
        'debug': result_data.string
    }


def search_data(expression, log_line):
    return re.search(expression, log_line.get('text'))


class MeleeFilter:
    def __init__(self):
        self.hits_regex = [
            re.compile(r"^(?P<source>.+?) (?P<dmgtype>\bhit|shoot|kick|slash|crush|pierce|bash|slam|strike|"
                       r"punch|backstab|bite|claw|smash|slice|gore|maul|rend|burn|sting|frenzy on|frenzies on\b)e?s?"
                       r" (?!by non-melee)(?P<target>.+?) for (?P<amount>\d+) points? of damage"
                       r"\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.ds_regex = [
            re.compile(r"^(?P<target>.+?) is \w+ by (?P<source>.+?)'?s? \w+ for (?P<amount>\d+) points? of "
                       r"(?P<dmgtype>non-melee) damage\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.misses_regex = [
            re.compile(r"^(?P<source>.+) \w+ to (?P<dmgtype>\w+)(?: on)? (?P<target>.+?), but .*?(?P<amount>\bmiss"
                       r"|riposte|parry|parries|dodge|block|blocks with \w\w\w shield|INVULNERABLE"
                       r"|magical skin absorbs the blow)e?s?!(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]

    def parse(self, log_line):
        result = self._hits_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        result = self._ds_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        result = self._misses_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        return None

    def _hits_data(self, log_line):
        for expression in self.hits_regex:
            return search_data(expression, log_line)

    def _ds_data(self, log_line):
        for expression in self.ds_regex:
            return search_data(expression, log_line)

    def _misses_data(self, log_line):
        for expression in self.misses_regex:
            return search_data(expression, log_line)


