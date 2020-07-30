from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView


class TriggerView(QTreeView):
    def __init__(self):
        super().__init__()
        self.create_gui()
        self.setHeaderHidden(True)

    def create_gui(self):
        tree_model = QStandardItemModel()
        self.setModel(tree_model)
        root_node = tree_model.invisibleRootItem()

        test = QStandardItem()

        test.setText('This is a test')
        test1 = QStandardItem()
        test1.setText('Sub Test')
        test.appendRow(test1)
        root_node.appendRow(test)
        pass
