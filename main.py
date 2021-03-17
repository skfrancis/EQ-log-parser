from PySide6.QtWidgets import QApplication, QMainWindow
from gui.mainwindow import MainWindow
from pathlib import Path
import sys


def main():
    cwd = Path.cwd()
    app = QApplication(sys.argv)
    window = MainWindow(app, cwd)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
