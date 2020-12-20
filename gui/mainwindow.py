from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from gui.triggerview import TriggerView
from gui.parserview import ParserView
from PyQt5.QtGui import QIcon
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._path = Path.cwd()
        # self._path = Path('d:/Games/Steam/steamapps/common/Everquest F2P/Logs')
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('EQ Parser')
        icon_path = self._path / 'img' / 'eq-icon.png'
        print(icon_path)
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        triggers = TriggerView(self)
        triggers.resize(750, 150)
        # parser = ParserView(self, self._path / 'eqlog_Rarshaak_aradune.txt')
        layout = QVBoxLayout()
        layout.addWidget(triggers)
        # layout.addWidget(parser)
        self.setLayout(layout)
        self.resize(750, 350)
        self.show()
