from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QIcon
from pathlib import Path


class TriggerItem(QTreeWidgetItem):
    def __init__(self, trigger_data):
        super().__init__()
        self.setData(0, self.UserType, trigger_data)
        self.create_gui()

    def create_gui(self):
        icon_path = Path.cwd() / 'img' / 'trigger.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setIcon(0, icon)
        self.setText(0, self.data(0, self.UserType).get('name'))
