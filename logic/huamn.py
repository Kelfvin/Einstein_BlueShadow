# 这里模仿其他的Player类
# 真实的操作是由人来控制，只是在界面上进行占位的

class HumanPlayer():
    def __init__(self):
        super().__init__()
        self.name = 'Human'

    def get_action(self,board):
        return None
    
    def set_color(self,color):
        self.color = color