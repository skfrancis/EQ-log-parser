import regex


class PartyFilter:
    def __init__(self):
        self.regexes = [
            regex.compile(r"^(?P<player>.+?)(?: have| has)? (?P<status>join)ed the (?P<type>group|raid)\.$"),
            regex.compile(r"^(?P<player>You) notify \w+ that you agree to (join) the (?P<type>group|raid)\.$"),
            regex.compile(r"^(?P<player>.+?) (?:have been|has been|has|were) (?P<status>(?:left|removed from))"
                          r" the (?P<type>group|raid)\."),
            regex.compile(r"^You (?P<status>remove) (?P<player>.+?) from the (?P<type>group|party|raid)\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            return {
                'timestamp': timestamp,
                'player': result_data.group(1),
                'status': result_data.group(2),
                'type': result_data.group(3),
                'debug': result_data.string
            }

        for expression in self.regexes:
            result = regex.search(expression, log_line.get('text'))
            if result:
                return process_data(log_line.get('timestamp'), result)

        return None
