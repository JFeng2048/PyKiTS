# -*- coding:utf-8 -*-
# file:LeNet.py
import torch.nn as nn
import torch.nn.functional as F

class ModernLeNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ModernLeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)    # 输入1通道，输出6个特征图，卷积核5x5
        self.pool1 = nn.AvgPool2d(2, stride=2) # 2x2平均池化
        self.conv2 = nn.Conv2d(6, 16, 5)  # 输入6通道，输出16个特征图
        self.pool2 = nn.AvgPool2d(2, stride=2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120) # 将16x5x5的特征图展平后全连接
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x))) # 卷积 -> ReLU -> 池化
        x = self.pool2(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5) # 将多维特征图展平为一维向量
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

if __name__ == '__main__':
    model = ModernLeNet()
    # 打印第一个卷积层的权重和偏置信息
    print("=== 第一个卷积层 (conv1) ===")
    print("权重形状:", model.conv1.weight.shape)
    print("第一个滤波器权重:")
    print(model.conv1.weight[0])
    print("第二个滤波器权重:")
    print(model.conv1.weight[1])
    print("第三个滤波器权重:")
    print(model.conv1.weight[2])
    print("第四个滤波器权重:")
    print(model.conv1.weight[3])
    print("第五个滤波器权重:")
    print(model.conv1.weight[4])
    print("第六个滤波器权重:")
    print(model.conv1.weight[5])
    print("偏置形状:", model.conv1.bias.shape)
    print("偏置值:", model.conv1.bias)
    
    # 打印第二个卷积层的权重和偏置信息
    print("\n=== 第二个卷积层 (conv2) ===")
    print("权重形状:", model.conv2.weight.shape)
    print("第一个滤波器权重:")
    print(model.conv2.weight[0])
    print("第二个滤波器权重:")
    print(model.conv2.weight[1])
    print("第三个滤波器权重:")
    print(model.conv2.weight[2])
    print("第四个滤波器权重:")
    print(model.conv2.weight[3])
    print("第五个滤波器权重:")
    print(model.conv2.weight[4])
    print("第六个滤波器权重:")
    print(model.conv2.weight[5])
    print("偏置形状:", model.conv2.bias.shape)
    print("偏置值:", model.conv2.bias)
    
    # 打印第一个全连接层的权重和偏置信息
    print("\n=== 第一个全连接层 (fc1) ===")
    print("权重形状:", model.fc1.weight.shape)
    print("权重矩阵:")
    print(model.fc1.weight)
    print("偏置形状:", model.fc1.bias.shape)
    print("偏置值:", model.fc1.bias)
    
    # 打印第二个全连接层的权重和偏置信息
    print("\n=== 第二个全连接层 (fc2) ===")
    print("权重形状:", model.fc2.weight.shape)
    print("权重矩阵:")
    print(model.fc2.weight)
    print("偏置形状:", model.fc2.bias.shape)
    print("偏置值:", model.fc2.bias)
    
    # 打印第三个全连接层的权重和偏置信息
    print("\n=== 第三个全连接层 (fc3) ===")
    print("权重形状:", model.fc3.weight.shape)
    print("权重矩阵:")
    print(model.fc3.weight)
    print("偏置形状:", model.fc3.bias.shape)
    print("偏置值:", model.fc3.bias)
    
    # 打印整个模型结构
    print("\n=== 模型结构 ===")
    print(model)