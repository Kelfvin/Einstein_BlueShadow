import time
import numpy as np

now_time = None
begin_time = None
end_time = None
pt = None
coe = 1.38

class Board:
    def __init__(self, par=None, col=None, a=None, pos=None, dice=None):
        self.parent = par
        self.validchess = []
        self.chess = [0, -1]
        self.posStep = [[], []]
        self.color = col
        self.board = np.zeros((5, 5), dtype=int)
        self.visit_times = 0
        self.win_time = 0
        self.quality = 0.0
        self.child = []

      
        if type(dice)!=int:
            if col == 0:
                for i in range(5):
                    for j in range(5):
                        temp = a[i][j]
                        self.board[i][j] = temp
                        if 1 <= temp <= 6:
                            self.validchess.append(temp)
            else:
                for i in range(5):
                    for j in range(5):
                        temp = a[i][j]
                        self.board[i][j] = temp
                        if temp >= 7:
                            self.validchess.append(temp - 6)

        else:
            self.parent = par
            self.color = col
            ch = [0] * 7

            if col == 0:
                for i in range(5):
                    for j in range(5):
                        temp = a[i][j]
                        self.board[i][j] = temp
