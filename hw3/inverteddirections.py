import numpy as np
import sys
def ReadInput(filename):
    obstacles=[]
    cars_start=[]
    cars_end=[]
    with open(filename) as fp:
        s=int(fp.readline())
        n=int(fp.readline())
        o=int(fp.readline())
        for i in range(o):
            a=map(int,fp.readline().strip().split(','))
            obstacles.append(a)
        for i in range(n):
            a=map(int,fp.readline().strip().split(','))
            cars_start.append(a)
        for i in range(n):
            a=map(int,fp.readline().strip().split(','))
            cars_end.append(a)
    return s,obstacles,cars_start,cars_end
    
def WriteOutput(averageRewards):
    with open("output.txt","w") as fw:
        for a in averageRewards:
            fw.write(str(int(np.floor(a))))
            fw.write('\n')
        
def GenerateTransitionMatrix(size):
    transitionMatrix=dict()
    for x in range(size):
        for y in range(size):
            for a in range(4):
                l=[]
                if a==3:
                    l.append((x-1,y,0.7)) if x>0 else l.append((x,y,0.7))
                    l.append((x+1,y,0.1)) if x<size-1 else l.append((x,y,0.1))
                    l.append((x,y+1,0.1)) if y<size-1 else l.append((x,y,0.1))
                    l.append((x,y-1,0.1)) if y>0 else l.append((x,y,0.1))
                elif a==2:
                    l.append((x-1,y,0.1)) if x>0 else l.append((x,y,0.1))
                    l.append((x+1,y,0.7)) if x<size-1 else l.append((x,y,0.7))
                    l.append((x,y+1,0.1)) if y<size-1 else l.append((x,y,0.1))
                    l.append((x,y-1,0.1)) if y>0 else l.append((x,y,0.1))
                elif a==1:
                    l.append((x-1,y,0.1)) if x>0 else l.append((x,y,0.1))
                    l.append((x+1,y,0.1)) if x<size-1 else l.append((x,y,0.1))
                    l.append((x,y+1,0.7)) if y<size-1 else l.append((x,y,0.7))
                    l.append((x,y-1,0.1)) if y>0 else l.append((x,y,0.1))
                elif a==0:
                    l.append((x-1,y,0.1)) if x>0 else l.append((x,y,0.1))
                    l.append((x+1,y,0.1)) if x<size-1 else l.append((x,y,0.1))
                    l.append((x,y+1,0.1)) if y<size-1 else l.append((x,y,0.1))
                    l.append((x,y-1,0.7)) if y>0 else l.append((x,y,0.7))
                transitionMatrix[x,y,a]=l
    return transitionMatrix

def CalculateUtility(x,y,transitionMatrix,u,rewardMatrix):
    if rewardMatrix[x,y]==99:
        return rewardMatrix[x,y],-1
    ma=-sys.maxint - 1
    action=0
    for a in range(4):
        l=transitionMatrix[x,y,a]
        v=0
        for s in l:
            v+=u[s[0],s[1]]*s[2]
        if v>ma:
            ma=v
            action=a
    return rewardMatrix[x,y]+0.9*ma,action
    
def GetOptimalPolicy(size,transitionMatrix,rewardMatrix,start,dest):
    gamma=0.9
    epsilon=0.1
    rewardMatrix[dest[0],dest[1]]=99
    u=np.zeros((size,size))
    u1=np.zeros((size,size))
    policy=np.full((size,size),-1)
    ite=0
    while True:
        u=u1.copy()
        delta = 0
        for x in range(size):
            for y in range(size):
                u1[x,y],policy[x,y]=CalculateUtility(x,y,transitionMatrix,u,rewardMatrix)
                delta=max(delta,np.abs(u1[x,y]-u[x,y]))
        ite+=1
        if delta<epsilon*(1-gamma)/gamma:
            print ite
            return u,policy
        
def Turn_Left(move):
    if move==0:
        return 2
    if move==1:
        return 3
    if move==2:
        return 1
    if move==3:
        return 0
    return -1

def Turn_Right(move):
    if move==0:
        return 3
    if move==1:
        return 2
    if move==2:
        return 0
    if move==3:
        return 1
    return -1

def UpdatePos(size,pos,move):
    if move==3:
        if pos[0]==0:
            return pos
        return pos[0]-1,pos[1]
    if move==2:
        if pos[0]==size-1:
            return pos
        return pos[0]+1,pos[1]
    if move==1:
        if pos[1]==size-1:
            return pos
        return pos[0],pos[1]+1    
    if move==0:
        if pos[1]==0:
            return pos
        return pos[0],pos[1]-1
    return pos

def Simulate(size,cars,ends,optimalPolicy,rewardMatrix):
    averageRewards=[0]*len(cars)
    for i in range(len(cars)):
        for j in range(10):
            pos = cars[i][0],cars[i][1]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k=0
            dest = ends[i][0],ends[i][1]
            reward=0
            while pos != dest:
                move = optimalPolicy[i,pos[0],pos[1]]
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = Turn_Left(Turn_Left(move))
                        else:
                            move = Turn_Left(move)
                    else:
                        move = Turn_Right(move)
                k+=1
                #updatepos
                pos=UpdatePos(size,pos,move)
                reward+=rewardMatrix[pos[0],pos[1]]
                #print pos,dest
            reward+=100

            averageRewards[i]+=reward

        averageRewards[i]=averageRewards[i]/10
    return averageRewards    
   
def main():
   global policyMatrix
   global utilityMatrix
   size,obstacles,cars_start,cars_end=ReadInput("input.txt")
   
   transitionMatrix=GenerateTransitionMatrix(size)
   rewardMatrix = np.full((size,size),-1.0)
   for a in obstacles:
       rewardMatrix[a[0],a[1]]=-101.0
   optimalPolicy=np.zeros((len(cars_start),size,size),np.int)
   for i in range(len(cars_start)):
       utilityMatrix,policyMatrix=GetOptimalPolicy(size,transitionMatrix,rewardMatrix.copy(),cars_start[i],cars_end[i])
       optimalPolicy[i]=policyMatrix

   averageRewards= Simulate(size,cars_start,cars_end,optimalPolicy,rewardMatrix)
   policyMatrix= policyMatrix.transpose()
   for a in averageRewards:
       print int(np.floor(a))
   #WriteOutput(averageRewards)
   
if __name__ == "__main__" :
    main()