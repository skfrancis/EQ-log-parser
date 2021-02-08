import re


class HealingFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(\w+) healed (.+?) over time for (\d+)(?: \((\d+)\))? hit points by (.+?)\.(?: \((.+?)\))?$"),
            re.compile(r"^(\w+) ha(?:s|ve) been healed over time for (\d+)(?: \((\d+)\))?"
                       r" hit points by (.+?)\.(?: \((.+?)\))?$"),
            re.compile(r"^(.+?) healed (.+?) for (\d+)(?: \((\d+)\))? hit points(?: by (.+?))?\.(?: \((.+?)\))?$")
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
                'type': 'healing',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
