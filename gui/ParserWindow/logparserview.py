from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

START_ROW = 0
MAX_ROWS = 1000
COLUMNS = 3
COLUMN_NAMES = ['Date', 'Time', 'Text']


class LogParserView(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.columns = COLUMNS
        self.column_names = COLUMN_NAMES
        self.create_gui()

    def create_gui(self):
        self.setColumnCount(self.columns)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHorizontalHeaderLabels(self.column_names)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.show()

    def display_row(self, data):
        values = []
        timestamp = data.pop('timestamp')
        values.append(timestamp.strftime('%x'))
        values.append(timestamp.strftime('%X'))
        values.append(data.get('text'))
        self.insertRow(START_ROW)
        for column in range(self.columnCount()):
            self.setItem(START_ROW, column, QTableWidgetItem(values[column]))
        if self.rowCount() > MAX_ROWS:
            self.removeRow(self.rowCount() - 1)
