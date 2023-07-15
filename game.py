from PySide6.QtWidgets import QApplication
from view.mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    mainw = MainWindow()
    mainw.show()
    app.exec()