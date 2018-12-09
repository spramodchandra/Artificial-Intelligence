import operator
global b
global p
global beds
global parking
global candidates
global spladomain
global lahsadomain
global commonDomain
global dic_efficiency
global setofpaths
global candidates_demand
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
    global candidates_demand
    beds=[]
    parking=[]
    candidates= dict([])
    candidates_demand= dict([])
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
            candidates_demand[a_id]=sum(days)
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
            if candidates_demand.get(S[i])>candidates_demand.get(c_id):
                c_id=S[i]
                l=k
            elif candidates_demand.get(S[i])==candidates_demand.get(c_id):
                if S[i]<c_id:
                    c_id=S[i]
                    l=k
    if maxefficiency==-1:
        return CalculateEfficiency(P,p),list()
    if not(c_id==100000):
        l.append(c_id)      
    return maxefficiency,l

def GetHighestDemandId(applicants):
    maxdemand=-1
    c_id=-1
    for a in applicants:
        value=candidates_demand.get(a)
        if value>maxdemand:
            maxdemand=value
            c_id=a
        elif value==maxdemand:
            if a<c_id:
                c_id=a
    return c_id


def CalculateMaxEfficiency(S,P,p):
    maxefficiency,sel=PlayAlone(S,P,p)
    c_id=-1
    if not(len(sel)==0):
        c_id=GetHighestDemandId(sel)
    return maxefficiency,c_id,set(sel)
    
def PlayGame(spla,lahsa,turn,parking,beds,splaChoose,lahsaChoose,lvl):
    global setofpaths
    maxEfficiency=-1
    otherEfficiency=-1
    c_id=100000  
    c_list=set()
    if max(parking)==0 or len(spla)==0:
        splaEfficiency=CalculateEfficiency(parking,p)
        lahsaEfficiency,c_l,sel= CalculateMaxEfficiency(lahsa,beds,b)
        return splaEfficiency,lahsaEfficiency,c_l,set()
    
    if max(beds)==0 or len(lahsa)==0:
        splaEfficiency,c_s,sel= CalculateMaxEfficiency(spla,parking,p)
        lahsaEfficiency=CalculateEfficiency(beds,b)
        return splaEfficiency,lahsaEfficiency,c_s,sel
    
    if turn==0:
        cantChoose=[]
        for a in spla:
            sel=set()
            if not(a in commonDomain):
                updatedspla=spla[:]
                updatedlahsa=lahsa[:]
                for common in commonDomain:
                    if common in updatedspla:
                        updatedspla.remove(common)
                splaEfficiency,c_s,sel= CalculateMaxEfficiency(updatedspla,parking,p)
                lahsaEfficiency,c_l,test= CalculateMaxEfficiency(updatedlahsa,beds,b)
                splaChooseUpdated=splaChoose.copy()
                splaChooseUpdated.add(c_s)
                lahsaChooseUpdated=lahsaChoose.copy()
                lahsaChooseUpdated.add(c_l)
                my_hash=hash(frozenset(splaChooseUpdated))+hash(frozenset(lahsaChooseUpdated))
                dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency,sel)
                if splaEfficiency>maxEfficiency:
                    return splaEfficiency,lahsaEfficiency,c_s,sel
                elif splaEfficiency==maxEfficiency:
                    if candidates_demand.get(c_s)>candidates_demand.get(c_id):
                        return splaEfficiency,lahsaEfficiency,c_s,sel
                    elif candidates_demand.get(c_s)==candidates_demand.get(c_id):
                        if c_s<c_id:
                            return splaEfficiency,lahsaEfficiency,c_s,sel
                        else:
                            return maxEfficiency,otherEfficiency,c_id,c_list
                break
            else:
                updatedParking=map(operator.sub, parking, candidates.get(a))
                if min(updatedParking)==-1:
                    cantChoose.append(a)
                    continue
                splaChooseUpdated=splaChoose.copy()
                splaChooseUpdated.add(a)
                my_hash=hash(frozenset(splaChooseUpdated))+hash(frozenset(lahsaChoose))
                splaEfficiency=0
                lahsaEfficiency=0
                if my_hash in dic_efficiency:
                    splaEfficiency,lahsaEfficiency,sel=dic_efficiency[my_hash]
                else:
                    updatedspla=spla[:]
                    updatedspla.remove(a)
                    updatedlahsa=lahsa[:]
                    if a in updatedlahsa:
                        updatedlahsa.remove(a)
                        
                    # remove those from cantChoose
                    for can in cantChoose:
                        updatedspla.remove(can)
                        
                    splaEfficiency,lahsaEfficiency,i,sel=PlayGame(updatedspla,updatedlahsa,(turn+1)%2,updatedParking,beds,splaChooseUpdated,lahsaChoose,lvl+1)
                    sel.add(a)
                    dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency,sel)
                
                if splaEfficiency>maxEfficiency:
                    maxEfficiency=splaEfficiency
                    otherEfficiency = lahsaEfficiency
                    c_id=a
                    c_list=sel.copy()
                    if lvl==0:
                        setofpaths=list()
                        setofpaths.append(sel)
                elif splaEfficiency==maxEfficiency:
                    if lvl==0:
                        setofpaths.append(sel)
                    if candidates_demand.get(a)>candidates_demand.get(c_id):
                        c_id=a
                        otherEfficiency = lahsaEfficiency
                        c_list=sel.copy()
                    elif candidates_demand.get(a)==candidates_demand.get(c_id):
                        if a<c_id:
                            c_id=a
                            otherEfficiency = lahsaEfficiency
                            c_list=sel.copy()

        if c_id!=100000:
            c_list.add(c_id)
        if maxEfficiency==-1:
            maxEfficiency= CalculateEfficiency(parking,p)
            otherEfficiency,k,test=CalculateMaxEfficiency(lahsa[:],beds,b)
        return maxEfficiency,otherEfficiency,c_id,c_list
    else:
        cantChoose=[]
        for a in lahsa:
            sel=set()
            if not(a in commonDomain):
                updatedspla=spla[:]
                updatedlahsa=lahsa[:]
                for common in commonDomain:
                    if common in updatedlahsa:
                        updatedlahsa.remove(common)
                splaEfficiency,c_s,sel= CalculateMaxEfficiency(updatedspla,parking,p)
                lahsaEfficiency,c_l,test= CalculateMaxEfficiency(updatedlahsa,beds,b)
                splaChooseUpdated=splaChoose.copy()
                splaChooseUpdated.add(c_s)
                lahsaChooseUpdated=lahsaChoose.copy()
                lahsaChooseUpdated.add(c_l)
                my_hash=hash(frozenset(splaChooseUpdated))^hash(frozenset(lahsaChooseUpdated))
                dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency,sel)
                if lahsaEfficiency>maxEfficiency:
                    return splaEfficiency,lahsaEfficiency,c_l,sel
                elif lahsaEfficiency==maxEfficiency:
                    if candidates_demand.get(c_l)>candidates_demand.get(c_id):
                        return splaEfficiency,lahsaEfficiency,c_l,sel
                    elif candidates_demand.get(c_l)==candidates_demand.get(c_id):
                        if c_l<c_id:
                            return splaEfficiency,lahsaEfficiency,c_l,sel
                        else:
                            return otherEfficiency,maxEfficiency,c_id,c_list
                break
            else:
                updatedBeds=map(operator.sub, beds, candidates.get(a))
                if min(updatedBeds)==-1:
                    cantChoose.append(a)
                    continue
                
                lahsaChooseUpdated=lahsaChoose.copy()
                lahsaChooseUpdated.add(a)
                my_hash=hash(frozenset(splaChoose))+hash(frozenset(lahsaChooseUpdated))
                splaEfficiency=0
                lahsaEfficiency=0
                if my_hash in dic_efficiency:
                    splaEfficiency,lahsaEfficiency,sel=dic_efficiency[my_hash]
                else:
                    updatedLahsa=lahsa[:]
                    updatedLahsa.remove(a)
                    updatedSpla=spla[:]
                    if a in updatedSpla:
                        updatedSpla.remove(a)
                        
                    # remove those from cantChoose
                    for can in cantChoose:
                        if can in updatedLahsa:
                            updatedLahsa.remove(can)
                    splaEfficiency,lahsaEfficiency,i,sel=PlayGame(updatedSpla,updatedLahsa,(turn+1)%2,parking,updatedBeds,splaChoose,lahsaChooseUpdated,lvl+1)
                    dic_efficiency[my_hash]=(splaEfficiency,lahsaEfficiency,sel)
                if lahsaEfficiency>maxEfficiency:  
                    maxEfficiency=lahsaEfficiency
                    otherEfficiency = splaEfficiency
                    c_id=a
                    c_list=sel.copy()
                elif lahsaEfficiency==maxEfficiency:
                    if candidates_demand.get(a)>candidates_demand.get(c_id):
                        c_id=a
                        otherEfficiency = splaEfficiency
                        c_list=sel.copy()
                    elif candidates_demand.get(a)==candidates_demand.get(c_id):
                        if a<c_id:
                            c_id=a
                            otherEfficiency = splaEfficiency
                            c_list=sel.copy()
                
        if maxEfficiency==-1:
            otherEfficiency,c_id,c_list= CalculateMaxEfficiency(spla[:],parking,p)
            maxEfficiency=CalculateEfficiency(beds,b)
        return otherEfficiency,maxEfficiency,c_id,c_list
    
def Game():
    global commonDomain
    global dic_efficiency
    global setofpaths
    setofpaths=list()
    dic_efficiency=dict(())
    spla_choose={'S'}
    lahsa_choose={'L'}
    spla=[]
    lahsa=[]
    commonDomain=spladomain&lahsadomain
    # process list and reorder
    for a in sorted(list(spladomain&lahsadomain)):
        spla.append(a)
        lahsa.append(a)

    for a in sorted(list(spladomain-lahsadomain)):
        spla.append(a)
    
    for a in sorted(list(lahsadomain-spladomain)):
        lahsa.append(a) 
    
    print spla,len(spla)
    
    print lahsa,len(lahsa)
    
    print commonDomain, len(commonDomain)
    
    splaEfficiency,lahsaEfficiecy,c_id,c_list=PlayGame(spla,lahsa,0,parking,beds,spla_choose,lahsa_choose,0)
    minvalue=9999999
    for a in setofpaths:
        k=a-commonDomain
        days=0
        for j in a:
            days+=sum(candidates.get(j))
        days+=(7*p-sum(parking))
        if days==splaEfficiency:
            if not(len(k)==0):
                maxdemand=-1
                for d in k:
                    temp=candidates_demand.get(d)
                    if temp>maxdemand:
                        maxdemand=temp
                        minvalue=d
                    elif temp==maxdemand:
                        minvalue=min(minvalue,d)
    a1=candidates_demand.get(c_id)
    a2=candidates_demand.get(minvalue)
    if a2<a1:
        return c_id
    elif a2>a1:
        if minvalue!=9999999:
            p1=map(operator.sub,parking,candidates.get(minvalue))
            if min(p1)!=-1:
                spla.remove(minvalue)
                if minvalue in lahsa:
                    lahsa.remove(minvalue)
                spla_choose.add(minvalue)
                dic_efficiency.clear()
                splaEfficiency1,lahsaEfficiecy1,c_id1,c_list=PlayGame(spla,lahsa,1,p1,beds,spla_choose,lahsa_choose,1) 
                if splaEfficiency1==splaEfficiency:
                    lahsaEfficiecy=lahsaEfficiecy1
                    c_id=minvalue
    else:
        if minvalue<c_id:
            if minvalue!=9999999:
                p1=map(operator.sub,parking,candidates.get(minvalue))
                if min(p1)!=-1:
                    spla.remove(minvalue)
                    if minvalue in lahsa:
                        lahsa.remove(minvalue)
                    spla_choose.add(minvalue)
                    #dic_efficiency.clear()
                    splaEfficiency1,lahsaEfficiecy1,c_id1,c_list=PlayGame(spla,lahsa,1,p1,beds,spla_choose,lahsa_choose,1) 
                    if splaEfficiency1==splaEfficiency:
                        lahsaEfficiecy=lahsaEfficiecy1
                        c_id=minvalue
    
    return c_id

def main():
    ReadInput("input.txt")
    c_id=Game()
    WriteOutput(c_id)

if __name__ == "__main__":
    main()