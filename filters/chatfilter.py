import re


class ChatFilter:
    def __init__(self):
        self.regexes = [
            re.compile(r"^(.+?) (?:say to your|told|tell your|tells the|tells?) (.+?),\s(?:in .+, )?\s?'(.+)'$"),
            re.compile(r"^(.+?) (says? out of character|says?|shouts?|auctions?),\s(?:in .+, )?'(.+)'$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            channel = result_data.group(2)
            target = None
            if channel.islower() == 'you' or result_data.string.startswith('You told'):
                channel = 'tell'
                target = result_data.group(2)
            if 'out of character' in result_data.group(2):
                channel = 'out of character'
            return {
                'timestamp': timestamp,
                'source': result_data.group(1),
                'channel': channel.rstrip('s'),
                'target': target,
                'message': result_data.group(3),
                'type': 'chat',
                'debug': result_data.string
            }

        for regex in self.regexes:
            result = re.search(regex, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
