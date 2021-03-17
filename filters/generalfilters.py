import re
import regex
from pprint import pprint
from PySide6.QtWidgets import QHeaderView


ResizeToContents = QHeaderView.ResizeToContents
Stretch = QHeaderView.ResizeToContents


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


class CastingFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Spell Casting'
        self.columns = ['Date', 'Time', 'Source', 'Spell']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^(.+?) begins? (?:casting|singing) (.+)\.$"),
            re.compile(r"^(.+?) activates? (.+)\.$"),
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[0]: result.group(2),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class ChatFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Chat'
        self.columns = ['Date', 'Time', 'Channel', 'Source', 'Target', 'Message']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents,
                      ResizeToContents, ResizeToContents, Stretch]
        self.regexes = [
            re.compile(r"^(.+?) (?:say to your|told|tell your|tells the|tells?) (.+?),\s(?:in .+, )?\s?'(.+)'$"),
            re.compile(r"^(.+?) (says? out of character|says?|shouts?|auctions?),\s(?:in .+, )?'(.+)'$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                channel = result.group(2).capitalize()
                target = None
                if channel.islower() == 'you' or result.string.startswith('You told'):
                    channel = 'Tell'
                    target = result.group(2)
                if 'out of character' in result.group(2):
                    channel = 'OoC'
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: channel.rstrip('s'),
                    self.columns[3]: result.group(1),
                    self.columns[4]: target,
                    self.columns[5]: result.group(3),
                    'debug': result .string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class ConsiderFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Consider'
        self.columns = ['Date', 'Time', 'Target', 'Level', 'Consider', 'Difficulty', 'Rare']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents,
                      ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"(.+) (-.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                       r" -- (.+) \(Lvl: (\d+)\)$"),
            re.compile(r"(.+)( -.+)? ((?:scowls|glares|glowers|regards|looks|judges|kindly) .+?)"
                       r" -- (.+) \(Lvl: (\d+)\)$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[3]: result.group(5),
                    self.columns[4]: result.group(3),
                    self.columns[5]: result.group(4),
                    self.columns[6]: bool(result.group(2)),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class FactionFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Faction'
        self.columns = ['Date', 'Time', 'Faction', 'Amount']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^Your faction standing with ([^.]+) has been adjusted by (-?\d+)\.$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[3]: result.group(2),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class LocationFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Location'
        self.columns = ['Date', 'Time', 'Y', 'X', 'Z']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^Your Location is (-?\d+.+?), (-?\d+.+?), (-?\d+.+?)$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[3]: result.group(2),
                    self.columns[4]: result.group(3),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class LogParserFilter:
    def __init__(self, display=False):
        self.display = display
        self.columns = ['Date', 'Time', 'Text']
        self.sizes = [ResizeToContents, ResizeToContents, Stretch]

    def parse(self, log_line):
        timestamp = log_line.get('timestamp')
        parsed = {
            self.columns[0]: timestamp.strftime('%x'),
            self.columns[1]: timestamp.strftime('%X'),
            self.columns[2]: log_line.get('text')
        }
        if self.display:
            display_data(parsed)
        return parsed

    def get_config(self):
        return create_config(self.columns, self.sizes)


class PartyFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Party'
        self.columns = ['Date', 'Time', 'Member', 'Status', 'Type']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^(?P<player>.+?)(?: have| has)? (?P<status>join)ed the (?P<type>group|raid)\.$"),
            re.compile(r"^(?P<player>You) notify \w+ that you agree to (join) the (?P<type>group|raid)\.$"),
            re.compile(r"^(?P<player>.+?) (?:have been|has been|has|were) (?P<status>(?:left|removed from))"
                       r" the (?P<type>group|raid)\."),
            re.compile(r"^You (?P<status>remove) (?P<player>.+?) from the (?P<type>group|party|raid)\.$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[3]: result.group(2),
                    self.columns[4]: result.group(3),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class PetLeaderFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Pet Leader'
        self.columns = ['Date', 'Time', 'Leader', 'Pet']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"(?P<pet>^[GJKLVXZ]([aeio][bknrs]){0,2}(ab|er|n|tik)) says, 'My leader is (?P<leader>\w+)\.'$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group('leader'),
                    self.columns[3]: result.group('pet'),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
            return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class SystemMessageFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'System Message'
        self.columns = ['Date', 'Time', 'Message']
        self.sizes = [ResizeToContents, ResizeToContents, Stretch]
        self.regexes = [
            re.compile(r"^<SYSTEMWIDE_MESSAGE>: ?(.+?)$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class TradesFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Tradeskills'
        self.columns = ['Date', 'Time', 'Source', 'Created', 'Item']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^(.+?) (have fashioned the items together to create [^:]+:) ([^.]+)\.$"),
            re.compile(r"^(.+?) (has fashioned) ([^.]+)\.$"),
            re.compile(r"^(.+?) (was not successful in making) ([^.]+)\.$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                created = False
                timestamp = log_line.get('timestamp')
                if 'fashioned' in result.group(2):
                    created = True
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    self.columns[3]: created,
                    self.columns[4]: result.group(3),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class WhoFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Who'
        self.columns = ['Date', 'Time', 'Name', 'Class', 'Level']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            regex.compile(r"^[A-Z\s]*\[(?:(ANONYMOUS)|(?P<lvl>\d+) (?P<class>[\w\s]+)|(?P<lvl>\d+)"
                          r" .+? \((?P<class>[\w\s]+)\))\](?:\s+(?P<name>\w+))"),
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group('name'),
                    self.columns[3]: result.group('class'),
                    self.columns[4]: result.group('lvl'),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)


class ZoningFilter:
    def __init__(self, display=False):
        self.display = display
        self.filter_name = 'Zoning'
        self.non_zones = [
            'an area where levitation effects do not function',
            'an Arena (PvP) area',
            'an area where Bind Affinity is allowed',
            'the Drunken Monkey stance adequately'
        ]
        self.columns = ['Date', 'Time', 'Zone']
        self.sizes = [ResizeToContents, ResizeToContents, ResizeToContents]
        self.regexes = [
            re.compile(r"^You have entered (.+)\.$")
        ]

    def parse(self, log_line):
        for expression in self.regexes:
            result = re.search(expression, log_line.get('text'))
            if result:
                for non_zone in self.non_zones:
                    if non_zone in result.group(1):
                        return None
                timestamp = log_line.get('timestamp')
                parsed_data = {
                    self.columns[0]: timestamp.strftime('%x'),
                    self.columns[1]: timestamp.strftime('%X'),
                    self.columns[2]: result.group(1),
                    'debug': result.string
                }
                if self.display:
                    display_data(parsed_data)
                return parsed_data
        return None

    def get_config(self):
        return create_config(self.columns, self.sizes)
