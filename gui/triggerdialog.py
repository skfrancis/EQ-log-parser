from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QCheckBox, QDialogButtonBox
from PyQt5.QtGui import QIcon
from pathlib import Path
from PyQt5.QtCore import pyqtSlot


class TriggerDialog(QDialog):
    def __init__(self, parent, trigger_data):
        super().__init__(parent)
        self._id = 'trigger'
        self._path = self.parent().path / 'img'
        self.trigger_data = trigger_data
        if trigger_data:
            self._name = QLineEdit(self.trigger_data.get('name'))
            self._search_text = QLineEdit(self.trigger_data.get('search_text'))
            self._alert_text = QLineEdit(self.trigger_data.get('alert_text'))
            self._use_audio = QCheckBox()
            self._use_audio.setChecked(eval(self.trigger_data.get('use_audio')))
            self._file_name = QLineEdit(self.trigger_data.get('file_name'))
        else:
            self._name = QLineEdit()
            self._search_text = QLineEdit()
            self._alert_text = QLineEdit()
            self._use_audio = QCheckBox()
            self._use_audio.setChecked(False)
            self._file_name = QLineEdit()
        self._button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
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
            'id': self._id,
            'name': self._name.text(),
            'search_text': self._search_text.text(),
            'alert_text': self._alert_text.text(),
            'use_audio': str(self._use_audio.isChecked()),
            'file_name': self._file_name.text()
        }
        self.accept()
