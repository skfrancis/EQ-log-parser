from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QAction
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QCursor
from gui.triggerdialog import TriggerDialog
from gui.groupdialog import GroupDialog
from gui.triggergroup import TriggerGroup
from gui.triggeritem import TriggerItem
from pathlib import Path
from lxml import etree


class TriggerView(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.path = Path.cwd()
        self._config_file = self.path / 'triggers.xml'
        self._root = self.invisibleRootItem()
        self.importTree()
        self.create_gui()

    def create_gui(self):
        print(self.path)
        self.setHeaderLabels(['Triggers'])
        self.setAlternatingRowColors(True)
        self.setColumnCount(1)
        self.addTopLevelItem(self._root)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.itemDoubleClicked.connect(self.open_item)
        self.customContextMenuRequested.connect(self.open_menu)
        self.show()

    def clear_selection(self):
        self.setCurrentItem(self._root)
        self.clearSelection()

    def importTree(self):
        def build(item, parent):
            for element in parent.getchildren():
                data = dict(element.attrib)
                data['id'] = element.tag
                if tag == 'group':
                    child = TriggerGroup(self.path, data)
                else:
                    child = TriggerItem(self.path, data)
                item.addChild(child)
                build(child, element)
            item.setExpanded(True)
        with open(self._config_file, 'rb') as file:
            tree = etree.parse(file)
            root = tree.getroot()
            build(self._root, root)

    def export_tree(self):
        def build(item, parent):
            for row in range(item.childCount()):
                child = item.child(row)
                data = child.data(0, QTreeWidgetItem.UserType)
                tag = data.pop('id')
                element = etree.SubElement(parent, tag, attrib=data)
                build(child, element)
        root = etree.Element('Triggers')
        tree = etree.ElementTree(root)
        build(self._root, root)
        with open(self._config_file, 'wb') as file:
            tree.write(file, encoding="utf-8", xml_declaration=True, pretty_print=True)

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
        if item:
            dialog = GroupDialog(self, None)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerGroup(self.path, dialog.group_data))
                else:
                    item.parent().addChild(TriggerGroup(self.path, dialog.group_data))
            self.clear_selection()
        else:
            dialog = GroupDialog(self, None)
            if dialog.exec():
                self.addTopLevelItem(TriggerGroup(self.path, dialog.group_data))
                self.clear_selection()
        self.export_tree()

    @pyqtSlot()
    def add_trigger(self):
        item = self.currentItem()
        if item:
            dialog = TriggerDialog(self, None)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerItem(self.path, dialog.trigger_data))
                else:
                    item.parent().addChild(TriggerItem(self.path, dialog.trigger_data))
                self.clear_selection()
        else:
            dialog = TriggerDialog(self, None)
            if dialog.exec():
                self.addTopLevelItem(TriggerItem(self.path, dialog.trigger_data))
                self.clear_selection()
        self.export_tree()

    @pyqtSlot()
    def delete_item(self):
        for item in self.selectedItems():
            (item.parent() or self._root).removeChild(item)
        self.export_tree()

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
        menu.exec(QCursor().pos())
