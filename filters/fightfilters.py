import re
from pprint import pprint

from PySide6.QtWidgets import QHeaderView

ResizeToContents = QHeaderView.ResizeToContents


def update_miss_data(data):
    if 'parries' in data:
        data = 'parry'
    if 'blocks with' in data:
        data = 'block'
    if 'magical skin absorbs' in data:
        data = 'magical skin'
    return data


def display_data(data):
    pprint(data)


def create_config(keys, values):
    config = {
        'columns': len(keys),
        'max_rows': 1000
    }
    for i in range(len(keys)):
        config[keys[i]] = values[i]
    return config


class FightFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Fight'
        self.columns = ['Timestamp', 'Source', 'Target', 'Amount', 'Ability', 'Mod', 'Type']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents,
                      ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.filters = [DeathFilter(self.columns), NonSpellFilter(self.columns),
                        SpellFilter(self.columns), HealingFilter(self.columns)]

    def parse(self, log_line):
        for fight_filter in self.filters:
            parsed_data = fight_filter.parse(log_line)
            if parsed_data:
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class DeathFilter:
    def __init__(self, columns):
        self.filter_name = 'Deaths'
        self.columns = columns
        self.regexes = [
            re.compile(r"^(?P<target>.+) (?:have|has) been slain by (?P<source>.+)!$"),
            re.compile(r"^(?P<source>You) have slain (?P<target>.+)!$"),
            re.compile(r"^(?P<source>(?P<target>.+)) dies?d?\.$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp,
                    self.columns[1]: result.group('source'),
                    self.columns[2]: result.group('target'),
                    self.columns[3]: None,
                    self.columns[4]: None,
                    self.columns[5]: None,
                    self.columns[6]: 'death',
                    'debug': result.string
                }
                return parsed_data
        return None


class NonSpellFilter:
    def __init__(self, columns):
        self.filter_name = 'Non Spells'
        self.columns = columns
        self.regexes = [
            re.compile(r"^(?P<source>.+?) (?P<dmgtype>\bhit|shoot|kick|slash|crush|pierce|bash|slam|strike|"
                       r"punch|backstab|bite|claw|smash|slice|gore|maul|rend|burn|sting|frenzy on|frenzies on\b)e?s?"
                       r" (?!by non-melee)(?P<target>.+?) for (?P<amount>\d+) points? of damage"
                       r"\.(?: \((?P<dmgmod>[\w\s]+)\))?"),
            re.compile(r"^(?P<target>.+?) is \w+ by (?P<source>.+?)'?s? \w+ for (?P<amount>\d+) points? of "
                       r"(?P<dmgtype>non-melee) damage\.(?: \((?P<dmgmod>[\w\s]+)\))?"),
            re.compile(r"^(?P<source>.+) \w+ to (?P<dmgtype>\w+)(?: on)? (?P<target>.+?), but .*?(?P<amount>\bmiss"
                       r"|parry|parries|dodge|block|blocks with \w\w\w shield|INVULNERABLE"
                       r"|magical skin absorbs the blow)e?s?!(?: \((?P<dmgmod>[\w\s]+)\))?")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                filter_type = 'nonspell hit' if result.group('amount').isnumeric() else 'nonspell miss'
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp,
                    self.columns[1]: result.group('source').replace('YOUR', 'You'),
                    self.columns[2]: result.group('target').capitalize(),
                    self.columns[3]: update_miss_data(result.group('amount')),
                    self.columns[4]: result.group('dmgtype'),
                    self.columns[5]: result.group('dmgmod'),
                    self.columns[6]: filter_type,
                    'debug': result.string
                }
                return parsed_data
        return None


class SpellFilter:
    def __init__(self, columns):
        self.columns = columns
        self.filter_name = 'Spells'
        self.regexes = [
            re.compile(r"^(?P<source>.+?) hit (?P<target>.+?) for (?P<amount>\d+) points? of .+? damage by "
                       r"(?P<spell>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?$"),
            re.compile(r"^(?P<target>.+?) has taken (?P<amount>\d+) damage from (?P<source>you)r (?P<spell>.+?)\."
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?"),
            re.compile(r"^(?P<target>.+?) ha(?:s|ve) taken (?P<amount>\d+) damage from (?P<spell>.+?) by "
                       r"(?P<source>.+?)\.(?: \((?P<dmgmod>[\w\s]+)\))?"),
            re.compile(r"^(?P<target>.+) (?P<amount>resist)ed (?P<source>you)r (?P<spell>.+?)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?"),
            re.compile(r"^(?P<target>You) (?P<amount>resist) (?P<source>.+?)'s (?P<spell>.+)!"
                       r"(?: \((?P<dmgmod>[\w\s]+)\))?")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                filter_type = 'spell hit' if result.group('amount').isnumeric() else 'spell miss'
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp,
                    self.columns[1]: result.group('source').replace('YOUR', 'You'),
                    self.columns[2]: result.group('target').capitalize(),
                    self.columns[3]: result.group('amount'),
                    self.columns[4]: result.group('spell'),
                    self.columns[5]: result.group('dmgmod'),
                    self.columns[6]: filter_type,
                    'debug': result.string
                }
                return parsed_data
        return None


class HealingFilter:
    def __init__(self, columns):
        self.columns = columns
        self.filter_name = 'Heals'
        self.regexes = [
            re.compile(r"^(?P<source>.+?) healed (?P<target>.+?) over time for (?P<actual>\d+)"
                       r"(?: \((?P<max>\d+)\))? hit points by (?P<spell>.+?)\.(?: \((?P<healmod>.+?)\))?"),
            re.compile(r"^(?P<source>.+?) healed (?P<target>.+?) for (?P<actual>\d+)"
                       r"(?: \((?P<max>\d+)\))? hit points(?: by (?P<spell>.+?))?\.(?: \((?P<healmod>.+?)\))?")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                maximum = result.group('max') if result.group('max') is not None else result.group('actual')
                parsed_data = {
                    self.columns[0]: timestamp,
                    self.columns[1]: result.group('source').replace('YOUR', 'You'),
                    self.columns[2]: result.group('target').capitalize(),
                    self.columns[3]: (result.group('actual'), maximum),
                    self.columns[4]: result.group('spell'),
                    self.columns[5]: result.group('healmod'),
                    self.columns[6]: 'heal',
                    'debug': result.string
                }
                return parsed_data
        return None
