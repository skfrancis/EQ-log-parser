from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('EQ Parser')
        self.resize(750, 750)
        self.show()


