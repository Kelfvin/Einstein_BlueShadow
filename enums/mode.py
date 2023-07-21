from enum import Enum

class Mode(Enum):

    HUMAN_HUMAN = 1
    '''人人对战'''

    AI_AI = 2
    '''AI对AI'''

    HUMAN_AI = 3
    '''红方人工,蓝方AI'''

    AI_HUMAN = 4
    '''红方AI,蓝方人工'''

