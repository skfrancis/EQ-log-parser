import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


def search_data(expression, log_line):
    return re.search(expression, log_line.get('text'))


class SpellFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Spells'
        self.hits_regex = [
            re.compile(r"^(?P<source>.+?) hit (?P<target>.+?) for (?P<amount>\d+) points? of .+? damage by "
                       r"(?P<spell>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.dots_regex = [
            re.compile(r"^(?P<target>.+?) has taken (?P<amount>\d+) damage from (?P<source>you)r (?P<spell>.+?)\."
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            re.compile(r"^(?P<target>.+?) ha(?:s|ve) taken (?P<amount>\d+) damage from (?P<spell>.+?) by "
                       r"(?P<source>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.resists_regex = [
            re.compile(r"^(?P<target>.+) (?P<amount>resist)ed (?P<source>you)r (?P<spell>.+?)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            re.compile(r"^(?P<target>You) (?P<amount>resist) (?P<source>.+?)'s (?P<spell>.+)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def return_data(timestamp, result_data):
            return {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Source': result_data.group('source'),
                'Target': result_data.group('target'),
                'Amount': result_data.group('amount'),
                'Attack': result_data.group('spell'),
                'Mod': result_data.group('dmgmod'),
                'debug': result_data.string
            }

        parses = [
            self._hits_data(log_line),
            self._dots_data(log_line),
            self._resists_data(log_line)
        ]
        for parse in parses:
            if parse:
                parsed = return_data(log_line.get('timestamp'), parse)
                if self.display:
                    display_data(parsed)
                return parsed
        return None

    def create_config(self):
        self.config = {
            'columns': 7,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Source': QHeaderView.ResizeToContents,
            'Target': QHeaderView.ResizeToContents,
            'Amount': QHeaderView.ResizeToContents,
            'Attack': QHeaderView.ResizeToContents,
            'Mod': QHeaderView.ResizeToContents
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name

    def _hits_data(self, log_line):
        for expression in self.hits_regex:
            return search_data(expression, log_line)

    def _dots_data(self, log_line):
        for expression in self.dots_regex:
            return search_data(expression, log_line)

    def _resists_data(self, log_line):
        for expression in self.resists_regex:
            return search_data(expression, log_line)
