import re


class CastingFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+?) begins? (?:casting|singing) (.+)\.$"),
            re.compile(r"^(.+?) activates? (.+)\.$"),
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group(1),
                'spell': result_data.group(2),
                'type': 'casting',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
