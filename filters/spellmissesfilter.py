import re


class SpellMissesFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+) resisted your (.+?)!$"),
            re.compile(r"^You resist (.+?)'s (.+)!$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            if result_data.string.startswith('You'):
                source = 'You'
                target = result_data.group(1)
            else:
                source = result_data.group(1)
                target = 'You'
            return {
                'timestamp': timestamp,
                'source': source,
                'target': target,
                'spell': result_data.group(2),
                'type': 'resist',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
