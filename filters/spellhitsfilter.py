import regex


class SpellHitsFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(?P<source>.+?) hit (?P<target>.+?) for (?P<amount>\d+) points? of (?P<dmgtype>.+?) "
                          r"damage by (?P<spell>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            regex.compile(r"^(?P<target>.+?) has taken (?P<amount>\d+) (?P<dmgtype>damage) from (?P<source>you)r "
                          r"(?P<spell>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            regex.compile(r"^(?P<target>.+?) ha(?:s|ve) taken (?P<amount>\d+) (?P<dmgtype>damage) from "
                          r"(?P<spell>.+?) by (?P<source>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group('source'),
                'target': result_data.group('target'),
                'amount': result_data.group('amount'),
                'damagetype': result_data.group('dmgtype'),
                'spell': result_data.group('spell'),
                'damagemod': result_data.group('dmgmod'),
                'type': 'spell',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
