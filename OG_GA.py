from random import betavariate
from CNF_Creator import *
import time

cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
sentence = cnfC.CreateRandomSentence(m=100) # m is number of clauses in the 3-CNF sentence  
#sentence = cnfC.ReadCNFfromCSVfile()

def GeneticAlgorithm(population):
    start_time=time.monotonic()
    frequency=0
    bestValue=0
    bestIndividual = [False for _ in range(50)]
    while(time.monotonic()-start_time<45 and fitnessFunction(bestIndividual)<1.0 and frequency<50):
        newPopulation=population[:2] 
        for i in range(len(population)-2):
            x=random.choices(population,weights=[(fitnessFunction(model)*100)**2 for model in population],k=1)[0]
            y=random.choices(population,weights=[(fitnessFunction(model)*100)**2 for model in population],k=1)[0]
            #arr=random.choices(population,weights=[(fitnessFunction(model)*100)**2 for model in population],k=4)
            #arr.sort(key=fitnessFunction,reverse=True)
            #x=arr[0]
            #y=arr[1]
            child=reproduce(x,y)
            if(frequency<=10):
                if(random.random()<0.03): #Give a small probability to mutate. 
                    child= mutate(child)
            else:
                child= mutate(child) #If it gets stuck in a local minima, then get it out by increasing mutation rate.
            newPopulation.append(child)
        newPopulation.sort(key=fitnessFunction,reverse=True)
        population=newPopulation
        bestIndividual=population[0]
        print(fitnessFunction(bestIndividual))

        if(abs(fitnessFunction(bestIndividual)- bestValue)<0.01*bestValue):
            frequency+=1
        else:
            bestValue=fitnessFunction(bestIndividual)
            frequency=0
    return bestIndividual, time.monotonic()-start_time

def mutate(child):
    bestFFindex=-1
    bestFF=fitnessFunction(child)
    for i in range(0, 50):
        temp=child
        if(child[i]==True):
            temp[i]=False
        else:
            temp[i]=True
        if(fitnessFunction(temp)>bestFF):
            bestFFindex=i
    if(bestFFindex<0):
        return child
    if(child[bestFFindex]==True):
        child[bestFFindex]=False
    else:
        child[bestFFindex]=True

        

    """
    temp=child
    a= random.randint(1,50)
    if(child[a-1]==True):
        temp[a-1]==False
        if(fitnessFunction(temp)>fitnessFunction(child)):
            child=temp
    elif(child[a-1]==False):
        temp[a-1]==True
        if(fitnessFunction(temp)>fitnessFunction(child)):
            child=temp
    """
    """
    for i in range(len(child)):
        for j in range(3):
            if (child[i][j]==a):
                child[i][j]=-a
            elif(child[i][j]==-a):
                child[i][j]=a
    """
    return child     


def reproduce(x,y):
    maxFF=0
    maxC=0
    n=len(x)
    for c in range(0,n):
        z= x[:c] + y[c:]
        w= y[:c] + x[c:]
        if(maxFF<fitnessFunction(w) or maxFF<fitnessFunction(z)):
            maxFF= max(fitnessFunction(w), fitnessFunction(z))
            maxC=c
    
    z= x[:maxC] + y[maxC:]
    w= y[:maxC] + x[maxC:]
    if(fitnessFunction(z)>fitnessFunction(w)):
        return z
    return w

def createPopulation(k):
    pop=[]
    for i in range(0,k):
        model=[]
        for j in range(0,50):
            var= bool(random.getrandbits(1))
            model.append(var)
        pop.append(model)
        #print(model)
    return pop


def fitnessFunction(model):
    numer=0
    denom=len(sentence)
    for i in range(len(sentence)):
        for j in range(0,3):
            num=sentence[i][j]
            if((num>0 and model[num-1]==True) or (num<0 and model[(num*(-1))-1]==False)):
                numer+=1
                break
    
    """
    denom=len(sentence)
    num=0
    for i in range(len(sentence)):
        for j in range(0,3):
            if(sentence[i][j]>0):
                num+=1
                break
    
    fitnessValue=num/denom
    return fitnessValue
    """
    
    fitnessValue=numer/denom
    return fitnessValue
    


def main():
    #print('Random sentence : ',sentence)

    k=20
    population= createPopulation(k)

    #print(population)
    optimalModel, time= GeneticAlgorithm(population)

    model=[]
    for i in range(len(optimalModel)):
        if(optimalModel[i]==True):
            model.append(i+1)
        else:
            model.append(-(i+1))

    #print(model, fitnessFunction(optimalModel)*100, time)

    
    #print('\nSentence from CSV file : ',sentence)

    print('\n\n')
    print('Roll No : 2019A7PS1010G')
    print('Number of clauses in CSV file : ',len(sentence))
    print('Best model : ',model)
    print('Fitness value of best model : ', fitnessFunction(optimalModel)*100, '%')
    print('Time taken : ', time)
    print('\n\n')
    

if __name__=='__main__':
    main()