# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 22:48:59 2018

@author: spramodchandra
"""

import operator
global b
global p
global beds
global parking
global candidates
global spladomain
global lahsadomain
global dic_efficiency
global commonDomain
global dic_days

def parseApplication(text):
    a_id= int(text[:5])
    sex= text[5]
    if sex=="M" or sex=="m":
        sex="M"
    elif sex=="F" or sex=="f":
        sex="F"
    elif sex=="O" or sex=="o":
        sex="M"
    age=int(text[6:9])
    pet = (True if (text[9]=="Y" or  text[9]=="y") else False )
    medicalCondition= (True if (text[10]=="Y" or  text[10]=="y") else False )
    car= (True if (text[11]=="Y" or  text[11]=="y") else False )
    drivingLicence= (True if (text[12]=="Y" or  text[12]=="y") else False )
    days=[]
    for day in (text[13:20]):
        days.append(int(day))
    
    return a_id,sex,age,pet,medicalCondition,car,drivingLicence,days

def ReadInput(filename):
    global b
    global p
    global beds
    global parking
    global candidates
    global spladomain
    global lahsadomain
    beds=[]
    parking=[]
    candidates= dict([])
    spla =set([])
    spladomain=set([])
    lahsa=set([])
    lahsadomain=set([])
    with open(filename) as fp:
        b=int(fp.readline())
        p=int(fp.readline())
        L=int(fp.readline())
        for i in range(7):
            beds.append(b)
            parking.append(p)
        for i in range(L):
            lahsa.add(int(fp.readline()))
        S=int(fp.readline())
        for i in range(S):
            spla.add(int(fp.readline()))
            
        A=int(fp.readline())
        for i in range(A):
            text=fp.readline()
            a_id,sex,age,pet,medicalCondition,car,drivingLicence,days=parseApplication(text)
            candidates[a_id]=days
            if(a_id in spla ):
                for i in range(7):
                    parking[i]-=days[i]
                continue
            if(a_id in lahsa):
                for i in range(7):
                    beds[i]-=days[i]
                continue
            if(sex=="F" and age>17 and pet==False):
                lahsadomain.add(a_id)
            if(car==True and drivingLicence ==True and medicalCondition==False):
                spladomain.add(a_id)

def WriteOutput(a_id):
    with open("output.txt","w") as fw:
        fw.write(str(a_id).zfill(5));
        
def CalculateEfficiency(P,p):
    return 7*p - sum(P)

def PlayAlone(S,P,p):
    c_id=100000 
    if len(S)==0 or max(P)==0:
        return CalculateEfficiency(P,p),list()
    
    if len(S)<=min(P):
        P1=P[:]
        for a in S:
            P1=map(operator.sub, P1, candidates.get(a))
        return CalculateEfficiency(P1,p),list(S)
    maxefficiency=-1
    l=[]
    for i in range(len(S)):
        P1=map(operator.sub, P, candidates.get(S[i]))
        if min(P1)==-1:
            continue
        temp1,k= PlayAlone(S[i+1:],P1,p)
        if temp1>maxefficiency:
            maxefficiency=temp1
            c_id=S[i]
            l=k
        elif temp1 ==maxefficiency:
            if S[i]<c_id:
                c_id=S[i]
                l=k
    if maxefficiency==-1:
        return CalculateEfficiency(P,p),list()
    if not(c_id==100000):
        l.append(c_id)      
    return maxefficiency,l

def CalculateMaxEfficiency(S,P,p):
    maxefficiency,sel=PlayAlone(S,P,p)
    c_id=-1
    if not(len(sel)==0):
        c_id=min(sel)
    return maxefficiency,c_id

def PlayGame(spla,lahsa,turn,parking,beds,splaChoose,lahsaChoose,lvl):
    maxEfficiency=-1
    otherEfficiency=-1
    c_id=100000 

    if max(parking)==0 or len(spla)==0:
        splaEfficiency=CalculateEfficiency(parking,p)
        lahsaEfficiency,j= CalculateMaxEfficiency(lahsa,beds,b)
        return splaEfficiency,lahsaEfficiency,j
    
    if max(beds)==0 or len(lahsa)==0:
        lahsaEfficiency=CalculateEfficiency(beds,b)
        splaEfficiency,i= CalculateMaxEfficiency(spla,parking,p)
        return splaEfficiency,lahsaEfficiency,i
        
    if len(set(spla)&set(lahsa))==0:
        splaEfficiency,c_s= CalculateMaxEfficiency(spla,parking,p)
        lahsaEfficiency,c_l= CalculateMaxEfficiency(lahsa,beds,b)
        if turn==0:
            return splaEfficiency,lahsaEfficiency,c_s
        else:
            return splaEfficiency,lahsaEfficiency,c_l
        
    if turn==0:
        for a in spla:
            updatedParking=map(operator.sub, parking, candidates.get(a))
            if min(updatedParking)==-1:
                continue
			
            splaChooseUpdated=splaChoose.copy()
            splaChooseUpdated.add(a)
            my_hash=hash(frozenset(splaChooseUpdated))+hash(frozenset(lahsaChoose))
            splaEfficiency=0
            lahsaEfficiency=0
            days=candidates.get(a)
            s=str()
            if lvl==0:
                if a in commonDomain:
                    s="1"
                else:
                    s="0"
            s+=''.join(map(str,days))
            if lvl==0 and s in dic_days:
                splaEfficiency,lahsaEfficiency=dic_days[s]
            if my_hash in dic_efficiency:
                splaEfficiency,lahsaEfficiency=dic_efficiency[my_hash]
            else:
                updatedspla=spla[:]
                updatedspla.remove(a)
                updatedlahsa=lahsa[:]
                if a in updatedlahsa:
                    updatedlahsa.remove(a)
                
                splaEfficiency,lahsaEfficiency,i=PlayGame(updatedspla,updatedlahsa,(turn+1)%2,updatedParking,beds,splaChooseUpdated,lahsaChoose,lvl+1)
                
                dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency)
                if lvl==0:
                    dic_days[s]=splaEfficiency,lahsaEfficiency
                
            if splaEfficiency>maxEfficiency:
                maxEfficiency=splaEfficiency
                otherEfficiency = lahsaEfficiency
                c_id=a
            elif splaEfficiency==maxEfficiency:
                if a<c_id:
                    c_id=a
                    otherEfficiency = lahsaEfficiency
                    
        if maxEfficiency==-1:
            maxEfficiency=CalculateEfficiency(parking,p)
            otherEfficiency,k=CalculateMaxEfficiency(lahsa[:],beds,b)
        return maxEfficiency,otherEfficiency,c_id
    else:
        for a in lahsa:
            updatedBeds=map(operator.sub, beds, candidates.get(a))
            if min(updatedBeds)==-1:
                continue

            lahsaChooseUpdated=lahsaChoose.copy()
            lahsaChooseUpdated.add(a)
            my_hash=hash(frozenset(splaChoose))+hash(frozenset(lahsaChooseUpdated))
            splaEfficiency=0
            lahsaEfficiency=0
            if my_hash in dic_efficiency:
                splaEfficiency,lahsaEfficiency=dic_efficiency[my_hash]
            else:
                updatedLahsa=lahsa[:]
                updatedLahsa.remove(a)
                updatedSpla=spla[:]
                if a in updatedSpla:
                    updatedSpla.remove(a)
                
                splaEfficiency,lahsaEfficiency,i=PlayGame(updatedSpla,updatedLahsa,(turn+1)%2,parking,updatedBeds,splaChoose,lahsaChooseUpdated,lvl+1)
                
                dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency)
            
            if lahsaEfficiency>maxEfficiency:  
                maxEfficiency=lahsaEfficiency
                otherEfficiency = splaEfficiency
                c_id=a
            elif lahsaEfficiency==maxEfficiency:
                if a<c_id:
                    c_id=a
                    otherEfficiency = splaEfficiency
        if maxEfficiency==-1:
            maxEfficiency=CalculateEfficiency(beds,b)
            otherEfficiency,c_id=CalculateMaxEfficiency(spla[:],parking,p)
        return otherEfficiency,maxEfficiency,c_id
    
def Game(turn=0):
    global dic_efficiency
    global dic_days
    global commonDomain
    dic_days=dict(())
    dic_efficiency=dict(())
    spla_choose={'S'}
    lahsa_choose={'L'}
    spla=[]
    lahsa=[]
    commonDomain=spladomain&lahsadomain
    # process list and reorder
    for a in sorted(list(commonDomain)):
        spla.append(a)
        lahsa.append(a)

    for a in sorted(list(spladomain-lahsadomain)):
        spla.append(a)
    
    for a in sorted(list(lahsadomain-spladomain)):
        lahsa.append(a) 
    
    splaEfficiency,lahsaEfficiecy,c_id=PlayGame(spla,lahsa,turn,parking,beds,spla_choose,lahsa_choose,0)
    print splaEfficiency,lahsaEfficiecy,c_id
    return c_id

def main():
    ReadInput("input.txt")
    c_id=Game()
    WriteOutput(c_id)
if __name__ == "__main__":
    main()