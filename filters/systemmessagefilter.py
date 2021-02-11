import regex


class SystemMessageFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^<SYSTEMWIDE_MESSAGE>: ?(.+?)$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'message': result_data.group(1),
                'type': 'sysmsg',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
