# 使用alpha-beta结合蒙特卡洛树搜索的方式进行决策

import copy
from enums.chess import ChessColor
from board import Board
from Agents.alpha_beta_boost.alpha_beta import Alpha_beta_player


class Mix_Alpha_Beta_Player:
    def __init__(self, color=ChessColor.BLUE):
        super().__init__()
        self.color = color
        self.name = "Mix_Alpha_Beta_Tree"
        self.each_move_stimulate_times = 2000

    def set_color(self, color: ChessColor):
        self.color = color

    def get_action(self, board: Board):
        # 进行模拟对战
        # 获取所有可能的走法
        _, moves = board.get_avaiable_moves()

        # 将moves转换成字典，key是move,value 是赢的次数
        move_dict = {}
        for move in moves:
            move_dict[move] = 0

        # 进行模拟对战
        player1 = Alpha_beta_player(self.color, depth=1)
        player2 = Alpha_beta_player(
            ChessColor.RED if self.color == ChessColor.BLUE else ChessColor.BLUE, depth=1)

        for key in moves:
            # 深度拷贝board
            board_ = copy.deepcopy(board)
            board_.do_move(move)
            for i in range(self.each_move_stimulate_times):
                if self.play_out(board_, player1, player2):
                    move_dict[key] += 1

                if i % 100 == 0:
                    print(f'已经模拟{i}次')

        print(move_dict)
        # 选择最大的move
        max_move = moves[0]
        max_win_times = 0
        for move in move_dict:
            if move_dict[move] > max_win_times:
                max_move = move
                max_win_times = move_dict[move]

        return max_move

    def play_out(self, board, player1, player2):
        board = copy.deepcopy(board)
        while board.checkWin() == None:
            board.get_point()
            turn = board.getturn()
            if turn == player1.color:
                board.do_move(player1.get_action(board))

            else:
                board.do_move(player2.get_action(board))

        # 判断是否胜利
        if board.checkWin() == self.color:
            return True
        else:
            return False
