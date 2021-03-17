from PySide6.QtCore import QObject, Slot, Signal
from pathlib import Path
from util.lineparse import line_parse
from os import SEEK_END


class LogParserThreadObject(QObject):
    stopped = Signal()
    data_ready = Signal(dict)

    def __init__(self, log_file):
        super().__init__()
        self._log_file = Path(log_file)
        self._active = True

    @Slot()
    def run(self):
        with self._log_file.open('r', encoding="utf8") as file:
            file.seek(0, SEEK_END)
            while self._active:
                line = file.readline()
                if line:
                    data = line_parse(line)
                    self.data_ready.emit(data)

    @Slot()
    def stop(self):
        self._active = False
        self.stopped.emit()
