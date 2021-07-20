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
"""
x_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Left/Left_26.png"
y_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Mid/Mid_26.png"
z_path = "D:/AI_Marine_Ship_Automation/AIdata/dataset/Right/Right_26.png"
"""

def import_dataset():
    dataset = pd.read_csv("D:\AI_Marine_Major_Project\AI_Marine_Ship_Automation\AIdata\dataset\dataset_test.csv")
    dataset =  dataset.values
    return dataset



classes ={
    #print(i)
            "nan" : 0,
            "Up" : 1,
            "Down" : 2,
            "Right": 3,
            "Right|Up":4,
            "Left|Up": 5,
            "Right|Down":6,
            "Left|Down": 7,
            "Left" : 8,
        }

labels ={
    0 : "nan",
    1 : "Up",
    2 : "Down",
    3 : "Right",
    4 : "Right|Up",
    5 : "Left|Up",
    6 : "Right|Down",
    7 : "Left|Down",
    8 : "Left",
}


speed = 10

def pred(x_paths,y_paths,z_paths,speeds):

    trans1 = transforms.ToTensor()

    im = Image.open(x_paths).convert('RGB')
    img1 = trans1(im).numpy()
    im.close()
    im = Image.open(y_paths).convert('RGB')
    img2 = trans1(im).numpy()
    im.close()
    im = Image.open(z_paths).convert('RGB')
    img3 = trans1(im).numpy()
    im.close()

    temp = []
    tempSpeed = []
    temp.append(np.array([img1,img2,img3]))
    tempSpeed.append(np.array([speeds]))

    img = torch.tensor(temp)
    speeds = torch.tensor(tempSpeed)

    X = img[:,0]
    Y = img[:,1]
    Z = img[:,2]
    S = speeds

    _, predicted = torch.max(model.forward(X,Y,Z,S), 1)

    return predicted.numpy()[0]
ds = import_dataset()
count = 0
length = len(ds[:, 0])
y = ds[:, 4]
#length = 500
print(length)
for i in range(length):
    
    predected_value  = pred(ds[i,0],ds[i,1],ds[i,2],ds[i,3])
    if predected_value == classes[str(y[i]).strip()]:
        count +=1
    print("S.NO "+str(i)+" Predected: "+labels[predected_value]+" expected: "+ str(y[i]).strip())
wrong = length - count
accuracy = (count/length)*100



print("\n\n Accuracy of this model is : "+ str(accuracy)+"%  Correct : "+str(count)+" Wrong: "+str(wrong))

