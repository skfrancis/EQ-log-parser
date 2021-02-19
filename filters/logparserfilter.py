from PyQt5.QtWidgets import QHeaderView
from pprint import pprint


class LogParserFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        timestamp = log_line.get('timestamp')
        parsed = {
            'Date': timestamp.strftime('%x'),
            'Time': timestamp.strftime('%X'),
            'Text': log_line.get('text')
        }
        if self.display:
            display_data(parsed)
        return parsed

    def create_config(self):
        self.config = {
            'columns': 3,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Text': QHeaderView.Stretch
        }

    def get_config(self):
        return self.config.copy()
