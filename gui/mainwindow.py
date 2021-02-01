from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from pathlib import Path
from gui.TriggerWindow.triggerview import TriggerView
from gui.ParserWindow.logparserview import LogParserView
from gui.ParserWindow.logparseobject import LogParserObject
from util.logparser import LogParser


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.path = Path.cwd()
        self.log_path = Path('d:/Games/Steam/steamapps/common/Everquest F2P/Logs')
        self.log_file = self.log_path / 'eqlog_Rarshaak_aradune.txt'
        self.log_parser = LogParserObject(self.log_file)
        self.log_thread = self.create_log_parser_thread()
        self.log_view = LogParserView(self)
        self.create_gui()

    def create_log_parser_thread(self):
        thread = QThread()
        self.log_parser.data_ready.connect(self.process_log_data)
        self.log_parser.moveToThread(thread)
        thread.started.connect(self.log_parser.run)
        thread.start()
        return thread

    def create_gui(self):
        self.setWindowTitle('EQ Parser')
        icon_path = self.path / 'img' / 'eq-icon.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        triggers = TriggerView(self)
        layout = QVBoxLayout()
        layout.addWidget(triggers)
        layout.addWidget(self.log_view)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.resize(950, 350)
        self.show()

    def process_log_data(self, data):
        self.log_view.display_row(data)
