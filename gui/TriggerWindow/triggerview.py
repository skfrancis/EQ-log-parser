from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QAction
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QCursor
from gui.TriggerWindow.triggerdialogs import GroupDialog, TriggerDialog
from gui.TriggerWindow.triggeritems import TriggerGroup, TriggerItem
from pathlib import Path
from lxml import etree


class TriggerView(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.path = Path.cwd()
        self.config_file = self.path / 'config' / 'triggers.xml'
        self.root = self.invisibleRootItem()
        self.importTree()
        self.create_gui()

    def create_gui(self):
        self.setHeaderLabels(['Triggers'])
        self.setAlternatingRowColors(True)
        self.setColumnCount(1)
        self.addTopLevelItem(self.root)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.itemDoubleClicked.connect(self.open_item)
        self.customContextMenuRequested.connect(self.open_menu)
        self.show()

    def importTree(self):
        def build(item, parent, path):
            data = {'Tag': parent.tag}
            child = item

            for element in parent.iterchildren():
                if element.tag != 'Groups' or element.tag != 'Triggers':
                    data[element.tag] = element.text
            if parent.tag == 'Group':
                child = TriggerGroup(path, data)
            elif parent.tag == 'Trigger':
                child = TriggerItem(path, data)
            if parent.find('Groups') is not None:
                for element in parent.find('Groups').iterchildren():
                    build(child, element, path)
            if parent.find('Triggers') is not None:
                for element in parent.find('Triggers').iterchildren():
                    build(child, element, path)
            if child != item:
                item.addChild(child)
                item.setExpanded(True)

        if self.config_file.exists():
            with open(self.config_file, 'rb') as file:
                tree = etree.parse(file)
                root = tree.getroot()
                build(self.root, root, self.path)

    def export_tree(self):
        def build(item, parent):
            groups = etree.SubElement(parent, 'Groups')
            triggers = etree.SubElement(parent, 'Triggers')
            for row in range(item.childCount()):
                child = item.child(row)
                data = child.data(0, QTreeWidgetItem.UserType)
                tag = data.pop('Tag')
                if tag == 'Group':
                    element = etree.SubElement(groups, tag)
                else:
                    element = etree.SubElement(triggers, tag)
                for key in data:
                    etree.SubElement(element, key).text = data.get(key)
                if child.childCount() > 0:
                    build(child, element)

        root = etree.Element('TriggerConfig')
        tree = etree.ElementTree(root)
        if self.root.childCount() > 0:
            build(self.root, root)

        with self.config_file.open('wb') as file:
            tree.write(file, encoding="utf-8", xml_declaration=True, pretty_print=True)

    def clear_selection(self):
        self.setCurrentItem(self.root)
        self.clearSelection()

    @pyqtSlot()
    def open_item(self):
        item = self.currentItem()
        if isinstance(item, TriggerGroup):
            dialog = GroupDialog(self, item.data(0, QTreeWidgetItem.UserType))
            if dialog.exec():
                item.setText(0, dialog.group_data.get('Name'))
                item.setData(0, QTreeWidgetItem.UserType, dialog.group_data)
            pass
        elif isinstance(item, TriggerItem):
            dialog = TriggerDialog(self, item.data(0, QTreeWidgetItem.UserType))
            if dialog.exec():
                item.setText(0, dialog.trigger_data.get('Name'))
                item.setData(0, QTreeWidgetItem.UserType, dialog.trigger_data)
        self.export_tree()

    @pyqtSlot()
    def add_group(self):
        item = self.currentItem()
        data = {'Tag': 'Group'}
        if item:
            dialog = GroupDialog(self, data)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerGroup(self.path, dialog.group_data))
                else:
                    if item.parent() is None:
                        self.addTopLevelItem(TriggerGroup(self.path, dialog.group_data))
                    else:
                        item.parent().addChild(TriggerGroup(self.path, dialog.group_data))
            self.clear_selection()
        else:
            dialog = GroupDialog(self, data)
            if dialog.exec():
                self.addTopLevelItem(TriggerGroup(self.path, dialog.group_data))
                self.clear_selection()
        self.export_tree()

    @pyqtSlot()
    def add_trigger(self):
        item = self.currentItem()
        data = {'Tag': 'Trigger'}
        if item:
            dialog = TriggerDialog(self, data)
            if dialog.exec():
                if isinstance(item, TriggerGroup):
                    item.addChild(TriggerItem(self.path, dialog.trigger_data))
                else:
                    if item.parent() is None:
                        self.addTopLevelItem(TriggerItem(self.path, dialog.trigger_data))
                    else:
                        item.parent().addChild(TriggerItem(self.path, dialog.trigger_data))
                self.clear_selection()
        else:
            dialog = TriggerDialog(self, data)
            if dialog.exec():
                self.addTopLevelItem(TriggerItem(self.path, dialog.trigger_data))
                self.clear_selection()
        self.export_tree()

    @pyqtSlot()
    def delete_item(self):
        for item in self.selectedItems():
            (item.parent() or self.root).removeChild(item)
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
