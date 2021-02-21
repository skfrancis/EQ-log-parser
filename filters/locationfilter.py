import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class LocationFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Location'
        self.regexes = [
            re.compile(r"^Your Location is (-?\d+.+?), (-?\d+.+?), (-?\d+.+?)$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Y': result_data.group(1),
                'X': result_data.group(2),
                'Z': result_data.group(3),
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
            'columns': 5,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'X': QHeaderView.ResizeToContents,
            'Y': QHeaderView.ResizeToContents,
            'Z': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
