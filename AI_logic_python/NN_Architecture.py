from numpy import double
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F


class Brain(nn.Module):
    def __init__(self):
        super(Brain,self).__init__()
        self.conv1_1 = nn.Conv2d(3, 3, 5)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv1_2 = nn.Conv2d(3, 16, 5)
        self.conv1_3 = nn.Conv2d(16, 3, 5)
        self.conv1_4 = nn.Conv2d(3, 3, 5)

        self.conv2_1 = nn.Conv2d(3, 3, 5)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv2_2 = nn.Conv2d(3, 16, 5)
        self.conv2_3 = nn.Conv2d(16, 3, 5)
        self.conv2_4 = nn.Conv2d(3, 3, 5)

        self.conv3_1 = nn.Conv2d(3, 3, 5)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.conv3_2 = nn.Conv2d(3, 16, 5)
        self.conv3_3 = nn.Conv2d(16, 3, 5)
        self.conv3_4 = nn.Conv2d(3, 3, 5)


        self.fc1 = nn.Linear(1585 , 844)
        self.fc2 = nn.Linear(844, 512)
        self.fc3 = nn.Linear(512,256)
        self.fc4 = nn.Linear(256,128)
        self.fc5 = nn.Linear(128,84)
        self.fc6 = nn.Linear(84, 9)
        
    def forward(self , x,y,z,speed):
        #print(x.shape)
        #print(y.shape)
        #print(z.shape)
        self.im1 = self.pool1(F.relu(self.conv1_1(x)))
        #print(self.im1.shape)
        self.im1 = self.pool1(F.relu(self.conv1_2(self.im1)))
        self.im1 = self.pool1(F.relu(self.conv1_3(self.im1)))
        self.im1 = self.pool1(F.relu(self.conv1_4(self.im1)))

        #print(self.im1.shape)
        self.im1 = self.im1.view(self.im1.size(0), -1)
        #print(self.im1.shape)

        self.im2 = self.pool1(F.relu(self.conv2_1(y)))
        self.im2 = self.pool1(F.relu(self.conv2_2(self.im2)))
        self.im2 = self.pool1(F.relu(self.conv2_3(self.im2)))
        self.im2 = self.pool1(F.relu(self.conv2_4(self.im2)))

        self.im2 =  self.im2.view(self.im2.size(0), -1)
        #print(self.im2.shape)

        self.im3 = self.pool1(F.relu(self.conv3_1(z)))
        self.im3 = self.pool1(F.relu(self.conv3_2(self.im3)))
        self.im3 = self.pool1(F.relu(self.conv3_3(self.im3)))
        self.im3 = self.pool1(F.relu(self.conv3_4(self.im3)))
        self.im3 =  self.im3.view(self.im3.size(0), -1)
        #print(self.im3.shape)
        #print(self.im3)
        #print(speed.shape)

        self.x = torch.cat((self.im1,self.im2,self.im3,speed), 1)
        #print("Label: "+ str(self.x.shape))
        self.x = F.relu(self.fc1(self.x.float()))
        self.x = F.relu(self.fc2(self.x))
        self.x = F.relu(self.fc3(self.x))
        self.x = F.relu(self.fc4(self.x))
        self.x = F.relu(self.fc5(self.x))
        self.x = self.fc6(self.x)
        return self.x