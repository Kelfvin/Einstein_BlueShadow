from enum import Enum

class Strategy(Enum):
    UCT = 1
    '''使用 UCT 进行搜索'''

    ALPHA_ZERO = 2
    '''使用 alpha-zer算法进行搜索'''
    