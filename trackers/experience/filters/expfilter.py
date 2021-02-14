import re
from pprint import pprint


class EXPFilter:
    def __init__(self, display=False):
        self.display = display
        self.regexes = [
            re.compile(r"^You gaine?d? (experience|party|raid)")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            if result_data.group(1) == 'experience':
                exptype = 'solo'
            else:
                exptype = result_data.group(1)
            return {
                'timestamp': timestamp,
                'exptype': exptype,
                'type': 'exp',
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
