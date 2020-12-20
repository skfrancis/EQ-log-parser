from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon
from pathlib import Path
from PyQt5.QtCore import pyqtSlot


class GroupDialog(QDialog):
    def __init__(self, parent, group_data):
        super().__init__(parent)
        self._id = 'group'
        self._path = self.parent().path / 'img'
        self.group_data = group_data
        if group_data:
            self._name = QLineEdit(self.group_data.get('name'))
        else:
            self._name = QLineEdit()
        self._button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
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
            'id': self._id,
            'name': self._name.text()
        }
        self.accept()
