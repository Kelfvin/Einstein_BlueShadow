# 用于测试两个Agent的强弱

import time
from enums.chess import ChessColor
from enums.Agents import Agents
from board import Board
from logger import Logger


class Game:

    def __init__(self, blueStrategy, redStrategy, filename=None):
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
        # agent = self.blueStrategy(play_num=20000)
        agent.set_color(ChessColor.BLUE)
        self.players[ChessColor.BLUE] = agent

    def setRedAgent(self):
        agent = self.redStrategy()
        agent.set_color(ChessColor.RED)
        self.players[ChessColor.RED] = agent

    def run(self, n_games=100):
        self.log.print(
            f'blue({self.blueStrategy})  vs red({self.redStrategy})')
        self.log.print(f'filename:{self.filename}')

        blueWin = redWin = 0

        for i in range(n_games):

            # 偶数是蓝方先手，奇数是红方先手
            firstPlayer = ChessColor.BLUE if i % 2 == 0 else ChessColor.RED
            self.board = Board(firstPlayer)

            # 双方均设置为最优布局进行测试,避免出现一方布局不好的情况
            self.board.blue_best_place()
            self.board.red_best_place()

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
                self.log.print(
                    f'{self.players[turn].name} end to stimulate, time cost:{time.time()-stimulateTimeStart}')
                self.log.print(f'move:{move}\n')

                self.do_move(move, show_msg=False)

                if self.board.checkWin() == ChessColor.RED:
                    redWin += 1

                if self.board.checkWin() == ChessColor.BLUE:
                    blueWin += 1

            # print(f'第{i+1}局结束，用时{time.time()-startTime}秒')
            # print(f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')

            self.log.print('*'*20)
            self.log.print(f'\n第{i+1}局结束，用时{time.time()-startTime}秒')
            self.log.print(
                f'blue({self.blueStrategy})  vs red({self.redStrategy}) --- {blueWin}:{redWin}')

    def do_move(self, move, show_msg=True):
        self.board.do_move(move)

        win = self.board.checkWin()

        if show_msg:
            if win == None:
                self.ui.boardStatusBar.append(
                    "现在该" + self.board.getturnStr() + "出手")
            elif win == ChessColor.BLUE:
                self.showMsg("蓝方赢了！")
            else:
                self.showMsg("红方赢了")


if __name__ == "__main__":

    # 获取当前的日期包含时间
    import datetime
    filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # 以当前日期加上时间作为文件名

    # 打印所有的Agent，并显示序号，让用户选择
    agent_names = list(Agents.keys())
    for i in range(len(agent_names)):
        print(f'{i+1}:{agent_names[i]}')
    # 选择Agent
    player1_choice = int(input('选择player1:'))
    player2_choice = int(input('选择player2:'))

    player1Class = Agents[agent_names[player1_choice-1]]
    player2Class = Agents[agent_names[player2_choice-1]]

    msg = input('输入备注信息：')

    filename = f'{filename}_{player1Class.__name__}_vs_{player2Class.__name__}_{msg}.txt'

    game = Game(player1Class, player2Class, filename=filename)
    game.run()
