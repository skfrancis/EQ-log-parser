from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QAction
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QCursor
from gui.triggerdialog import TriggerDialog
from gui.groupdialog import GroupDialog
from gui.triggergroup import TriggerGroup
from gui.triggeritem import TriggerItem
# Remove when done testing
from PyQt5.QtWidgets import QApplication
import sys


class TriggerView(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._root = self.invisibleRootItem()
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

    def _clear_selection(self):
        self.setCurrentItem(self._root)
        self.clearSelection()

    @pyqtSlot()
    def open_item(self):
        item = self.currentItem()
        if isinstance(item, TriggerGroup):
            dialog = GroupDialog(self, item.data(0, QTreeWidgetItem.UserType))
            if dialog.exec():
                item.setText(0, dialog.group_data.get('name'))
                item.setData(0, QTreeWidgetItem.UserType, dialog.group_data)
            pass
        elif isinstance(item, TriggerItem):
            dialog = TriggerDialog(self, item.data(0, QTreeWidgetItem.UserType))
            if dialog.exec():
                item.setText(0, dialog.trigger_data.get('name'))
                item.setData(0, QTreeWidgetItem.UserType, dialog.trigger_data)

    @pyqtSlot()
    def add_group(self):
        item = self.currentItem()
        # TODO: build new group
        data = {'id': 0, 'name': '', 'search_text': '', 'alert_text': '', 'use_audio': False, 'audio_file': ''}
        if item:
            dialog = GroupDialog(self, data)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerGroup(dialog.group_data))
                else:
                    item.parent().addChild(TriggerGroup(dialog.group_data))
            self._clear_selection()
        else:
            dialog = GroupDialog(self, data)
            if dialog.exec():
                self.addTopLevelItem(TriggerGroup(dialog.group_data))
                self._clear_selection()

    @pyqtSlot()
    def add_trigger(self):
        item = self.currentItem()
        # TODO: build new trigger
        data = {'id': 0, 'name': '', 'search_text': '', 'alert_text': '', 'use_audio': False, 'audio_file': ''}
        if item:
            dialog = TriggerDialog(self, data)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerItem(dialog.trigger_data))
                else:
                    item.parent().addChild(TriggerItem(dialog.trigger_data))
                self._clear_selection()
        else:
            dialog = TriggerDialog(self, data)
            if dialog.exec():
                self.addTopLevelItem(TriggerItem(dialog.trigger_data))
                self._clear_selection()

    @pyqtSlot()
    def delete_item(self):
        for item in self.selectedItems():
            (item.parent() or self._root).removeChild(item)

    @pyqtSlot()
    def open_menu(self):
        menu = QMenu(self)
        add_group = QAction('Add Group', self)
        add_trigger = QAction('Add Trigger', self)
        add_group.triggered.connect(self.add_group)
        add_trigger.triggered.connect(self.add_trigger)
        menu.addAction(add_group)
        menu.addAction(add_trigger)
        menu.addSeparator()
        add_edit = QAction('Edit', self)
        add_delete = QAction('Delete', self)
        add_edit.triggered.connect(self.open_item)
        add_delete.triggered.connect(self.delete_item)
        menu.addAction(add_edit)
        menu.addAction(add_delete)
        menu.exec(QCursor.pos())


# Remove when done testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TriggerView(None)
    sys.exit(app.exec_())
