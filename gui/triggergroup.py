from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QIcon
from pathlib import Path


class TriggerGroup(QTreeWidgetItem):
    def __init__(self, group_data):
        super().__init__()
        self.setData(0, self.UserType, group_data)
        self.create_gui()

    def create_gui(self):
        icon_path = Path.cwd() / 'img' / 'folder.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setIcon(0, icon)
        self.setText(0, self.data(0, self.UserType).get('name'))
