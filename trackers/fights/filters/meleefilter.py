import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


def search_data(expression, log_line):
    return re.search(expression, log_line.get('text'))


class MeleeFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Melee'
        self.hits_regex = [
            re.compile(r"^(?P<source>.+?) (?P<dmgtype>\bhit|shoot|kick|slash|crush|pierce|bash|slam|strike|"
                       r"punch|backstab|bite|claw|smash|slice|gore|maul|rend|burn|sting|frenzy on|frenzies on\b)e?s?"
                       r" (?!by non-melee)(?P<target>.+?) for (?P<amount>\d+) points? of damage"
                       r"\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.ds_regex = [
            re.compile(r"^(?P<target>.+?) is \w+ by (?P<source>.+?)'?s? \w+ for (?P<amount>\d+) points? of "
                       r"(?P<dmgtype>non-melee) damage\.(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]
        self.misses_regex = [
            re.compile(r"^(?P<source>.+) \w+ to (?P<dmgtype>\w+)(?: on)? (?P<target>.+?), but .*?(?P<amount>\bmiss"
                       r"|riposte|parry|parries|dodge|block|blocks with \w\w\w shield|INVULNERABLE"
                       r"|magical skin absorbs the blow)e?s?!(?: \((?P<dmgmod>[\w\s]+)\))?$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def return_data(timestamp, result_data):
            if result_data.group('amount').isnumeric():
                filter_type = 'hit'
            else:
                filter_type = 'miss'
            return {
                'Timestamp': timestamp,
                'Source': result_data.group('source').replace('YOUR', 'You'),
                'Target': result_data.group('target').replace('YOU', 'You'),
                'Amount': result_data.group('amount'),
                'Attack': result_data.group('dmgtype'),
                'Mod': result_data.group('dmgmod'),
                'Type': filter_type,
                'debug': result_data.string
            }

        parses = [
            self._hits_data(log_line),
            self._ds_data(log_line),
            self._misses_data(log_line)
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
            'columns': 6,
            'max_rows': 1000,
            'Timestamp': QHeaderView.ResizeToContents,
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

    def _ds_data(self, log_line):
        for expression in self.ds_regex:
            return search_data(expression, log_line)

    def _misses_data(self, log_line):
        for expression in self.misses_regex:
            return search_data(expression, log_line)
