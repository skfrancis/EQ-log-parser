from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class ParserView(QTableWidget):
    def __init__(self, parent, columns, column_names):
        super().__init__(parent)
        self._columns = columns
        self._column_names = column_names
        self.create_gui()

    def create_gui(self):
        self.setColumnCount(self._columns)
        self.setHorizontalHeaderLabels(self._column_names)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.show()

    # TODO: split date and time
    def add_row(self, data):
        row = self.rowCount()
        self.insertRow(row)
        values = list(data.values())
        for column in range(self.columnCount()):
            self.setItem(row, column, QTableWidgetItem(str(values[column])))
        self.show()
