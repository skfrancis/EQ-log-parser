import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class ConsiderFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Consider'
        self.regexes = [
            re.compile(r"(.+) (-.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                       r" -- (.+) \(Lvl: (\d+)\)$"),
            re.compile(r"(.+)( -.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                       r" -- (.+) \(Lvl: (\d+)\)$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Target': result_data.group(1),
                'Level': result_data.group(5),
                'Consider': result_data.group(3),
                'Difficulty': result_data.group(4),
                'Rare': bool(result_data.group(2)),
                'debug': result_data.string
            }
            if self.display:
                display_data(parsed)
            return parsed

        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None

    def create_config(self):
        self.config = {
            'columns': 7,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Target': QHeaderView.ResizeToContents,
            'Level': QHeaderView.ResizeToContents,
            'Consider': QHeaderView.ResizeToContents,
            'Difficulty': QHeaderView.ResizeToContents,
            'Rare': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
