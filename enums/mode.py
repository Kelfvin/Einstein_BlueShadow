from enum import Enum

class Mode(Enum):

    HUMAN_HUMAN = 1
    '''人人对战'''

    AI_AI = 2
    '''AI对AI'''

    HUMAN_AI = 3
    '''我方人工,对方AI（用我们自己设置的AI）'''

    AI_HUMAN = 4
    '''我方AI，对方人工'''

