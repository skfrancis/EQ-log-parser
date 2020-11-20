from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QThread
from util.parser import Parser


class ParserView(QTableWidget):
    def __init__(self, parent, log_file):
        super().__init__(parent)
        self.log_file = log_file
        self.columns = 2
        self.column_names = ['timestamp', 'text']
        self.parser = Parser(self.log_file)
        self.thread = QThread()
        self.create_parser()
        self.create_gui()

    def create_parser(self):
        self.parser.data_ready.connect(self.add_row)
        self.parser.moveToThread(self.thread)
        self.thread.started.connect(self.parser.run)
        self.thread.start()

    def create_gui(self):
        self.setColumnCount(self.columns)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHorizontalHeaderLabels(self.column_names)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.show()

    # TODO: split date and time
    def add_row(self, data):
        row = self.rowCount()
        self.insertRow(row)
        values = list(data.values())
        for column in range(self.columnCount()):
            self.setItem(row, column, QTableWidgetItem(str(values[column])))
