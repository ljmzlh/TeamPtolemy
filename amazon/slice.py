import os
import cv2
from tqdm import tqdm

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--tif_path",type=str,default='../dataset/Validation/')
parser.add_argument("--s3_path",type=str,default='s3://ljm-map')
args = parser.parse_args()


dlt=1280

try:
    os.mkdir('slice_'+str(dlt))
except:
    pass

flist=os.listdir(args.tif_path)
for i in tqdm(range(len(flist))):
    fn=flist[i]
    if(not fn.endswith('.tif')):
        continue
    fn=fn[:fn.find('.tif')]
    path=args.tif_path+fn+'.tif'
    
    try:
        prefix='slice_'+str(dlt)+'/'+fn
        image=cv2.imread(path)

        cnt=0
        H,W=image.shape[0],image.shape[1]
        
        for hst in range(0,H,dlt):
            for wst in range(0,W,dlt):
                hed,wed=min(H,hst+dlt),min(W,wst+dlt)
                
                img=image[hst:hed,wst:wed,:]
                cnt+=1
                path=prefix+'_'+str(cnt)+'.tif'
                
                cv2.imwrite(path,img)
        
                cmd='aws s3 cp '+path+' '+args.s3_path
                os.system(cmd)
    
    except:
        pass





