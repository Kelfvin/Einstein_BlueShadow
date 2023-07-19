from enum import Enum

class Strategy(Enum):
    HUMAN = 0

    UCT = 1
    '''使用 UCT 进行搜索'''

    ALPHA_ZERO = 2
    '''使用 alpha-zer算法进行搜索'''

    PURE_MCTS = 3
    '''正宗的蒙特卡洛'''


    
