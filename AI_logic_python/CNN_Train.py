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


import numpy as np

import csv




# import dataset
def import_dataset():
    dataset = pd.read_csv('D:\AI_Marine_Ship_Automation\AIdata\dataset\dataset.csv')
    dataset =  dataset.values
    return dataset



# data preprocessing
classes ={
            "nan" : 0,
            "Up" : 1,
            "Down" : 2,
            "Right": 3,
            "Right|Up":4,
            "Left|Up": 5,
            "Right|Down":6,
            "Left|Down": 7,
            "Left" : 8
        }
        
def dataPrep(datasets):
    temp = []
    tempSpeed = []
    tempLab = []
    x = datasets[:,:-1]
    y = datasets[: , 4]
    trans1 = transforms.ToTensor()

    for i  in range(len(y)):
        #img1 = copy.deepcopy(Image.open(x[i,0]).convert('RGB'))
        #img2 = copy.deepcopy(Image.open(x[i,1]).convert('RGB'))
        #img3 = copy.deepcopy(Image.open(x[i,2]).convert('RGB'))
        im = Image.open(x[i,0]).convert('RGB')
        img1 = trans1(im).numpy()
        im.close()
        im = Image.open(x[i,1]).convert('RGB')
        img2 = trans1(im).numpy()
        im.close()
        im = Image.open(x[i,2]).convert('RGB')
        img3 = trans1(im).numpy()
        im.close()
        speed = x[i,3]
        label = classes[str(y[i]).strip()]
        temp.append(np.array([img1,img2,img3]))
        tempSpeed.append(np.array([speed]))
        tempLab.append(np.array([label]))
        
        #print(temp)
        
    images = torch.tensor(temp)
    speeds = torch.tensor(tempSpeed)
    lab = torch.tensor(tempLab)
    return images,speeds,lab
 

# creating Class for the dataset and creating traiing loader

class TrainingDataset(Dataset):
    def __init__(self):
        ds = import_dataset()
        img,speeds,labl = dataPrep(ds)
        self.img1 = img[:,0]
        self.img2 = img[:,1]
        self.img3 = img[:,2]
        self.speed = speeds
        self.label = labl[:,0]
        self.n_samples = len(labl)
    def __getitem__(self,index):
        return self.img1[index],self.img2[index],self.img3[index],self.speed[index],self.label[index]
        
    def __len__(self):
        return self.n_samples

datasetClass = TrainingDataset()        
dataLoader = DataLoader(dataset = datasetClass, batch_size = 8 ,shuffle=True)



# Defining Brain
model =  Arch.Brain()




# Train model
epochs = 100
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = 0.001)

Losses = []

def trainModel():
    for epoch in range(epochs):  # loop over the dataset multiple times
        running_loss = 0.0
        count = 0
        for i, data in enumerate(dataLoader, 0):
            count += 1
            # get the inputs
            img1,img2,img3,speed, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model.forward(img1,img2,img3,speed)
            #print(outputs.dtype)
            labels = labels.type(torch.LongTensor)
           
            loss = criterion(outputs,labels)
            
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        Losses.append(running_loss)
        print('Epoch [%d, %5d] loss: %.3f' %(epoch + 1, i + 1, running_loss/count))
        running_loss = 0.0
        count = 0
    PATH = "state_dict_model_1.pt"
    torch.save(model.state_dict(), PATH)
    print('Finished Training')




# Test Model
def testModel():
    pass


trainModel()


print("\n\n++++++++++++++++++++++++++++++++++++++ End Reached +++++++++++++++++++++++++++++++++++++")