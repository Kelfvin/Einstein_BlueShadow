from enum import Enum

class ChessColor(Enum):
    '''RED红方，BLUE蓝方'''
    RED = -1
    BLUE = 1
    

if __name__ == '__main__':
    print(type(ChessColor.BLUE.value))
    a = ChessColor.BLUE
    print(a.value*2>1)