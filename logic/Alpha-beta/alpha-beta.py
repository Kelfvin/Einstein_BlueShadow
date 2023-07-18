import math

class Alphabet(object):
    def __init__(self):
        self.whoplay = 0
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

        SIZE = 5
        LINE = 5
        self.redValue = [0] * SIZE
        self.blueValue = [0] * SIZE
        self.redProbability = [0] * SIZE
        self.blueProbability = [0] * SIZE
        self.redthreaten = [0] * SIZE
        self.bluethreaten = [0] * SIZE

        self.blueprobabilityflag = [[0] * 2 for _ in range(SIZE)]
        self.redprobabilityflag = [[0] * 2 for _ in range(SIZE)]

        self.virtueTable = [[0] * LINE for _ in range(LINE)]

    def isThereBlue(self):
        for i in range(len(self.virtueTable)):
            for j in range(len(self.virtueTable[i])):
                if self.virtueTable[i][j] > 0:
                    return True
        return False

    def isThereRed(self):
        for i in range(len(self.virtueTable)):
            for j in range(len(self.virtueTable[i])):
                if self.virtueTable[i][j] < 0:
                    return True
        return False

    def judgeResult(self):
        if self.virtueTable[0][0] > 0 or not self.isThereRed():
            return 1
        if self.virtueTable[4][4] < 0 or not self.isThereBlue():
            return 2
        return 0
    
    def blueWhereToGo():

    def specialDeal():

    def blueMin():

    def redMax():


    def value(self):
        blueDistance = 0
        reddistance = 0
        blueThreaten = 0
        redThreaten = 0
        val = 0

        self.blueReady()
        for i in range(self.SIZE):
            if math.abs(blueProbability[i]>0.005) > 0.005:
                blueDistance += blueProbability[i]*blueValue[i]
                blueThreaten += blueProbability[i]*bluethreaten[i]
        self.redReady()
        for i in range(self.SIZE):
            if abs(redProbability[i] > 0.005) > 0.005:
                reddistance += redProbability[i] * redValue[i]
                redThreaten += redProbability[i] * redthreaten[i]
        val = (k1 * reddistance + k2 * bluedistance + k3 * blueThreaten + k4 * redThreaten);

        return val 

    def blueReady():

    def redReady():

    def getPointTOGO():
        
    def init():

    
    
        


