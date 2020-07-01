from pathlib import Path
import re


class Parser:
    def __init__(self, log_file):
        self._log_file = Path(log_file)
        self._parsed_data = []

    def open(self):
        with self._log_file.open() as file:
            for line in file:
                data = {}
                if line.find('[') != -1:
                    data['timestamp'] = line.split('[', 1)[1].split(']', 1)[0].split()
                    data['text'] = line.split('] ', 1)[1].rstrip("\n")
                    self._parsed_data.append(data)

    def search(self, regex):
        matched_data = []
        for line in self._parsed_data:
            text = line.get('text')
            if re.search(regex, text):
                matched_data.append(line)
        return matched_data

    def watch(self):
        pass
#    datetime.strptime(line.split('[', 1)[1].split(']', 1)[0], '%a %b %d %H:%M:%S %Y')
