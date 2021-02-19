import re
from pprint import pprint


class ZoningFilter:
    def __init__(self, display=False):
        self.display = display
        self.non_zones = [
            'an area where levitation effects do not function',
            'an Arena (PvP) area',
            'an area where Bind Affinity is allowed',
            'the Drunken Monkey stance adequately'
        ]
        self.regexes = [
            re.compile(r"^You have entered (.+)\.$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            for non_zone in self.non_zones:
                if non_zone in result_data.group(1):
                    return None
            return {
                'timestamp': timestamp,
                'zone': result_data.group(1),
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                parsed = process_data(log_line.get('timestamp'), result)
                if self.display:
                    display_data(parsed)
                return parsed
        return None
