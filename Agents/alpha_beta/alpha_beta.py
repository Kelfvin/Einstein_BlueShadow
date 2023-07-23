import math
import sys
from random import randint
import copy


SIZE = 5
LINE = 5
class AlphabetPlayer(object):
    def set_color(self, color):
        self.direction = color

    ##传入参数：棋局与深度
    def get_action(self, board, depth=5):
        move = self.caculate(board,depth)
        return board.location_to_move(move)
    
    def __init__(self):
        
        self.name = "Alphabet" ##算法名字
        
        self.redValueChart = [
            [0, 2, 2, 2, 2],
            [2, 4, 4, 4, 5],
            [2, 4, 8, 8, 10],
            [2, 4, 8, 16, 20],
            [2, 5, 10, 20, 32]
        ]
        self.blueValueChart = [
            [32, 20, 10, 5, 2],
            [20, 16, 8, 4, 2],
            [10, 8, 8, 4, 2],
            [5, 4, 4, 4, 2],
            [2, 2, 2, 2, 1]
        ]


        self.redValue = [0] * SIZE
        self.blueValue = [0] * SIZE
        self.redProbability = [0] * SIZE
        self.blueProbability = [0] * SIZE
        self.redthreaten = [0] * SIZE
        self.bluethreaten = [0] * SIZE

        self.blueprobabilityflag = [[0] * 2 for _ in range(SIZE)]
        self.redprobabilityflag = [[0] * 2 for _ in range(SIZE)]

        self.virtueTable = [[0] * LINE for _ in range(LINE)]

        self.k1 = 20  # 需要的k1系数
        self.k2 = -16  # 需要的k2系数
        self.k3 = -12  # 需要的k3系数
        self.k4 = 10  # 需要的k4系数
        self.infinity = 128
        self.SIZE = 6
        self.LINE = 5
    
   
        
    def isThereBlue(self):
        for i in range(len(self.self.virtueTable)):
            for j in range(len(self.self.virtueTable[i])):
                if self.self.virtueTable[i][j] > 0:
                    return True
        return False

    def isThereRed(self):
        for i in range(len(self.self.virtueTable)):
            for j in range(len(self.self.virtueTable[i])):
                if self.self.virtueTable[i][j] < 0:
                    return True
        return False

    def judgeResult(self):
        if self.self.virtueTable[0][0] > 0 or not self.isThereRed():
            return 1
        if self.self.virtueTable[4][4] < 0 or not self.isThereBlue():
            return 2
        return 0
    
    def blueWhereToGo(self,x, y, depth, alpha, beta):
        a1 = 0  # 用于保存三个方向的棋值
        val = 0
        temp = 0
        flag = 0
        bestmoveX = None
        bestmoveY = None

        if x > 0 and y > 0:  # 有左上方

            a1 = self.self.virtueTable[x - 1][y - 1]
            self.self.virtueTable[x - 1][y - 1] = self.self.virtueTable[x][y]
            self.self.virtueTable[x][y] = 0

            # 计算左上点价值
            for i in range(5):
                for j in range(5):
                    if self.self.virtueTable[i][j] < 0:
                        self.redReady()
                        val += self.redProbability[-self.self.virtueTable[i][j] - 1] * self.redMax(i, j, depth, alpha, beta)
                        flag += 1

            # 最优棋步，杀得对方一个也没有了
            bestmoveX = x - 1
            bestmoveY = y - 1
            if flag == 0:
                x = bestmoveX
                y = bestmoveY
                return (x, y)
            flag = 0

            # 恢复棋盘
            self.self.virtueTable[x][y] = self.self.virtueTable[x - 1][y - 1]
            self.self.virtueTable[x - 1][y - 1] = a1

            # 蓝棋走左上--------------------------------------------------------

            # 蓝棋走左边
            a1 = self.self.virtueTable[x - 1][y]
            self.self.virtueTable[x - 1][y] = self.self.virtueTable[x][y]
            self.self.virtueTable[x][y] = 0

            # 计算左边价值
            for i in range(5):
                for j in range(5):
                    if self.self.virtueTable[i][j] < 0:
                        self.redReady()
                        temp += self.redProbability[-self.self.virtueTable[i][j] - 1] * self.redMax(i, j, depth, alpha, beta)
                        flag += 1

            # 最优棋步
            if flag == 0:
                x = bestmoveX
                y = bestmoveY
                return (x, y)
            flag = 0

            if temp < val:
                val = temp
                bestmoveX = x - 1
                bestmoveY = y

            temp = 0

            # 恢复棋盘
            self.self.virtueTable[x][y] = self.self.virtueTable[x - 1][y]
            self.self.virtueTable[x - 1][y] = a1

            # 蓝棋走左边--------------------------------------------------------

            # 蓝棋走上方--------------------------------------------------------
            a1 = self.virtueTable[x][y - 1]
            self.virtueTable[x][y - 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0

            # 计算上方价值
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        temp += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth, alpha, beta)
                        flag += 1

            if flag == 0:
                x = bestmoveX
                y = bestmoveY
                return (x, y)
            flag = 0

            # 最优棋步
            if temp < val:
                val = temp
                bestmoveX = x
                bestmoveY = y - 1

            # 蓝棋走上方--------------------------------------------------------

           
            self.virtueTable[x][y] = self.virtueTable[x][y - 1]
            self.virtueTable[x][y - 1] = a1

            # 最终最优棋步
            x = bestmoveX
            y = bestmoveY
            return (x, y)

        elif x == 0:  # 左边为墙，用不着估值，因为只能走啊
            y = y - 1
            return (x, y)
        elif y == 0:  # 上方为墙，用不着估值，因为只能走啊
            x = x - 1
            return (x, y)
        
    def blueMin(self,x,y,depth,alpha,beta):
        if self.judgeResult() == 1:
            return -sys.maxsize()
        if self.judgeResult() == 2:
            return sys.maxsize()

        a2 = 0
        val = 0
        temp = 0

        if self.depth == 0:
            if x > 0 and y > 0:
                a2 = self.virtueTable[x - 1][y - 1]
                self.virtueTable[x - 1][y - 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()
                self.virtueTable[x][y] = self.virtueTable[x - 1][y - 1]
                self.virtueTable[x - 1][y - 1] = a2
                beta = min(beta, val)
                if beta <= alpha:
                    return beta

                a2 = self.virtueTable[x - 1][y]
                self.virtueTable[x - 1][y] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                temp = self.value()
                self.virtueTable[x][y] = self.virtueTable[x - 1][y]
                if temp < val:
                    val = temp
                self.virtueTable[x - 1][y] = a2
                beta = min(beta, val)
                if beta <= alpha:
                    return beta

                a2 = self.virtueTable[x][y - 1]
                self.virtueTable[x][y - 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                temp = self.value()
                self.virtueTable[x][y] = self.virtueTable[x][y - 1]
                if temp < val:
                    val = temp
                self.virtueTable[x][y - 1] = a2
                beta = min(beta, val)
                if beta <= alpha:
                    return beta
            elif x == 0:
                a2 = self.virtueTable[x][y - 1]
                self.virtueTable[x][y - 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()
                self.virtueTable[x][y] = self.virtueTable[x][y - 1]
                self.virtueTable[x][y - 1] = a2
            elif y == 0:
                a2 = self.virtueTable[x - 1][y]
                self.virtueTable[x - 1][y] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()
                self.virtueTable[x][y] = self.virtueTable[x - 1][y]
                self.virtueTable[x - 1][y] = a2
            return val

        if x > 0 and y > 0:
            a2 = self.virtueTable[x - 1][y - 1]
            self.virtueTable[x - 1][y - 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        val += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x - 1][y - 1]
            self.virtueTable[x - 1][y - 1] = a2
            beta = min(beta, val)
            if beta <= alpha:
                return beta

            a2 = self.virtueTable[x - 1][y]
            self.virtueTable[x - 1][y] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        temp += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth - 1, alpha, beta)
            if temp < val:
                val = temp
            temp = 0
            self.virtueTable[x][y] = self.virtueTable[x - 1][y]
            self.virtueTable[x - 1][y] = a2
            beta = min(beta, val)
            if beta <= alpha:
                return beta

            a2 = self.virtueTable[x][y - 1]
            self.virtueTable[x][y - 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        temp += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth - 1, alpha, beta)
            if temp < val:
                val = temp
            self.virtueTable[x][y] = self.virtueTable[x][y - 1]
            self.virtueTable[x][y - 1] = a2
            beta = min(beta, val)
            if beta <= alpha:
                return beta
        elif x == 0:
            a2 = self.virtueTable[x][y - 1]
            self.self.virtueTable[x][y] = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        val += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x][y - 1]
            self.virtueTable[x][y - 1] = a2
        elif y == 0:
            a2 = self.virtueTable[x - 1][y]
            self.virtueTable[x - 1][y] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] < 0:
                        self.redReady()
                        val += self.redProbability[-self.virtueTable[i][j] - 1] * self.redMax(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x - 1][y]
            self.virtueTable[x - 1][y] = a2
        return val


    def redMax(self,x, y, depth, alpha, beta):
        if self.judgeResult() == 1:
            return -sys.maxsize()
        if self.judgeResult() == 2:
            return sys.maxsize()

        if depth == 0:
            if x < 4 and y < 4:
                a = self.virtueTable[x + 1][y + 1]
                self.virtueTable[x + 1][y + 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()

                self.virtueTable[x][y] = self.virtueTable[x + 1][y + 1]
                self.virtueTable[x + 1][y + 1] = a
                alpha = max(alpha, val)
                if beta <= alpha:
                    return alpha

                a = self.virtueTable[x + 1][y]
                self.virtueTable[x + 1][y] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                temp = self.value()
                self.virtueTable[x][y] = self.virtueTable[x + 1][y]
                if temp > val:
                    val = temp
                self.virtueTable[x + 1][y] = a
                alpha = max(alpha, val)
                if beta <= alpha:
                    return alpha

                a = self.virtueTable[x][y + 1]
                self.virtueTable[x][y + 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                temp = self.value()
                self.virtueTable[x][y] = self.virtueTable[x][y + 1]
                if temp > val:
                    val = temp
                self.virtueTable[x][y + 1] = a
                alpha = max(alpha, val)
                if beta <= alpha:
                    return alpha
            elif x == 4:
                a = self.virtueTable[x][y + 1]
                self.virtueTable[x][y + 1] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()
                self.virtueTable[x][y] = self.virtueTable[x][y + 1]
                self.virtueTable[x][y + 1] = a
            elif y == 4:
                a = self.virtueTable[x + 1][y]
                self.virtueTable[x + 1][y] = self.virtueTable[x][y]
                self.virtueTable[x][y] = 0
                val = self.value()
                self.virtueTable[x][y] = self.virtueTable[x + 1][y]
                self.virtueTable[x + 1][y] = a
            return val

        if x < 4 and y < 4:
            a = self.virtueTable[x + 1][y + 1]
            self.virtueTable[x + 1][y + 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            val = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] > 0:
                        self.blueReady()
                        val += self.blueProbability[self.virtueTable[i][j] - 1] * self.blueMin(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x + 1][y + 1]
            self.virtueTable[x + 1][y + 1] = a
            alpha = max(alpha, val)
            if beta <= alpha:
                return alpha

            a = self.virtueTable[x + 1][y]
            self.virtueTable[x + 1][y] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            val = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] > 0:
                        self.blueReady()
                        val += self.blueProbability[self.virtueTable[i][j] - 1] * self.blueMin(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x + 1][y]
            self.virtueTable[x + 1][y] = a
            alpha = max(alpha, val)
            if beta <= alpha:
                return alpha

            a = self.virtueTable[x][y + 1]
            self.virtueTable[x][y + 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            val = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] > 0:
                        self.blueReady()
                        val += self.blueProbability[self.virtueTable[i][j] - 1] * self.blueMin(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x][y + 1]
            self.virtueTable[x][y + 1] = a
            alpha = max(alpha, val)
            if beta <= alpha:
                return alpha
        elif x == 4:
            a = self.virtueTable[x][y + 1]
            self.virtueTable[x][y + 1] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            val = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] > 0:
                        self.blueReady()
                        val += self.blueProbability[self.virtueTable[i][j] - 1] * self.blueMin(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x][y + 1]
            self.virtueTable[x][y + 1] = a
        elif y == 4:
            a = self.virtueTable[x + 1][y]
            self.virtueTable[x + 1][y] = self.virtueTable[x][y]
            self.virtueTable[x][y] = 0
            val = 0
            for i in range(5):
                for j in range(5):
                    if self.virtueTable[i][j] > 0:
                        self.blueReady()
                        val += self.blueProbability[self.virtueTable[i][j] - 1] * self.blueMin(i, j, depth - 1, alpha, beta)
            self.virtueTable[x][y] = self.virtueTable[x + 1][y]
            self.virtueTable[x + 1][y] = a

        return val


    def value(self):
        blueDistance = 0
        reddistance = 0
        blueThreaten = 0
        redThreaten = 0
        val = 0

        self.blueReady()
        for i in range(self.SIZE):
            if math.abs(self.blueProbability[i]>0.005) > 0.005:
                blueDistance += self.blueProbability[i]*self.blueValue[i]
                blueThreaten += self.blueProbability[i]*self.bluethreaten[i]
        self.redReady()
        for i in range(self.SIZE):
            if abs(self.redProbability[i] > 0.005) > 0.005:
                reddistance += self.redProbability[i] * self.redValue[i]
                redThreaten += self.redProbability[i] * self.redthreaten[i]
        val = (self.k1 * reddistance + self.k2 * blueDistance + self.k3 * blueThreaten + self.k4 * redThreaten)

        return val 

    def blueReady(self):
        bluedistancerate = [0] * SIZE

        for i in range(LINE):
            self.blueProbability[i] = 0

        for i in range(LINE):
            for j in range(2):
                self.blueprobabilityflag[i][j] = False

        for i in range(LINE):
            self.redValue[i] = 0

        for i in range(LINE):
            self.blueValue[i] = 0

        for i in range(LINE):
            self.bluethreaten[i] = 0

        for i in range(LINE):
            for j in range(LINE):
                if self.virtueTable[i][j] > 0:
                    self.blueValue[self.virtueTable[i][j] - 1] = self.blueValueChart[i][j]
                elif self.virtueTable[i][j] < 0:
                    self.redValue[-self.virtueTable[i][j] - 1] = self.redValueChart[i][j]

        for i in range(LINE):
            for j in range(LINE):
                if self.virtueTable[i][j] > 0:
                    if i != 0 and j != 0:
                        self.blueProbabilityflag[self.virtueTable[i][j] - 1][0] = True
                        a = 0
                        b = 0
                        c = 0
                        temp = 0

                        if self.virtueTable[i][j - 1] < 0:
                            a = self.redValue[-self.virtueTable[i][j - 1] - 1]
                        if self.virtueTable[i - 1][j - 1] < 0:
                            b = self.redValue[-self.virtueTable[i - 1][j - 1] - 1]
                        if self.virtueTable[i - 1][j] < 0:
                            c = self.redValue[-self.virtueTable[i - 1][j] - 1]

                        temp = max(a, b)
                        temp = max(temp, c)
                        self.bluethreaten[self.virtueTable[i][j] - 1] = temp

                    elif i == 0 and j != 0:
                        self.blueProbabilityflag[self.virtueTable[i][j] - 1][0] = True
                        temp = 0
                        if self.virtueTable[i][j - 1] < 0:
                            temp = self.redValue[-self.virtueTable[i][j - 1] - 1]
                        self.bluethreaten[self.virtueTable[i][j] - 1] = temp

                    elif i != 0 and j == 0:
                        self.blueProbabilityflag[self.virtueTable[i][j] - 1][0] = True
                        temp = 0
                        if self.virtueTable[i - 1][j] < 0:
                            temp = self.blueValue[-self.virtueTable[i - 1][j] - 1]
                        self.bluethreaten[self.virtueTable[i][j] - 1] = temp

        distancerate = 0
        for i in range(5):
            for k in range(i + 1):
                if self.virtueTable[i][k] > 0:
                    bluedistancerate[distancerate] = self.virtueTable[i][k]
                    distancerate += 1
            for k in range(i, 0, -1):
                if self.virtueTable[k - 1][i] > 0:
                    bluedistancerate[distancerate] = self.virtueTable[k - 1][i]
                    distancerate += 1

        num = 0
        sum_val = 0
        for i in range(6):
            if bluedistancerate[i] > 0:
                num = bluedistancerate[i] - 1
                while num > 0 and not self.blueProbabilityflag[num - 1][0] and not self.blueProbabilityflag[num][1]:
                    sum_val += 1
                    self.blueProbabilityflag[num - 1][1] = True
                    num -= 1

                num = bluedistancerate[i] - 1
                while num < 5 and not self.blueProbabilityflag[num + 1][0] and not self.blueProbabilityflag[num][1]:
                    sum_val += 1
                    self.blueProbabilityflag[num + 1][1] = True
                    num += 1

                num = bluedistancerate[i] - 1
                sum_val += 1
                self.blueProbabilityflag[num][1] = True

                self.blueProbability[num] = sum_val / 6.0
                sum_val = 0


    def redReady(self):
    
        reddistancerate = [0] * SIZE

        for i in range(LINE):
            self.redProbability[i] = 0

        for i in range(LINE):
            for j in range(2):
                self.redprobabilityflag[i][j] = False

        for i in range(LINE):
            self.redValue[i] = 0

        for i in range(LINE):
            self.blueValue[i] = 0

        for i in range(LINE):
            self.redthreaten[i] = 0

        for i in range(LINE):
            for j in range(LINE):
                if self.virtueTable[i][j] > 0:
                    self.blueValue[self.virtueTable[i][j] - 1] = self.blueValueChart[i][j]
                elif self.virtueTable[i][j] < 0:
                    self.redValue[-self.virtueTable[i][j] - 1] = self.redValueChart[i][j]

        for i in range(LINE):
            for j in range(LINE):
                if self.virtueTable[i][j] < 0:
                    if i != 4 and j != 4:
                        self.redprobabilityflag[-self.virtueTable[i][j] - 1][0] = True
                        a = 0
                        b = 0
                        c = 0
                        temp = 0

                        if self.virtueTable[i][j + 1] > 0:
                            a = self.blueValue[self.virtueTable[i][j + 1] - 1]
                        if self.virtueTable[i + 1][j + 1] > 0:
                            b = self.blueValue[self.virtueTable[i + 1][j + 1] - 1]
                        if self.virtueTable[i + 1][j] > 0:
                            c = self.blueValue[self.virtueTable[i + 1][j] - 1]

                        temp = max(a, b)
                        temp = max(temp, c)
                        self.redthreaten[-self.virtueTable[i][j] - 1] = temp

                    elif i == 4 and j != 4:
                        self.redprobabilityflag[-self.virtueTable[i][j] - 1][0] = True
                        temp = 0
                        if self.virtueTable[i][j + 1] > 0:
                            temp = self.blueValue[self.virtueTable[i][j + 1] - 1]
                        self.redthreaten[-self.virtueTable[i][j] - 1] = temp

                    elif i != 4 and j == 4:
                        self.redprobabilityflag[-self.virtueTable[i][j] - 1][0] = True
                        temp = 0
                        if self.virtueTable[i + 1][j] > 0:
                            temp = self.blueValue[self.virtueTable[i + 1][j] - 1]
                        self.redthreaten[-self.virtueTable[i][j] - 1] = temp

        distancerate = 0
        for i in range(LINE - 1, -1, -1):
            for k in range(LINE - 1, i - 1, -1):
                if self.virtueTable[i][k] < 0:
                    reddistancerate[distancerate] = self.virtueTable[i][k]
                    distancerate += 1

            for k in range(i, LINE - 1):
                if self.virtueTable[k + 1][i] < 0:
                    reddistancerate[distancerate] = self.virtueTable[k + 1][i]
                    distancerate += 1

        num = 0
        sum = 0
        for i in range(SIZE):
            if reddistancerate[i] < 0:
                num = -reddistancerate[i] - 1
                while num > 0 and not (self.redprobabilityflag[num - 1][0] or self.redprobabilityflag[num - 1][1]):
                    sum += 1
                    self.redprobabilityflag[num - 1][1] = True

                num = -reddistancerate[i] - 1
                while num < LINE and not (self.redprobabilityflag[num + 1][0] or self.redprobabilityflag[num + 1][1]):
                    sum += 1
                    self.self.redprobabilityflag[num + 1][1] = True

                num = -reddistancerate[i] - 1
                sum += 1
                self.redprobabilityflag[num][1] = True
                self.redProbability[num] = sum / 6.0
                sum = 0


    def getPointToGo(self):
        
        if self.direction == 1:
            returnData = [[0,0], [0,0]]
            for i in range(LINE):
                for j in range(LINE):
                    if self.virtueTable[i][j] == self.random:
                        returnData[0] = [i,j]
                        returnData[1] = self.blueWhereToGo(i, j, self.depth, -sys.maxsize(), sys.maxsize())
                        return returnData

            temp1 = 0
            temp2 = 7
            k1, l1 = 0, 0
            k2, l2 = 0, 0

            for k in range(5):
                for l in range(5):
                    if self.self.virtueTable[k][l] > temp1 and self.self.virtueTable[k][l] < self.random:
                        temp1 = self.virtueTable[k][l]
                        k1, l1 = k, l
                    elif self.self.virtueTable[k][l] > self.random and self.self.virtueTable[k][l] < temp2:
                        temp2 = self.self.virtueTable[k][l]
                        k2, l2 = k, l

            if temp1 != 0 and temp2 == 7:
                returnData[0] = [k1,l1]
                returnData[1] = self.blueWhereToGo(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                return returnData
            elif temp1 == 0 and temp2 != 7:
                returnData[0] = [k2,l2]
                returnData[1] = self.blueWhereToGo(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                return returnData
            else:
                value1 = self.blueMin(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                value2 = self.blueMin(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                if value1 > value2:
                    returnData[0] = [k2, l2]
                    returnData[1] = self.blueWhereToGo(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                    return returnData
                else:
                    returnData[0] = [k1, l1]
                    returnData[1] = self.blueWhereToGo(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                    return returnData
        elif self.direction == -1:
            returnData = [[0, 0], [0, 0]]
            for i in range(LINE):
                for j in range(LINE):
                    if self.self.virtueTable[i][j] == self.rand:
                        returnData[0] = [4 - j, 4 - i]
                        returnData[1] = self.blueWhereToGo(i, j, self.depth, -sys.maxsize(), sys.maxsize())
                        temp = 4 - returnData[1].x()
                        returnData[1].setX(4 - returnData[1].y())
                        returnData[1].setY(temp)
                        return returnData

            temp1 = 0
            temp2 = 7
            k1, l1 = 0, 0
            k2, l2 = 0, 0

            for k in range(5):
                for l in range(5):
                    if self.self.virtueTable[k][l] > temp1 and self.self.virtueTable[k][l] < self.rand:
                        temp1 = self.self.virtueTable[k][l]
                        k1, l1 = k, l
                    elif self.self.virtueTable[k][l] > randint() and self.self.virtueTable[k][l] < temp2:
                        temp2 = self.virtueTable[k][l]
                        k2, l2 = k, l

            if temp1 != 0 and temp2 == 7:
                returnData[0] = [4 - l1, 4 - k1]
                returnData[1] = self.blueWhereToGo(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                temp = 4 - returnData[1].x()
                returnData[1].setX(4 - returnData[1].y())
                returnData[1].setY(temp)
                return returnData
            elif temp1 == 0 and temp2 != 7:
                returnData[0] =[4 - l2, 4 - k2]
                returnData[1] = self.blueWhereToGo(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                temp = 4 - returnData[1].x()
                returnData[1].setX(4 - returnData[1].y())
                returnData[1].setY(temp)
                return returnData
            else:
                value1 = self.blueMin(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                value2 = self.blueMin(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                if value1 > value2:
                    returnData[0] = [4 - l2, 4 - k2]
                    returnData[1] = self.blueWhereToGo(k2, l2, self.depth, -sys.maxsize(), sys.maxsize())
                    temp = 4 - returnData[1].x()
                    returnData[1].setX(4 - returnData[1].y())
                    returnData[1].setY(temp)
                    return returnData
                else:
                    returnData[0] = [4 - l1, 4 - k1]
                    returnData[1] = self.blueWhereToGo(k1, l1, self.depth, -sys.maxsize(), sys.maxsize())
                    temp = 4 - returnData[1].x()
                    returnData[1].setX(4 - returnData[1].y())
                    returnData[1].setY(temp)
                    return returnData 
    def caculate(self,board,depth=4):
        self.rand  = board.dice
        self.virtueTable = copy.deepcopy(board.board)
        self.depth = depth
        
    
    
        


