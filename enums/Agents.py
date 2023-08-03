from Agents.UCT.UCT import UCTPlayer
from Agents.Net.pure_mcts import MCTSPlayer
from Agents.UCT_fast_version.UCT_fast_version import UCT_fast_version_player
from Agents.human.huamn import HumanPlayer
from Agents.alpha_beta_boost.alpha_beta import Alpha_beta_player
from Agents.Mix.mix_player import MixPlayer

Agents = {
    'Human': HumanPlayer,
    'UCT': UCTPlayer,
    'MCTS': MCTSPlayer,
    'UCT_fast_version': UCT_fast_version_player,
    'AlphaBeta': Alpha_beta_player,
    'MixPlayer': MixPlayer
}
