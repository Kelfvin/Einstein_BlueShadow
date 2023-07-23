"""策略价值网络"""

import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torch.cuda.amp import autocast
from board import Board
from torch.autograd import Variable
PYTORCH_ENABLE_MPS_FALLBACK = 1


class ResBlock(nn.Module):
    '''残差块'''

    def __init__(self, num_filters=256):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=num_filters, out_channels=num_filters, kernel_size=(
            3, 3), stride=(1, 1), padding=1)
        self.conv1_bn = nn.BatchNorm2d(num_filters, )
        self.conv1_act = nn.ReLU()
        self.conv2 = nn.Conv2d(in_channels=num_filters, out_channels=num_filters, kernel_size=(
            3, 3), stride=(1, 1), padding=1)
        self.conv2_bn = nn.BatchNorm2d(num_filters, )
        self.conv2_act = nn.ReLU()

    def forward(self, x):
        y = self.conv1(x)
        y = self.conv1_bn(y)
        y = self.conv1_act(y)
        y = self.conv2(y)
        y = self.conv2_bn(y)
        y = x + y
        return self.conv2_act(y)


class Net(nn.Module):
    '''搭建骨干网络，输入：N, 4, 5, 5 --> N, C, H, W'''

    def __init__(self, num_channels=256, num_res_blocks=7):
        '''num_channels: 通道数，特征
        num_res_blocks:残差块的个数'''
        super().__init__()
        # 全局特征
        # self.global_conv = nn.Conv2D(in_channels=9, out_channels=512, kernel_size=(10, 9))
        # self.global_bn = nn.BatchNorm2D(512)
        # 初始化特征
        self.conv_block = nn.Conv2d(4, num_channels, kernel_size=3, padding=1)
        self.conv_block_bn = nn.BatchNorm2d(256)
        self.conv_block_act = nn.ReLU()
        # 残差块抽取特征
        self.res_blocks = nn.ModuleList(
            [ResBlock(num_filters=num_channels) for _ in range(num_res_blocks)])
        # 策略头
        self.policy_conv = nn.Conv2d(num_channels, 16, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(16)
        self.policy_act = nn.ReLU()
        # 所有的走子的情况有：
        self.policy_fc = nn.Linear(16 * 5 * 5, 56)
        # 价值头
        self.value_conv = nn.Conv2d(num_channels, 8, kernel_size=1,)
        self.value_bn = nn.BatchNorm2d(8)
        self.value_act1 = nn.ReLU()
        self.value_fc1 = nn.Linear(8 * 5 * 5, 64)
        self.value_act2 = nn.ReLU()
        self.value_fc2 = nn.Linear(64, 1)

    # 定义前向传播
    def forward(self, x):
        # 公共头
        x = self.conv_block(x)
        x = self.conv_block_bn(x)
        x = self.conv_block_act(x)
        for layer in self.res_blocks:
            x = layer(x)
        # 策略头
        policy = self.policy_conv(x)
        policy = self.policy_bn(policy)
        policy = self.policy_act(policy)
        # ?
        policy = torch.reshape(policy, [-1, 16 * 5 * 5])
        policy = self.policy_fc(policy)
        policy = F.log_softmax(policy)
        # 价值头
        value = self.value_conv(x)
        value = self.value_bn(value)
        value = self.value_act1(value)
        value = torch.reshape(value, [-1, 8 * 5 * 5])
        value = self.value_fc1(value)
        value = self.value_act1(value)
        value = self.value_fc2(value)
        value = F.tanh(value)

        return policy, value


def try_gpu(i=0):
    """如果存在，则返回gpu(i)，如果是有苹果的GPU则用mps，否则返回cpu()"""
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')

    if torch.has_mps:
        return torch.device('mps')

    return torch.device('cpu')


def set_learning_rate(optimizer, lr):
    """Sets the learning rate to the given value"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class PolicyValueNet:
    '''策略值网络，用来进行模型的训练'''

    def __init__(self, model_file=None, device=try_gpu()):
        self.l2_const = 2e-3    # l2 正则化
        self.device = device
        self.policy_value_net = Net().to(self.device)
        '''用的还是之前定义的骨干网络'''
        self.optimizer = torch.optim.Adam(params=self.policy_value_net.parameters(
        ), lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=self.l2_const)
        print(model_file)
        if model_file:
            net_params = torch.load(model_file)
            self.policy_value_net.load_state_dict(net_params)

    def policy_value(self, state_batch):
        '''输入一个批次的状态，输出一个批次的动作概率和状态价值'''
        state_batch = Variable(torch.tensor(state_batch).to(self.device))
        log_act_probs, value = self.policy_value_net(state_batch)
        log_act_probs, value = log_act_probs.cpu(), value.cpu()
        act_probs = np.exp(log_act_probs.detach().numpy())
        return act_probs, value.data.cpu().numpy()

    def policy_value_fn(self, board: Board):
        '''输入棋盘，返回每个合法动作的（动作，概率）元组列表，以及棋盘状态的分数'''
        # 获取合法动作id列表
        legal_positions, _ = board.get_avaiable_moves()
        current_state = np.ascontiguousarray(
            board.get_current_state().reshape(-1, 4, 5, 5))
        current_state = torch.as_tensor(current_state).to(
            self.device, dtype=torch.float32)

        log_act_probs, value = self.policy_value_net(
            Variable(current_state))
        act_probs = np.exp(log_act_probs.data.cpu().numpy().flatten())

        # 只取出合法动作
        act_probs = zip(legal_positions, act_probs[legal_positions])
        value = value.data[0][0]
        # 返回动作概率，以及状态价值

        return act_probs, value

    def train_step(self, state_batch, mcts_probs, winner_batch, lr=0.002):
        '''执行一步训练'''
        self.policy_value_net.train()
        # 包装变量
        state_batch = Variable(torch.FloatTensor(state_batch).to(self.device))
        mcts_probs = Variable(torch.FloatTensor(mcts_probs).to(self.device))
        winner_batch = Variable(
            torch.FloatTensor(winner_batch).to(self.device))
        # 清零梯度
        self.optimizer.zero_grad()
        # 设置学习率
        set_learning_rate(self.optimizer, lr)

        # 前向运算
        log_act_probs, value = self.policy_value_net(state_batch)
        # define the loss = (z - v)^2 - pi^T * log(p) + c||theta||^2
        # Note: the L2 penalty is incorporated in optimizer

        # 价值损失
        value_loss = F.mse_loss(value.view(-1), winner_batch)
        # 策略损失
        # 希望两个向量方向越一致越好
        policy_loss = -torch.mean(torch.sum(mcts_probs * log_act_probs, dim=1))
        # 总的损失，注意l2惩罚已经包含在优化器内部
        loss = value_loss + policy_loss
        # 反向传播及优化
        loss.backward()
        self.optimizer.step()
        # 计算策略的熵，仅用于评估模型
        with torch.no_grad():
            entropy = -torch.mean(
                torch.sum(torch.exp(log_act_probs) * log_act_probs, dim=1)
            )
        return loss.item(), entropy.item()

    def get_policy_param(self):
        net_params = self.policy_value_net.state_dict()
        return net_params

    # 保存模型
    def save_model(self, model_file):
        net_params = self.get_policy_param()
        torch.save(net_params, model_file)
