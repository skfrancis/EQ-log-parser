import regex


class ExpAAFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^You have gained (\d+) ability point\(s\)!\s+You now have (\d+) ability point\(s\).$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'gained': result_data.group(1),
                'banked': result_data.group(2),
                'type': 'aaexp',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
