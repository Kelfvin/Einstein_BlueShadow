#!/usr/bin/python

from PySide6.QtWidgets import QMainWindow,QApplication,QMessageBox
from PySide6.QtCore import Slot,QPoint,QEvent
from PySide6.QtGui import QPainter, QPen, QColor, QFont,Qt,QBrush,QMouseEvent
from view.mainwindow_ui import Ui_MainWindow
import sys
from logic.board import Board
from random import randint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.board = Board()

        self.mode = 'human'

        # 光标选中的棋盘上的位置
        self.selectedPosition = QPoint(-1,-1)

        # 安装事件过滤器
        self.installEventFilter(self)

        # 棋盘 Ui 参数
        self.startX = 0;
        self.startY = 0
        self.boardWidth = 400
        self.boardHeight = self.boardWidth
        self.gridX = self.boardWidth/5
        self.gridY = self.boardWidth/5

        self.chessSeted = False

        self.initUI()
        self.initSlot()


    def initUI(self):
        '''UI元素的值进行初始化'''
        self.initSearchDeepCombBox()
        self.initSetOurColorCombBox()
        self.initSetDiceCombBox()
        self.initSetSenteCombBox()
        self.initStrategySelectCombBox()


    def initStrategySelectCombBox(self):
        '''初始化策略选择的下拉框'''
        self.ui.strategySelectCombBox.addItem('UCT')


    def initSetSenteCombBox(self):
        '''初始化先手选择的下拉框'''
        self.ui.setSenteComboBox.addItem("蓝色")
        self.ui.setSenteComboBox.addItem("红色")


    def initSearchDeepCombBox(self):
        '''初始化搜索深度的下拉框'''
        for i in range(1, 7):
            self.ui.searchDeepCombBox.addItem(str(i))
    
    def initSetOurColorCombBox(self):
        '''初始化我方队伍颜色选择的下拉框'''
        self.ui.setOurColorComboBox.addItem("蓝色")
        self.ui.setOurColorComboBox.addItem("红色")

    def initSetDiceCombBox(self):  
        '''初始化指定骰子的下拉框''' 
        for i in range(1, 7):
            self.ui.setDiceComboBox.addItem(str(i))



    def initSlot(self):
        pass

    @Slot()
    def on_diceButton_clicked(self):
        dice = randint(1, 6)
        self.board.setDice(dice)

        str = f"{self.board.getNowPlayerStr()}投掷出了{dice}"
        self.ui.boardStatusBar.append(str)

        # 如果是我们的轮，就让 AI 算法来走
        if self.board.getNowPlayer() == self.board.getOurColor():
            self.ourTurn()

        self.enemyTurn()

    @Slot()
    def on_startMatchButton_clicked(self):
        checkResult = self.board.checkBoardSet()

        if checkResult:

            self.chessSeted = True
            msgBox = QMessageBox()
            msgBox.setText("比赛开始！")
            msgBox.exec()
            self.board.setNowPlayer(self.board.getSente())

            self.ui.boardStatusBar.append("现在是" + self.board.getNowPlayerStr() + "出手")

            self.ui.setDiceComboBox.setEnabled(True)
            self.ui.useGivenDiceButton.setEnabled(True)
            self.ui.startMatchButton.setEnabled(False)
            self.ui.diceButton.setEnabled(True)
            self.ui.backButton.setEnabled(False)
            self.ui.setSenteComboBox.setEnabled(False)
            self.ui.setOurColorComboBox.setEnabled(False)


        else:
            msgBox = QMessageBox()
            msgBox.setText("布局非法，请检查！")
            msgBox.exec()


    @Slot(int)
    def on_setOurColorComboBox_currentIndexChanged(self,index):
        color = 1 if index == 0  else -1
        self.board.setOurColor(color)
        print(f'设置我方队伍颜色为{color}')

    def ourTurn():
        '''这里写轮到我方的时候，是什么策略'''
        pass

    def enemyTurn():
        '''这里写对方走的时候是什么策略。之所以这么弄是为了方便调试
        '''
        pass


    def paintEvent(self, event):
            self.drawBoardLine()
            self.drawBoardColor()
            self.drawBoardNumber()

    def drawBoardLine(self):
        # 实现绘制棋盘线的逻辑
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)
        # 画棋盘

        for i in range(6):
            # 画横线
            # 画竖线
            painter.drawLine(self.startX, self.startY + self.gridY * i, self.startX + self.boardWidth, self.startY + self.gridY * i)
            painter.drawLine(self.startX + i * self.gridX, self.startY, self.startX + i * self.gridX, self.startY + self.boardHeight)
        painter.end()

    def drawBoardColor(self):
        # 实现绘制棋盘颜色的逻辑
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)
        # 绘制棋子颜色（不带数字）
        for i in range(5):
            for j in range(5):
                chess = self.board.getChess(i, j)  # 获取棋子值
                if chess != 0:
                    if chess < 0:
                        brush = QBrush(QColor(255, 0, 0), Qt.SolidPattern)  # 红方
                    else:
                        brush = QBrush(QColor(0, 0, 255), Qt.SolidPattern)  # 蓝方
                    painter.setBrush(brush)
                    painter.drawRect(self.startX + i * self.gridX, self.startY + j * self.gridY, self.gridX, self.gridY)

        x = self.selectedPosition.x()
        y = self.selectedPosition.y()
        if x >= 0 and y >= 0:
            brush = QBrush(QColor(185, 214, 163), Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawRect(self.startX + x * self.gridX, self.startY + y * self.gridY, self.gridX, self.gridY)

        painter.end()

    def drawBoardNumber(self):
        # 实现绘制棋盘数字的逻辑
        for i in range(5):
            for j in range(5):
                self.drawChessNumber(i, j)  # 绘制棋子数字

    def drawChessNumber(self,x,y):
        # 绘制棋子数字的逻辑
        painter = QPainter(self)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        chessNumber = abs(self.board.getChess(x, y))  

        font = QFont("Arial", 40)
        painter.setFont(font)

        if(chessNumber>0):
            painter.drawText(self.startX + self.gridX * (x + 0.3), self.startY + self.gridY * (y + 0.7), str(chessNumber))
        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        point = event.pos()  # 获取点击位置

        x = int(point.x()// self.gridX) 
        y = int(point.y()//self.gridY)
        
        # 点击棋盘
        if x < 5 and y < 5:
            print(x,y)
            self.onBoardTap(x, y)
            self.update()

        
    def onBoardTap(self, x, y):
        if not self.chessSeted:  # 表示还可以设置棋子
            chessNumber = self.board.getChess(x, y)
            if  chessNumber!= 0:  # 不允许设置空白区
                chessNumber = self.chessNumberIncrease(chessNumber)
                self.board.setChess((x,y), chessNumber)

        else:  # 棋子数字已经设置完毕
            if self.selectedPosition.x() == -1:
                self.selectedPosition.setX(x)
                self.selectedPosition.setY(y) 
            else:
                self.moveChess(self.selectedPosition.x(), self.selectedPosition.y(), x, y)

    def chessNumberIncrease(self,chessNumber:int)->int:
        '''返回棋子value+1，且让棋子在其范围内滚动
            红棋 在 -1~-6
            蓝棋 在 1~6'''
        
        sign = chessNumber/abs(chessNumber)
        chessNumber = (abs(chessNumber)+1)%7

        if chessNumber == 0:
            chessNumber = 1
        
        return chessNumber*sign
    
    def letAIDo():
        '''交给AI做(听天由命>_<)
            后期改成可以在多个模型中进行切换，以防万一'''
        
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         

        
        # To do 这里放 传给AI的东西


    def moveChess(self, x1, y1, x2, y2):

        success = self.board.moveChess((x1, y1), (x2, y2))

        self.selectedPosition.setX(-1)
        self.selectedPosition.setY(-1)

        # 如果成功移动棋子
        if success:
            self.board.backupBoard()
            self.ui.backButton.setEnabled(True)

            win = self.board.checkWin()
            if win == 0:
                self.ui.boardStatusBar.append("现在该" + self.board.getNowPlayerStr() + "出手")
            elif win == 1:
                self.showMsg("蓝方赢了！")
            else:
                self.showMsg("红方赢了")

        else:
            self.showMsg("操作非法！")

        self.update()

    def showMsg(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()


    




