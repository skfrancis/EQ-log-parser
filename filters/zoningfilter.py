import regex


class ZoningFilter:
    def __init__(self):
        self.non_zones = [
            'an area where levitation effects do not function',
            'an Arena (PvP) area',
            'an area where Bind Affinity is allowed',
            'the Drunken Monkey stance adequately'
        ]
        self.regexes = [
            regex.compile(r"^You have entered (.+)\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            for non_zone in self.non_zones:
                if non_zone in result_data.group(1):
                    return None
            return {
                'timestamp': timestamp,
                'Zone': result_data.group(1),
                'type': 'zoning',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
