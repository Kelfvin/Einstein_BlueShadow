from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from view.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    mainw = MainWindow()
    mainw.setWindowTitle("成都理工大学 Einstein_KYL")
    mainw.setWindowIcon(QIcon("/assets/icon.ico"))
    mainw.show()
    app.exec()
