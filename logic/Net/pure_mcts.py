import numpy as np
import copy
from operator import itemgetter


def rollout_policy_fn(board):
    """a coarse, fast version of policy_fn used in the rollout phase."""
    # rollout randomly
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
        batch = self._children.get(board.dice, None)    # get this point's edge
        if not batch: return True, None    # this node is the leaf
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
            self._parent.update_recursive(-leaf_value)    # - leaf_value because the MCTS tree is a max-min tree
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
        while(1):
            is_leaf, action_node = node.select(state, self._c_puct)
            if is_leaf: break
            state.do_move(action_node[0])
            node = action_node[1]

        # value is useless here
        action_probs, _ = self._policy(state)
        # Check for end of game
        winner = state.checkWin()
        if winner == None:
            node.expand(action_probs, state.dice)
        # Evaluate the leaf node by random rollout
        leaf_value = self._evaluate_rollout(state)
        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)

    def _evaluate_rollout(self, state, limit=1000):
        """
        Use the rollout policy to play until the end of the game,
        returning +1 if the current player wins, -1 if the opponent wins,
        and 0 if it is a tie.
        """
        player = state.turn
        for i in range(limit):
            winner = state.checkWin()
            if winner: break
            action_probs = rollout_policy_fn(state)
            max_action = max(action_probs, key=itemgetter(1))[0]
            state.do_move(max_action)
        else:
            # If no break from the loop, issue a warning.
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
    def __init__(self, c_puct=5, n_playout=30000):
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
    


