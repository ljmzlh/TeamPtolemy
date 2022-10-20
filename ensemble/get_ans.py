from doctest import BLANKLINE_MARKER
import os
import json
import time
import pandas as pd
from func import get_amaz,get_tess
from utils import get_clue,get_targets,err,output_can,get_output,glo,upd_thre,filter_by_constr
import matplotlib.pyplot as plt
from get_23 import get_23
import argparse





def get_ans(args):
    try:
        os.mkdir('output')
    except:
        pass

    dlist=os.listdir(args.csv_path)
    cnt=0
    res=[[],[],[]]
    llist=[]
    llist2=[]
    llist1=[]
    llist2err=[]

    list23=[]


    for sb in dlist:
        if(not sb.startswith('GEO')):
            continue
        dn=sb[:sb.find('.csv')]


        glo.dn=dn
        upd_thre()

        cnt+=1

        can_lat,can_long=[],[]

        clue_lat,clue_long=get_clue(args.clue_path+dn+'_clue.csv')
        targets_csv=get_targets(args.csv_path+dn+'.csv')
        input_csv=get_targets(args.csv_path+dn+'.csv')
        print(dn,clue_lat,clue_long)
        
        try:
        #if(True):
            can_lat_0,can_long_0=get_amaz(dn,clue_lat,clue_long)
        except:
            pass

        try:
            can_lat_1,can_long_1=get_tess(dn,clue_lat,clue_long)
        except:
            pass

        can_lat,can_long=merge(can_lat_0,can_lat_1),merge(can_long_0,can_long_1)

        can_lat=filter_by_constr(can_lat,glo.constr,dn)
        can_long=filter_by_constr(can_long,glo.constr,dn)

        glo.can_lat,glo.can_long=can_lat,can_long

        n=len(targets_csv['row'])
        target=[]
        for i in range(n):
            target.append((targets_csv['row'][i],targets_csv['col'][i]))

        
        target_lat,flag_lat=get_output(target,can_lat,clue_lat,'lat',dn)
        target_long,flag_long=get_output(target,can_long,clue_long,'long',dn)

        stat=int(flag_lat=='c')+int(flag_long=='c')
        res[stat].append(dn)


        if(stat==1 and (glo.lat_cnt==2 or  glo.long_cnt==2)):
            who='lat' if glo.lat_cnt==2 else 'long'
            tmp=get_23(target,clue_lat,clue_long,dn)
            if(who=='lat'):
                target_lat=tmp
            else:
                target_long=tmp




        targets_csv['NAD83_x']=[long for long in target_long]
        targets_csv['NAD83_y']=[lat for lat in target_lat]

        # put all the results into single csv
        output_csv=pd.DataFrame()
        output_csv=pd.concat([targets_csv, output_csv], ignore_index=True)
        output_csv.to_csv('output/output_'+dn+'.csv', index=False)
        
        loss=cal_loss(input_csv,output_csv)

        

        llist.append(loss)
        if(stat==2):
            llist2.append(loss)
            if(loss>0.02):
                llist2err.append(dn)
        elif(stat==1):
            llist1.append(loss)

    plotloss(llist)
    plotloss(llist1)
    plotloss(llist2)

    print(llist[int(len(llist)*0.5)])
    print(llist[int(len(llist)*0.55)])
    print(llist[int(len(llist)*0.60)])

    print(err.less_than_3)
    print(err.linear_cand)
    print(err.check_err)
        
    print()

    for i in range(3):
        print(len(res[i]))

    for i in range(3):
        res[i].sort()

    with open('0','w') as f:
        f.write(json.dumps(res[0]))
    
    with open('1','w') as f:
        f.write(json.dumps(res[1]))

    with open('2','w') as f:
        f.write(json.dumps(res[2]))
    
    with open('23','w') as f:
        f.write(json.dumps(list23))
    
    llist2err.sort()
    with open('2err','w') as f:
        f.write(json.dumps(llist2err))

def dis(a,b):
    x1,y1=a['pos']
    x2,y2=b['pos']

    return ((x1-x2)**2+(y1-y2)**2)**0.5

def merge(a1,a2):
    ret=[a1[i] for i in range(len(a1))]
    
    for y in a2:
        bo=True
        for x in a1:
            if(dis(x,y)<400):
                bo=False
                break
        if(bo):
            ret.append(y)

    return ret


def cal_loss(gold,pred):
    n=len(gold['NAD83_x'])
    ret=0
    for i in range(n):
        ret+=(gold['NAD83_x'][i]-pred['NAD83_x'][i])**2
        ret+=(gold['NAD83_y'][i]-pred['NAD83_y'][i])**2
    
    ret/=2*n

    return ret**0.5


def plotloss(y):
    n=len(y)
    y.sort()
    x=[i for i in range(n)]
    plt.ylim(0,0.1)
    plt.xlim(0,n)

    plt.bar(x=x, height=y, label='',
    color='steelblue', alpha=0.8)

    plt.show()
        




if(__name__=='__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path",type=str,default='../dataset/Validation_csv')
    parser.add_argument("--clue_path",type=str,default='../dataset/Validation_csv')
    
    args = parser.parse_args()
    get_ans(args)
