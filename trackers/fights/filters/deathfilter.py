import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class DeathFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Deaths'
        self.regexes = [
            re.compile(r"^(?P<target>.+) (?:have|has) been slain by (?P<source>.+)!$"),
            re.compile(r"^(?P<source>You) have slain (?P<target>.+)!$"),
            re.compile(r"^(?P<source>(?P<target>.+)) dies?d?\.$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            return {
                'Timestamp': timestamp,
                'Source': result_data.group('source'),
                'Target': result_data.group('target'),
                'Amount': 'death',
                'Attack': None,
                'Mod': None,
                'Type': 'death',
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                parsed = process_data(log_line.get('timestamp'), result)
                if self.display:
                    display_data(parsed)
                return parsed
        return None

    def create_config(self):
        self.config = {
            'columns': 5,
            'max_rows': 1000,
            'Timestamp': QHeaderView.ResizeToContents,
            'Source': QHeaderView.ResizeToContents,
            'Target': QHeaderView.ResizeToContents,
            'Amount': QHeaderView.ResizeToContents,
            'Mod': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
