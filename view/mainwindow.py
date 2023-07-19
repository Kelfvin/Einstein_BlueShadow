#!/usr/bin/python

from PySide6.QtWidgets import QMainWindow,QApplication,QMessageBox
from PySide6.QtCore import Slot,QPoint,QEvent
from PySide6.QtGui import QPainter, QPen, QColor, QFont,Qt,QBrush,QMouseEvent
from logic.huamn import HumanPlayer
from view.mainwindow_ui import Ui_MainWindow
import sys
from logic.board import Board
from random import randint
from enums.chess import ChessColor
from enums.mode import Mode
from enums.strategy import Strategy
from logic.UCT.UCT import UCT
from logic.Net.pure_mcts import MCTSPlayer
import asyncio
import time



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 界面控制参数

        self.board = Board()
        '''保存棋局'''


        self.mode = Mode.HUMAN_HUMAN
        '''当前的对战模式'''

        self.blueStrategy = Strategy.PURE_MCTS
        self.redStrategy = Strategy.PURE_MCTS

        self.players = {
            ChessColor.BLUE:None,
            ChessColor.RED:None
        }




        # 是否完成了棋盘的摆放
        self.chessSeted = False

        # 光标选中的棋盘上的位置
        self.selectedPosition = QPoint(-1,-1)

        # 安装事件过滤器
        self.installEventFilter(self)

        # 棋盘 Ui 参数
        self.startX = 0
        self.startY = 0
        self.boardWidth = 400
        self.boardHeight = self.boardWidth
        self.gridX = self.boardWidth/5
        self.gridY = self.boardWidth/5


        # 策略模型的初始化

        self.modules = {
            Strategy.HUMAN:HumanPlayer,
            Strategy.UCT:UCTPlayer,
            Strategy.PURE_MCTS: MCTSPlayer
            # Strategy.ALPHA_ZERO:
        }


        # 初始化图形界面和信号槽的绑定
        self.initUI()


    def setRedAgent(self):
        Agent = self.modules[self.redStrategy]()
        Agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = Agent


    def setBlueAgent(self):
        Agent = self.modules[self.blueStrategy]()
        Agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = Agent


    def initUI(self):
        '''UI元素的值进行初始化'''
        self.initSearchDeepCombBox()
        self.initSetDiceCombBox()
        self.initSetSenteCombBox()
        self.initStrategySelectCombBox()
        self.initGameModeSlectCombBox()


    def initStrategySelectCombBox(self):
        '''初始化策略选择的下拉框'''
        for strategy in Strategy:
            self.ui.redStrategySelectCombBox.addItem(strategy.name)
            self.ui.blueStrategySelectCombBox.addItem(strategy.name)

    
    def initGameModeSlectCombBox(self):
        '''初始化游戏模式选择的下拉框'''
        for mode in Mode:
            self.ui.gameModeSelectCombBox.addItem(mode.name)

    def initSetSenteCombBox(self):
        '''初始化先手选择的下拉框'''
        self.ui.setSenteComboBox.addItem("蓝色")
        self.ui.setSenteComboBox.addItem("红色")


    def initSearchDeepCombBox(self):
        '''初始化搜索深度的下拉框'''
        for i in range(1, 7):
            self.ui.searchDeepCombBox.addItem(str(i))
    

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

        str = f"{self.board.getturnStr()}投掷出了{dice}"
        self.ui.boardStatusBar.append(str)
        

    @Slot()
    def on_startMatchButton_clicked(self):
        checkResult = self.board.checkBoardSet()

        if checkResult:

            self.chessSeted = True

            self.setBlueAgent()
            self.setRedAgent()

            
            self.showMsg('比赛开始！')

            self.ui.boardStatusBar.append("现在是" + self.board.getturnStr() + "出手")

            # ui 上一些按钮的禁用和启用
            self.ui.setDiceComboBox.setEnabled(True)
            self.ui.letAIDoButton.setEnabled(True)
            self.ui.startMatchButton.setEnabled(False)
            self.ui.diceButton.setEnabled(True)
            self.ui.backButton.setEnabled(False)
            self.ui.setSenteComboBox.setEnabled(False)
            self.ui.gameModeSelectCombBox.setEnabled(False)

            
            if self.mode == Mode.AI_AI:
            # 如果是AI对战，那么就让AI开始下棋
                blueWin = redWin = 0
                
                for i in range(100):
                    print(f'\n第{i+1}局')
                    startTime = time.time()
                    while self.board.checkWin() == None:
                        self.on_diceButton_clicked()
                        turn = self.board.getturn()
                        print(f'{self.players[turn].name} start to stimulate')
                        stimulateTimeStart = time.time()
                        move = self.players[turn].get_action(self.board)
                        print(f'{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}')


                        self.do_move(move,show_msg=False)
                        self.update()   
                        QApplication.processEvents()  # 等待界面更新完成

                        if self.board.checkWin() == ChessColor.RED:
                            redWin+=1

                        if self.board.checkWin() == ChessColor.BLUE:
                            blueWin+=1


                    print(f'第{i+1}局结束，用时{time.time()-startTime}秒')
                    print(f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')

                    self.board = Board()
                    self.setBlueAgent()
                    self.setRedAgent()
                    


        else:
            msgBox = QMessageBox()
            msgBox.setText("布局非法，请检查！")
            msgBox.exec()

    @Slot(int)
    def handleGameModeChanged(self,int):
        for mode in Mode:
            if mode.name ==  self.ui.gameModeSelectCombBox.currentText():
                self.mode = mode

        print(f'改变游戏模式为:{mode}')


    @Slot(int)
    def redStrategyChanged(self,int):
        for strategy in Strategy:
            if strategy == self.ui.redStrategySelectCombBox.currentText():
                self.redStrategy = strategy

        print(f'切换红方策略:{strategy}')

    @Slot(int)
    def blueStrategyChanged(self,int):
        for strategy in Strategy:
            if strategy == self.ui.blueStrategySelectCombBox.currentText():
                self.blueStrategy = strategy

        print(f'切换蓝方策略:{strategy}')


    @Slot()
    def letAIDo(self):
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

        
        # 根据当前是谁的回合交给对应的agent进行处理
        turn = self.board.getturn()
        move = self.players[turn].get_action(self.board)
        # 后面写一个人的agent，不返回任何的move
        if move:
            self.do_move(move)


    def do_move(self,move):
        self.board.do_move(move)
        self.update()

        win = self.board.checkWin()
        if win == None:
            self.ui.boardStatusBar.append("现在该" + self.board.getturnStr() + "出手")
        elif win == ChessColor.BLUE:
            self.showMsg("蓝方赢了！")
        else:
            self.showMsg("红方赢了")


    @Slot()
    def on_replayMatchButton_clicked(self):
        '''重开'''
        pass

    @Slot(int)
    def on_setOurColorComboBox_currentIndexChanged(self,index):
        color = ChessColor.BLUE if index == 0 else ChessColor.RED
        self.board.setOurColor(color)
        self.ui.boardStatusBar.append(f'设置我方队伍颜色为{color.name}')

    @Slot(int)
    def onSetDiceComboBoxIndexChanged(self,index):
        self.board.setDice(index+1)
        self.ui.boardStatusBar.append(f'指定骰子数目为{index+1}')

    @Slot(int)
    def on_setSenteComboBox_currentIndexChanged(self,index):
        color = ChessColor.BLUE if index == 0 else ChessColor.RED
        self.board.setSente(color)
        self.ui.boardStatusBar.append(f"设置先手颜色为{color.name}")

    @Slot()
    def on_backButton_clicked(self):
        result = Board.undo()

        if not result:
            self.showMsg('不能撤销了！')

        self.update()


    def blueTurn(self):
        if self.mode == Mode.AI_AI or self.mode == Mode.AI_HUMAN:
            self.on_diceButton_clicked()
            self.letAIDo()

        else:
            pass
            # 这里就是说人来走

    def redTurn(self):
        if self.mode == Mode.HUMAN_AI:
            self.letAIDo()

        else:
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
                self.moveChess(self.selectedPosition.toTuple(), (x,y))

    def chessNumberIncrease(self,chessNumber:int)->int:
        '''返回棋子value+1，且让棋子在其范围内滚动
            红棋 在 -1~-6
            蓝棋 在 1~6'''
        
        sign = chessNumber/abs(chessNumber)
        chessNumber = (abs(chessNumber)+1)%7

        if chessNumber == 0:
            chessNumber = 1
        
        return chessNumber*sign
    


    def moveChess(self, fromPosition, toPosition):

        success = self.board.moveChess(fromPosition, toPosition)

        self.selectedPosition.setX(-1)
        self.selectedPosition.setY(-1)

        # 如果成功移动棋子
        if success:
            self.board.backupBoard()
            self.ui.backButton.setEnabled(True)

            win = self.board.checkWin()
            if win == None:
                self.ui.boardStatusBar.append("现在该" + self.board.getturnStr() + "出手")
            elif win == ChessColor.BLUE:
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


    




