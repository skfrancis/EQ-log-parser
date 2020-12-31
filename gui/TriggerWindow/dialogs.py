from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QCheckBox, QDialogButtonBox
from PyQt5.QtGui import QIcon
from pathlib import Path
from PyQt5.QtCore import pyqtSlot


class TriggerDialog(QDialog):
    def __init__(self, parent, trigger_data):
        super().__init__(parent)
        self._tag = 'Trigger'
        self._path = self.parent().path / 'img'
        self.trigger_data = trigger_data
        if trigger_data:
            self._name = QLineEdit(self.trigger_data.get('Name'))
            self._search_text = QLineEdit(self.trigger_data.get('SearchText'))
            self._alert_text = QLineEdit(self.trigger_data.get('AlertText'))
            self._use_audio = QCheckBox()
            self._use_audio.setChecked(eval(self.trigger_data.get('UseAudio')))
            self._file_name = QLineEdit(self.trigger_data.get('FileName'))
        else:
            self._name = QLineEdit()
            self._search_text = QLineEdit()
            self._alert_text = QLineEdit()
            self._use_audio = QCheckBox()
            self._use_audio.setChecked(False)
            self._file_name = QLineEdit()
        self._button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self._button_box.accepted.connect(self.save)
        self._button_box.rejected.connect(self.reject)
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Trigger Editor')
        icon_path = self._path / 'trigger.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        form_layout = QFormLayout()
        form_layout.addRow('Trigger Name:', self._name)
        form_layout.addRow('Search Text:', self._search_text)
        form_layout.addRow('Alert Text:', self._alert_text)
        form_layout.addRow('Use Audio:', self._use_audio)
        form_layout.addRow('Audio File:', self._file_name)
        form_layout.addRow(self._button_box)
        self.setLayout(form_layout)
        self.open()

    @pyqtSlot()
    def save(self):
        self.trigger_data = {
            'Tag': self._tag,
            'Name': self._name.text(),
            'SearchText': self._search_text.text(),
            'AlertText': self._alert_text.text(),
            'UseAudio': str(self._use_audio.isChecked()),
            'FileName': self._file_name.text()
        }
        self.accept()


class GroupDialog(QDialog):
    def __init__(self, parent, group_data):
        super().__init__(parent)
        self._tag = 'Group'
        self._path = self.parent().path / 'img'
        self.group_data = group_data
        if group_data:
            self._name = QLineEdit(self.group_data.get('Name'))
        else:
            self._name = QLineEdit()
        self._button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self._button_box.accepted.connect(self.save)
        self._button_box.rejected.connect(self.reject)
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Group Editor')
        icon_path = self._path / 'folder.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        form_layout.addRow('Group Name:', self._name)
        form_layout.addRow(self._button_box)
        self.setLayout(form_layout)
        self.open()

    @pyqtSlot()
    def save(self):
        self.group_data = {
            'Tag': self._tag,
            'Name': self._name.text()
        }
        self.accept()
