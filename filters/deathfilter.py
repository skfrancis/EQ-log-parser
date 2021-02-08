import re


class DeathFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+) (?:have|has) been slain by (.+)!$"),
            re.compile(r"^You have slain (.+)!$"),
            re.compile(r"^(.+) died\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            if len(result_data.groups()) > 1:
                source = result_data.group(1)
                target = result_data.group(2)
            else:
                if result_data.string.startswith('You'):
                    source = 'You'
                else:
                    source = None
                target = result_data.group(1)
            return {
                'timestamp': timestamp,
                'source': source,
                'target': target,
                'type': 'death',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
