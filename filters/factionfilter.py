import regex


class FactionFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^Your faction standing with ([^.]+) has been adjusted by (-?\d+)\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'faction': result_data.group(1),
                'amount': result_data.group(2),
                'type': 'faction',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
