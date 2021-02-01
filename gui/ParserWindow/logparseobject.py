from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from pathlib import Path
from util.logparser import line_parse


class LogParserObject(QObject):
    data_ready = pyqtSignal(dict)

    def __init__(self, log_file):
        super().__init__()
        self._log_file = Path(log_file)
        self._active = True

    @pyqtSlot()
    def run(self):
        with self._log_file.open('r', encoding="utf8") as file:
            file.seek(0, SEEK_END)
            while self._active:
                line = file.readline()
                if line:
                    data = line_parse(line)
                    self.data_ready.emit(data)

    def stop(self):
        self._active = False









