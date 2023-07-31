from enums.chess import ChessColor
from board import Board
import Agents.alpha_beta_boost.logic as logic


class Alpha_beta_player:
    def __init__(self, color=ChessColor.BLUE, depth=4):
        super().__init__()
        self.color = color
        self.depth = depth
        self.name = "Alpha_beta_player"

    def set_color(self, color: ChessColor):
        self.color = color

    def set_depth(self, depth: int):
        self.depth = depth

    def get_action(self, board: Board):

        board_ = board.board.tolist()
        move = logic.get_move(board_, board.dice, self.depth,
                              board.sente.value, self.color.value)
        move = board.location_to_move(move)

        return move
