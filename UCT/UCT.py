
from Board import *
import time
import random

def UCT(dice, board):
    root = None
    none = None
    if dice <= 6:
        root = Board(none, 0, board, dice)
    else:
        root = Board(none, 1, board, dice)
    
    begin = time.time()
    end = time.time()
    while end - begin < 5:
        p = Treepolicy(root)
        result = simulate(p)
        Backup(p, result)
        end = time.time()
    
    best = MostWin(root)
    return best

def simulate(v):
    origin = [[v.board[i][j] for j in range(5)] for i in range(5)]
    tempColor = v.color
    while not is_Terminal(v):
        tempColor = RandomMove(v, tempColor)
    
    red = sum(1 for i in range(5) for j in range(5) if 1 <= v.board[i][j] <= 6)
    blue = sum(1 for i in range(5) for j in range(5) if v.board[i][j] >= 7)
    if blue == 0 or (1 <= v.board[4][4] <= 6):
        result = 0
    else:
        result = 1
    
    for i in range(5):
        for j in range(5):
            v.board[i][j] = origin[i][j]
    
    return result

def Backup(v, result):
    while v:
        v.visit_times += 1
        if v.color ^ result:
            v.win_time += 1
        v.quality = v.win_time / v.visit_times
        v = v.parent

def MostWin(v):
    p = None
    max_quality = -1.0
    for child in v.child:
        if child.quality - max_quality > 0.0:
            max_quality = child.quality
            p = child
    return p

def Treepolicy(v):
    while not is_Terminal(v):
        if not is_Expanded(v):
            return Expand(v)
        else:
            v = BestChild(v, coe)
    return v

def is_Terminal(v):
    red = sum(1 for i in range(5) for j in range(5) if 1 <= v.board[i][j] <= 6)
    blue = sum(1 for i in range(5) for j in range(5) if v.board[i][j] >= 7)
    if red == 0 or blue == 0 or v.board[0][0] >= 7 or (1 <= v.board[4][4] <= 6):
        return True
    else:
        return False

def is_Expanded(v):
    if len(v.posStep[0]) > len(v.child):
        return False
    else:
        return True

def Expand(v):
    posChess = [[], []]
    for i in range(len(v.posStep[0])):
        flag = False
        for child in v.child:
            if child.chess[0] == v.posStep[0][i] and child.chess[1] == v.posStep[1][i]:
                flag = True
                break
        if not flag:
            posChess[0].append(v.posStep[0][i])
            posChess[1].append(v.posStep[1][i])
    
    index = random.randint(0, len(posChess[0])-1)
    newBoard = [[v.board[i][j] for j in range(5)] for i in range(5)]
    pos = [posChess[0][index], posChess[1][index]]
    newChild = Board(v, not v.color, newBoard, pos)
    v.child.append(newChild)
    return newChild


def BestChild(v, c):
    q = None
    max_quality = -1.0
    for child in v.child:
        UCB = child.quality / child.visit_times + c * math.sqrt(2 * math.log(v.visit_times) / child.visit_times)
        if UCB - max_quality > 0.0:
            q = child
            max_quality = UCB
    return q

def oneMove(v, newboard, chess, direction):
    x, y = 0, 0
    if v.color == 0:
        for i in range(5):
            for j in range(5):
                if newboard[i][j] == chess:
                    x = i
                    y = j
                    break
        if direction == 0:
            newboard[x][y + 1] = chess
            newboard[x][y] = 0
        elif direction == 1:
            newboard[x + 1][y] = chess
            newboard[x][y] = 0
        else:
            newboard[x + 1][y + 1] = chess
            newboard[x][y] = 0
    else:
        for i in range(5):
            for j in range(5):
                if newboard[i][j] == chess + 6:
                    x = i
                    y = j
                    break
        if direction == 0:
            newboard[x][y - 1] = chess + 6
            newboard[x][y] = 0
        elif direction == 1:
            newboard[x - 1][y] = chess + 6
            newboard[x][y] = 0
        else:
            newboard[x - 1][y - 1] = chess + 6
            newboard[x][y] = 0

def RandomMove(v, col):
    ch = [0] * 7
    x, y = 0, 0
    DICE = random.randint(1, 6)
    if col == 0:
        for i in range(5):
            for j in range(5):
                temp = v.board[i][j]
                if 1 <= temp <= 6:
                    ch[temp] += 1
        if ch[DICE] == 1:
            for i in range(5):
                for j in range(5):
                    if v.board[i][j] == DICE:
                        x = i
                        y = j
                        break
            if x == 4:
                v.board[x][y + 1] = DICE
                v.board[x][y] = 0
            elif y == 4:
                v.board[x + 1][y] = DICE
                v.board[x][y] = 0
            else:
                direct = random.randint(0, 2)
                if direct == 0:
                    v.board[x][y + 1] = DICE
                    v.board[x][y] = 0
                elif direct == 1:
                    v.board[x + 1][y] = DICE
                    v.board[x][y] = 0
                else:
                    v.board[x + 1][y + 1] = DICE
                    v.board[x][y] = 0
        else:
            cand_1, cand_2 = 9, 9
            for i in range(DICE - 1, 0, -1):
                if ch[i] == 1:
                    cand_1 = i
                    break
            for i in range(DICE + 1, 7):
                if ch[i] == 1:
                    cand_2 = i
                    break
            if cand_1 != 9 and cand_2 != 9:
                cand = random.randint(0, 1)
                if cand == 0:
                    choice = cand_1
                else:
                    choice = cand_2
            elif cand_1 == 9:
                choice = cand_2
            elif cand_2 == 9:
                choice = cand_1
            for i in range(5):
                for j in range(5):
                    if v.board[i][j] == choice:
                        x = i
                        y = j
                        break
            if x == 4:
                v.board[x][y + 1] = choice
                v.board[x][y] = 0
            elif y == 4:
                v.board[x + 1][y] = choice
                v.board[x][y] = 0
            else:
                direct = random.randint(0, 2)
                if direct == 0:
                    v.board[x][y + 1] = choice
                    v.board[x][y] = 0
                elif direct == 1:
                    v.board[x + 1][y] = choice
                    v.board[x][y] = 0
                else:
                    v.board[x + 1][y + 1] = choice
                    v.board[x][y] = 0
    else:
        for i in range(5):
            for j in range(5):
                temp = v.board[i][j]
                if temp >= 7:
                    ch[temp - 6] += 1
        if ch[DICE] == 1:
            for i in range(5):
                for j in range(5):
                    if v.board[i][j] == DICE + 6:
                        x = i
                        y = j
                        break
            if x == 0:
                v.board[x][y - 1] = DICE + 6
                v.board[x][y] = 0
            elif y == 0:
                v.board[x - 1][y] = DICE + 6
                v.board[x][y] = 0
            else:
                direct = random.randint(0, 2)
                if direct == 0:
                    v.board[x][y - 1] = DICE + 6
                    v.board[x][y] = 0
                elif direct == 1:
                    v.board[x - 1][y] = DICE + 6
                    v.board[x][y] = 0
                else:
                    v.board[x - 1][y - 1] = DICE + 6
                    v.board[x][y] = 0
        else:
            cand_1, cand_2 = 19, 19
            for i in range(DICE - 1, 0, -1):
                if ch[i] == 1:
                    cand_1 = i + 6
                    break
            for i in range(DICE + 1, 7):
                if ch[i] == 1:
                    cand_2 = i + 6
                    break
            if cand_1 != 19 and cand_2 != 19:
                cand = random.randint(0, 1)
                if cand == 0:
                    choice = cand_1
                else:
                    choice = cand_2
            elif cand_1 == 19:
                choice = cand_2
            elif cand_2 == 19:
                choice = cand_1
            for i in range(5):
                for j in range(5):
                    if v.board[i][j] == choice:
                        x = i
                        y = j
                        break
            if x == 0:
                v.board[x][y - 1] = choice
                v.board[x][y] = 0
            elif y == 0:
                v.board[x - 1][y] = choice
                v.board[x][y] = 0
            else:
                direct = random.randint(0, 2)
                if direct == 0:
                    v.board[x][y - 1] = choice
                    v.board[x][y] = 0
                elif direct == 1:
                    v.board[x - 1][y] = choice
                    v.board[x][y] = 0
                else:
                    v.board[x - 1][y - 1] = choice
                    v.board[x][y] = 0
    return not col
