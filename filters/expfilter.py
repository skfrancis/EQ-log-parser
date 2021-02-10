import regex


class EXPFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^You gaine?d? (experience|party|raid)")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            if result_data.group(1) == 'experience':
                exptype = 'solo'
            else:
                exptype = result_data.group(1)
            return {
                'timestamp': timestamp,
                'exptype': exptype,
                'type': 'exp',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
