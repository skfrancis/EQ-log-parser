import re
from pprint import pprint


class LootCoinFilter:
    def __init__(self, display=False):
        self.display = display
        self.config = None
        self.regexes = [
            re.compile(r"^(?:(You) receive) (?:(\d+) (\w+?), )?(?:(\d+) (\w+?), )?(?:(\d+) (\w+?) and )?"
                       r"(?:(\d+) (\w+?) )(?:from the corpse|as your split)\.$"),
            re.compile(r"^The master looter, (\w+?), looted (?:(\d+) (\w+?), )?(?:(\d+) (\w+?), )?(?:(\d+) "
                       r"(\w+?) and )?(?:(\d+) (\w+?) )(?:from the corpse|as your split)\.$")
        ]

    def parse(self, log_line):
        def process_data(timestamp, result_data):
            data = {
                'timestamp': timestamp,
                'target': result_data.group(1),
                'platinum': None,
                'gold': None,
                'silver': None,
                'copper': None, 'debug': result_data.string,
                result_data.group(9): result_data.group(8)
            }

            if result_data.group(7):
                data[result_data.group(7)] = result_data.group(6)
            if result_data.group(5):
                data[result_data.group(5)] = result_data.group(4)
            if result_data.group(3):
                data[result_data.group(3)] = result_data.group(2)
            return data

        def display_data(data):
            pprint(data)

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
            'columns': 5,
            'max_rows': 1000,
            'Date': QHeaderView.ResizeToContents,
            'Time': QHeaderView.ResizeToContents,
            'Looter': QHeaderView.ResizeToContents,
            'Platinum': QHeaderView.ResizeToContents,
            'Gold': QHeaderView.ResizeToContents,
            'Silver': QHeaderView.ResizeToContents,
            'Copper': QHeaderView.ResizeToContents
        }
