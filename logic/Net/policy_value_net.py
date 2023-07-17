
import numpy as np
import torch
import os

class PolicyValueNet():
    '''
    policy and value net for the mctsplayer
    '''
    def __init__(self, board_width, board_height):
        # width, height: 5 - 5
        self.board_width = board_width
        self.board_height = board_height
        self.model_file = './model/torch_policy_WTN_model'

        # Define the tensorflow neural network
        # 1. Input:
        self.input_states = torch.tensor(
                torch.float32, shape=(-1, 4, board_height, board_width))   # mini-batch, 4, board_height, board_width
        self.input_state = tf.transpose(self.input_states, [0, 2, 3, 1])  # NHWC 输入格式
        # 2. Common Networks Layers
        # input: 输入棋盘张量
        # filters: 卷积核数目
        # kernel_size: 卷积核维度
        # data_format: NHWC
        # activation: 激活函数使用 relu
        self.conv1 = tf.layers.conv2d(inputs=self.input_state,
                                      filters=32, kernel_size=[3, 3],
                                      padding="same", data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv2 = tf.layers.conv2d(inputs=self.conv1, filters=64,
                                      kernel_size=[3, 3], padding="same",
                                      data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv3 = tf.layers.conv2d(inputs=self.conv2, filters=128,
                                      kernel_size=[3, 3], padding="same",
                                      data_format="channels_last",
                                      activation=tf.nn.relu)
        # 3-1 Action Networks，生成对应的落子动作
        self.action_conv = tf.layers.conv2d(inputs=self.conv3, filters=4,
                                            kernel_size=[1, 1], padding="same",
                                            data_format="channels_last",
                                            activation=tf.nn.relu)
        # Flatten the tensor，平坦生成带批次的全连接层
        self.action_conv_flat = tf.reshape(
                self.action_conv, [-1, 4 * board_height * board_width])
        # 3-2 Full connected layer, the output is the log probability of moves
        
        # the legal move on the board, 56 means the legal moves for red or blue player
        # create the probilities of 56 kinds of the moves
        self.action_fc = tf.layers.dense(inputs = self.action_conv_flat,
                                         units = 56,
                                         activation = tf.nn.log_softmax)


        # 4 Evaluation Networks，评估头
        self.evaluation_conv = tf.layers.conv2d(inputs=self.conv3, filters=2,
                                                kernel_size=[1, 1],
                                                padding="same",
                                                data_format="channels_last",
                                                activation=tf.nn.relu)
        # 全连接
        self.evaluation_conv_flat = tf.reshape(
                self.evaluation_conv, [-1, 2 * board_height * board_width])
        self.evaluation_fc1 = tf.layers.dense(inputs=self.evaluation_conv_flat,
                                              units=64, activation=tf.nn.relu)
        # output the score of evaluation on current state
        self.evaluation_fc2 = tf.layers.dense(inputs=self.evaluation_fc1,
                                              units=1, activation=tf.nn.tanh)
                                              

        # Define the Loss function
        # 1. Label: the array containing if the game wins or not for each state
        self.labels = tf.placeholder(tf.float32, shape=[None, 1])    # 第一个维度是批次
        # 2. Predictions: the array containing the evaluation score of each state
        # which is self.evaluation_fc2
        # 3-1. Value Loss function
        self.value_loss = tf.losses.mean_squared_error(self.labels, self.evaluation_fc2)

        # 3-2. Policy Loss function
        self.mcts_probs = tf.placeholder(tf.float32, shape=[None, 56])
        # self.policy_loss = tf.negative(tf.reduce_mean(
        #                 tf.reduce_sum(tf.multiply(self.mcts_probs, self.action_fc), 1)))
        self.policy_loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits=self.action_fc, labels=self.mcts_probs))
                
        # 3-3. L2 penalty (regularization)
        l2_penalty_beta = 1e-4
        vars = tf.trainable_variables()
        l2_penalty = l2_penalty_beta * tf.add_n(
            [tf.nn.l2_loss(v) for v in vars if 'bias' not in v.name.lower()])    # l2 损失不计算偏置变量
        # 3-4 Add up to be the Loss function
        self.loss = self.value_loss + self.policy_loss + l2_penalty

        # Define the optimizer we use for training
        self.learning_rate = tf.placeholder(tf.float32)
        self.optimizer = tf.train.AdamOptimizer(
                learning_rate=self.learning_rate).minimize(self.loss)

        # Make a session
        self.session = tf.Session()

        # calc policy entropy, for monitoring only
        # self.entropy = tf.negative(tf.reduce_mean(
        #   tf.reduce_sum(tf.exp(self.action_fc) * self.action_fc, 1)))
        self.entropy = self.policy_loss
        # Initialize variables
        init = tf.global_variables_initializer()
        self.session.run(init)

        # For saving and restoring
        self.saver = tf.train.Saver()
        
        self.restore_model()

    def policy_value(self, state_batch):
        """
        input: a batch of states
        output: a batch of action probabilities and state values
        """
        log_act_probs, value = self.session.run(
                [self.action_fc, self.evaluation_fc2],
                feed_dict={self.input_states: state_batch}
                )
        # act_probs: 56, valule: 1
        act_probs = np.exp(log_act_probs)
        return act_probs, value

    def policy_value_fn(self, board):
        """
        input: board
        output: a list of (action, probability) tuples for each available
        action and the score of the board state
        """
        # 加入对应的合法行棋, 已经获得了筛子的点数
        moves, true_moves = board.get_avaiable_moves()
        # 添加一个批次维度，不加的话，没有办法加入到网络中计算
        current_state = np.ascontiguousarray(board.get_current_state().reshape(
                -1, 4, self.board_width, self.board_height))
        act_probs, value = self.policy_value(current_state)
        # 返回可选的走子和对应的选择概率的元组列表
        act_probs = zip(true_moves, act_probs[0][moves])
        return act_probs, value

    def train_step(self, state_batch, mcts_probs, winner_batch, lr):
        """perform a training step"""
        winner_batch = np.reshape(winner_batch, (-1, 1))
        loss, entropy, _ = self.session.run(
                [self.loss, self.entropy, self.optimizer],
                feed_dict={self.input_states: state_batch,
                           self.mcts_probs: mcts_probs,
                           self.labels: winner_batch,
                           self.learning_rate: lr})
        return loss, entropy

    def restore_model(self):        
        if os.path.exists(self.model_file + '.meta'):
            # restore the model into the sess
            self.saver.restore(self.session, self.model_file)
            print("restore the lastest model ...")
        else:
            # do not exist the model file, try to init all the variable and prepare to train
            self.session.run(tf.global_variables_initializer())