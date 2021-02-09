import regex


class LocationFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^Your Location is (-?\d+.+?), (-?\d+.+?), (-?\d+.+?)$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'Y': result_data.group(1),
                'X': result_data.group(2),
                'Z': result_data.group(3),
                'type': 'location',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
