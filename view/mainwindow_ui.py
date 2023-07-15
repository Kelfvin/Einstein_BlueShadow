# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1006, 721)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 481, 421))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(620, 10, 361, 661))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.boardStatusBar = QTextEdit(self.verticalLayoutWidget_2)
        self.boardStatusBar.setObjectName(u"boardStatusBar")
        self.boardStatusBar.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.boardStatusBar)

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setGeometry(QRect(150, 510, 112, 34))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 440, 111, 41))
        self.searchDeepCombBox = QComboBox(self.centralwidget)
        self.searchDeepCombBox.setObjectName(u"searchDeepCombBox")
        self.searchDeepCombBox.setGeometry(QRect(120, 450, 91, 31))
        self.diceButton = QPushButton(self.centralwidget)
        self.diceButton.setObjectName(u"diceButton")
        self.diceButton.setGeometry(QRect(20, 510, 112, 34))
        self.startMatchButton = QPushButton(self.centralwidget)
        self.startMatchButton.setObjectName(u"startMatchButton")
        self.startMatchButton.setGeometry(QRect(290, 590, 112, 34))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 470, 81, 18))
        self.setOurColorComboBox = QComboBox(self.centralwidget)
        self.setOurColorComboBox.setObjectName(u"setOurColorComboBox")
        self.setOurColorComboBox.setGeometry(QRect(380, 470, 99, 24))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(280, 520, 81, 18))
        self.setSenteComboBox = QComboBox(self.centralwidget)
        self.setSenteComboBox.setObjectName(u"setSenteComboBox")
        self.setSenteComboBox.setGeometry(QRect(380, 520, 99, 24))
        self.replayMatchButton = QPushButton(self.centralwidget)
        self.replayMatchButton.setObjectName(u"replayMatchButton")
        self.replayMatchButton.setGeometry(QRect(420, 590, 112, 34))
        self.useGivenDiceButton = QPushButton(self.centralwidget)
        self.useGivenDiceButton.setObjectName(u"useGivenDiceButton")
        self.useGivenDiceButton.setGeometry(QRect(150, 590, 121, 41))
        self.setDiceComboBox = QComboBox(self.centralwidget)
        self.setDiceComboBox.setObjectName(u"setDiceComboBox")
        self.setDiceComboBox.setGeometry(QRect(20, 590, 111, 31))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 560, 111, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1006, 29))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"\u6094\u68cb", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6df1\u5ea6", None))
        self.diceButton.setText(QCoreApplication.translate("MainWindow", u"PC\u63b7\u9ab0\u5b50", None))
        self.startMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6bd4\u8d5b", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6211\u65b9\u989c\u8272", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5148\u624b", None))
        self.replayMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u5f00\u59cb", None))
        self.useGivenDiceButton.setText(QCoreApplication.translate("MainWindow", u"\u6307\u5b9a\u6570\u884c\u8d70", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6307\u5b9a\u9ab0\u5b50\u6570\u76ee", None))
    # retranslateUi

