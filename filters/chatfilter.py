import re
from pprint import pprint
from PyQt5.QtWidgets import QHeaderView


class ChatFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.create_config()
        self.filter_name = 'Chat'
        self.regexes = [
            re.compile(r"^(.+?) (?:say to your|told|tell your|tells the|tells?) (.+?),\s(?:in .+, )?\s?'(.+)'$"),
            re.compile(r"^(.+?) (says? out of character|says?|shouts?|auctions?),\s(?:in .+, )?'(.+)'$")
        ]

    def parse(self, log_line):
        def display_data(data):
            pprint(data)

        def process_data(timestamp, result_data):
            channel = result_data.group(2).capitalize()
            target = None
            if channel.islower() == 'you' or result_data.string.startswith('You told'):
                channel = 'Tell'
                target = result_data.group(2)
            if 'out of character' in result_data.group(2):
                channel = 'OoC'
            parsed = {
                'Date': timestamp.strftime('%x'),
                'Time': timestamp.strftime('%X'),
                'Channel': channel.rstrip('s'),
                'Source': result_data.group(1),
                'Target': target,
                'Message': result_data.group(3),
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
            'columns': 6,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Channel': QHeaderView.ResizeToContents,
            'Source': QHeaderView.ResizeToContents,
            'Target': QHeaderView.ResizeToContents,
            'Message': QHeaderView.Stretch
        }

    def get_config(self):
        return self.config.copy()

    def get_filter_name(self):
        return self.filter_name
