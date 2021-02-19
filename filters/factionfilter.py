import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class FactionFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.regexes = [
            re.compile(r"^Your faction standing with ([^.]+) has been adjusted by (-?\d+)\.$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Faction': result_data.group(1),
                'Amount': result_data.group(2),
                'debug': result_data.string
            }
            if self.display:
                display_data(parsed)
            return parsed

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None

    def create_config(self):
        self.config = {
            'columns': 4,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Faction': QHeaderView.ResizeToContents,
            'Amount': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()
