import torch
import torchvision
import torch.nn as nn


class Brain(nn.Module):
    def __init__(self):
        super(Brain,self).__init__()
        self.conv1_1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv1_2 = nn.Conv2d(6, 16, 5)

        self.conv2_1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2_1 = nn.Conv2d(6, 16, 5)

        self.conv3_1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv3_1 = nn.Conv2d(6, 16, 5)


        self.fc1 = nn.Linear((16 * 5 * 5)*3 +2 , 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 9)
    def forward(self , x,y,z,speed):
        pass