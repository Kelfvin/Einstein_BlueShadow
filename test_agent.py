# 用于测试两个Agent的强弱

import time
from enums.chess import ChessColor
from enums.Agents import Strategy

from logic.Net.pure_mcts import MCTSPlayer
from logic.UCT.UCT import UCTPlayer
from logic.board import Board
from logic.Net.UCT_fast_version import UCT_fast_version_player

class Logger(object):
    def __init__(self, log_path="default.log"):
        import sys
        self.terminal = sys.stdout
        self.log = open(log_path, "w", buffering=64, encoding="utf-8")
 
    def print(self, *message):
        message = ",".join([str(it) for it in message])
        self.terminal.write(str(message) + "\n")
        self.log.write(str(message) + "\n")
 
    def flush(self):
        self.terminal.flush()
        self.log.flush()
 
    def close(self):
        self.log.close()


class Game:

    def __init__(self, blueStrategy, redStrategy,filename=None):
        self.board = Board()
        self.blueStrategy = blueStrategy
        self.redStrategy = redStrategy
        self.players = {}
        self.filename = filename

        # 打开文件到子目录下
        if filename:
            self.log = Logger(f'./test_result/{filename}.txt')

        self.setBlueAgent()
        self.setRedAgent()


    def setBlueAgent(self):
        agent = self.blueStrategy()
        agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = agent

    def setRedAgent(self):
        agent = self.redStrategy()
        agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = agent


    def run(self, n_games=100):
        self.log.print(f'blue({self.blueStrategy})  vs red({self.redStrategy})')
        self.log.print(f'filename:{self.filename}')
        

        blueWin = redWin = 0
        
        for i in range(n_games):

            # 偶数是蓝方先手，奇数是红方先手
            firstPlayer = ChessColor.BLUE if i%2==0 else ChessColor.RED
            self.board = Board(firstPlayer)
            self.setBlueAgent()
            self.setRedAgent()

            self.log.print(f'\n第{i+1}局')
            # 记录先手后手信息
            self.log.print(f'first_player: {self.board.sente}')


            startTime = time.time()
            while self.board.checkWin() == None:
                self.log.print(self.board.board.T)
                point = self.board.get_point()
                self.log.print(f'point:{point}')
                turn = self.board.getturn()

                # 修改成文件输出
                self.log.print(f'{self.players[turn].name} start to stimulate')
                stimulateTimeStart = time.time()
                move = self.players[turn].get_action(self.board)
                self.log.print(f'{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}')
                self.log.print(f'move:{move}\n')

                self.do_move(move,show_msg=False)

                if self.board.checkWin() == ChessColor.RED:
                    redWin+=1

                if self.board.checkWin() == ChessColor.BLUE:
                    blueWin+=1


            # print(f'第{i+1}局结束，用时{time.time()-startTime}秒')
            # print(f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')

            self.log.print('*'*20)
            self.log.print(f'\n第{i+1}局结束，用时{time.time()-startTime}秒')
            self.log.print(f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')



    def do_move(self, move, show_msg=True):
        self.board.do_move(move)

        win = self.board.checkWin()


        if show_msg:
            if win == None:
                self.ui.boardStatusBar.append("现在该" + self.board.getturnStr() + "出手")
            elif win == ChessColor.BLUE:
                self.showMsg("蓝方赢了！")
            else:
                self.showMsg("红方赢了")

if __name__ == "__main__":

    # 获取当前的日期包含时间
    import datetime
    filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # 以当前日期加上时间作为文件名

    player1Class = UCT_fast_version_player
    player2Class = UCTPlayer

    msg = f'C_out=2.5 time limit=20s 改进root'

    filename = f'{filename}_{player1Class.__name__}_vs_{player2Class.__name__}_{msg}.txt'



    game = Game(UCT_fast_version_player, UCTPlayer,filename=filename)
    game.run()
