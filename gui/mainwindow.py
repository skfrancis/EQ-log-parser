from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QStatusBar, QLabel, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from pathlib import Path
from gui.parseview import ParseView
from filters.logparserfilter import LogParserFilter
from filters.zoningfilter import ZoningFilter
from gui.widgets.triggers.triggerview import TriggerView
from gui.widgets.log.logparserthreadobject import LogParserThreadObject


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.path = Path.cwd()
        self.log_path = Path('d:/Games/Steam/steamapps/common/Everquest F2P/Logs')
        self.log_file = self.log_path / 'eqlog_Sithraak_aradune.txt'
        self.log_parser = LogParserThreadObject(self.log_file)
        self.log_filter = LogParserFilter()
        self.log_thread = self.create_log_parser_thread()
        self.log_view = ParseView(self, self.log_filter.get_config())

        self.status_bar = QStatusBar()

        self.zone_filter = ZoningFilter()
        self.zone_label = QLabel('Current Zone: {}'.format(None))

        self.status_bar.addPermanentWidget(self.zone_label)
        self.create_gui()

    def create_log_parser_thread(self):
        thread = QThread()
        self.log_parser = LogParserThreadObject(self.log_file)
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
        self.setStatusBar(self.status_bar)
        self.resize(950, 350)
        self.show()

    def process_log_data(self, data):
        self.update_current_zone(self.zone_filter.parse(data))
        self.log_view.display_row(self.log_filter.parse(data))

    def update_current_zone(self, zone_data):
        if zone_data:
            self.zone_label.setText('Current Zone: {}'.format(zone_data.get('zone')))
