import regex


class LootFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^--(\w+) \w+ looted (an?|\d+) ([^.]+) from ([^.]+)?\s?\.--$"),
            regex.compile(r"^(\w+) grabbed a (.+) from ([^.]+?)\s?\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            quantity = 1
            if result_data.group(2).isnumeric():
                quantity = result_data.group(2)

            return {
                'timestamp': timestamp,
                'looter': result_data.group(1),
                'quantity': quantity,
                'item': result_data.group(3),
                'source': result_data.group(4).replace('\'s corpse', ''),
                'type': 'loot',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
