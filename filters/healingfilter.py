import regex


class HealingFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(\w+) healed (.+?) over time for (\d+)(?: \((\d+)\))? hit points by (.+?)\."
                          r"(?: \((?P<healmod>.+?)\))?$"),
            regex.compile(r"^(\w+) ha(?:s|ve) been healed over time for (\d+) (?:\((\d+)\))? hit points by "
                          r"(.+?)\.(?: \((.+?)\))?$"),
            regex.compile(r"^(.+?) healed (.+?) for (\d+)(?: \((\d+)\))? hit points(?: by (.+?))?\."
                          r"(?: \((?P<healmod>.+?)\))?$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'source': result_data.group(1),
                'target': result_data.group(2),
                'amount': result_data.group(3),
                'original': result_data.group(4),
                'spell': result_data.group(5),
                'healmod': result_data.group('healmod'),
                'type': 'healing',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
