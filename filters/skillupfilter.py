import re


class SkillUpFilter:
    def __init__(self):
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

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
