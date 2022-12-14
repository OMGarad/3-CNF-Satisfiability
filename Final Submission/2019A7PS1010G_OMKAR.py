from hashlib import new
from random import betavariate
from CNF_Creator import *
import time


#Sentence is kept global to allow access to all functions
cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
#sentence= cnfC.CreateRandomSentence(m=120) # m is number of clauses in the 3-CNF sentence  
sentence = cnfC.ReadCNFfromCSVfile()

def GeneticAlgorithm(population):
    start_time=time.monotonic()   
    frequency=0
    bestValue=0
    iter=0

    arr=random.choices(population,weights=[(fitnessFunction(model)*100)**4 for model in population],k=4)
    arr.sort(key=fitnessFunction,reverse=True)
    bestIndividual=arr[0] #Making bestIndividual the best model out of the sorted array
    while(time.monotonic()-start_time<45 and fitnessFunction(bestIndividual)<1.0 and frequency<50):
        if(iter==0):
            newPopulation=arr[:2] #Initially keeping the best 2 models in the new population
        else:
            newPopulation=population[:2] #Keeping the best 2 models from the previous generation in the current one
        for i in range(len(population)-2):
            x=random.choices(population,weights=[(fitnessFunction(model)*100)**6 for model in population],k=1)[0] #Randomly choosing 2 arrays with weights of their fitness values
            y=random.choices(population,weights=[(fitnessFunction(model)*100)**6 for model in population],k=1)[0] #*100**6 makes the high fintess function values higher and lower ones lower
            
            child=reproduce(x,y) #Reproducing new children using the given arrays
            if(frequency<10):              
                if(random.random()<0.01): #Give a small probability to mutate. 
                    newChild, child= mutate(child)
                    newPopulation.append(newChild)
            else:
                if(random.random()<0.5): #If after 10 iterations, the best model isn't found, then we try to mutate it with a higher porbability
                    newChild, child= mutate(child)
                    newPopulation.append(newChild)
            newPopulation.append(child)
        newPopulation.sort(key=fitnessFunction,reverse=True)
        population=newPopulation[:len(population)] #Culling: Taking the best n models after sorting
        bestIndividual=population[0] #bestIndividual is at the first index of population after sorting 
        iter+=1
        #print(fitnessFunction(bestIndividual))
        if(abs(fitnessFunction(bestIndividual)- bestValue)<0.01*bestValue): #If FF value is within 1% of bestValue, then frequency increases
            frequency+=1
        else:
            bestValue=fitnessFunction(bestIndividual)
            frequency=0
    return bestIndividual, time.monotonic()-start_time


#Mutating the child by finding the best position for mutation
def mutate(child):
    child=child.copy()
    bestFFindex=-1
    secondbestModel=child
    secondbestFFIndex=bestFFindex
    bestFF=fitnessFunction(child)
    secondbestFF=bestFF
    for i in range(0, 50):
        temp=child
        if(child[i]==True):
            temp[i]=False
        else:
            temp[i]=True
        if(fitnessFunction(temp)>bestFF):
            secondbestFFIndex=bestFFindex
            secondbestFF=bestFF
            bestFFindex=i
            bestFF=fitnessFunction(temp)
    
    if(child[secondbestFFIndex]==True):
        secondbestModel[secondbestFFIndex]=False
    else:
        secondbestModel[secondbestFFIndex]=True
    
    if(bestFFindex<0):
        return child, secondbestModel
    if(child[bestFFindex]==True):
        child[bestFFindex]=False
    else:
        child[bestFFindex]=True

    return child, secondbestModel   

    
#Reproducing with both parents
def reproduce(x,y):
    x=x.copy()
    y=y.copy()
    maxFF=0
    maxC=0
    n=len(x)
    for c in range(0,n):
        z= x[:c] + y[c:]
        w= y[:c] + x[c:]
        if(maxFF<fitnessFunction(w) or maxFF<fitnessFunction(z)):
            maxFF= max(fitnessFunction(w), fitnessFunction(z))
            maxC=c  

    childOne= x[:maxC] + y[maxC:]
    childTwo= y[:maxC] + x[maxC:]
    if(fitnessFunction(childOne)>fitnessFunction(childTwo)):
        return childOne
    return childTwo



#Creating population of size k
def createPopulation(k):
    population=[]
    for i in range(0,k):
        model=[]
        for j in range(0,50):
            var= bool(random.getrandbits(1))
            model.append(var)
        population.append(model)
    return population


def fitnessFunction(model):
    numer=0
    denom=len(sentence)
    for i in range(len(sentence)):
        for j in range(0,3):
            num=sentence[i][j]
            if((num>0 and model[num-1]==True) or (num<0 and model[(num*(-1))-1]==False)):
                numer+=1
                break
    
    fitnessValue=numer/denom
    return fitnessValue
    


def main():
    #print('Random sentence : ',sentence)
    #print('\nSentence from CSV file : ',sentence)

    k=20
    population= createPopulation(k)
    
    optimalModel, timeTaken= GeneticAlgorithm(population)

    model=[]
    for i in range(len(optimalModel)):
        if(optimalModel[i]==True):
            model.append(i+1)
        else:
            model.append(-(i+1))


    print('\n\n')
    print('Roll No : 2019A7PS1010G')
    print('Number of clauses in CSV file : ',len(sentence))
    print('Best model : ',model)
    print('Fitness value of best model : ', fitnessFunction(optimalModel)*100, '%')
    print('Time taken : ', timeTaken, "seconds")
    print('\n\n')
    
    

if __name__=='__main__':
    main()