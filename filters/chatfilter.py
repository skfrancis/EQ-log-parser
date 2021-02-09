import regex


class ChatFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(.+?) (?:say to your|told|tell your|tells the|tells?) (.+?),\s(?:in .+, )?\s?'(.+)'$"),
            regex.compile(r"^(.+?) (says? out of character|says?|shouts?|auctions?),\s(?:in .+, )?'(.+)'$")
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

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
