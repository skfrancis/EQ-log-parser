from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

START_ROW = 0


class ParseView(QTableWidget):
    def __init__(self, parent, config):
        super(ParseView, self).__init__(parent)
        self.columns = config.pop('columns')
        self.max_rows = config.pop('max_rows')
        self.column_names = list(config.keys())
        self.column_sizes = list(config.values())
        self.create_gui()

    def create_gui(self):
        self.setColumnCount(self.columns)
        header = self.horizontalHeader()
        for column in range(self.columnCount()):
            header.setSectionResizeMode(column, self.column_sizes[column])
        self.setHorizontalHeaderLabels(self.column_names)
        # self.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.setSortingEnabled(True)
        self.show()

    def display_row(self, data):
        self.insertRow(START_ROW)
        for column in range(self.columnCount()):
            self.setItem(START_ROW, column, QTableWidgetItem(data[self.column_names[column]]))
        if self.max_rows:
            if self.rowCount() > self.max_rows:
                self.removeRow(self.rowCount() - 1)
