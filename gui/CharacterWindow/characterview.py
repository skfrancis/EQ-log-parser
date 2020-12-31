from PyQt5.QtWidgets import QListWidget


class CharacterView(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_gui()

    def create_gui(self):
        self.setAlternatingRowColors(True)
