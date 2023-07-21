from logic.UCT.UCT import UCTPlayer
from logic.Net.pure_mcts import MCTSPlayer
from logic.Net.UCT_fast_version import UCT_fast_version_player
from logic.alpha_beta.alpha_beta import AlphabetPlayer

Agents = {
    'UCT': UCTPlayer,
    'MCTS': MCTSPlayer,
    'UCT_fast_version': UCT_fast_version_player,
    'AlphaBeta': AlphabetPlayer
}




    
