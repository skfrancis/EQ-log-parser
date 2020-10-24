from pathlib import Path
from os import SEEK_END
from datetime import datetime
from gui.parserview import ParserView


def line_parse(line):
    data = {}
    if line.startswith('['):
        line = line.rstrip("\n")
        split_line = line.split('[', 1)[1].split('] ', 1)
        data['timestamp'] = datetime.strptime(split_line[0], '%a %b %d %H:%M:%S %Y')
        data['text'] = split_line[1]
    return data


class Parser:
    def __init__(self, parent, log_file, alerter):
        self._log_file = Path(log_file)
        self._alerter = alerter
        self.view = ParserView(parent, 2, ['timestamp', 'text'])

    def open(self):
        parsed_data = []
        with self._log_file.open('r', encoding="utf8") as file:
            for line in file:
                data = line_parse(line)
                if data:
                    self.view.add_row(data)
                    parsed_data.append(data)
        return parsed_data

    def watch(self):
        with self._log_file.open('r', encoding="utf8") as file:
            file.seek(0, SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    continue
                data = line_parse(line)
                alert_text = self._alerter.search(data.get('text'))
                print(data, alert_text)
                self.view.add_row(data)

