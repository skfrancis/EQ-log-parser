import regex


class SpellMissesFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(?P<target>.+) resisted (?P<source>you)r (?P<spell>.+?)!$"),
            regex.compile(r"^(?P<target>You) resist (?P<source>.+?)'s (?P<spell>.+)!$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group('source'),
                'target': result_data.group('target'),
                'spell': result_data.group('spell'),
                'type': 'resist',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
