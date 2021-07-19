import pandas as pd
import numpy as np

shipLocationFile = pd.read_csv("D:\AI_Marine_Ship_Automation\AIdata\dataset\shipCoordinate.csv")
portsLocationFile = pd.read_csv("D:\AI_Marine_Ship_Automation\AIdata\dataset\PortsCoordinates.csv")

population_size = 600

print(shipLocationFile)
print("\n")
print(portsLocationFile)
print("\n")
print("\n")


shipLocation = shipLocationFile.values[:,0]
portsLocation = portsLocationFile.values

x= []
y = []
distances = {}

for i in range(len(portsLocation[:,0])+1):
    if(i == 0):
        coordinate1 = shipLocation[0].split("||")
        x.append(float(coordinate1[0]))
        y.append(float(coordinate1[1]))

    else:
        coordinate1 = portsLocation[i-1,1].split("||")
        x.append(float(coordinate1[0]))
        y.append(float(coordinate1[1]))

x = np.array(x)
y = np.array(y)

for i in range(len(portsLocation[:,0])+1):
    for j in range(1,len(portsLocation[:,0])+1):
        if(i!=j):
            index = str(i)+"-"+str(j) 
            
            if(i == 0):
                coordinate1 = shipLocation[0].split("||")
                coordinate2 = portsLocation[j-1,1].split("||")
                dist = ((((float(coordinate2[0]) - float(coordinate1[0]) )**2) + ((float(coordinate2[1])-float(coordinate1[1]))**2) )**0.5)
                distances[index] = dist
            else:
                coordinate1 = portsLocation[i-1,1].split("||")
                coordinate2 = portsLocation[j-1,1].split("||")
                dist = ((((float(coordinate2[0]) - float(coordinate1[0]) )**2) + ((float(coordinate2[1])-float(coordinate1[1]))**2) )**0.5)
                distances[index] = dist

print(distances)

print("\n")
print("\n")

# Genitic algorithm start here
# Fiding Fittness value less value means more fit
def cost(chromosome):
    prev = str(0)
    fit = 0
    for i in range(len(chromosome)):
        next = str(chromosome[i])
        fit+= distances[prev+"-"+next]
        prev = next
    return fit

# initialising population  
population = []
import random
choices = (portsLocation[:,0])

for i in range(population_size):
    random.shuffle(choices)
    totalDistance =cost(choices)
    indevidual = {'chromosomes':choices,'cost':totalDistance**10 , 'distance': totalDistance}
    population.append(indevidual)


# Sorting popultion

""""
def sortPopulation(population):
    n = population_size
    for i in range(n):
        for j in range(0, n-i-1):
            if population[j]['cost'] > population[j+1]['cost'] :
                population[j], population[j+1] = population[j+1], population[j]
    return population

"""

#population = sortPopulation(population)

def sortPopulation(nlist):
    
    if len(nlist)>1:
        mid = len(nlist)//2
        lefthalf = nlist[:mid]
        righthalf = nlist[mid:]

        sortPopulation(lefthalf)
        sortPopulation(righthalf)
        i=j=k=0       
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i]['cost'] < righthalf[j]['cost']:
                nlist[k]=lefthalf[i]
                i=i+1
            else:
                nlist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            nlist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            nlist[k]=righthalf[j]
            j=j+1
            k=k+1
    

test = np.copy(population).tolist()

sortPopulation(population)










"""
Natural Selection
"""
def get_probability_list():
    total_fit =0
    for i in population:
        total_fit +=i['cost']
    relative_fitness = [f['cost']/total_fit for f in population]
    probabilities = [1-sum(relative_fitness[:i+1]) 
                     for i in range(len(relative_fitness))]
    return probabilities
def roulette_wheel_pop(population, probabilities, number):
    chosen = []
    for n in range(number):
        while True:
            r = random.random()
            index = random.randrange(10)
            if r <= probabilities[index]:
                chosen.append(population[index]['chromosomes'])
                break
    return chosen



"""
Crossover

"""
def pointCrossover(selection):
    newIndevidual1 =[]
    newIndevidual2 =[]
    ind1 = np.copy(selection[0])
    ind2 = np.copy(selection[1])
    point = random.randint(2,len(portsLocation[:,0])-2)
    arrayAfterPoint = np.copy(ind1[point :])
    fullArray = np.copy(ind2)
    delete =[]
    for i in range(len(fullArray)):
        for j in arrayAfterPoint:
            if fullArray[i] == j:
                delete.append(i)
    resArray = np.delete(fullArray,delete ,axis =0)
    #print(arrayAfterPoint)
    #print(resArray)
    newIndevidual1 = np.hstack((np.copy(resArray),arrayAfterPoint))
    
    arrayBeforePoint = np.copy(ind2[: point])
    fullArray = np.copy(ind1)
    delete =[]
    for i in range(len(fullArray)):
        for j in arrayBeforePoint:
            if fullArray[i] == j:
                delete.append(i)
    resArray = np.delete(fullArray,delete ,axis =0)
    newIndevidual2 = np.hstack((arrayBeforePoint,np.copy(resArray)))
    return newIndevidual1,newIndevidual2



"""
Mutation

"""

def pointMutation(indevidual,prob):
    decisonVariable =random.randrange(101)
    if decisonVariable<=prob:
        point1 =random.randint(0,len(portsLocation[:,0])-1)
        point2 = random.randint(0,len(portsLocation[:,0])-1)
        temp1 = indevidual[point1]
        temp2 = indevidual[point2]
        indevidual[point1] =temp2
        indevidual[point2] =temp1
        point1 =random.randint(0,len(portsLocation[:,0])-1)
        point2 = random.randint(0,len(portsLocation[:,0])-1)
        temp1 = indevidual[point1]
        temp2 = indevidual[point2]
        indevidual[point1] =temp2
        indevidual[point2] =temp1
        point1 =random.randint(0,len(portsLocation[:,0])-1)
        point2 = random.randint(0,len(portsLocation[:,0])-1)
        temp1 = indevidual[point1]
        temp2 = indevidual[point2]
        indevidual[point1] =temp2
        indevidual[point2] =temp1
    return indevidual

test = 0
prev = 0
next = 0
prev_seq = 0
for i in range(0,100000):
    test +=1
    if test ==1:
        prev = population[0]['distance']

    if(not (prev_seq == population[0]['cost'])):
        prev_seq = population[0]['cost']
        print("generation "+str(i))
        print(population[0])
    probablities = get_probability_list()
    selection = roulette_wheel_pop(population, probablities, 2)
    ind1,ind2 =pointCrossover(selection)
    mut1 = pointMutation(ind1,100)
    mut2 = pointMutation(ind2,100)
    cst =cost(mut1)
    indevidual_1 = {'chromosomes':mut1,'cost':cst**10,'distance':cst}
    cst =cost(mut2)
    indevidual_2 = {'chromosomes':mut1,'cost':cst**10,'distance':cst}
    #print(indevidual_1)
    #print(indevidual_2)
    population[population_size-4] = indevidual_1
    population[population_size-3]= indevidual_2

    sortPopulation(population)

    if test > 15000:
        test = 0
        next = population[0]['distance']
        if prev <= next:
            print("generation "+str(i))
            print(population[0])
            break


print("\n")
print("\n")

"""
Finding all the solutions found by our algorithm

"""
minTime = population[0]['distance']
sol = {}
for i in population:
    if i['distance'] == minTime:
        ch =np.array2string(i['chromosomes'])
        sol[ch] = i['distance']
print(sol)


import matplotlib.pyplot as plt



sequence = population[0]["chromosomes"]
x_value = []
y_value = []
n = []
for i in range(len(x+1)):
    if(i == 0):
        x_value.append(x[0])
        y_value.append(y[0])
        n.append(0)
    else:
       x_value.append(x[sequence[i-1]])
       y_value.append(y[sequence[i-1]]) 
       n.append(sequence[i-1])

x_value= np.array(x_value)
y_value= np.array(y_value)
fig, ax = plt.subplots()
ax.scatter(x_value, y_value)

for i, txt in enumerate(n):
    ax.annotate(txt, (x_value[i], y_value[i]))
plt.plot(x_value, y_value)
plt.show()




