import regex
from pprint import pprint


class WhoFilter:
    def __init__(self, display=False):
        self.display = display
        self.regexes = [
            regex.compile(r"^[A-Z\s]*\[(?:(ANONYMOUS)|(?P<lvl>\d+) (?P<class>[\w\s]+)|(?P<lvl1>\d+)"
                          r" .+? \((?P<class1>[\w\s]+)\))\](?:\s+(?P<name>\w+))"),
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'name': result_data.group('name'),
                'class': result_data.group('class'),
                'level': result_data.group('lvl'),
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                parsed = process_data(log_line.get('timestamp'), result)
                if self.display:
                    display_data(parsed)
                return parsed
        return None
