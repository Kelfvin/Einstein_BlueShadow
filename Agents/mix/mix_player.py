import jpype
from board import Board
from enums.chess import ChessColor


class MixPlayer:
    def __init__(self, color=ChessColor.BLUE, play_num=100000):
        self.color = color
        self.name = "Mix"
        self.play_num = play_num

    def init_jvm(self, jvmpath=None):
        if jpype.isJVMStarted():
            return

        jvmArg = "./Agents/Mix/"
        jpype.startJVM(jpype.getDefaultJVMPath(), '-ea',
                       f'-Djava.class.path={jvmArg}')

    def set_color(self, color):
        self.color = color

    def get_action(self, board: Board):

        self.init_jvm()
        MixClass = jpype.JClass("ahu.ewn.Main")

        javaMixClass = MixClass()

        board_ = board.board.tolist()
        point = board.dice

        result = javaMixClass.entry(
            board_, point, self.color.value, self.play_num)
        location = []
        for i in result:
            location.append(i)
        move = board.location_to_move(location)

        print(self.color)
        print(f'play_num:{self.play_num}')

        return move
