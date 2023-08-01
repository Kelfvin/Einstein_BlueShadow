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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(955, 779)
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
        self.verticalLayoutWidget_2.setGeometry(QRect(560, 80, 321, 401))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.boardStatusBar = QTextEdit(self.verticalLayoutWidget_2)
        self.boardStatusBar.setObjectName(u"boardStatusBar")
        self.boardStatusBar.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.boardStatusBar)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(753, 500, 131, 171))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.startMatchButton = QPushButton(self.verticalLayoutWidget_3)
        self.startMatchButton.setObjectName(u"startMatchButton")

        self.verticalLayout_3.addWidget(self.startMatchButton)

        self.diceButton = QPushButton(self.verticalLayoutWidget_3)
        self.diceButton.setObjectName(u"diceButton")

        self.verticalLayout_3.addWidget(self.diceButton)

        self.backButton = QPushButton(self.verticalLayoutWidget_3)
        self.backButton.setObjectName(u"backButton")

        self.verticalLayout_3.addWidget(self.backButton)

        self.replayMatchButton = QPushButton(self.verticalLayoutWidget_3)
        self.replayMatchButton.setObjectName(u"replayMatchButton")

        self.verticalLayout_3.addWidget(self.replayMatchButton)

        self.verticalLayoutWidget_4 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(560, 500, 181, 195))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.modeSelectLable = QLabel(self.verticalLayoutWidget_4)
        self.modeSelectLable.setObjectName(u"modeSelectLable")
        self.modeSelectLable.setMargin(0)

        self.horizontalLayout_3.addWidget(self.modeSelectLable)

        self.gameModeSelectCombBox = QComboBox(self.verticalLayoutWidget_4)
        self.gameModeSelectCombBox.setObjectName(u"gameModeSelectCombBox")

        self.horizontalLayout_3.addWidget(self.gameModeSelectCombBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.red_pos_lineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.red_pos_lineEdit.setObjectName(u"red_pos_lineEdit")

        self.horizontalLayout_8.addWidget(self.red_pos_lineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.verticalLayoutWidget_4)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.blue_pos_lineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.blue_pos_lineEdit.setObjectName(u"blue_pos_lineEdit")

        self.horizontalLayout.addWidget(self.blue_pos_lineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.blue_best_place_pushButton = QPushButton(self.verticalLayoutWidget_4)
        self.blue_best_place_pushButton.setObjectName(u"blue_best_place_pushButton")

        self.horizontalLayout_9.addWidget(self.blue_best_place_pushButton)

        self.red_best_place_pushButton = QPushButton(self.verticalLayoutWidget_4)
        self.red_best_place_pushButton.setObjectName(u"red_best_place_pushButton")

        self.horizontalLayout_9.addWidget(self.red_best_place_pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.setSenteComboBox = QComboBox(self.verticalLayoutWidget_4)
        self.setSenteComboBox.setObjectName(u"setSenteComboBox")

        self.horizontalLayout_2.addWidget(self.setSenteComboBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutWidget_5 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(290, 460, 191, 61))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget_5)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.searchDeepCombBox = QComboBox(self.horizontalLayoutWidget_5)
        self.searchDeepCombBox.setObjectName(u"searchDeepCombBox")

        self.horizontalLayout_5.addWidget(self.searchDeepCombBox)

        self.verticalLayoutWidget_5 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(32, 458, 201, 171))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.redStrategySelectLable = QLabel(self.verticalLayoutWidget_5)
        self.redStrategySelectLable.setObjectName(u"redStrategySelectLable")

        self.horizontalLayout_7.addWidget(self.redStrategySelectLable)

        self.redStrategySelectCombBox = QComboBox(self.verticalLayoutWidget_5)
        self.redStrategySelectCombBox.setObjectName(u"redStrategySelectCombBox")

        self.horizontalLayout_7.addWidget(self.redStrategySelectCombBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.blueStrategySelectLable = QLabel(self.verticalLayoutWidget_5)
        self.blueStrategySelectLable.setObjectName(u"blueStrategySelectLable")

        self.horizontalLayout_6.addWidget(self.blueStrategySelectLable)

        self.blueStrategySelectCombBox = QComboBox(self.verticalLayoutWidget_5)
        self.blueStrategySelectCombBox.setObjectName(u"blueStrategySelectCombBox")

        self.horizontalLayout_6.addWidget(self.blueStrategySelectCombBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.setDiceLable = QLabel(self.verticalLayoutWidget_5)
        self.setDiceLable.setObjectName(u"setDiceLable")

        self.horizontalLayout_4.addWidget(self.setDiceLable)

        self.setDiceComboBox = QComboBox(self.verticalLayoutWidget_5)
        self.setDiceComboBox.setObjectName(u"setDiceComboBox")

        self.horizontalLayout_4.addWidget(self.setDiceComboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.letAIDoButton = QPushButton(self.verticalLayoutWidget_5)
        self.letAIDoButton.setObjectName(u"letAIDoButton")

        self.verticalLayout_5.addWidget(self.letAIDoButton)

        self.red_team_name_text = QPlainTextEdit(self.centralwidget)
        self.red_team_name_text.setObjectName(u"red_team_name_text")
        self.red_team_name_text.setGeometry(QRect(560, 40, 131, 31))
        self.vs_lable = QLabel(self.centralwidget)
        self.vs_lable.setObjectName(u"vs_lable")
        self.vs_lable.setGeometry(QRect(710, 50, 58, 16))
        self.blue_team_name_text = QPlainTextEdit(self.centralwidget)
        self.blue_team_name_text.setObjectName(u"blue_team_name_text")
        self.blue_team_name_text.setGeometry(QRect(760, 40, 121, 31))
        self.vs_lable_2 = QLabel(self.centralwidget)
        self.vs_lable_2.setObjectName(u"vs_lable_2")
        self.vs_lable_2.setGeometry(QRect(560, 20, 58, 16))
        self.vs_lable_3 = QLabel(self.centralwidget)
        self.vs_lable_3.setObjectName(u"vs_lable_3")
        self.vs_lable_3.setGeometry(QRect(760, 20, 58, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 955, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.letAIDoButton.clicked.connect(MainWindow.letAIDo)
        self.gameModeSelectCombBox.currentIndexChanged.connect(MainWindow.handleGameModeChanged)
        self.redStrategySelectCombBox.currentIndexChanged.connect(MainWindow.redStrategyChanged)
        self.blueStrategySelectCombBox.currentIndexChanged.connect(MainWindow.blueStrategyChanged)
        self.setDiceComboBox.currentIndexChanged.connect(MainWindow.onSetDiceComboBoxIndexChanged)
        self.red_pos_lineEdit.returnPressed.connect(MainWindow.place_red_pos)
        self.blue_pos_lineEdit.returnPressed.connect(MainWindow.place_blue_pos)
        self.blue_best_place_pushButton.clicked.connect(MainWindow.blue_best_place)
        self.red_best_place_pushButton.clicked.connect(MainWindow.red_best_place)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.startMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6bd4\u8d5b", None))
        self.diceButton.setText(QCoreApplication.translate("MainWindow", u"PC\u63b7\u9ab0\u5b50", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"\u6094\u68cb", None))
        self.replayMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u5f00\u59cb", None))
        self.modeSelectLable.setText(QCoreApplication.translate("MainWindow", u"\u6e38\u620f\u6a21\u5f0f", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9\u624b\u52a8\u5e03\u5c40", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9\u624b\u52a8\u5e03\u5c40", None))
        self.blue_best_place_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9PC\u5e03\u5c40", None))
        self.red_best_place_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9PC\u5e03\u5c40", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5148\u624b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6df1\u5ea6", None))
        self.redStrategySelectLable.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9\u7b56\u7565", None))
        self.blueStrategySelectLable.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9\u7b56\u7565", None))
        self.setDiceLable.setText(QCoreApplication.translate("MainWindow", u"\u6307\u5b9a\u9ab0\u5b50\u6570\u76ee", None))
        self.letAIDoButton.setText(QCoreApplication.translate("MainWindow", u"AI DO", None))
        self.red_team_name_text.setPlainText(QCoreApplication.translate("MainWindow", u"player1", None))
        self.vs_lable.setText(QCoreApplication.translate("MainWindow", u"vs", None))
        self.blue_team_name_text.setPlainText(QCoreApplication.translate("MainWindow", u"player2", None))
        self.vs_lable_2.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9", None))
        self.vs_lable_3.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9", None))
    # retranslateUi

