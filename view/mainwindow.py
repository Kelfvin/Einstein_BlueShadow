#!/usr/bin/python

import time
from random import randint

from PySide6.QtCore import QPoint, QTimer, Slot
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPalette,
    QPen,
    Qt,
)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from board import Board
from enums.Agents import Agents
from enums.chess import ChessColor
from enums.mode import Mode
from view.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.board = Board()

        self.chessSeted = False
        """是否已经设置了棋子"""

        self.selectedPosition = QPoint(-1, -1)
        """当前选中的棋子的位置"""

        self.mode = Mode.HUMAN_HUMAN
        """当前的对战模式"""

        self.redAgentName = "Human"

        self.blueAgentName = "Human"

        self.players = {
            ChessColor.BLUE: None,
            ChessColor.RED: None
        }

        self.sente = ChessColor.BLUE

        # 安装事件过滤器
        self.installEventFilter(self)

        # 棋盘 Ui 参数
        self.startX = 0
        self.startY = 0
        self.boardWidth = 400
        self.boardHeight = self.boardWidth
        self.gridX = self.boardWidth/5
        self.gridY = self.boardWidth/5

        self.timer = QTimer()

        # 初始化图形界面和信号槽的绑定
        self.initUI()

        # 初始化新游戏
        self.init_new_game()

    def init_new_game(self) -> None:
        """初始化新游戏,包括参数的设置，和ui的初始化，每次重开游戏的时候调用这个"""
        self.board = Board()
        self.chessSeted = False
        self.selectedPosition = QPoint(-1, -1)
        self.set_ui_before_match_start()
        # 双方各有4分钟的时间
        self.timer.stop()
        self.redTime = 240
        self.blueTime = 240

    def setRedAgent(self) -> None:
        agent = Agents[self.redAgentName]()
        agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = agent

    def setBlueAgent(self) -> None:
        agent = Agents[self.blueAgentName]()
        agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = agent

    def initUI(self) -> None:
        """UI元素的值进行初始化"""
        self.initSetDiceCombBox()
        self.initSetSenteCombBox()
        self.initStrategySelectCombBox()
        self.initGameModeSlectCombBox()

        self.init_lcdNumber()

        # 一些按键的禁用
        self.ui.backButton.setEnabled(False)
        self.ui.letAIDoButton.setEnabled(False)
        self.ui.diceButton.setEnabled(False)
        self.ui.setDiceComboBox.setEnabled(False)
        self.ui.record_button.setEnabled(False)

    def init_lcdNumber(self) -> None:
        """初始化lcdNumber"""
        self.ui.red_time_lcdNumber.setDigitCount(3)
        self.ui.blue_time_lcdNumber.setDigitCount(3)

    def initStrategySelectCombBox(self) -> None:
        """初始化策略选择的下拉框"""
        for agentName in Agents:
            self.ui.redStrategySelectCombBox.addItem(agentName)
            self.ui.blueStrategySelectCombBox.addItem(agentName)

    def initGameModeSlectCombBox(self) -> None:
        """初始化游戏模式选择的下拉框"""
        for mode in Mode:
            self.ui.gameModeSelectCombBox.addItem(mode.name)

    def initSetSenteCombBox(self) -> None:
        """初始化先手选择的下拉框"""
        self.ui.setSenteComboBox.addItem("蓝色")
        self.ui.setSenteComboBox.addItem("红色")

    def initSetDiceCombBox(self) -> None:
        """初始化指定骰子的下拉框"""
        for i in range(1, 7):
            self.ui.setDiceComboBox.addItem(str(i))

    def update_point_lcdNum(self) -> None:
        """更新骰子点数的显示"""
        dice = self.board.getDice()
        self.ui.point_lcdNum.display(dice)
        # 设置 QLCDNumber 的颜色
        palette = self.ui.point_lcdNum.palette()
        if self.board.getturn() == ChessColor.RED:
            palette.setColor(QPalette.WindowText,
                             QColor(255, 0, 0))  # 设置数字颜色为红色

        else:
            palette.setColor(QPalette.WindowText, QColor(0, 0, 255))
        self.ui.point_lcdNum.setPalette(palette)

        # 把数字显示在UI上
        self.ui.point_lcdNum.display(dice)
        self.update()

    def initSlot(self) -> None:
        pass

    @Slot()
    def on_diceButton_clicked(self) -> None:
        dice = randint(1, 6)
        self.board.setDice(dice)

        # 更新骰子点数的显示
        self.update_point_lcdNum()

    def set_ui_before_match_start(self) -> None:
        """比赛开始前的UI设置"""

        self.ui.startMatchButton.setEnabled(True)
        self.ui.gameModeSelectCombBox.setEnabled(True)
        self.ui.red_pos_lineEdit.setEnabled(True)
        self.ui.blue_pos_lineEdit.setEnabled(True)
        self.ui.red_best_place_pushButton.setEnabled(True)
        self.ui.blue_best_place_pushButton.setEnabled(True)
        self.ui.setSenteComboBox.setEnabled(True)
        self.ui.setDiceComboBox.setEnabled(False)
        self.ui.letAIDoButton.setEnabled(False)
        self.ui.diceButton.setEnabled(False)
        self.ui.record_button.setEnabled(False)

        self.ui.red_time_lcdNumber.display(240)
        self.ui.blue_time_lcdNumber.display(240)

        self.ui.boardStatusBar.clear()

        # 设置 QLCDNumber 的颜色
        palette = self.ui.red_time_lcdNumber.palette()
        palette.setColor(QPalette.WindowText,
                         QColor(255, 0, 0))  # 设置数字颜色为红色

        self.ui.red_time_lcdNumber.setPalette(palette)

        # 设置 QLCDNumber 的颜色
        palette = self.ui.blue_time_lcdNumber.palette()
        palette.setColor(QPalette.WindowText,
                         QColor(0, 0, 255))  # 设置数字颜色为蓝色
        self.ui.blue_time_lcdNumber.setPalette(palette)

    def set_ui_after_match_start(self) -> None:
        """比赛开始时，更新一些UI的状态"""

        # 开局后禁用开始比赛按钮
        self.ui.startMatchButton.setEnabled(False)

        # 开始游戏后，不允许再设置游戏的模式
        self.ui.gameModeSelectCombBox.setEnabled(False)

        # 开局后不允许再设置棋子
        self.ui.red_pos_lineEdit.setEnabled(False)
        self.ui.blue_pos_lineEdit.setEnabled(False)
        self.ui.red_best_place_pushButton.setEnabled(False)
        self.ui.blue_best_place_pushButton.setEnabled(False)

        # 开局后不能设置先手后手
        self.ui.setSenteComboBox.setEnabled(False)

        # 开局后可以指定骰子点数
        self.ui.setDiceComboBox.setEnabled(True)

        # 开局后AI按钮可以使用
        self.ui.letAIDoButton.setEnabled(True)
        self.ui.diceButton.setEnabled(True)

        self.ui.record_button.setEnabled(True)

        # 开始倒计时
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_count_down_lcdNum)
        self.timer.start(1000)

        # 显示开局信息
        self.ui.boardStatusBar.append(self.board.initial_pos_info())

    def update_count_down_lcdNum(self) -> None:
        """更新倒计时的显示"""
        turn = self.board.getturn()
        if turn == ChessColor.RED:
            self.redTime -= 1
            self.ui.red_time_lcdNumber.display(self.redTime)

        else:
            self.blueTime -= 1
            self.ui.blue_time_lcdNumber.display(self.blueTime)

        self.update()

    @Slot()
    def on_startMatchButton_clicked(self) -> None:
        checkResult = self.board.checkBoardSet()
        if not checkResult:
            self.showMsg("棋子没有摆放正确!")
            return

        # 获取双方队伍的名称
        blue_team_name = self.ui.blue_team_name_text.text()
        red_team_name = self.ui.red_team_name_text.text()
        # 如果为空就提醒
        if blue_team_name == "" or red_team_name == "":
            self.showMsg("玩家名称不能为空!")
            return

        self.chessSeted = True

        self.setBlueAgent()
        self.setRedAgent()
        self.board.setSente(self.sente)
        self.board.setturn(self.sente)

        self.showMsg("比赛开始！")
        self.ui.boardStatusBar.append(self.get_game_info())

        # 保存棋子布局,用于后面的日志输出
        self.board.save_initial_pos()

        # ui 上一些按钮的禁用和启用
        self.set_ui_after_match_start()

        if self.mode == Mode.AI_AI:
            # 如果是AI对战，那么就让AI开始下棋
            blueWin = redWin = 0

            for i in range(100):
                print(f"\n第{i+1}局")
                startTime = time.time()
                while self.board.checkWin() is None:
                    self.on_diceButton_clicked()
                    turn = self.board.getturn()
                    print(f"{self.players[turn].name} start to stimulate")
                    stimulateTimeStart = time.time()
                    move = self.players[turn].get_action(self.board)
                    print(
                        f"{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}")

                    self.do_move(move, show_msg=False)
                    self.update()
                    QApplication.processEvents()  # 等待界面更新完成

                    if self.board.checkWin() == ChessColor.RED:
                        redWin += 1

                    if self.board.checkWin() == ChessColor.BLUE:
                        blueWin += 1

                print(f"第{i+1}局结束，用时{time.time()-startTime}秒")
                print(
                    f"blue({self.blueAgentName})  vs red({self.redAgentName}) --- {blueWin}:{redWin}")

                # 偶数是蓝方先手，奇数是红方先手
                firstPlayer = ChessColor.BLUE if i % 2 == 0 else ChessColor.RED
                # 重新进行初始化，以便下一局
                self.board = Board(firstPlayer)
                self.setBlueAgent()
                self.setRedAgent()

        else:
            pass
            # 不做操作，根据界面上的按钮事件来进行操作

    @Slot()
    def place_red_pos(self) -> None:
        """从文本框中获取输入进行布局"""
        # 获取输入的棋子序列
        pieces_text = self.ui.red_pos_lineEdit.text()
        # 输入的是一串数字字符，如：123456
        # 从红方的角落，从上往下，一排一排的放
        if len(pieces_text) == 6:
            pieces_list = []
            for chess in pieces_text:
                pieces_list.append(int(chess))

            self.board.place_red_pos(pieces_list)

        self.update()

    @Slot()
    def place_blue_pos(self) -> None:
        """从文本框中获取输入进行布局"""
        # 获取输入的棋子序列
        pieces_text = self.ui.blue_pos_lineEdit.text()
        # 输入的是一串数字字符，如：123456
        # 从蓝方的角落，从下往上，一排一排的放

        if len(pieces_text) == 6:
            pieces_list = []
            for chess in pieces_text:
                pieces_list.append(int(chess))

            self.board.place_blue_pos(pieces_list)

        self.update()

    @Slot()
    def red_best_place(self) -> None:
        """红方最佳布局"""
        self.board.red_best_place()
        self.update()

    @Slot()
    def blue_best_place(self) -> None:
        """蓝方最佳布局"""
        self.board.blue_best_place()
        self.update()

    @Slot(int)
    def handleGameModeChanged(self, index: int) -> None:
        for mode in Mode:
            if mode.name == self.ui.gameModeSelectCombBox.currentText():
                self.mode = mode
                break

        print(f"改变游戏模式为:{mode.name}")

    @Slot(int)
    def redStrategyChanged(self, index: int) -> None:
        self.redAgentName = self.ui.redStrategySelectCombBox.currentText()
        self.setRedAgent()

        print(f"切换红方策略:{self.redAgentName}")

    @Slot(int)
    def blueStrategyChanged(self, index: int) -> None:

        self.blueAgentName = self.ui.blueStrategySelectCombBox.currentText()
        self.setBlueAgent()
        print(f"切换蓝方策略:{self.blueAgentName}")

    @Slot()
    def letAIDo(self) -> None:
        """交给AI做(听天由命>_<)
            后期改成可以在多个模型中进行切换，以防万一"""

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
        if self.players[turn].name != "Human":
            move = self.players[turn].get_action(self.board)
            self.do_move(move)

        else:
            self.showMsg("不能使用 AI 作弊，现在是人工操作！")

    def do_move(self, move: int, show_msg: bool = True) -> None:
        """移动棋子，通过move代码"""
        self.board.do_move(move)
        self.update()
        self.ui.boardStatusBar.append(self.board.last_move_info())
        win = self.board.checkWin()

        if win:
            # 保存日志
            # 就是查看一下日志是不是正确的，如果说一局在1分钟之内完成了，那么可能会覆盖，因为文件名可能是一样的
            self.record_game()

        if show_msg and win:
            self.timer.stop()
            if win == ChessColor.BLUE:
                self.showMsg("蓝方赢了！")
            else:
                self.showMsg("红方赢了")

    @Slot()
    def on_replayMatchButton_clicked(self) -> None:
        """重开"""
        self.init_new_game()
        self.update()

    @Slot(int)
    def on_setOurColorComboBox_currentIndexChanged(self, index: int) -> None:
        color = ChessColor.BLUE if index == 0 else ChessColor.RED
        self.board.setOurColor(color)
        self.ui.boardStatusBar.append(f"设置我方队伍颜色为{color.name}")

    @Slot(int)
    def onSetDiceComboBoxIndexChanged(self, index: int) -> None:
        self.board.setDice(index+1)
        self.update_point_lcdNum()

    @Slot(int)
    def on_setSenteComboBox_currentIndexChanged(self, index: int) -> None:
        self.sente = ChessColor.BLUE if index == 0 else ChessColor.RED

    @Slot()
    def on_backButton_clicked(self) -> None:
        result = self.board.undo()

        if not result:
            self.showMsg("不能撤销了！")

        self.update()

    def blueTurn(self) -> None:
        if self.mode == Mode.AI_AI or self.mode == Mode.AI_HUMAN:
            self.on_diceButton_clicked()
            self.letAIDo()

        else:
            pass
            # 这里就是说人来走

    def redTurn(self) -> None:
        if self.mode == Mode.HUMAN_AI:
            self.letAIDo()

        else:
            pass

    def paintEvent(self, event: QPaintEvent) -> None:
        self.drawBoardLine()
        self.drawBoardColor()
        self.drawBoardNumber()

    def drawBoardLine(self) -> None:
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

    def drawBoardColor(self) -> None:
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

    def drawBoardNumber(self) -> None:
        # 实现绘制棋盘数字的逻辑
        for i in range(5):
            for j in range(5):
                self.drawChessNumber(i, j)  # 绘制棋子数字

    def drawChessNumber(self, x: float, y: float) -> None:
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        point = event.pos()  # 获取点击位置

        x = int(point.x() // self.gridX)
        y = int(point.y()//self.gridY)

        # 点击棋盘
        if x < 5 and y < 5:
            self.onBoardTap(x, y)
            self.update()

    def onBoardTap(self, x: float, y: float) -> None:
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
        """返回棋子value+1，且让棋子在其范围内滚动
            红棋 在 -1~-6
            蓝棋 在 1~6"""

        sign = chessNumber/abs(chessNumber)
        chessNumber = (abs(chessNumber)+1) % 7

        if chessNumber == 0:
            chessNumber = 1

        return chessNumber*sign

    def moveChess(self, fromPosition: tuple, toPosition: tuple) -> None:
        """移动棋子"""
        success = self.board.moveChess(fromPosition, toPosition)

        self.selectedPosition.setX(-1)
        self.selectedPosition.setY(-1)

        if not success:
            self.showMsg("操作非法！")
            return

        # 如果成功移动棋子
        self.ui.backButton.setEnabled(True)
        self.ui.boardStatusBar.append(self.board.last_move_info())

        win = self.board.checkWin()

        if win:
            # 保存日志
            self.record_game()
            self.timer.stop()
            if win == ChessColor.BLUE:
                self.showMsg("蓝方赢了！")
            else:
                self.showMsg("红方赢了")

        self.update()

    def record_game(self) -> None:
        file_path = "game_record/"
        date = time.strftime("%Y%m%d%H%M", time.localtime())

        # 获取玩家信息
        red_player = self.ui.red_team_name_text.text()
        blue_player = self.ui.blue_team_name_text.text()

        # 如果玩家的信息为空，则警告
        if red_player == "" or blue_player == "":
            self.showMsg("玩家信息不能为空")
            return

        first_player = red_player if self.board.sente == ChessColor.RED else blue_player
        second_player = blue_player if self.board.sente == ChessColor.RED else red_player

        winner = "先手胜" if self.board.checkWin() == self.board.sente else "后手胜"

        file_name = f"WTN-{first_player}vs{second_player}-{winner}{date}.txt"
        with open(file_path+file_name, "w", encoding="gb2312", newline="\r\n") as f:
            # 写入比赛的信息
            f.write(self.get_game_info()+"\n")
            # 写入开局布局
            f.write(self.board.initial_pos_info()+"\n")

            # 写入每一步的走法
            f.write(self.board.get_movements_info()+"\n")

    def get_game_info(self) -> str:
        """游戏开始时的信息，标准棋谱输出"""
        place = "线上"
        date = time.strftime("%Y.%m.%d %H:%M", time.localtime())
        date_place = f"{date} {place}"
        red_player = self.ui.red_team_name_text.text()
        blue_player = self.ui.blue_team_name_text.text()
        match_name = "2023 CCGC"
        first_player = red_player if self.board.sente == ChessColor.RED else blue_player
        second_player = blue_player if self.board.sente == ChessColor.RED else red_player
        first_player_color = "R" if self.board.sente == ChessColor.RED else "B"
        second_player_color = "B" if self.board.sente == ChessColor.RED else "R"

        winner = self.board.checkWin()

        if winner is None:
            pass

        elif self.board.checkWin() == self.board.sente:
            winner = "先手胜"

        else:
            winner = "后手胜"

        return f"#[{first_player} {first_player_color}][{second_player} {second_player_color}][{winner}][{date_place}][{match_name}];"

    def showMsg(self, message: str) -> None:
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()
