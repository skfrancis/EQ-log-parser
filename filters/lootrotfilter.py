import re


class LootRotFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^No one was interested in the .+: (.+)\. These items")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'item': result_data.group(1),
                'type': 'lootrot',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
