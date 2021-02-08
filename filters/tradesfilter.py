import re


class TradesFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+?) (have fashioned the items together to create [^:]+:) ([^.]+)\.$"),
            re.compile(r"^(.+?) (lacked the skills to fashion) ([^.]+)\.$"),
            re.compile(r"^(.+?) (has fashioned) ([^.]+)\.$"),
            re.compile(r"^(.+?) (was not successful in making) ([^.]+)\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            created = False
            if 'fashioned' in result_data.group(2):
                created = True
            return {
                'timestamp': timestamp,
                'source': result_data.group(1),
                'created': created,
                'item': result_data.group(3),
                'type': 'tradeskill',
                'debug': result_data.string

            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None

