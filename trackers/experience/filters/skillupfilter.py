import re
from pprint import pprint


class SkillUpFilter:
    def __init__(self, display=False):
        self.display = display
        self.regexes = [
            re.compile(r"^You have become better at (.+)! \((\d+)\)$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'skill': result_data.group(1),
                'level': result_data.group(2),
                'type': 'skillup',
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
