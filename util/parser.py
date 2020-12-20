from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from datetime import datetime
from pathlib import Path
from os import SEEK_END


def line_parse(line):
    data = {}
    if line.startswith('['):
        line = line.rstrip("\n")
        split_line = line.split('[', 1)[1].split('] ', 1)
        data['timestamp'] = datetime.strptime(split_line[0], '%a %b %d %H:%M:%S %Y')
        data['text'] = split_line[1]
    return data


class Parser(QObject):
    finished = pyqtSignal()
    data_ready = pyqtSignal(dict)

    def __init__(self, log_file):
        super().__init__()
        self._log_file = Path(log_file)

    @pyqtSlot()
    def run(self):
        with self._log_file.open('r', encoding="utf8") as file:
            file.seek(0, SEEK_END)
            # TODO: convert this while?
            while True:
                line = file.readline()
                if not line:
                    continue
                else:
                    data = line_parse(line)
                    # print(data) # debugging purposes
                    self.data_ready.emit(data)







