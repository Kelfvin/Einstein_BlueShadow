import numpy as np
import copy
import pprint
import pickle
import sys
from enums.chess import ChessColor
from logic.Net.pytorch_net import PolicyValueNet
from logic.board import Board


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class TreeNode:
    """
    A node in the MCTS tree.

    Each node keeps track of its own value Q, prior probability P, and
    its visit-count-adjusted prior score u.
    """

    def __init__(self, parent, prior_p):
        self._parent = parent    # root's parent is None
        # {1: {}, 2：{}, 3:{}, 4:{}, 5:{}, 6:{treenode, treenode, treenode, ...}}
        self._children = {}
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self, action_priors, point):
        """
        Expand tree by creating new children.
        action_priors: a list of tuples of actions and their prior probability
        according to the policy function.
        """
        self._children[point] = {}
        for action, prob in action_priors:
            self._children[point][action] = TreeNode(self, prob)

    def select(self, board, c_puct):
        """
        Select action among children that gives maximum action value Q
        plus bonus u(P).
        Return: A tuple of (action, next_node)
        """
        # the game rule has a random cases in the select procedure
        board.get_point()
        # get this point's edge
        batch = self._children.get(board.point, None)
        if not batch:
            return True, None    # this node is the leaf
        return False, max(batch.items(),
                          key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):
        """
        Update node values from leaf evaluation.
        leaf_value: the value of subtree evaluation from the current player's
        perspective.
        """
        # Count visit.
        self._n_visits += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0 * (leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """
        Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            # - leaf_value because the MCTS tree is a max-min tree
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        """
        Calculate and return the value for this node.
        It is a combination of leaf evaluations Q, and this node's prior
        adjusted for its visit count, u.
        c_puct: a number in (0, inf) controlling the relative impact of
            value Q, and prior probability P, on this node's score.
        """
        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_root(self):
        return self._parent is None


class MCTS:
    """
    An implementation of Monte Carlo Tree Search.
    """

    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        """
        policy_value_fn: a function that takes in a board state and outputs
            a list of (action, probability) tuples and also a score in [-1, 1]
            (i.e. the expected value of the end game score from the current
            player's perspective) for the current player.
        c_puct: a number in (0, inf) that controls how quickly exploration
            converges to the maximum-value policy. A higher value means
            relying on the prior more.
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        """
        Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        state is a board instance from the game.py file.
        """
        node = self._root
        # ipdb.set_trace()
        while True:
            is_leaf, action_node = node.select(state, self._c_puct)
            if is_leaf:
                break
            state.do_move(action_node[0])
            node = action_node[1]

        # Evaluate the leaf using a network which outputs a list of
        # (action, probability) tuples p and also a score v in [-1, 1]
        # for the `current player`.

        action_probs, leaf_value = self._policy(state)
        # Check for end of game.
        winner = state.checkWin()
        if not winner:
            node.expand(action_probs, state.point)
        else:
            leaf_value = 1.0 if winner == state.turn else -1.0

        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)

    def get_move_probs(self, state, temp=1e-3):
        """
        Run all playouts sequentially and return the available actions and
        their corresponding probabilities.
        state: the current game state
        temp: temperature parameter in (0, 1] controls the level of exploration

        2018.7.10: try to use multiprocessing to parallel this function
        """
        for _ in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children[state.point].items()]
        acts, visits = zip(*act_visits)
        # different from the paper
        act_probs = softmax(1.0 / temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def cheating_move(self, qq, state, temp=1e-3):
        '''
        This is the cheating function try to add the simulation in oppo's time
        Only add the number of the simulation, do not need to return other paramenters
        '''
        flag = qq.get()
        # print('Begin to auto simulation ...', self._root._n_visits)
        while flag:
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
            qq.put(True)
            flag = qq.get()
        # print('End to auto simlulation ...', self._root._n_visits)

    def update_with_move(self, point, last_move):
        """
        Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if point == -1:
            # reset the tree
            self._root = TreeNode(None, 1.0)
        else:
            if last_move in self._root._children[point]:
                self._root = self._root._children[point][last_move]
                self._root._parent = None
            else:
                self._root = TreeNode(None, 1.0)


class MCTSPlayer:
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=5000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay
        self.name = "alphazero"

    def set_color(self, color):
        self.color = color

    def reset_player(self):
        self.mcts.update_with_move(-1, -1)

    def oppo_go_down_tree(self, point, move):
        if not self.mcts._root._children:
            # begin chess and the mcts is empty, do not exec
            return
        # this function collect the alphazero's oppo move, and renew the mcts
        # print("collect the oppo point and move", point, move)
        self.mcts.update_with_move(point, move)

    def haveto(self, board):
        move_index, moves = board.get_avaiable_moves()
        # one step to win
        for move in moves:
            bx, by, dx, dy = board.move_to_location(move)
            if board.turn == ChessColor.RED:
                if dx == 4 and dy == 4:
                    return move
                if len(board.blue_pieces) == 1 and board.board[dx][dy] > 0:
                    return move
            elif board.turn == ChessColor.BLUE:
                if dx == 0 and dy == 0:
                    return move
                if len(board.red_pieces) == 1 and board.board[dx][dy] < 0:
                    return move

        # one step to lose
        for move in moves:
            bx, by, dx, dy = board.move_to_location(move)
            if board.turn == ChessColor.RED:
                if board.board[dx][dy] > 0:
                    if dx == 1 and dy == 1:
                        return move
                    elif dx == 1 and dy == 0:
                        return move
                    elif dx == 0 and dy == 1:
                        return move
            elif board.turn == ChessColor.BLUE:
                if board.board[dx][dy] < 0:
                    if dx == 3 and dy == 3:
                        return move
                    elif dx == 3 and dy == 4:
                        return move
                    elif dx == 4 and dy == 3:
                        return move
        '''            
        if board.turn == 1:
            # 一步之后对手可以无法被歼灭并且十分靠近我方终点并且走子概率很高
            for move in moves:
                bx, by, dx, dy = board.move_to_location(move)
                if board.map[dx][dy] < 0:
                    for deltax, deltay in [(-1, -1), (-1, 0), (0, -1)]:
                        ddx = dx + deltax if dx + deltax >= 0 else 0
                        ddy = dy + deltay if dy + deltay >= 0 else 0
                        # 查询 ddx, ddy 该点是否为蓝棋的不可歼灭点
                        flag = True
                        for i in range(ddx + 1):
                            for j in range(ddy + 1):
                                if i == bx and j == by: continue
                                if board.map[i][j] > 0:
                                    flag = False
                                    break
                            if not flag: break
                        if flag:
                            # ddx, ddy 不可歼灭
                            print("Hidden have to move has been activated !")
                            return move
        elif board.turn == 2:
            # 一步之后我方可以无法被歼灭并且十分的靠近敌方终点并且走子概率很高
            for move in moves:
                bx, by, dx, dy = board.move_to_location(move)
                if board.map[dx][dy] > 0:
                    for deltax, deltay in [(1, 1), (1, 0), (0, 1)]:
                        ddx = dx + deltax if dx + deltax <= 4 else 4
                        ddy = dy + deltay if dy + deltay <= 4 else 4
                        flag = True
                        for i in range(ddx, 5):
                            for j in range(ddy, 5):
                                if i == bx and j == by: continue
                                if board.map[i][j] < 0:
                                    flag = False
                                    break
                            if not flag: break
                        if flag:
                            print("Hidden have to move has been activated !")
                            return move
        '''

        return None

    def get_action(self, board, temp=1e-3, return_prob=0):
        # get the point for the turns
        while True:
            try:
                point = int(input("Input point (1~6): "))
                if point <= 0 or point > 6:
                    raise Exception()
                break
            except KeyboardInterrupt:
                exit(1)
            except:
                print('Please input the right point to move !')

        board.get_point(point)
        print(board.point)
        # ipdb.set_trace()

        # have to
        move = self.haveto(board)
        if move:
            print('Have to function has been activated !')
            if return_prob:
                return move, 1
            else:
                return move

        acts, probs = self.mcts.get_move_probs(
            board, temp)    # 获得确定的点数下的走法及其对应的概率

        # create the size 56 mcts_probs
        move_probs = np.zeros(56)
        for id, act in enumerate(acts):
            if board.turn == ChessColor.RED:
                move_probs[board.red_legal_moves.index(act)] = probs[id]
            else:
                move_probs[board.blue_legal_moves.index(act)] = probs[id]

        if self._is_selfplay:
            # add Dirichlet Noise for exploration (needed for
            # self-play training)
            move = np.random.choice(
                acts,
                p=0.75 * probs + 0.25 *
                np.random.dirichlet(0.3 * np.ones(len(probs)))
            )
            # update the root node and reuse the search tree
            self.mcts.update_with_move(board.dice, move)
        else:
            # with the default temp=1e-3, it is almost equivalent
            # to choosing the move with the highest prob

            # 选择最大概率的走子方案
            move = np.random.choice(acts, p=probs)
            # move = acts[np.argmax(probs)]

            # reset the root node
            # self.mcts.update_with_move(-1, -1)

            # do not reset the tree, otherwise try to save the tree for the mctsplayer
            # this is not enough, also need to move from the human side
            self.mcts.update_with_move(board.dice, move)

        if return_prob:
            return move, move_probs
        else:
            return move
