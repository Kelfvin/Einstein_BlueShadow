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
                        if 1 <= temp <= 6:
                            ch[temp] += 1
                if ch[dice] == 1:
                    self.validchess.append(dice)
                else:
                    for i in range(dice - 1, 0, -1):
                        if ch[i] == 1:
                            self.validchess.append(i)
                            break
                    for i in range(dice + 1, 7):
                        if ch[i] == 1:
                            self.validchess.append(i)
                            break
            else:
                for i in range(5):
                    for j in range(5):
                        temp = a[i][j]
                        self.board[i][j] = temp
                        if temp >= 7:
                            ch[temp - 6] += 1
                if ch[dice - 6] == 1:
                    self.validchess.append(dice - 6)
                else:
                    for i in range(dice - 7, 0, -1):
                        if ch[i] == 1:
                            self.validchess.append(i)
                            break
                    for i in range(dice - 5, 7):
                        if ch[i] == 1:
                            self.validchess.append(i)
                            break

        self.com_posStep()

        

    def com_posStep(self):
        if self.color == 0:
            for valid_chess in self.validchess:
                for j in range(5):
                    for k in range(5):
                        if self.board[j][k] == valid_chess:
                            x = j
                            y = k
                            break
                if x == 4:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(0)
                elif y == 4:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(1)
                else:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(0)
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(1)
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(2)
        else:
            for valid_chess in self.validchess:
                for j in range(5):
                    for k in range(5):
                        if self.board[j][k] == valid_chess + 6:
                            x = j
                            y = k
                            break
                if x == 0:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(0)
                elif y == 0:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(1)
                else:
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(0)
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(1)
                    self.posStep[0].append(valid_chess)
                    self.posStep[1].append(2)