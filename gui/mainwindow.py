from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QStatusBar, QLabel, QWidget, QTabWidget, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSlot
from pathlib import Path
import json
from gui.parseview import ParseView
from filters.logparserfilter import LogParserFilter

from filters.chatfilter import ChatFilter
from filters.partyfilter import PartyFilter
from filters.considerfilter import ConsiderFilter
from filters.factionfilter import FactionFilter
from filters.locationfilter import LocationFilter
from filters.systemmessagefilter import SystemMessageFilter
from filters.castingfilter import CastingFilter
from filters.zoningfilter import ZoningFilter

from gui.widgets.triggers.triggerview import TriggerView
from gui.widgets.settings.settingsdialog import SettingsDialog
from gui.widgets.log.logparserthreadobject import LogParserThreadObject


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.path = Path.cwd()
        self.settings_path = self.path / 'config'
        self.settings_data = self.load_settings()
        self.game_path = Path(self.settings_data.get('game_directory', ''))
        self.log_parser = None
        self.log_thread = self.create_log_parser()
        self.log_filter = LogParserFilter()
        self.log_view = ParseView(self, self.log_filter.get_config())
        self.tabs_widget = QTabWidget()
        self.create_trigger_view()
        self.filters = []
        self.create_parse_filters()
        self.views = []
        self.create_parse_views()
        self.zone_filter = ZoningFilter()
        self.server_label = QLabel('Server: {}'.format(self.settings_data.get('server_name', '')))
        self.character_label = QLabel('Character: {}'.format(self.settings_data.get('character', '')))
        self.zone_label = QLabel('Current Zone: {}'.format(None))
        self.log_thread.start()
        self.create_menu_bar()
        self.create_status_bar()
        self.create_gui()

    def load_settings(self):
        def load_data(file_name):
            json_data = {}
            if file_name.exists():
                with file_name.open() as file:
                    json_data = json.load(file)
                    file.close()
                    return json_data
            return json_data

        settings_file = self.settings_path / 'settings.json'
        return load_data(settings_file)

    def open_settings(self):
        dialog = SettingsDialog(self, self.settings_data)
        if dialog.exec():
            self.save_settings(dialog.settings_data)
            self.settings_data = dialog.settings_data

    def save_settings(self, settings_data):
        settings_file = self.settings_path / 'settings.json'
        with settings_file.open('w') as file:
            json.dump(settings_data, file, indent=4)
            file.close()

    def create_trigger_view(self):
        triggers = TriggerView(self)
        self.tabs_widget.addTab(triggers, 'Triggers')

    def create_log_parser(self):
        thread = QThread()
        log_path = self.game_path / 'Logs'
        log_file = log_path / self.settings_data.get('log_file', '')
        if log_file.exists():
            self.log_parser = LogParserThreadObject(log_file)
            self.log_parser.data_ready.connect(self.process_log_data)
            self.log_parser.moveToThread(thread)
            thread.started.connect(self.log_parser.run)
        return thread

    def create_parse_filters(self):
        self.filters.append(ChatFilter())
        self.filters.append(PartyFilter())
        self.filters.append(ConsiderFilter())
        self.filters.append(FactionFilter())
        self.filters.append(LocationFilter())
        self.filters.append(SystemMessageFilter())
        self.filters.append(CastingFilter())

    def create_parse_views(self):
        for filter_name in self.filters:
            view = ParseView(self, filter_name.get_config())
            self.create_tab_view(view, filter_name.get_filter_name())
            self.views.append(view)

    def create_tab_view(self, view, tab_name):
        self.tabs_widget.addTab(view, tab_name)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = QMenu('File', self)
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.open_settings)
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close_event)
        file_menu.addAction(settings_action)
        file_menu.addAction(exit_action)
        help_menu = QMenu('Help', self)
        about_action = QAction('About', self)
        help_menu.addAction(about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(help_menu)

    def create_status_bar(self):
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(self.server_label)
        status_bar.addPermanentWidget(self.character_label)
        status_bar.addPermanentWidget(self.zone_label)

    def create_gui(self):
        self.setWindowTitle('EQ Parser')
        icon_path = self.path / 'img' / 'eq-icon.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs_widget)
        layout.addWidget(self.log_view)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.resize(950, 350)
        self.show()

    def process_log_data(self, data):
        for filter_name in self.filters:
            if filter_name.parse(data):
                index = self.filters.index(filter_name)
                self.views[index].display_row(filter_name.parse(data))
        self.update_current_zone(self.zone_filter.parse(data))
        self.log_view.display_row(self.log_filter.parse(data))

    def update_current_zone(self, zone_data):
        if zone_data:
            self.zone_label.setText('Current Zone: {}'.format(zone_data.get('zone')))

    def close_event(self):
        self.close()
