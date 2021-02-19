import regex


class LootRotFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^No one was interested in the .+: (.+)\. These items"),
            regex.compile(r"^--\w+ left (?:an?|\d+) ([^.]+) on [^.]+?\s?\.--$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'item': result_data.group(1),
                'type': 'lootrot',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
