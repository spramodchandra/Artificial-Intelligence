global n
global currentMax
def ModifyMatrix(x,y,matrix):
    for k in xrange(x+1,n):
        matrix[k][y]=-1
    i = x+1
    j = y+1
    while i<n and j<n:
        matrix[i][j]=-1
        i+=1
        j+=1
    i = x+1
    j = y-1
    while i<n and j>=0:
        matrix[i][j]=-1
        i+=1
        j-=1
            
def MaxInMatrix(matrix,level):
    maximum=-1
    secondMaximun = -1
    thirdmax=-1
    for i in xrange(level,n):
        for j in range(n):
            temp =matrix[i][j]
            if temp > thirdmax:
                if temp >= secondMaximun:
                    if temp >= maximum:
                        maximum, secondMaximun, thirdmax = temp, maximum , secondMaximun            
                    else:
                        secondMaximun, thirdmax = temp, secondMaximun
                else:
                    thirdmax = temp
    return maximum,secondMaximun,thirdmax
  
        
def RecmaxActivity(p,matrix,level,sumtillnow):
    global currentMax
    maxinMatrix,secondMaximum,thirdmax = MaxInMatrix(matrix,level)
    returnvalue =-1
    expectedvalue = -1
    if maxinMatrix==-1:
        return -1
    if currentMax>0:
        expectedvalue = (currentMax -sumtillnow)*1.0/p
        if expectedvalue > maxinMatrix:
            return -1
        if secondMaximum ==-1 and p>1:
            return -1
        if sumtillnow+maxinMatrix + secondMaximum *(p-1) <currentMax:
            return -1
        if thirdmax ==-1 and p>2:
            return -1
        if sumtillnow+maxinMatrix + secondMaximum+ thirdmax*(p-2) < currentMax:
            return -1
    if p==1:
        if sumtillnow+maxinMatrix >currentMax:
            currentMax = sumtillnow +maxinMatrix
            return 0
        else:
            return -1
    
    for i in range(level,n-p+1):
        if max(matrix[i])==-1:
            continue
        for j in range(n):
            if matrix[i][j]==-1:
                continue
            modifiedMatrix = [[matrix[x][y] for y in range(n)] for x in range(n)]
            ModifyMatrix(i,j,modifiedMatrix)
            temp = RecmaxActivity(p-1,modifiedMatrix,i+1,sumtillnow+matrix[i][j])
            if temp==-1:
                continue
            returnvalue=0
    return returnvalue         
            
def MaxActivity(p,matrix):
    global currentMax
    if p==1:
        currentMax, secondValue,thirdmax = MaxInMatrix(matrix,0)
        return
    for i in xrange(n-p+1):
        for j in xrange(n):
            modifiedMatrix = [[matrix[x][y] for y in range(n)] for x in range(n)]
            ModifyMatrix(i,j,modifiedMatrix)
            RecmaxActivity(p-1,modifiedMatrix,i+1,matrix[i][j])
       
def main():
    global n
    global currentMax
    currentMax=0
    p=0
    s=0
    matrix=0
    with open("input.txt") as fp:
        n= int(fp.readline().strip())
        p= int(fp.readline().strip())
        s= int(fp.readline().strip())
        matrix = [[0]*n for i in range(n)]
       
        for i in range(s*12):
            a=map(int,fp.readline().strip().split(','))
            matrix[a[0]][a[1]]+=1
    if not(s==0) or not(p==0):
       MaxActivity(p,matrix)
   
    with open("output.txt","w") as fw:
        fw.write(str(currentMax));
        
if __name__ == "__main__" :
    main()    