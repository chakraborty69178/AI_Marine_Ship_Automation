import pandas as pd
import numpy as np

shipLocationFile = pd.read_csv("D:\AI_Marine_Ship_Automation\AIdata\dataset\shipCoordinate.csv")
portsLocationFile = pd.read_csv("D:\AI_Marine_Ship_Automation\AIdata\dataset\PortsCoordinates.csv")

print(shipLocationFile)
print(portsLocationFile)

shipLocation = shipLocationFile.values[:,0]
portsLocation = portsLocationFile.values[:,1]
print(shipLocation[0])