import random

import numpy as np
from logic.board import Board
from enums.chess import ChessColor
import time
from collections import deque
import queue,threading

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

    def start_play(self, player1, player2, player1_color:ChessColor, player2_color:ChessColor, start_player, is_show = 1):
        '''
        # default show for human
        # this function for the human-alphazero and alphazero-puremcts
        # for alphazerp, but both of them need to save the tree when they chess with each other
        '''
        if start_player not in ChessColor:
            raise Exception('First player must be RED or BLUE !')
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
        '''return: winner, zip(states, mcts_probs, winner_z)'''
        # play with itself (AIPlayer), default not show
        first_player = random.choice(list(ChessColor))  # random get the first player
        self.board.initBoard(first_player)    
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board, temp = temp, return_prob = 1)
            # store the data
            states.append(self.board.get_current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.turn)

            self.board.do_move(move)
            if is_show: self.show()
            winner = self.board.checkWin()
            if winner:
                # game end, collect the data for training
                # 跟走的步数对应上
                winner_z = np.zeros(len(current_players))
                # 赢的奖励，输的扣分
                winner_z[np.array(current_players) == winner] = 1.0
                winner_z[np.array(current_players) != winner] = -1.0
                player.reset_player()    # reset the MCTS Tree
                if is_show: print('red win' if winner == ChessColor.RED else 'blue win')
                return winner, zip(states, mcts_probs, winner_z)
