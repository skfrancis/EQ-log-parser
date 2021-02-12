import re


def return_data(timestamp, result_data):
    return {
        'timestamp': timestamp,
        'source': result_data.group('source'),
        'target': result_data.group('target'),
        'amount': result_data.group('amount'),
        'attack': result_data.group('spell'),
        'damagemod': result_data.group('dmgmod'),
        'debug': result_data.string
    }


def search_data(expression, log_line):
    return re.search(expression, log_line.get('text'))


class SpellFilter:
    def __init__(self):
        self.hits_regex = [
            re.compile(r"^(?P<source>.+?) hit (?P<target>.+?) for (?P<amount>\d+) points? of .+? damage by "
                       r"(?P<spell>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.dots_regex = [
            re.compile(r"^(?P<target>.+?) has taken (?P<amount>\d+) damage from (?P<source>you)r (?P<spell>.+?)\."
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            re.compile(r"^(?P<target>.+?) ha(?:s|ve) taken (?P<amount>\d+) damage from (?P<spell>.+?) by "
                       r"(?P<source>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.resists_regex = [
            re.compile(r"^(?P<target>.+) (?P<amount>resist)ed (?P<source>you)r (?P<spell>.+?)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            re.compile(r"^(?P<target>You) (?P<amount>resist) (?P<source>.+?)'s (?P<spell>.+)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]

    def parse(self, log_line):
        result = self._hits_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        result = self._dots_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        result = self._resists_data(log_line)
        if result:
            return return_data(log_line.get('timestamp'), result)

        return None

    def _hits_data(self, log_line):
        for expression in self.hits_regex:
            return search_data(expression, log_line)

    def _dots_data(self, log_line):
        for expression in self.dots_regex:
            return search_data(expression, log_line)

    def _resists_data(self, log_line):
        for expression in self.resists_regex:
            return search_data(expression, log_line)
