import regex


class DeathFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(?P<target>.+) (?:have|has) been slain by (?P<source>.+)!$"),
            regex.compile(r"^(?P<source>You) have slain (?P<target>.+)!$"),
            regex.compile(r"^(?P<source>(?P<target>.+)) dies?d?\.$")
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

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
