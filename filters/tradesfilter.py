import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class TradesFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Tradeskills'
        self.regexes = [
            re.compile(r"^(.+?) (have fashioned the items together to create [^:]+:) ([^.]+)\.$"),
            re.compile(r"^(.+?) (has fashioned) ([^.]+)\.$"),
            re.compile(r"^(.+?) (was not successful in making) ([^.]+)\.$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            created = False
            if 'fashioned' in result_data.group(2):
                created = True
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Player': result_data.group(1),
                'Created': created,
                'Item': result_data.group(3),
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
            'Player': QHeaderView.ResizeToContents,
            'Created': QHeaderView.ResizeToContents,
            'Item': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name