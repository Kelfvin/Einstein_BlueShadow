import time
import datetime
from typing import List


class Einstein:
    def __init__(self):
        self.logger = []
        self.filename = ""  # log filename
        self.chessboard = [0] * 25
        self.dice = 0
        self.begin_time = time.time()
        self.end_time = time.time()

    def to_int(self, s: str, begin: int, end: int, a: List[int], line: int) -> None:
        i = begin
        j = begin + 1
        t = 0
        while j < end + 1:
            if s[j] == ',' or s[j] == ']':
                x = s[i:j]
                a[line * 5 + t] = int(x)
                t += 1
                i = j + 2
            j += 1

    def parse(self, s: str) -> int:
        k = s.find("], [", 0)
        l = s.find("], [", k + 4)
        m = s.find("], [", l + 4)
        n = s.find("], [", m + 4)
        p = s.find("]]|", n + 4)
        self.to_int(s, 2, k, self.chessboard, 0)
        self.to_int(s, k + 4, l, self.chessboard, 1)
        self.to_int(s, l + 4, m, self.chessboard, 2)
        self.to_int(s, m + 4, n, self.chessboard, 3)
        self.to_int(s, n + 4, p, self.chessboard, 4)
        d = s[p + 3:]
        self.dice = int(d)
        if len(self.logger) == 0:
            self.begin_time = time.time()
            return 0
        else:
            g = self.logger[-1]
            last = [0] * 25
            f = g.find("[[", 0)
            k = g.find("], [", f + 2)
            l = g.find("], [", k + 4)
            m = g.find("], [", l + 4)
            n = g.find("], [", m + 4)
            p = g.find("]]|", n + 4)
            self.to_int(g, f + 2, k, last, 0)
            self.to_int(g, k + 4, l, last, 1)
            self.to_int(g, l + 4, m, last, 2)
            self.to_int(g, m + 4, n, last, 3)
            self.to_int(g, n + 4, p, last, 4)
            diff = 0
            for i in range(25):
                if self.chessboard[i] != last[i]:
                    diff += 1
            if diff <= 4:
                return 0
            else:
                ze = g.rfind(" ")
                pr = g.rfind("|")
                chess = int(g[ze + 1:pr])
                operation = g[pr + 1:]
                t = 0
                while last[t] != chess:
                    t += 1
                if operation == "up":
                    last[t - 5] = chess
                    last[t] = 0
                elif operation == "left":
                    last[t - 1] = chess
                    last[t] = 0
                elif operation == "leftup":
                    last[t - 6] = chess
                    last[t] = 0
                elif operation == "down":
                    last[t + 5] = chess
                    last[t] = 0
                elif operation == "right":
                    last[t + 1] = chess
                    last[t] = 0
                else:
                    last[t + 6] = chess
                    last[t] = 0
                self.end_time = time.time()
                lasting = self.end_time - self.begin_time
                self.begin_time = time.time()
                if chess >= 7:
                    red = 0
                    for i in range(25):
                        if last[i] >= 1 and last[i] <= 6:
                            red += 1
                    if red == 0 or last[0] == chess:
                        self.logging("Game over! Blue wins! Time: " + str(lasting) + "s")
                        return 0
                    else:
                        self.logging("Game over! Red wins! Time: " + str(lasting) + "s")
                        return 0
                else:
                    blue = 0
                    for i in range(25):
                        if last[i] >= 7 and last[i] <= 12:
                            blue += 1
                    if blue == 0 or last[24] == chess:
                        self.logging("Game over! Red wins! Time: " + str(lasting) + "s")
                        return 0
                    else:
                        self.logging("Game over! Blue wins! Time: " + str(lasting) + "s")
                        return 0

    def handle(self) -> int:
        t = self.clientsocket.recvMsg()
        if t == 0:
            a = self.clientsocket.getRecvMsg()
            rec = a.decode()
            self.parse(rec)
            board = [[0] * 5 for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    board[i][j] = self.chessboard[i * 5 + j]
            # str = fool(dice, board)
            best = self.UCT(self.dice, board)
            if self.dice <= 6:
                if best.chess[1] == 0:
                    str = str(best.chess[0]) + "|right"
                elif best.chess[1] == 1:
                    str = str(best.chess[0]) + "|down"
                elif best.chess[1] == 2:
                    str = str(best.chess[0]) + "|rightdown"
            else:
                if best.chess[1] == 0:
                    str = str(best.chess[0] + 6) + "|left"
                elif best.chess[1] == 1:
                    str = str(best.chess[0] + 6) + "|up"
                elif best.chess[1] == 2:
                    str = str(best.chess[0] + 6) + "|leftup"
            self.now_time = time.time()
            self.clientsocket.sendMsg(str.encode())
            m = rec + " operation " + str
            pt = time.localtime(self.now_time)
            log = (
                str(pt.tm_year + 1900)
                + "-"
                + str(pt.tm_mon + 1)
                + "-"
                + str(pt.tm_mday)
                + " "
                + str(pt.tm_hour)
                + "-"
                + str(pt.tm_min)
                + "-"
                + str(pt.tm_sec)
                + " : "
                + m
            )
            self.logging(log)
            print(best.quality * 100.0, "%", sep="")
            self.DeleteAll(best.parent)
            return 1
        else:
            g = self.logger[-1]
            last = [0] * 25
            f = g.find("[[", 0)
            k = g.find("], [", f + 2)
            l = g.find("], [", k + 4)
            m = g.find("], [", l + 4)
            n = g.find("], [", m + 4)
            p = g.find("]]|", n + 4)
            self.to_int(g, f + 2, k, last, 0)
            self.to_int(g, k + 4, l, last, 1)
            self.to_int(g, l + 4, m, last, 2)
            self.to_int(g, m + 4, n, last, 3)
            self.to_int(g, n + 4, p, last, 4)
            diff = 0
            for i in range(25):
                if self.chessboard[i] != last[i]:
                    diff += 1
            if diff <= 4:
                return 0
            else:
                ze = g.rfind(" ")
                pr = g.rfind("|")
                chess = int(g[ze + 1:pr])
                operation = g[pr + 1:]
                t = 0
                while last[t] != chess:
                    t += 1
                if operation == "up":
                    last[t - 5] = chess
                    last[t] = 0
                elif operation == "left":
                    last[t - 1] = chess
                    last[t] = 0
                elif operation == "leftup":
                    last[t - 6] = chess
                    last[t] = 0
                elif operation == "down":
                    last[t + 5] = chess
                    last[t] = 0
                elif operation == "right":
                    last[t + 1] = chess
                    last[t] = 0
                else:
                    last[t + 6] = chess
                    last[t] = 0
                self.end_time = time.time()
                lasting = self.end_time - self.begin_time
                if chess >= 7:
                    red = 0
                    for i in range(25):
                        if last[i] >= 1 and last[i] <= 6:
                            red += 1
                    if red == 0 or last[0] == chess:
                        self.logging("Game over! Blue wins! Time: " + str(lasting) + "s")
                        return 0
                    else:
                        self.logging("Game over! Red wins! Time: " + str(lasting) + "s")
                        return 0
                else:
                    blue = 0
                    for i in range(25):
                        if last[i] >= 7 and last[i] <= 12:
                            blue += 1
                    if blue == 0 or last[24] == chess:
                        self.logging("Game over! Red wins! Time: " + str(lasting) + "s")
                        return 0
                    else:
                        self.logging("Game over! Blue wins! Time: " + str(lasting) + "s")
                        return 0
            return 0

    def logging(self, s: str) -> int:
        self.logger.append(s)
        print(s)
        return 0
