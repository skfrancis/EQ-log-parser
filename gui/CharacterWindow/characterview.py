from PyQt5.QtWidgets import QListWidget


class CharacterView(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.path = Path.cwd()
        self._config_file = self.path / 'config'
        self.create_gui()

    def create_gui(self):
        self.setAlternatingRowColors(True)
