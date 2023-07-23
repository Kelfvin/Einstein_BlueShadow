#!/usr/bin/python
# Author: GMFTBY
# Time  : 2018.7.3

import numpy as np
from collections import deque
import random, time, queue, threading

class Board:
    def __init__(self):
        # red - 1, blue - 2
        self.width = self.height = 5
        self.point = -1
        self.movements = []    # save the procedure of the game
        self.points = []
        self.first = -1        # first player in the game (red - 1, blue - 2)
        self.turn  = -1        # the current player
        self.map   = [[0, 0, 0, 0, 0] for _ in range(5)]
        self.red_pieces = [1, 2, 3, 4, 5, 6]
        self.blue_pieces = [1, 2, 3, 4, 5, 6]
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

    def get_avaiable_moves(self):
        # Use after get the point
        pieces = self.get_avaiable_pieces()
        moves = []
        true_moves = []
        if self.turn == 1:
            # red point moves
            for piece in pieces:
                # get the position of the piece
                x, y = -1, -1
                getted = False
                for i in range(5):
                    for j in range(5):
                        if self.map[i][j] == piece:
                            x, y = i, j
                            getted = True
                            break
                    if getted: break
                for dx, dy in [(1, 1), (1, 0), (0, 1)]:
                    move = self.location_to_move((x, y, x + dx, y + dy))
                    if move in self.red_legal_moves: 
                        moves.append(self.red_legal_moves.index(move))
                        true_moves.append(move)
                    else: continue
        else:
            # blue point moves
            for piece in pieces:
                # get the position of the piece
                x, y = -1, -1
                getted = False
                for i in range(5):
                    for j in range(5):
                        if self.map[i][j] == -piece:
                            x, y = i, j
                            getted = True
                            break
                    if getted: break
                for dx, dy in [(-1, -1), (-1, 0), (0, -1)]:
                    move = self.location_to_move((x, y, x + dx, y + dy))
                    if move in self.blue_legal_moves: 
                        moves.append(self.blue_legal_moves.index(move))
                        true_moves.append(move)
                    else: continue
        return moves, true_moves

    def init_board(self, start_player = 1, red_pieces = None, blue_pieces = None):
        # default red first
        # default red_pieces: [(0, 0, 3), (0, 1, 5), (0, 2, 6), (1, 0, 1), (1, 1, 4), (2, 0, 2)]
        # default bluepieces: [(4, 4, 3), (3, 4, 5), (2, 4, 6), (4, 3, 1), (3, 3, 4), (4, 2, 2)]
        self.turn = self.first = start_player
        self.points, self.movements = [], []
        self.map = [[0, 0, 0, 0, 0] for _ in range(5)]
        self.red_pieces = [1, 2, 3, 4, 5, 6]
        self.blue_pieces = [1, 2, 3, 4, 5, 6]
        if not red_pieces:
            # red_pieces = [(0, 0, 3), (0, 1, 5), (0, 2, 6), (1, 0, 1), (1, 1, 4), (2, 0, 2)]
            red_pieces = [(0, 0, 1), (0, 1, 6), (0, 2, 2), (1, 0, 5), (1, 1, 3), (2, 0, 4)]
        if not blue_pieces:
            blue_pieces = [(4, 4, 3), (3, 4, 5), (2, 4, 6), (4, 3, 1), (3, 3, 4), (4, 2, 2)]

        # add the TUI to fix the position of the chess point
        red_pieces, blue_pieces = [], []
        print('Input Red Chess Position (follow the order of the number): ')
        for i in range(1, 7):
            position = input('Position ' + str(i) + ': ')
            xxx, yyy = map(int, position.split(','))
            red_pieces.append((xxx, yyy, i))

        print('Input Blue Chess Position (follow the order of the number): ')
        for i in range(1, 7):
            position = input('Position ' + str(i) + ': ')
            xxx, yyy = map(int, position.split(','))
            blue_pieces.append((xxx, yyy, i))

        print('-' * 50)

        # for log
        self.mine_pos, self.oppo_pos = red_pieces, blue_pieces

        for x, y, index in red_pieces:
            self.map[x][y] = index
        for x, y, index in blue_pieces:
            self.map[x][y] = - index    # blue pieces' index is negative, different from the red pieces

    def get_point(self, point = None):
        # get the point function get called in get_action or MCTS search function
        if point: 
            self.point = point
        else: 
            self.point = random.randint(1, 6)
            # print("Point is", self.point)
        self.points.append(self.point)

    def move_to_location(self, move):
        # move is a integar, refer to the self.red_legal_moves
        beginx = move // 1000
        beginy = (move - beginx * 1000) // 100
        destx  = (move - beginx * 1000 - beginy * 100) // 10
        desty =  (move - beginx * 1000 - beginy * 100 - destx * 10) 
        return beginx, beginy, destx, desty

    def location_to_move(self, location):
        bx, by, dx, dy = location
        return bx * 1000 + by * 100 + dx * 10 + dy
  
    def get_avaiable_pieces(self):
        if self.turn == 1:
            if self.point in self.red_pieces: return [self.point]
            else:
                collections = []
                for point in range(self.point - 1, 0, -1):
                    if point in self.red_pieces:
                        collections.append(point)
                        break
                for point in range(self.point + 1, 7):
                    if point in self.red_pieces:
                        collections.append(point)
                        break
                return collections
        elif self.turn == 2:
            if self.point in self.blue_pieces: return [self.point]
            else:
                collections = []
                for point in range(self.point - 1, 0, -1):
                    if point in self.blue_pieces:
                        collections.append(point)
                        break
                for point in range(self.point + 1, 7):
                    if point in self.blue_pieces:
                        collections.append(point)
                        break
                return collections

    def get_current_state(self):
        # before call this function, need to get the self.point
        # 4 * 5 * 5: current board, last move, 
        #   move pieces (container the information about the current player)
        #   current player: 1 red, 2 blue
        state = np.zeros((4, self.width, self.height))
        state[0] = self.map
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
                    if piece == self.map[i][j]:
                        state[2][i, j] = 1
                        
        if self.turn == 1: state[3][:, :] = 1.0
        elif self.turn == 2: state[3][:, :] = 2.0
        
        return state

    def do_move(self, move):
        self.movements.append(move)
        self.turn = 2 if self.turn == 1 else 1
        # change the map and may change pieces in the borad
        bx, by, dx, dy = self.move_to_location(move)
        if self.map[dx][dy] > 0: self.red_pieces.remove(self.map[dx][dy])
        elif self.map[dx][dy] < 0: self.blue_pieces.remove(-self.map[dx][dy])
        self.map[dx][dy] = self.map[bx][by]
        self.map[bx][by] = 0

    def if_win(self):
        if len(self.red_pieces) == 0: return True, 2    # blue win
        elif len(self.blue_pieces) == 0: return True, 1 # red  win
        if self.map[4][4] > 0: return True, 1           # red  win 
        elif self.map[0][0] < 0: return True, 2         # blue win
        return False, None




class Game:
    def __init__(self):
        self.board = Board()
        self.q = queue.Queue()
    
    def show(self):
        # terminal
        print('     0  1  2  3  4  Y')
        for i in range(5):
            print(' ', i, end='')
            for j in range(5):
                print('{0:3}'.format(self.board.map[i][j]), end='')
            print()
        print('  X')

    def start_play(self, player1, player2, player1_color, player2_color, start_player, is_show = 1):
        # default show for human
        # this function for the human-alphazero and alphazero-puremcts
        # for alphazerp, but both of them need to save the tree when they chess with each other
        if start_player not in [1, 2]:
            raise Exception('First player must be 1(red) or 2(blue) !')
        self.board.init_board(start_player)
        player1.set_color(player1_color)
        player2.set_color(player2_color)
        players = {player1_color: player1, player2_color: player2}
        if is_show == 1: 
            self.show()
        while True:
            # if self.board.turn == 1: print('-------------------\nRed player play ...')
            # else: print('-------------------\nBlue player play ...')
            player_in_turn = players[self.board.turn]
            
            # IF NOT THE ALPHAZERO, MULTITHREADING TO SIMULATION
            if player_in_turn.name == "human":
                # the human or the pure mcts play turn
                alphaplayer = players[2 if player_in_turn.color == 1 else 1]
                self.q.put(True)
                self.cheating = threading.Thread(target = alphaplayer.mcts.cheating_move, \
                        args = (self.q, self.board,))
                self.cheating.start()
                # print('Start simulation ... ')
            else:
                # add the False flag into the threading queue
                # to stop the auto simulations
                self.q.put(False)
                try:
                    self.cheating.join()
                    # print('End simulation ... ')
                except:
                    pass

            # get_action must call the get_point function
            move = player_in_turn.get_action(self.board)    # the move is the integar

            # alphazero collect oppo's movement
            if player_in_turn.name == "human":
                # the human or the pure mcts play turn
                alphazero_player = players[1] if player_in_turn.color == 2 else players[2]
                if alphazero_player.name != 'alphazero': 
                    # both of the player are not alphazero
                    pass
                else: alphazero_player.oppo_go_down_tree(self.board.point, move)

            self.board.do_move(move)

            if is_show: 
                self.show()
            end, winner = self.board.if_win()
            if end:
                self.write_log(players[start_player].name, players[1 if start_player == 2 else 2].name,\
                        players[winner].name)
                if is_show: print('red win' if winner == 1 else 'blue win')
                self.q.put(False)
                self.cheating.join()
                return winner
        
    def write_log(self, first_name, second_name, winner):
        # this function when the start_play end and write the log according to the new rule of the game
        filename = './chess_log/WTN-' + first_name + '-' + second_name + '-' + winner + '-' + '-'.join(time.asctime().split()) + '-' + '2018CCGC'
        with open(filename, 'w') as f:
            f.write('#[][place][][date][];\n')
            f.write('R:')
            for x, y, index in self.board.mine_pos:
                x, y = 5 - x, chr(65 + y)
                f.write(y + str(x) + '-' + str(index) + ';')
            f.write('\n')
            f.write('B:')
            for x, y, index in self.board.oppo_pos:
                x, y = 5 - x, chr(65 + y)
                f.write(y + str(x) + '-' + str(index) + ';')
            f.write('\n')
            i = 1
            for move, point in zip(self.board.movements, self.board.points):
                x, y, dx, dy = self.board.move_to_location(move)
                x, y, dx, dy = 5 - x, chr(65 + y), 5 - dx, chr(65 + dy)
                f.write(str(i) + ':' + str(point) + ';(' + y + str(x) + ',' + dy + str(dx) + ')\n')
                i += 1

    def start_self_play(self, player, is_show = 0, temp = 1e-3):
        # play with itself (AIPlayer), default not show
        self.board.init_board(random.randint(1, 2))    # random get the first player
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board, temp = temp, return_prob = 1)
            # store the data
            states.append(self.board.get_current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.turn)

            self.board.do_move(move)
            if is_show: self.show()
            end, winner = self.board.if_win()
            if end:
                # game end, collect the data for training
                winner_z = np.zeros(len(current_players))
                winner_z[np.array(current_players) == winner] = 1.0
                winner_z[np.array(current_players) != winner] = -1.0
                player.reset_player()    # reset the MCTS Tree
                if is_show: print('red win' if winner == 1 else 'blue win')
                return winner, zip(states, mcts_probs, winner_z)
