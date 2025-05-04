import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 定义五子棋棋盘的大小
BOARD_SIZE = 15

# 定义五子棋模型
class GomokuModel(nn.Module):
    def __init__(self):
        super(GomokuModel, self).__init__()
        # 输入层：棋盘大小为15x15，有2个通道，分别表示黑棋和白棋的位置
        self.conv1 = nn.Conv2d(2, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(256 * BOARD_SIZE * BOARD_SIZE, 1024)
        self.fc2 = nn.Linear(1024, BOARD_SIZE * BOARD_SIZE)

    def forward(self, x):
        # 卷积层
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        # 展平
        x = x.view(-1, 256 * BOARD_SIZE * BOARD_SIZE)
        # 全连接层
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 将棋盘状态转换为模型输入
def board_to_input(board):
    # 创建一个大小为15x15x2的输入张量
    input_tensor = np.zeros((2, BOARD_SIZE, BOARD_SIZE), dtype=np.float32)
    # 黑棋为1，白棋为-1
    input_tensor[0, :, :] = (board == 1).astype(np.float32)
    input_tensor[1, :, :] = (board == -1).astype(np.float32)
    return torch.tensor(input_tensor).unsqueeze(0)  # 增加批量维度

# 模拟一个简单的五子棋棋盘
def simulate_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int8)
    # 随机放置一些棋子
    for _ in range(10):
        x = np.random.randint(0, BOARD_SIZE)
        y = np.random.randint(0, BOARD_SIZE)
        board[x, y] = np.random.choice([-1, 1])
    return board

# 定义损失函数和优化器
model = GomokuModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
def train_model():
    model.train()
    for epoch in range(10):  # 训练10个epoch
        # 模拟一个棋盘状态
        board = simulate_board()
        # 将棋盘状态转换为模型输入
        input_tensor = board_to_input(board)
        # 随机选择一个目标位置作为标签
        target = torch.randint(0, BOARD_SIZE * BOARD_SIZE, (1,))
        # 清空梯度
        optimizer.zero_grad()
        # 前向传播
        output = model(input_tensor)
        # 计算损失
        loss = criterion(output, target)
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 打印损失
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# 测试模型
def test_model():
    model.eval()
    # 模拟一个棋盘状态
    board = simulate_board()
    # 将棋盘状态转换为模型输入
    input_tensor = board_to_input(board)
    # 前向传播
    output = model(input_tensor)
    # 获取模型预测的位置
    predicted_position = torch.argmax(output).item()
    print(f'Predicted position: {predicted_position // BOARD_SIZE}, {predicted_position % BOARD_SIZE}')

# 主函数
if __name__ == '__main__':
    train_model()
    test_model()