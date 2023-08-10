import copy
import random

import numpy as np

from enums.chess import ChessColor


class Board:
    def __init__(self, start_player: ChessColor = ChessColor.BLUE, dice: int = 1) -> None:
        """默认起手为蓝方"""
        self.initBoard()
        self.dice = dice  # 骰子的数
        self.boardBackup = []  # 用于备份棋盘
        self.turn = start_player  # 目前轮到
        self.sente = start_player   # 先手

        self.movements = []  # 保存行棋的历史
        self.points = []  # 保存点数的历史
        self.blue_initial_pos = []
        self.red_initial_pos = []

        self.red_pieces = [-1, -2, -3, -4, -5, -6]
        self.blue_pieces = [1, 2, 3, 4, 5, 6]

        # 红蓝双方的可以走的合法位置
        self.red_legal_moves = [11, 10, 1, 112, 111, 102, 213, 212, 203, 314, 313, 304, 414,
                                1021, 1020, 1011, 1122, 1121, 1112, 1223, 1222, 1213, 1324, 1323,
                                1314, 1424, 2031, 2030, 2021, 2132, 2131, 2122, 2233, 2232, 2223,
                                2334, 2333, 2324, 2434, 3041, 3040, 3031, 3142, 3141, 3132, 3243,
                                3242, 3233, 3344, 3343, 3334, 3444, 4041, 4142, 4243, 4344]
        self.blue_legal_moves = [100, 201, 302, 403, 1000, 1100, 1101, 1110, 1201, 1202, 1211,
                                 1302, 1303, 1312, 1403, 1404, 1413, 2010, 2110, 2111, 2120, 2211,
                                 2212, 2221, 2312, 2313, 2322, 2413, 2414, 2423, 3020, 3120, 3121,
                                 3130, 3221, 3222, 3231, 3322, 3323, 3332, 3423, 3424, 3433, 4030,
                                 4130, 4131, 4140, 4231, 4232, 4241, 4332, 4333, 4342, 4433, 4434, 4443]

        # 红蓝双方棋子初始放置的合法位置
        self.red_legal_place_pos = [
            (0, 0), (1, 0), (2, 0),
            (0, 1), (1, 1),
            (0, 2)
        ]

        self.blue_legal_place_pos = [
            (4, 2),
            (3, 3), (4, 3),
            (2, 4), (3, 4), (4, 4)
        ]

        self.num_char_map = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }

    def place_blue_pos(self, pieces_list: list) -> None:
        """放置蓝方棋子
        piece_list:棋子序列:list
        """
        if len(pieces_list) == 6:
            for pos, piece in zip(self.blue_legal_place_pos, pieces_list, strict=True):
                self.setChess(pos, piece)
                self.blue_pieces = pieces_list

    def place_red_pos(self, pieces_list: list) -> None:
        """放置红方棋子
        piece_list:棋子序列:list
        """
        if len(pieces_list) == 6:
            for pos, piece in zip(self.red_legal_place_pos, pieces_list, strict=True):
                self.setChess(pos, -piece)
                self.red_pieces = [-i for i in pieces_list]

    def red_best_place(self) -> None:
        """红方最佳放置棋子"""
        best_pieces_list = [1, 6, 3, 2, 4, 5]
        self.place_red_pos(best_pieces_list)

    def blue_best_place(self) -> None:
        """蓝方最佳放置棋子"""
        best_pieces_list = [5, 4, 2, 3, 6, 1]
        self.place_blue_pos(best_pieces_list)

    def update_pieces(self) -> None:
        """更新双方的棋子
        主要是用在撤销的时候，为了能够重新扫描棋盘，还原棋子
        所以在使用之前，要先确保棋盘是正确的"""
        self.red_pieces = []
        self.blue_pieces = []

        for i in range(5):
            for j in range(5):
                if self.board[i][j] > 0:
                    self.blue_pieces.append(self.board[i][j])
                elif self.board[i][j] < 0:
                    self.red_pieces.append(self.board[i][j])

    def showBoard(self) -> None:
        """打印棋盘"""

        # 打印棋盘，将numpy数组格式化输出，行变成列
        print(np.array(self.board).T)

    def save_initial_pos(self) -> None:
        """保存开局的布局信息，用于后面输出日志"""
        blue_initial_pos = []
        red_initial_pos = []

        for x in range(5):
            for y in range(5):
                if self.board.T[x][y] > 0:
                    blue_initial_pos.append((x, y, self.board.T[x][y]))
                elif self.board.T[x][y] < 0:
                    red_initial_pos.append((x, y, self.board.T[x][y]))

        self.blue_initial_pos = blue_initial_pos
        self.red_initial_pos = red_initial_pos

    def get_avaiable_pieces(self) -> list | None:
        """根据骰子的值，返回目前可以移动的棋子"""
        if self.turn == ChessColor.BLUE:
            # 有这个棋子就直接加入
            if self.dice in self.blue_pieces:
                return [self.dice]

            collections = []
            # 没有这个棋子就加入离骰子数最近的两个棋子

            for chess in range(self.dice - 1, 0, -1):
                if chess in self.blue_pieces:
                    collections.append(chess)
                    break
            for chess in range(self.dice + 1, 7):
                if chess in self.blue_pieces:
                    collections.append(chess)
                    break
            return collections

        if self.turn == ChessColor.RED:
            if -self.dice in self.red_pieces:
                return [-self.dice]

            collections = []
            for chess in range(-self.dice + 1, 0):
                if chess in self.red_pieces:
                    collections.append(chess)
                    break
            for chess in range(-self.dice - 1, -7, -1):
                if chess in self.red_pieces:
                    collections.append(chess)
                    break
            return collections
        return None

    def get_avaiable_moves(self) -> (list, list):
        """根据投的骰子，得出可以进行的操作
        moves:可进行的操作的id，也就是在list中的下标
        true_moves:实际上的action"""
        pieces = self.get_avaiable_pieces()
        moves = []
        true_moves = []
        if self.turn == ChessColor.RED:
            # red dice moves
            for piece in pieces:
                # get the position of the piece
                x, y = -1, -1
                getted = False
                for i in range(5):
                    for j in range(5):
                        if self.board[i][j] == piece:
                            x, y = i, j
                            getted = True
                            break
                    if getted:
                        break
                for dx, dy in [(1, 1), (1, 0), (0, 1)]:
                    move = self.location_to_move((x, y, x + dx, y + dy))
                    if move in self.red_legal_moves:
                        moves.append(self.red_legal_moves.index(move))
                        true_moves.append(move)
                    else:
                        continue
        else:
            # blue dice moves
            for piece in pieces:
                # get the position of the piece
                x, y = -1, -1
                getted = False
                for i in range(5):
                    for j in range(5):
                        if self.board[i][j] == piece:
                            x, y = i, j
                            getted = True
                            break
                    if getted:
                        break
                for dx, dy in [(-1, -1), (-1, 0), (0, -1)]:
                    move = self.location_to_move((x, y, x + dx, y + dy))
                    if move in self.blue_legal_moves:
                        moves.append(self.blue_legal_moves.index(move))
                        true_moves.append(move)
                    else:
                        continue
        return moves, true_moves

    def move_to_location(self, move: int) -> (int, int, int, int):
        """操作映射到位置"""
        beginx = move // 1000
        beginy = (move - beginx * 1000) // 100
        destx = (move - beginx * 1000 - beginy * 100) // 10
        desty = (move - beginx * 1000 - beginy * 100 - destx * 10)
        return beginx, beginy, destx, desty

    def location_to_move(self, location: tuple) -> int:
        """将操作映射为成数字"""
        bx, by, dx, dy = location
        return bx * 1000 + by * 100 + dx * 10 + dy

    def do_move(self, move: int) -> None:
        """给定move(int)，认为传入的动作是正确的，不进行验证"""
        # 进行备份
        self.movements.append(move)
        self.backupBoard()
        self.points.append(self.dice)
        self.swapturn()
        bx, by, dx, dy = self.move_to_location(move)
        if self.board[dx][dy] < 0:
            self.red_pieces.remove(self.board[dx][dy])
        elif self.board[dx][dy] > 0:
            self.blue_pieces.remove(self.board[dx][dy])
        self.board[dx][dy] = self.board[bx][by]
        self.board[bx][by] = 0

    def get_current_state(self) -> np.array:
        """用于神经网络网络的输入
        返回 4*5*5 的矩阵，每一层的信息：
        0:棋局
        1:对手上一次的移动
        2:目前可以移动的棋子信息
        3:current turn,1 blue, -1 red
        注意：调用前先获取骰子数目"""
        state = np.zeros((4, 5, 5))
        state[0] = self.board

        # last move
        if len(self.movements) != 0:
            # if movements is empty, do not exec
            lx, ly, ldx, ldy = self.move_to_location(self.movements[-1])
            state[1][ldx, ldy], state[1][lx, ly] = 1, 1

        # move pieces
        pieces = self.get_avaiable_pieces()
        for piece in pieces:
            for i in range(5):
                for j in range(5):
                    if piece == self.board[i][j]:
                        state[2][i, j] = 1

        if self.turn == ChessColor.RED:
            state[3][:, :] = -1
        elif self.turn == ChessColor.BLUE:
            state[3][:, :] = 1

        return state

    def initBoard(self, start_player: ChessColor = ChessColor.BLUE) -> np.array:
        """初始化默认棋盘，每次棋子的布局都是随机的，后期再来进行布局"""

        self.start_player = start_player

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

        self.board = board

        self.update_pieces()

        return board

    def setChess(self, position: tuple, value: int) -> bool:
        """放置棋子
        Args:
            position (tuple or list): 表示位置的元组或列表，例如 (row, column) 或 [row, column]
            value: 要放置的棋子的值,between [-6,6]
        Returns:
            bool: 表示是否成功放置棋子的布尔值
        """
        x, y = position
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False

        self.board[x][y] = value
        return True

    def moveChess(self, from_position: tuple, end_position: tuple) -> bool:
        """移动棋子从起始位置到指定的位置,通过坐标移动，主要是给前端使用的
            如果成功移动，返回True，错误返回False
            只要是移动，最后都是经过do_move的"""
        from_x, from_y = from_position
        end_x, end_y = end_position

        move = self.location_to_move((from_x, from_y, end_x, end_y))

        if move not in self.get_avaiable_moves()[1]:
            return False

        self.do_move(move)

        return True

    def swapturn(self) -> None:
        """交换行棋方"""
        self.turn = ChessColor.RED if self.turn == ChessColor.BLUE else ChessColor.BLUE

    def checkBoardSet(self) -> bool:
        """开局的时候，检查10个棋子是否正确安放
        一开始就限制了安放棋子只能在指定的位置（在ui上限定），所以这里直接扫描整个棋盘
        """
        chessSet = set()
        for row in self.board:
            for e in row:
                chessSet.add(e)

        # 如果12个棋子全部摆放完毕
        return len(chessSet) == 13

    def backupBoard(self) -> None:
        """备份当前棋局到备份列表中"""
        # 这里需要使用深拷贝，否则会出现引用问题
        self.boardBackup.append(copy.deepcopy(self.board))

    def undo(self) -> bool:
        """悔棋"""
        if len(self.boardBackup) == 0:
            return False

        # 取出上一次备份的棋盘
        self.board = self.boardBackup.pop()
        self.points.pop()
        self.movements.pop()
        self.update_pieces()

        self.swapturn()
        return True

    def getChess(self, x: int, y: int) -> int:
        """返回棋盘上指定位置的值"""
        return self.board[x][y]

    def checkWin(self) -> ChessColor | None:
        """查看是否已经有一方获胜
            Return: BLUE表示蓝方获胜, RED 表示红方获胜，None表示还没有人获胜"""

        if self.board[0][0] > 0 or np.all(self.board >= 0):
            return ChessColor.BLUE

        if self.board[4][4] < 0 or np.all(self.board <= 0):
            return ChessColor.RED

        return None

    def getChessSign(self, x: int, y: int) -> int:
        """返回棋子的符号，蓝方返回1，红方返回1,空白返回1"""
        chessNumber = self.board[x][y]
        if chessNumber == 0:
            return 0

        if chessNumber > 1:
            return 1

        return -1

    def getturn(self) -> ChessColor:
        return self.turn

    def getturnStr(self) -> str:
        return "蓝方" if self.turn == ChessColor.BLUE else "红方"

    def setDice(self, diceNum: int) -> None:
        self.dice = diceNum

    def getDice(self) -> int:
        return self.dice

    def setturn(self, color: ChessColor) -> None:
        self.turn = color

    def setSente(self, color: ChessColor) -> None:
        self.sente = color

    def getSente(self) -> ChessColor:
        return self.sente

    def get_point(self, point: int = None) -> int:
        """获取点数，如果没有指定点数，则随机生成点数"""
        if point:
            self.dice = point
        else:
            self.dice = random.randint(1, 6)
            # print("Point is", self.point)

        return self.dice

    def last_move_info(self) -> str:
        """返回上一次移动的信息,返回的是标准棋谱的信息"""
        # 写入每一步的走法

        num_char_map = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }
        i = len(self.movements) - 1
        x, y, dx, dy = self.move_to_location(self.movements[i])
        # 这里 x 和 y 还是用的最原始的，可以索引到棋子
        chess_index = self.boardBackup[i][x][y]
        sign = "R" if chess_index < 0 else "B"
        chess_index = abs(chess_index)
        dy = abs(5-dy)
        dx = num_char_map[dx]

        for i, (move, point) in enumerate(zip(self.movements, self.points, strict=True)):
            x, y, dx, dy = self.move_to_location(move)
            # 这里 x 和 y 还是用的最原始的，可以索引到棋子
            print((self.boardBackup[i].T))
            chess_index = self.boardBackup[i][x][y]
            sign = "R" if chess_index < 0 else "B"
            chess_index = abs(chess_index)
            dy = abs(5-dy)
            dx = num_char_map[dx]

        return f"{i+1}:{point};({sign}{chess_index},{dx}{dy})"

    def initial_pos_info(self) -> str:
        """返回初始位置信息，返回标准棋谱的字符串"""
        info = ""
        info += "R:"
        for x, y, index in self.red_initial_pos:
            y = abs(5-y)
            x = self.num_char_map[x]
            chess_index = abs(index)
            info += f"{x}{y}-{chess_index};"

        info += "\n"
        # 写入蓝方
        info += "B:"
        for x, y, index in self.blue_initial_pos:
            y = abs(5-y)
            x = self.num_char_map[x]
            chess_index = abs(index)
            info += f"{x}{y}-{chess_index};"

        return info

    def get_movements_info(self) -> str:
        """返回所有的行棋记录信息"""
        info = ""
        for i, (move, point) in enumerate(zip(self.movements, self.points, strict=True)):
            x, y, dx, dy = self.move_to_location(move)
            # 这里 x 和 y 还是用的最原始的，可以索引到棋子
            chess_index = self.boardBackup[i][x][y]
            sign = "R" if chess_index < 0 else "B"
            chess_index = abs(chess_index)
            dy = abs(5-dy)
            dx = self.num_char_map[dx]
            info += f"{i+1}:{point};({sign}{chess_index},{dx}{dy})\n"

        return info


if __name__ == "__main__":
    board = Board()
    board.red_pieces = [1, 2, 4]
    board.dice = 3
    print(board.get_avaiable_pieces())
