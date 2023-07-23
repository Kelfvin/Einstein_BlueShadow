import random, time
import numpy as np

from collections import defaultdict
from collections import deque

from board import Board
from game_without_GUI import Game
from logic.Net.pytorch_net import PolicyValueNet
from logic.Net.pure_mcts import MCTSPlayer as MCTS_Pure
from logic.Net.alphazero_mcts import MCTSPlayer


import os


class TrainPipeline():
    def __init__(self,init_model=None):
        # params of the board and the game
        self.board_width = 5
        self.board_height = 5
        self.game = Game()
        self.board = Board()
        
        # training params 
        self.learn_rate = 0.002
        self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.temp = 1.0 # the temperature param
        self.n_playout = 500 # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 512 # mini-batch size for training
        self.data_buffer = deque(maxlen=self.buffer_size)        
        self.play_batch_size = 1 
        self.epochs = 5 # num of train_steps for each update
        self.kl_targ = 0.02
        self.check_freq = 100
        self.game_batch_num = 2000
        self.best_win_ratio = 0.0
        # num of simulations used for the pure mcts, which is used as the opponent to evaluate the trained policy
        self.pure_mcts_playout_num = 3000
        
        # start training from a new policy-value net

        if init_model:
            # start training from an initial policy-value net
            self.policy_value_net = PolicyValueNet(model_file=init_model)
        else:
            # start training from a new policy-value net
            self.policy_value_net = PolicyValueNet()
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      c_puct=self.c_puct,
                                      n_playout=self.n_playout,
                                      is_selfplay=1)
        

    def collect_selfplay_data(self, n_games=1):
        """
        获取自我对弈的数据
        默认获取一局游戏的数据
        """
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player, temp=self.temp)
            self.data_buffer.extend(play_data)
                        
    def policy_update(self, verbose=False):
        """
        update the policy-value net
        verbose to show more details of the training steps, default not show
        """
        # ipdb.set_trace()
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]            
        
        old_probs, old_v = self.policy_value_net.policy_value(state_batch)
        
        loss_list = []
        entropy_list = []
        for i in range(self.epochs): 
            loss, entropy = self.policy_value_net.train_step(state_batch, 
                                             mcts_probs_batch, 
                                             winner_batch,
                                             self.learn_rate * self.lr_multiplier)
            
            loss_list.append(loss)
            entropy_list.append(entropy)
            
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (
                    np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)),
                    axis=1)
            )
            if kl > self.kl_targ * 4:  # early stopping if D_KL diverges badly
                break
        
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5
            
        if verbose:
            explained_var_old = (1 -
                                 np.var(np.array(winner_batch) - old_v.flatten()) /
                                 np.var(np.array(winner_batch)))
            explained_var_new = (1 -
                                 np.var(np.array(winner_batch) - new_v.flatten()) /
                                 np.var(np.array(winner_batch)))
            
            print(("kl: {:.3f}, "
                   "lr_multiplier: {:.3f}\n"
                   "last loss: {:.3f}, "
                   "mean loss: {:.3f}, "
                   "mean entropy: {:.3f}\n"
                   "explained old: {:.3f}, "
                   "explained new: {:.3f}\n"
                   ).format(kl,
                            self.lr_multiplier,
                            loss_list[-1],
                            np.mean(loss_list),
                            np.mean(entropy_list),
                            explained_var_old,
                            explained_var_new))        

        
    def policy_evaluate(self, n_games=10):
        """
        Evaluate the trained policy by playing games against the pure MCTS player
        Note: this is only for monitoring the progress of training
        """
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct, n_playout=3000)
        pure_mcts_player = MCTS_Pure(c_puct=5, n_playout=self.pure_mcts_playout_num)
        win_cnt = defaultdict(int)
        for i in range(n_games):
            # alphazero always red, but change the first player in the game 
            winner = self.game.start_play(current_mcts_player, pure_mcts_player, 1, 2, start_player= (i % 2) + 1, is_show=0)
            print("winner is {}".format(winner))
            win_cnt[winner] += 1
        # 计算红方(alphazero)的胜率
        win_ratio = win_cnt[1] / n_games
        print("num_playouts:{}, win: {}, lose: {}".format(self.pure_mcts_playout_num, win_cnt[1], win_cnt[2]))
        return win_ratio
    
    def run(self):
        """run the training pipeline"""
        try:
            for i in range(self.game_batch_num):  
                print("game", i, 'start ...')
                bt = time.time()
                self.collect_selfplay_data(self.play_batch_size)
                print('game', i, 'cost', int(time.time() - bt), 's')
             
                if len(self.data_buffer) > self.batch_size:
                    print("#### batch i:{} ####\n".format(i + 1))
                    for vi in range(5):
                        verbose = vi % 5 == 0
                        self.policy_update(verbose)         

                # check the performance of the current model，and save the model params
                # every 1000 check once
                if (i+1) % self.check_freq == 0:
                    print("current self-play batch: {}".format(i+1))
                    self.policy_value_net.saver.save(self.policy_value_net.session, self.policy_value_net.model_file)
                    win_ratio = self.policy_evaluate()
                    print('*****win ration: {:.2f}%\n'.format(win_ratio*100))
                    
                    if win_ratio > self.best_win_ratio: 
                        print("New best policy!!!!!!!!")
                        self.best_win_ratio = win_ratio
                        # save the model
                        self.policy_value_net.saver.save(self.policy_value_net.session, self.policy_value_net.model_file) # update the best_policy
                        if self.best_win_ratio == 1.0 and self.pure_mcts_playout_num < 5000:
                            self.pure_mcts_playout_num += 100
                            self.best_win_ratio = 0.0
        except KeyboardInterrupt:
            # save before quit
            self.policy_value_net.saver.save(self.policy_value_net.session, self.policy_value_net.model_file)
            print('quit, Bye !')
    
if __name__ == '__main__':
    training_pipeline = TrainPipeline()
    training_pipeline.run()
