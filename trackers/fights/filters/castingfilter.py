import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class CastingFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Spell Casting'
        self.regexes = [
            re.compile(r"^(.+?) begins? (?:casting|singing) (.+)\.$"),
            re.compile(r"^(.+?) activates? (.+)\.$"),
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Source': result_data.group(1),
                'Spell': result_data.group(2),
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
            'columns': 4,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Source': QHeaderView.ResizeToContents,
            'Spell': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
