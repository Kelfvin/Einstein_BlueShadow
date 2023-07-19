# 用于测试两个Agent的强弱

import time
from enums.chess import ChessColor
from enums.strategy import Strategy

from logic.Net.pure_mcts import MCTSPlayer
from logic.UCT.UCT import UCTPlayer
from logic.board import Board


agents = {
    Strategy.PURE_MCTS: MCTSPlayer,
    Strategy.UCT: UCTPlayer,
}

class Game:

    def __init__(self, blueStrategy, redStrategy):
        self.board = Board()
        self.blueStrategy = blueStrategy
        self.redStrategy = redStrategy
        self.players = {}

    
        self.setBlueAgent()
        self.setRedAgent()


    def setBlueAgent(self):
        agent = agents[self.blueStrategy]()
        agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = agent

    def setRedAgent(self):
        agent = agents[self.redStrategy]()
        agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = agent


    def run(self, n_games=100):
        blueWin = redWin = 0
        
        for i in range(100):
            print(f'\n第{i+1}局')
            startTime = time.time()
            while self.board.checkWin() == None:
                self.on_diceButton_clicked()
                turn = self.board.getturn()
                print(f'{self.players[turn].name} start to stimulate')
                stimulateTimeStart = time.time()
                move = self.players[turn].get_action(self.board)
                print(f'{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}')


                self.do_move(move,show_msg=False)

                if self.board.checkWin() == ChessColor.RED:
                    redWin+=1

                if self.board.checkWin() == ChessColor.BLUE:
                    blueWin+=1


            print(f'第{i+1}局结束，用时{time.time()-startTime}秒')
            print(f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')

            self.board = Board()
            self.setBlueAgent()
            self.setRedAgent()

if __name__ == "__main__":

    print('可用的Agent列表：')
    for i in agents:
        print(f'{i} : {agents[i].__name__}')

    print('请输入蓝方Agent的策略：')
    blueStrategy = Strategy(int(input()))
    print('请输入红方Agent的策略：')
    redStrategy = Strategy(int(input()))

    print(f'蓝方Agent：{agents[blueStrategy].__name__}')
    print(f'红方Agent：{agents[redStrategy].__name__}')

    game = Game(Strategy.UCT, Strategy.PURE_MCTS)
    game.run()
