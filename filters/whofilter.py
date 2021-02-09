import regex


class WhoFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^[A-Z\s]*\[(?:(ANONYMOUS)|(?P<level>\d+) (?P<class>[\w\s]+)|(?P<lvl>\d+)"
                          r" .+? \((?P<class>[\w\s]+)\))\] (?P<name>\w+)(?: \((?P<race>[\w\s]+)\))?")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'name': result_data.group('name'),
                'level': result_data.group('level'),
                'class': result_data.group('class'),
                'race': result_data.group('race'),
                'type': 'who',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
