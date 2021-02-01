from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QCheckBox, QDialogButtonBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from pathlib import Path
from uuid import uuid4


class TriggerDialog(QDialog):
    def __init__(self, parent, trigger_data):
        super().__init__(parent)
        self.trigger_data = trigger_data
        self.tag = self.trigger_data.get('Tag')
        self.uuid = str(uuid4())
        self.path = self.parent().path / 'img'
        self.name = QLineEdit(self.trigger_data.get('Name', ''))
        self.search_text = QLineEdit(self.trigger_data.get('SearchText', ''))
        self.alert_text = QLineEdit(self.trigger_data.get('AlertText', ''))
        self.use_audio = QCheckBox()
        self.use_audio.setChecked(eval(self.trigger_data.get('UseAudio', 'False')))
        self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.save)
        self.button_box.rejected.connect(self.reject)
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Trigger Editor')
        icon_path = self.path / 'trigger.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        form_layout = QFormLayout()
        form_layout.addRow('Trigger Name:', self.name)
        form_layout.addRow('Search Text:', self.search_text)
        form_layout.addRow('Alert Text:', self.alert_text)
        form_layout.addRow('Use Audio:', self.use_audio)
        form_layout.addRow(self.button_box)
        self.setLayout(form_layout)
        self.open()

    @pyqtSlot()
    def save(self):
        self.trigger_data = {
            'Tag': self.tag,
            'Name': self.name.text(),
            'SearchText': self.search_text.text(),
            'AlertText': self.alert_text.text(),
            'UseAudio': str(self.use_audio.isChecked()),
            'id': self.uuid
        }
        self.accept()


class GroupDialog(QDialog):
    def __init__(self, parent, group_data):
        super().__init__(parent)
        self.group_data = group_data
        self.tag = self.group_data.get('Tag')
        self.uuid = str(uuid4())
        self.path = self.parent().path / 'img'
        self.name = QLineEdit(self.group_data.get('Name', ''))
        self.comments = QLineEdit(self.group_data.get('Comments', ''))
        self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.button_box.accepted.connect(self.save)
        self.button_box.rejected.connect(self.reject)
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Group Editor')
        icon_path = self.path / 'folder.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        form_layout.addRow('Group Name:', self.name)
        form_layout.addRow('Comments: ', self.comments)
        form_layout.addRow(self.button_box)
        self.setLayout(form_layout)
        self.open()

    @pyqtSlot()
    def save(self):
        self.group_data = {
            'Tag': self.tag,
            'Name': self.name.text(),
            'Comments': self.comments.text(),
            'id': self.uuid
        }
        self.accept()
