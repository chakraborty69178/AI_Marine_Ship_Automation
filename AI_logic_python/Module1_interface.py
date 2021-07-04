import torch
import torch.nn as nn
from torch.utils import data
from torch.utils.data import DataLoader,Dataset
import torchvision.transforms as transforms
import pandas as pd;
import NN_Architecture as Arch
from PIL import Image
import copy
from sklearn import preprocessing
import torch.nn.functional as F


import numpy as np

import csv

model = Arch.Brain()
model.load_state_dict(torch.load("state_dict_model_1.pt"))

x_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Left/Left_26.png"
y_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Mid/Mid_26.png"
z_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Right/Right_26.png"


speed = 10


trans1 = transforms.ToTensor()

im = Image.open(x_path).convert('RGB')
img1 = trans1(im).numpy()
im.close()
im = Image.open(y_path).convert('RGB')
img2 = trans1(im).numpy()
im.close()
im = Image.open(z_path).convert('RGB')
img3 = trans1(im).numpy()
im.close()

temp = []
tempSpeed = []
temp.append(np.array([img1,img2,img3]))
tempSpeed.append(np.array([speed]))

img = torch.tensor(temp)
speeds = torch.tensor(tempSpeed)

X = img[:,0]
Y = img[:,1]
Z = img[:,2]
S = speeds

_, predicted = torch.max(model.forward(X,Y,Z,S), 1)

print(predicted)

