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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLCDNumber, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(985, 745)
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
        self.verticalLayoutWidget_2.setGeometry(QRect(540, 0, 401, 411))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.boardStatusBar = QTextEdit(self.verticalLayoutWidget_2)
        self.boardStatusBar.setObjectName(u"boardStatusBar")
        self.boardStatusBar.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.boardStatusBar)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(280, 440, 231, 221))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 30, 201, 171))
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

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 440, 251, 251))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 40, 231, 191))
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

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(530, 450, 151, 221))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_3)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 30, 131, 171))
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

        self.record_button = QPushButton(self.verticalLayoutWidget_3)
        self.record_button.setObjectName(u"record_button")

        self.verticalLayout_3.addWidget(self.record_button)

        self.replayMatchButton = QPushButton(self.verticalLayoutWidget_3)
        self.replayMatchButton.setObjectName(u"replayMatchButton")

        self.verticalLayout_3.addWidget(self.replayMatchButton)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(700, 450, 261, 191))
        self.horizontalLayoutWidget = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 30, 231, 82))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.vs_lable_2 = QLabel(self.horizontalLayoutWidget)
        self.vs_lable_2.setObjectName(u"vs_lable_2")

        self.verticalLayout_6.addWidget(self.vs_lable_2)

        self.red_team_name_text = QLineEdit(self.horizontalLayoutWidget)
        self.red_team_name_text.setObjectName(u"red_team_name_text")

        self.verticalLayout_6.addWidget(self.red_team_name_text)

        self.red_time_lcdNumber = QLCDNumber(self.horizontalLayoutWidget)
        self.red_time_lcdNumber.setObjectName(u"red_time_lcdNumber")
        self.red_time_lcdNumber.setSmallDecimalPoint(False)
        self.red_time_lcdNumber.setDigitCount(8)
        self.red_time_lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.red_time_lcdNumber.setProperty("value", 0.000000000000000)

        self.verticalLayout_6.addWidget(self.red_time_lcdNumber)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.vs_lable = QLabel(self.horizontalLayoutWidget)
        self.vs_lable.setObjectName(u"vs_lable")

        self.horizontalLayout_5.addWidget(self.vs_lable)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.vs_lable_3 = QLabel(self.horizontalLayoutWidget)
        self.vs_lable_3.setObjectName(u"vs_lable_3")

        self.verticalLayout_7.addWidget(self.vs_lable_3)

        self.blue_team_name_text = QLineEdit(self.horizontalLayoutWidget)
        self.blue_team_name_text.setObjectName(u"blue_team_name_text")

        self.verticalLayout_7.addWidget(self.blue_team_name_text)

        self.blue_time_lcdNumber = QLCDNumber(self.horizontalLayoutWidget)
        self.blue_time_lcdNumber.setObjectName(u"blue_time_lcdNumber")
        self.blue_time_lcdNumber.setSegmentStyle(QLCDNumber.Flat)

        self.verticalLayout_7.addWidget(self.blue_time_lcdNumber)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)

        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(20, 130, 161, 41))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.point_label = QLabel(self.horizontalLayoutWidget_3)
        self.point_label.setObjectName(u"point_label")

        self.horizontalLayout_11.addWidget(self.point_label)

        self.point_lcdNum = QLCDNumber(self.horizontalLayoutWidget_3)
        self.point_lcdNum.setObjectName(u"point_lcdNum")
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        self.point_lcdNum.setFont(font)
        self.point_lcdNum.setSmallDecimalPoint(False)
        self.point_lcdNum.setSegmentStyle(QLCDNumber.Flat)

        self.horizontalLayout_11.addWidget(self.point_lcdNum)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 985, 24))
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
        self.record_button.clicked.connect(MainWindow.record_game)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"AI \u76f8\u5173", None))
        self.redStrategySelectLable.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9\u7b56\u7565", None))
        self.blueStrategySelectLable.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9\u7b56\u7565", None))
        self.setDiceLable.setText(QCoreApplication.translate("MainWindow", u"\u6307\u5b9a\u9ab0\u5b50\u6570\u76ee", None))
        self.letAIDoButton.setText(QCoreApplication.translate("MainWindow", u"AI DO", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5f00\u5c40\u8bbe\u7f6e", None))
        self.modeSelectLable.setText(QCoreApplication.translate("MainWindow", u"\u6e38\u620f\u6a21\u5f0f", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9\u624b\u52a8\u5e03\u5c40", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9\u624b\u52a8\u5e03\u5c40", None))
        self.blue_best_place_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9PC\u5e03\u5c40", None))
        self.red_best_place_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9PC\u5e03\u5c40", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5148\u624b", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u6309\u94ae\u533a", None))
        self.startMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6bd4\u8d5b", None))
        self.diceButton.setText(QCoreApplication.translate("MainWindow", u"PC\u63b7\u9ab0\u5b50", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"\u6094\u68cb", None))
        self.record_button.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u68cb\u8c31", None))
        self.replayMatchButton.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u5f00\u59cb", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u73a9\u5bb6\u4fe1\u606f", None))
        self.vs_lable_2.setText(QCoreApplication.translate("MainWindow", u"\u7ea2\u65b9", None))
        self.vs_lable.setText(QCoreApplication.translate("MainWindow", u"vs", None))
        self.vs_lable_3.setText(QCoreApplication.translate("MainWindow", u"\u84dd\u65b9", None))
        self.point_label.setText(QCoreApplication.translate("MainWindow", u"\u9ab0\u5b50\u7684\u70b9\u6570", None))
    # retranslateUi

