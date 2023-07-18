# 用于测试接口的文件

from logic.Net.pytorch_net import Net
import torch
from logic.Net.pytorch_net import try_gpu
import random 
from enums.chess import ChessColor

if __name__ == '__main__':
    print(random.choice(list(ChessColor)))