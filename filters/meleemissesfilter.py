import re


class MeleeMissesFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+) \w+ to (\w+)(?: on)? (.+?), but .*?(miss|riposte|parry|parries|dodge|block|blocks"
                       r" with \w\w\w shield|INVULNERABLE|magical skin absorbs the blow)e?s?!(?:\s\(([^\(\)]+)\))?$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group(1),
                'damage': result_data.group(2),
                'target': result_data.group(3),
                'misstype': result_data.group(4),
                'special': '',
                'type': 'miss',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
