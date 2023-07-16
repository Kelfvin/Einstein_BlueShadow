import random
import numpy as np
from enums.chess import ChessColor


class Board:
    def __init__(self) -> None:
        self.board = self.initBoard()
        self.dice = 1  # 骰子的数
        self.boardBackup = []  # 用于备份棋盘
        self.ourColor = ChessColor.BLUE  # 我方队伍的颜色
        self.nowPlayer = ChessColor.BLUE  # 目前轮到
        self.sente = ChessColor.BLUE   # 先手

    def initBoard(self,):
        '''初始化默认棋盘，每次棋子的布局都是随机的，后期再来进行布局'''

        board = np.array([[-1, -1, -1, 0, 0],
                         [-1, -1,  0, 0, 0],
                         [-1,  0,  0, 0, 1],
                         [0,  0,  0, 1, 1],
                         [0,  0,  1, 1, 1],])

        chesses = [1, 2, 3, 4, 5, 6]
        random.shuffle(chesses)

        # 蓝方棋子
        board[4][2] = chesses[0]
        board[3][3] = chesses[1]
        board[4][3] = chesses[2]
        board[2][4] = chesses[3]
        board[3][4] = chesses[4]
        board[4][4] = chesses[5]

        random.shuffle(chesses)
        # 红方棋子
        board[0][0] = -chesses[0]
        board[0][1] = -chesses[1]
        board[0][2] = -chesses[2]
        board[1][0] = -chesses[3]
        board[1][1] = -chesses[4]
        board[2][0] = -chesses[5]

        return board

    def setChess(self, position, value) -> bool:
        '''放置棋子
        Args:
            position (tuple or list): 表示位置的元组或列表，例如 (row, column) 或 [row, column]
            value: 要放置的棋子的值,between [1,6]
        Returns:
            bool: 表示是否成功放置棋子的布尔值
        '''
        x, y = position
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False

        self.board[x][y] = value
        return True

    def moveChess(self, from_position, end_position):
        '''移动棋子从起始位置到指定的位置
            如果成功移动，返回True，错误返回False'''
        from_x, from_y = from_position
        end_x, end_y = end_position

        # 不能原地踏步
        if from_x == end_x and from_y == end_y:
            return False

        # 移动的棋子
        chess = self.board[from_x][from_y]

        # 不能移动空白
        if chess == 0:
            return False

        # 不能移动别人的棋子
        if self.nowPlayer.value * chess < 0:
            return False

        # 棋子的移动终点是否合法
        if self.nowPlayer.value > 0:  # 蓝方
            # 不能向着右下方行走
            if end_x > from_x or end_y > from_y:
                return False
            # 不能越界
            if end_x < from_x - 1 or end_y < from_y - 1:
                return False
        else:  # 红方
            # 不能向左上方走
            if end_x < from_x or end_y < from_y:
                return False
            # 不能越界
            if end_x > from_x + 1 or end_y > from_y + 1:
                return False

        # 行棋前先备份
        self.backupBoard()

        self.board[end_x][end_y] = self.board[from_x][from_y]
        self.board[from_x][from_y] = 0

        self.swapNowPlayer()

        return True
    
    def swapNowPlayer(self):
        '''交换行棋方'''
        self.nowPlayer = ChessColor.RED if self.nowPlayer == ChessColor.BLUE else ChessColor.BLUE

    def checkBoardSet(self):
        '''开局的时候，检查10个棋子是否正确安放
        一开始就限制了安放棋子只能在指定的位置（在ui上限定），所以这里直接扫描整个棋盘
        '''
        chessSet = set()
        for row in self.board:
            for e in row:
                chessSet.add(e)

        # 如果12个棋子全部摆放完毕
        if len(chessSet) == 13:
            return True
        else:
            return False

    def backupBoard(self):
        '''备份当前棋局到备份列表中'''
        self.boardBackup.append(self.board)

    def undo(self):
        '''悔棋'''
        if len(self.boardBackup) == 0:
            return False

        self.board = self.boardBackup.pop()
        self.swapNowPlayer()
        return True

    def getChess(self, x:int, y:int)->int:
        '''返回棋盘上指定位置的值'''
        return self.board[x][y]

    def checkWin(self):
        '''查看是否已经有一方获胜
            Return: BLUE表示蓝方获胜, RED 表示红方获胜，None表示还没有人获胜'''

        if self.board[0][0] > 0 or np.all(self.board >= 0):
            return ChessColor.BLUE

        if self.board[4][4] < 0 or np.all(self.board <= 0):
            return ChessColor.RED
        
        return None

    def getChessSign(self,x,y):
        '''返回棋子的符号，蓝方返回1，红方返回1,空白返回1'''
        chessNumber = self.board[x][y]
        if chessNumber == 0:
            return 0
        
        if chessNumber >1 :
            return 1
        
        else:
            return -1
        
    def setOurColor(self,color:ChessColor):
        '''设置我方的棋子颜色
            colorCode:1表示蓝方，1表示红方'''
        self.ourColor = color

    def getNowPlayerStr(self):
        return '蓝方' if self.nowPlayer == ChessColor.BLUE else '红方'
    

    def setDice(self,diceNum):
        self.dice = diceNum

    def getDice(self):
        return self.dice

    def setNowPlayer(self,color:ChessColor):
        self.nowPlayer = color

    def setSente(self,color:ChessColor):
        self.sente = color

    def getSente(self)->ChessColor:
        return self.sente