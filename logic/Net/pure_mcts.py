import numpy as np
import copy
from operator import itemgetter


def rollout_policy_fn(board):
    """
    一个粗糙的，快速的策略函数，用于模拟阶段。
    """
    # 从当前棋盘状态中获取可用的动作
    moves, true_moves = board.get_avaiable_moves()
    action_probs = np.random.rand(len(moves))
    return zip(true_moves, action_probs)


def policy_value_fn(board):
    """a function that takes in a state and outputs a list of (action, probability)
    tuples and a score for the state"""
    # return uniform probabilities and 0 score for pure MCTS
    moves, true_moves = board.get_avaiable_moves()
    action_probs = np.ones(len(moves)) / len(moves)
    return zip(true_moves, action_probs), 0


class TreeNode:
    """
    A node in the MCTS tree.

    蒙特卡诺树中的一个节点。
    每个节点都跟踪其自身的值Q，先前的概率P以及其访问计数调整的先前分数u。
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
        batch = self._children.get(board.dice, None)    # get this point's edge
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
        # Update Q, a running average of values for all visits.   wtf ??? this line is rigth but kind of wired !
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
        计算并返回此节点的价值
        它是叶子评估Q和此节点的先前访问计数u的组合。
        c_puct：控制相对影响的数字
        值Q和先前概率P，对此节点的分数。
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
        policy_value_fn: 一个函数，接受一个棋盘状态作为输入，并输出一个由动作和概率组成的列表，还有一个在[-1, 1]范围内的分数（即从当前玩家的角度看，游戏结束时的预期价值）。

        c_puct: 一个在(0, 无穷大)范围内的数值，用于控制探索如何快速收敛到最大价值策略。较高的值意味着更依赖先前的策略。
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        """
        进行一次从根节点到叶节点的单次模拟，得到叶节点的值，并将其传播回其父节点。
        状态是就地修改的，因此必须提供副本。
        """
        node = self._root
        while (1):
            is_leaf, action_node = node.select(state, self._c_puct)
            if is_leaf:
                break
            state.do_move(action_node[0])
            node = action_node[1]

        # 价值是无用的
        action_probs, _ = self._policy(state)
        # 检查游戏是否结束
        winner = state.checkWin()
        if winner == None:
            node.expand(action_probs, state.dice)
        # 评估叶节点用随机模拟
        leaf_value = self._evaluate_rollout(state)
        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)

    def _evaluate_rollout(self, state, limit=1000):
        """
        使用随机策略玩游戏，直到游戏结束，返回+1如果当前玩家赢了，-1如果对手赢了，0如果是平局。
        当然不可能出现平局
        """
        player = state.turn
        for i in range(limit):
            winner = state.checkWin()
            if winner:
                break
            action_probs = rollout_policy_fn(state)
            max_action = max(action_probs, key=itemgetter(1))[0]
            state.do_move(max_action)
        else:
            # 如果没有 break。发出警告。
            print("WARNING: rollout reached move limit")
            return -1
        return 1 if winner == player else -1

    def get_move(self, state):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state

        Return: the selected action

        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        return max(self._root._children[state.dice].items(),
                   key=lambda act_node: act_node[1]._n_visits)[0]

    def cheating_move(self, qq, state, temp=1e-3):
        flag = qq.get()
        while flag:
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
            qq.put(True)
            flag = qq.get()

    def update_with_move(self, point, last_move):
        """
        Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if point == -1:
            # reset the tree
            self._root = TreeNode(None, 1.0)
        else:
            self._root = self._root._children[point][last_move]
            self._root._parent = None


class MCTSPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, c_puct=1.38, n_playout=50000):
        self.mcts = MCTS(policy_value_fn, c_puct, n_playout)
        self.name = "puremcts"

    def set_color(self, color):
        self.color = color

    def reset_player(self):
        self.mcts.update_with_move(-1, -1)

    def get_action(self, board):
        move = self.mcts.get_move(board)
        self.mcts.update_with_move(-1, -1)
        return move
