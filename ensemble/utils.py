import pandas as pd
import random
import functools
import numpy as np

class glo:
    dn=None
    threshold=None
    lat_long_thre=65

    bigmap=['GEO_0572',
    'GEO_0931',
    'GEO_0795',
    'GEO_0196',
    'GEO_0481',
    'GEO_0130',
    'GEO_0917',
    'GEO_0723',
    'GEO_0760',
    'GEO_0761',
    'GEO_0824']

    hugemap=['GEO_0824']

    constr={"GEO_0002":[-1,-1,4000,-1],
    "GEO_0007":[-1,-1,-1,10000],
    "GEO_0079":[-1,-1,5800,-1],
    "GEO_0100":[-1,8000,-1,-1],
    "GEO_0110":[-1,9000,6500,-1],
    "GEO_0179":[-1,-1,1600,-1],
    "GEO_0402":[-1,7000,-1,-1],
    "GEO_0438":[-1,-1,7000,-1],
    "GEO_0496":[-1,6000,-1,-1],
    "GEO_0543":[-1,-1,-1,12000],    
    "GEO_0570":[-1,-1,7000,-1],
    "GEO_0741":[-1,3600,-1,-1],
    "GEO_0911":[-1,-1,-1,7000],
    "GEO_0961":[-1,3000,1750,4500],
    "GEO_0983":[-1,-1,4000,-1],
    }

    lat_cnt,long_cnt=0,0
    can_lat,can_long=None,None

    eps=1e-7

def upd_thre():
    dn=glo.dn
    if(dn in glo.hugemap):
        glo.threshold=20
    elif(dn in glo.bigmap):
        glo.threshold=5
    else:
        glo.threshold=1.5

    #glo.threshold=20#####

class err():
    less_than_3=0
    linear_cand=0
    check_err=0


def get_clue(clue_csv_path):
    ret=None
    try:
        clue_csv=pd.read_csv(clue_csv_path)
        ret=(clue_csv['NAD83_y'].values[0], clue_csv['NAD83_x'].values[0])
    except:
        pass
    return ret

def get_targets(target_csv_path):
    target_cvs=pd.read_csv(target_csv_path)
    return target_cvs

def convert(s):
    
    s=s.replace(' ','')

    flag=None

    if(len(s)<2):
        return None,False,None

    
    def get_2_dig(s,st):
        dig='0123456789'
        i=st+1
        ret,cnt=0,0
        while(1):
            if(i>=len(s)):
                return ret,i
            if(s[i] in dig):
                break
            i+=1
        
        while(1):
            if(i>=len(s)):
                return ret,i
            if(s[i] in dig):
                ret=ret*10+int(s[i])
                cnt+=1
                if(cnt>=2):
                    return ret,i
            else:
                return ret,i
            i+=1

    pos=s.find('°')


    if(pos==-1):
        return None,False
    
    
    if(pos==len(s)-1):
        flag='d'
    else:
        flag='m'
    
    deg,mit,sec=int(s[:pos]),0,0

    pos_m=s.find("'",pos+1)

    if(pos_m!=-1):
        mit=int(s[pos+1:pos_m])
        sec,_=get_2_dig(s,pos_m)
    else:
        mit,pos_m=get_2_dig(s,pos)
        sec,_=get_2_dig(s,pos_m)


    ret=deg+mit/60+sec/60/60

    return ret,True,flag

def filter(can,std):
    std=abs(std)
    ret=[]

    for ins in can:
        if(abs(std-ins['val'])<glo.threshold):
            ret.append(ins)
    return ret
    
def tess_center(box,hst,wst):
    x=hst+box["top"]+box["height"]/2
    y=wst+box["left"]+box["width"]/2

    return x,y

def amaz_center(box,hst,wst,h,w):
    box=box["Geometry"]["BoundingBox"]
    x=hst+box["Top"]*h+box["Height"]*h/2
    y=wst+box["Left"]*w+box["Width"]*w/2

    return x,y


def flag_filter(candi):
    ret=[]
    for ins in candi:
        if(ins['f']=='m'):
            ret.append(ins)
    if(len(ret)>=3):
        return ret
    return candi

def verti(c1,c2):
        return (abs(c1['pos'][1]-c2['pos'][1])<300)
    
def horiz(c1,c2):
        return (abs(c1['pos'][0]-c2['pos'][0])<300)


def choose_cand(candi,tag):

    #output_can(candi,tag)

    candi=flag_filter(candi)

    if(tag=='lat'):
        glo.lat_cnt=len(candi)
    else:
        glo.long_cnt=len(candi)

    if(len(candi)<3):
        return None
    
    def cmp(x,y):
        a,b=x['pos'],y['pos']
        if(a[1]<b[1]):
            return -1
        if(a[1]>b[1]):
            return 1
        if(a[0]<b[0]):
            return -1
        return 1

    
    
    def find_c2(c1,candi):
        c2=candi[-1]
        ret=candi[:-1]
        flag=-1
        for i in range(len(candi)-1):
            c=candi[i]
            if(verti(c1,c) or horiz(c1,c)):
                c2=c
                ret=candi[:i]+candi[i+1:]
                if(verti(c1,c)):
                    flag=0
                else:
                    flag=1
                break

        return c2,ret,flag


    candi.sort(key=functools.cmp_to_key(cmp))

    
    c1,c2,c3=candi[0],None,None
    candi=candi[1:]

    c2,candi,flag=find_c2(c1,candi)
    #flag -1/0/1 -1/ver/hor

    if(not verti(c1,c2)):
        for c in candi:
            if(verti(c1,c) or verti(c2,c)):
                c3=c
                break
            
    
    if(c3==None and (not horiz(c1,c2))):
        for c in candi:
            if(horiz(c1,c) or horiz(c2,c)):
                c3=c
                break

    if(c3==None and (verti(c1,c2))):
        for c in candi:
            if((not verti(c1,c)) and (not verti(c2,c))):
                c3=c
                break

    if(c3==None and (horiz(c1,c2))):
        for c in candi:
            if((not horiz(c1,c)) and (not horiz(c2,c))):
                c3=c
                break


    if(c3==None):
        c3=candi[len(candi)//2]


    return [c1,c2,c3]


def takeh(e):
  return e['h']

def takew(e):
  return e['w']



def guess(target,clue,tag):
    n=len(target)
    ret=[0 for _ in range(n)]
    a=[{'h':target[i][0],'w':target[i][1],'id':i} for i in range(n)]

    if(tag=='lat'):
        a.sort(key=takeh)
    else:
        a.sort(key=takew)

    dlt=[0.5/n*(n-i)-0.25 for i in range(n)]
    noise=(np.random.random(n)-0.5)*0.1
    for i in range(n):
        dlt[i]+=noise[i]
    dlt.sort(reverse=True)

    for i in range(n):
        ret[a[i]['id']]=clue+dlt[i]
    
    #h+ lat-
    #w+ long-

    return ret


def get_vec(a,b):
    ret={}
    ret['pos']=(b['pos'][0]-a['pos'][0],b['pos'][1]-a['pos'][1])
    ret['val']=b['val']-a['val']
    return ret

def decompose(v,v1,v2):
    a1,a2=0,0
    A=np.mat([[v1['pos'][0],v2['pos'][0]],
              [v1['pos'][1],v2['pos'][1]]])
    b=np.mat([v['pos'][0],v['pos'][1]]).T
    tmp=np.linalg.solve(A,b)

    tmp=np.array(tmp)
    tmp=tmp.reshape(-1).tolist()
    a1,a2=tmp[0],tmp[1]
    return a1,a2



def parallelogram(target,candi):
    v1,v2=get_vec(candi[0],candi[1]),get_vec(candi[0],candi[2])

    ret=[]
    for i in range(len(target)):
            tp={'pos':target[i],'val':0}
            dv=get_vec(candi[0],tp)
            a1,a2=decompose(dv,v1,v2)
            ret.append(candi[0]['val']+a1*v1['val']+a2*v2['val'])
        
    return ret
   
        


def get_output(target,candi,clue,tag,dn,bo=False):

    candi=filter_by_constr(candi,glo.constr,dn)

    candi=choose_cand(candi,tag)

    #if(bo):
    #    output_can(candi,tag)



    ret,flag=None,None

    if(candi==None):
        ret,flag=guess(target,clue,tag),'g'
        err.less_than_3+=1
    else:
        try:
        #if(True):
            ret=parallelogram(target,candi)
            if(tag=='long'):
                for i in range(len(ret)):
                    ret[i]=-ret[i]
            flag='c'
        except:
            ret,flag=guess(target,clue,tag),'g'
            err.linear_cand+=1
    
    
    try:
        for i in range(len(ret)):
            assert abs(ret[i]-clue)<glo.threshold
    except:
        output_can(candi,tag)
        #sb=input()
        ret,flag=guess(target,clue,tag),'g'
        err.check_err+=1
    
    return ret,flag


    
    

def output_can(a,flag):
    print(flag)
    for ins in a:
        print(ins['val'],int(ins['pos'][0]),int(ins['pos'][1]),ins['f'])



def filter_by_constr(candi,constr,dn):
    if(constr.get(dn)==None):
        return candi
    
    constr=constr[dn]
    
    ret=[]
    for t in candi:
        h,l=t['pos']
        if(constr[0]!=-1 and h<constr[0]):
            continue
        if(constr[1]!=-1 and h>constr[1]):
            continue
        if(constr[2]!=-1 and l<constr[2]):
            continue
        if(constr[3]!=-1 and l>constr[3]):
            continue
        ret.append(t)
    
    return ret