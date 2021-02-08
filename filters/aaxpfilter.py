import re


class AAXPFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^You have gained (\d+) ability point\(s\)!\s+You now have (\d+) ability point\(s\).$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'gained': result_data.group(1),
                'banked': result_data.group(2),
                'type': 'aaxp',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
