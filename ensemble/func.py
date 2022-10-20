import os
import json
import time
import pandas as pd
from utils import tess_center,convert,amaz_center,filter,glo


def get_tess(dn,clue_lat,clue_long):
        path='../pytesseract/tess_processed/'
        flist=os.listdir(path+dn)

        can_lat,can_long=[],[]
            
        for fn in flist:
                with open(path+dn+'/'+fn) as f:
                    a=json.loads(f.read())
                hst,wst,h,w=a['hst'],a['wst'],a['h'],a['w']
                tmp=a['box']

                n=len(tmp['level'])
                boxes=[]
                for i in range(n):
                    box={'top':tmp['top'][i],'left':tmp['left'][i],
                         'height':tmp['height'][i],'width':tmp['width'][i],
                         'text':tmp['text'][i]}

                    center=tess_center(box,hst,wst)
                    if(len(box['text'])>2):
                        boxes.append({'Text':box['text'],'pos':center})
                
                boxes=merge_dm(boxes,fn)
                
                
                for box in boxes:
                    try:
                        num,bo,flag=convert(box['text'])
                    except:
                        num,bo=None,False
                   
                    
                    if(num!=None and bo==True):
                        if(num<glo.lat_long_thre):
                            can_lat.append({'val':num,'pos':center,'f':flag})
                        else:
                            can_long.append({'val':num,'pos':center,'f':flag})

        can_lat=filter(can_lat,clue_lat)
        can_long=filter(can_long,clue_long)
            
        return can_lat,can_long


def get_amaz(dn,clue_lat,clue_long):
    path='../amazon/amazon_processed/'

    flist=os.listdir(path+dn)
    can_lat,can_long=[],[]
    boxes=[]

    for fn in flist:
        with open(path+dn+'/'+fn) as f:
                    a=json.loads(f.read())
        hst,wst,h,w=a['hst'],a['wst'],a['h'],a['w']

                
        for box in a['box']:
                    if(box['BlockType']=='WORD'):
                        center=amaz_center(box,hst,wst,h,w)
                        tmp={'Text':box['Text'],'pos':center}
                        boxes.append(tmp)
                
    boxes=merge_dm(boxes,fn)
                
                
    for box in boxes:
                    try:
                        num,bo,flag=convert(box['Text'])
                    except:
                        num,bo=None,False
                
                    if(num!=None and bo==True):
                        if(num<glo.lat_long_thre):
                            can_lat.append({'val':num,'pos':box['pos'],'f':flag})
                        else:
                            can_long.append({'val':num,'pos':box['pos'],'f':flag})
    
    
    can_lat=filter(can_lat,clue_lat)
    can_long=filter(can_long,clue_long)
            
    return can_lat,can_long



def merge_dm(boxes,fn):
    dm=[]
    d=[]
    m=[]
    for box in boxes:
        try:
            posd=box['Text'].find('°')
            posm=box['Text'].find("'")
            if(posd!=-1 and posm!=-1):
                dm.append(box)
            elif(posd!=-1):
                d.append(box)
            elif(posm!=-1):
                m.append(box)
        except:
            pass

    merged=[]
    
    od=[]

    for i in range(len(d)):
        bo=False
        for j in range(len(m)):
            if(dis(d[i],m[j])<150):
                if(lr(d[i],m[j]) or ud(d[i],m[j])):
                    merged.append({'Text':d[i]['Text']+m[j]['Text'],
                                   'pos':
                                    (d[i]['pos'][0]/2+m[j]['pos'][0]/2,d[i]['pos'][1]/2+m[j]['pos'][1]/2)
                                })
                    bo=True
                    break
        if(bo==False):
            od.append(d[i])
    
    
    return dm+merged+od

def dis(a,b):
    a,b=a['pos'],b['pos']
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def lr(a,b):
    a,b=a['pos'],b['pos']
    if(abs(a[0]-b[0])<50 and a[1]<b[1]):
        return True
    return False

def ud(a,b):
    a,b=a['pos'],b['pos']
    if(abs(a[1]-b[1])<50 and a[0]<b[0]):
        return True
    return False