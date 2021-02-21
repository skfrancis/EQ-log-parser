import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class HealingFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Healing'
        self.regexes = [
            re.compile(r"^(\w+) healed (.+?) over time for (\d+)(?: \((\d+)\))? hit points by (.+?)\."
                       r"(?: \((?P<healmod>.+?)\))?$"),
            re.compile(r"^(\w+) ha(?:s|ve) been healed over time for (\d+) (?:\((\d+)\))? hit points by "
                       r"(.+?)\.(?: \((.+?)\))?$"),
            re.compile(r"^(.+?) healed (.+?) for (\d+)(?: \((\d+)\))? hit points(?: by (.+?))?\."
                       r"(?: \((?P<healmod>.+?)\))?$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            return {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Source': result_data.group(1),
                'Target': result_data.group(2),
                'Amount': result_data.group(3),
                'Original': result_data.group(4),
                'Spell': result_data.group(5),
                'Mod': result_data.group('healmod'),
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
            'columns': 8,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Source': QHeaderView.ResizeToContents,
            'Target': QHeaderView.ResizeToContents,
            'Amount': QHeaderView.ResizeToContents,
            'Original': QHeaderView.ResizeToContents,
            'Spell': QHeaderView.ResizeToContents,
            'Mod': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
