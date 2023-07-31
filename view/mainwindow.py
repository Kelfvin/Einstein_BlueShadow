#!/usr/bin/python

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtCore import Slot, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QFont, Qt, QBrush, QMouseEvent
import numpy as np
from view.mainwindow_ui import Ui_MainWindow
from board import Board
from random import randint
from enums.chess import ChessColor
from enums.mode import Mode
from enums.Agents import Agents
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 界面控制参数

        self.board = Board()
        '''保存整个游戏的数据'''

        self.mode = Mode.HUMAN_HUMAN
        '''当前的对战模式'''

        self.blueAgentName = 'Human'
        self.redAgentName = 'Human'

        self.players = {
            ChessColor.BLUE: None,
            ChessColor.RED: None
        }

        # 是否完成了棋盘的摆放
        self.chessSeted = False

        # 光标选中的棋盘上的位置
        self.selectedPosition = QPoint(-1, -1)

        # 安装事件过滤器
        self.installEventFilter(self)

        # 棋盘 Ui 参数
        self.startX = 0
        self.startY = 0
        self.boardWidth = 400
        self.boardHeight = self.boardWidth
        self.gridX = self.boardWidth/5
        self.gridY = self.boardWidth/5

        # 初始化图形界面和信号槽的绑定
        self.initUI()

    def setRedAgent(self):
        agent = Agents[self.redAgentName]()
        agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = agent

    def setBlueAgent(self):
        agent = Agents[self.blueAgentName]()
        agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = agent

    def initUI(self):
        '''UI元素的值进行初始化'''
        self.initSearchDeepCombBox()
        self.initSetDiceCombBox()
        self.initSetSenteCombBox()
        self.initStrategySelectCombBox()
        self.initGameModeSlectCombBox()

    def initStrategySelectCombBox(self):
        '''初始化策略选择的下拉框'''
        for agentName in Agents:
            self.ui.redStrategySelectCombBox.addItem(agentName)
            self.ui.blueStrategySelectCombBox.addItem(agentName)

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
            self.board.setturn(self.board.sente)

            self.showMsg('比赛开始！')

            # 保存棋子布局,用于后面的日志输出
            self.board.save_initial_pos()

            self.ui.boardStatusBar.append(
                "现在是" + self.board.getturnStr() + "出手")

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
                        print(
                            f'{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}')

                        self.do_move(move, show_msg=False)
                        self.update()
                        QApplication.processEvents()  # 等待界面更新完成

                        if self.board.checkWin() == ChessColor.RED:
                            redWin += 1

                        if self.board.checkWin() == ChessColor.BLUE:
                            blueWin += 1

                    print(f'第{i+1}局结束，用时{time.time()-startTime}秒')
                    print(
                        f'blue({self.blueAgentName})  vs red({self.redAgentName}) --- {blueWin}:{redWin}')

                    # 偶数是蓝方先手，奇数是红方先手
                    firstPlayer = ChessColor.BLUE if i % 2 == 0 else ChessColor.RED
                    # 重新进行初始化，以便下一局
                    self.board = Board(firstPlayer)
                    self.setBlueAgent()
                    self.setRedAgent()

            else:
                pass
                # 不做操作，根据界面上的按钮事件来进行操作

        else:
            msgBox = QMessageBox()
            msgBox.setText("布局非法，请检查！")
            msgBox.exec()

    @Slot(int)
    def handleGameModeChanged(self, int):
        for mode in Mode:
            if mode.name == self.ui.gameModeSelectCombBox.currentText():
                self.mode = mode
                break

        print(f'改变游戏模式为:{mode.name}')

    @Slot(int)
    def redStrategyChanged(self, int):
        self.redAgentName = self.ui.redStrategySelectCombBox.currentText()
        self.setRedAgent()

        print(f'切换红方策略:{self.redAgentName}')

    @Slot(int)
    def blueStrategyChanged(self, int):

        self.blueAgentName = self.ui.blueStrategySelectCombBox.currentText()
        self.setBlueAgent()
        print(f'切换蓝方策略:{self.blueAgentName}')

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

        # 判断是否可以让AI下棋
        turn = self.board.getturn()
        if self.players[turn].name != 'Human':
            move = self.players[turn].get_action(self.board)
            self.do_move(move)

        else:
            self.showMsg('不能使用 AI 作弊，现在是人工操作！')

    def do_move(self, move, show_msg=True):
        '''移动棋子，通过move代码'''
        self.board.do_move(move)
        self.update()

        win = self.board.checkWin()

        if win:
            # 保存日志
            # 就是查看一下日志是不是正确的，如果说一局在1分钟之内完成了，那么可能会覆盖，因为文件名可能是一样的
            self.record_game()

        if show_msg:
            if win == None:
                self.ui.boardStatusBar.append(
                    "现在该" + self.board.getturnStr() + "出手")

            else:
                if win == ChessColor.BLUE:
                    self.showMsg("蓝方赢了！")
                else:
                    self.showMsg("红方赢了")

    @Slot()
    def on_replayMatchButton_clicked(self):
        '''重开'''
        self.chessSeted = False
        self.ui.setDiceComboBox.setEnabled(False)
        self.ui.letAIDoButton.setEnabled(False)
        self.ui.startMatchButton.setEnabled(True)
        self.ui.diceButton.setEnabled(False)
        self.ui.backButton.setEnabled(False)
        self.ui.setSenteComboBox.setEnabled(True)
        self.ui.gameModeSelectCombBox.setEnabled(True)
        self.board = Board()
        self.update()

    @Slot(int)
    def on_setOurColorComboBox_currentIndexChanged(self, index):
        color = ChessColor.BLUE if index == 0 else ChessColor.RED
        self.board.setOurColor(color)
        self.ui.boardStatusBar.append(f'设置我方队伍颜色为{color.name}')

    @Slot(int)
    def onSetDiceComboBoxIndexChanged(self, index):
        self.board.setDice(index+1)
        self.ui.boardStatusBar.append(f'指定骰子数目为{index+1}')

    @Slot(int)
    def on_setSenteComboBox_currentIndexChanged(self, index):
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
            painter.drawLine(self.startX, self.startY + self.gridY * i,
                             self.startX + self.boardWidth, self.startY + self.gridY * i)
            painter.drawLine(self.startX + i * self.gridX, self.startY,
                             self.startX + i * self.gridX, self.startY + self.boardHeight)
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
                        brush = QBrush(QColor(255, 0, 0),
                                       Qt.SolidPattern)  # 红方
                    else:
                        brush = QBrush(QColor(0, 0, 255),
                                       Qt.SolidPattern)  # 蓝方
                    painter.setBrush(brush)
                    painter.drawRect(
                        self.startX + i * self.gridX, self.startY + j * self.gridY, self.gridX, self.gridY)

        x = self.selectedPosition.x()
        y = self.selectedPosition.y()
        if x >= 0 and y >= 0:
            brush = QBrush(QColor(185, 214, 163), Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawRect(self.startX + x * self.gridX,
                             self.startY + y * self.gridY, self.gridX, self.gridY)

        painter.end()

    def drawBoardNumber(self):
        # 实现绘制棋盘数字的逻辑
        for i in range(5):
            for j in range(5):
                self.drawChessNumber(i, j)  # 绘制棋子数字

    def drawChessNumber(self, x, y):
        # 绘制棋子数字的逻辑
        painter = QPainter(self)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        chessNumber = abs(self.board.getChess(x, y))

        font = QFont("Arial", 40)
        painter.setFont(font)

        if (chessNumber > 0):
            painter.drawText(self.startX + self.gridX * (x + 0.3),
                             self.startY + self.gridY * (y + 0.7), str(chessNumber))
        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        point = event.pos()  # 获取点击位置

        x = int(point.x() // self.gridX)
        y = int(point.y()//self.gridY)

        # 点击棋盘
        if x < 5 and y < 5:
            print(x, y)
            self.onBoardTap(x, y)
            self.update()

    def onBoardTap(self, x, y):
        if not self.chessSeted:  # 表示还可以设置棋子
            chessNumber = self.board.getChess(x, y)
            if chessNumber != 0:  # 不允许设置空白区
                chessNumber = self.chessNumberIncrease(chessNumber)
                self.board.setChess((x, y), chessNumber)

        else:  # 棋子数字已经设置完毕
            if self.selectedPosition.x() == -1:
                self.selectedPosition.setX(x)
                self.selectedPosition.setY(y)
            else:
                self.moveChess(self.selectedPosition.toTuple(), (x, y))

    def chessNumberIncrease(self, chessNumber: int) -> int:
        '''返回棋子value+1，且让棋子在其范围内滚动
            红棋 在 -1~-6
            蓝棋 在 1~6'''

        sign = chessNumber/abs(chessNumber)
        chessNumber = (abs(chessNumber)+1) % 7

        if chessNumber == 0:
            chessNumber = 1

        return chessNumber*sign

    def moveChess(self, fromPosition, toPosition):
        '''移动棋子'''

        success = self.board.moveChess(fromPosition, toPosition)

        self.selectedPosition.setX(-1)
        self.selectedPosition.setY(-1)

        # 如果成功移动棋子
        if success:
            self.ui.backButton.setEnabled(True)

            win = self.board.checkWin()
            if win == None:
                self.ui.boardStatusBar.append(
                    "现在该" + self.board.getturnStr() + "出手")
            else:
                # 保存日志
                self.record_game()
                if win == ChessColor.BLUE:
                    self.showMsg("蓝方赢了！")
                else:
                    self.showMsg("红方赢了")

        else:
            self.showMsg("操作非法！")

        self.update()

    def record_game(self):
        file_path = 'game_record/'
        place = '线上'
        date = time.strftime("%Y.%m.%d %H:%M", time.localtime())
        date_place = f'{date} {place}'
        red_player = self.ui.red_team_name_text.toPlainText()
        blue_player = self.ui.blue_team_name_text.toPlainText()
        match_name = '2023 CCGC'

        first_player = red_player if self.board.sente == ChessColor.RED else blue_player
        second_player = blue_player if self.board.sente == ChessColor.RED else red_player
        first_player_color = 'R' if self.board.sente == ChessColor.RED else 'B'
        second_player_color = 'B' if self.board.sente == ChessColor.RED else 'R'

        # 这里先写死，后面再改

        # 12345 到 ABCDE 映射,写成字典
        num_char_map = {
            0: 'A',
            1: 'B',
            2: 'C',
            3: 'D',
            4: 'E'
        }

        if self.board.checkWin() == self.board.sente:
            winner = '先手胜'

        else:
            winner = '后手胜'

        file_name = f'WTN-{first_player} vs {second_player}-{winner}-{date_place}-{match_name}.txt'
        game_info = f'#[{first_player} {first_player_color}][{second_player} {second_player_color}][{winner}][{date_place}][{match_name}];'
        with open(file_path+file_name, 'w', encoding='gb2312', newline='\r\n') as f:
            # 写入比赛的信息
            f.write(game_info+'\n')
            # 写入开局布局
            # 写入红方
            f.write('R:')
            for x, y, index in self.board.red_initial_pos:
                y = abs(5-y)
                x = num_char_map[x]
                chess_index = abs(index)
                f.write(f'{x}{y}-{chess_index};')

            f.write('\n')
            # 写入蓝方
            f.write('B:')
            for x, y, index in self.board.blue_initial_pos:
                y = abs(5-y)
                x = num_char_map[x]
                chess_index = abs(index)
                f.write(f'{x}{y}-{chess_index};')
            f.write('\n')

            # 写入每一步的走法
            for i, (move, point) in enumerate(zip(self.board.movements, self.board.points)):
                x, y, dx, dy = self.board.move_to_location(move)
                # 这里 x 和 y 还是用的最原始的，可以索引到棋子
                print((self.board.boardBackup[i].T))
                chess_index = self.board.boardBackup[i][x][y]
                sign = 'R' if chess_index < 0 else 'B'
                chess_index = abs(chess_index)
                dy = abs(5-dy)
                dx = num_char_map[dx]

                f.write(f'{i+1}:{point};({sign}{chess_index},{dx}{dy})\n')

    def showMsg(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()
