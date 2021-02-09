import regex


class ConsiderFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"(.+) (-.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                          r" -- (.+) \(Lvl: (\d+)\)$"),
            regex.compile(r"(.+)( -.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                          r" -- (.+) \(Lvl: (\d+)\)$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'target': result_data.group(1),
                'rare': bool(result_data.group(2)),
                'faction': result_data.group(3),
                'difficulty': result_data.group(4),
                'level': result_data.group(5),
                'type': 'consider',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
