from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QCursor
from gui.triggerdialog import TriggerDialog
from gui.triggergroup import TriggerGroup
from gui.triggeritem import TriggerItem
# Remove when done testing
from PyQt5.QtWidgets import QApplication
import sys


class TriggerView(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        trigger_data = {
            'id': 123,
            'name': 'Feign Death',
            'search_text': '^You begin casting Feign Death',
            'alert_text': 'Casted Feign Death',
            'use_audio': True,
            'audio_file': 'testing'
        }
        self._root = TriggerItem(trigger_data)
        self.create_gui()

    def create_gui(self):
        self.setHeaderLabels(['Triggers'])
        self.setAlternatingRowColors(True)
        self.setColumnCount(1)
        self.addTopLevelItem(self._root)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.itemDoubleClicked.connect(self.open_item)
        self.customContextMenuRequested.connect(self.open_menu)
        self.show()

    @pyqtSlot()
    def open_item(self):
        item = self.currentItem()
        if isinstance(item, TriggerGroup):
            pass
        elif isinstance(item, TriggerItem):
            dialog = TriggerDialog(self, item.data(0, QTreeWidgetItem.UserType))
            if dialog.exec():
                item.setText(0, dialog.trigger_data.get('name'))
                item.setData(0, QTreeWidgetItem.UserType, dialog.trigger_data)

    @pyqtSlot()
    def open_menu(self):
        menu = QMenu(self)
        menu.addAction('Add Group')
        menu.addAction('Add Trigger')
        menu.addSeparator()
        menu.addAction('Edit')
        menu.addAction('Delete')
        menu.exec(QCursor.pos())


# Remove when done testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TriggerView(None)
    sys.exit(app.exec_())
