import re
from pprint import pprint


class DeathFilter:
    def __init__(self, display=False):
        self.display = display
        self.regexes = [
            re.compile(r"^(?P<target>.+) (?:have|has) been slain by (?P<source>.+)!$"),
            re.compile(r"^(?P<source>You) have slain (?P<target>.+)!$"),
            re.compile(r"^(?P<source>(?P<target>.+)) dies?d?\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group('source'),
                'target': result_data.group('target'),
                'amount': 'death',
                'attack': None,
                'damagemod': None,
                'debug': result_data.string
            }

        def display_data(data):
            pprint(data)

        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                parsed = process_data(log_line.get('timestamp'), result)
                if self.display:
                    display_data(parsed)
                return parsed
        return None
