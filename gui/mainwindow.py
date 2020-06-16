from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_gui()

    def create_gui(self):
        self.setGeometry(100, 100, 750, 750)
        self.setWindowTitle('EQ Parser')
        self.show()


